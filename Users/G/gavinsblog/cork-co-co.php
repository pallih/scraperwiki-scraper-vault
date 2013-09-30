<?php

/*
 * Planning applications for Cork City Council
 *
 * The LGCSB's ePlan app is a POS aspx nightmare which forcibly paginates results
 * and refuses GETs on its search form.  Yay Government.
 * Once we grab all received applications for the last N days, we loop through
 * only those applications in the state of 'New Application' (and ignore 'Incomplete')
 * because the City adds Irish grid references to the 'Site location' detail page.
 *
 * TODO: Add data to datastore after checking we haven't added the same planning ref number
 * previously.
 */

require  'scraperwiki/simple_html_dom.php';

/*
 * Setting any global vars here in order to
 * make reuse easier
 */

$authority_code = "CC";
$authority_name = "Cork City Council";
$authority_short_name = "Cork City";
$nearby_api_key = "64c962e53d1c01"; # Seriously. Don't use this if you're not me. Sign up at nearby.org.uk

/*
 * scraperpost()
 * A function to use instead of scraperwiki::scrape since that function only performs simple GETs
 *
 * Variables:
 * $url - a URL to which we will post form variables
 * $postvars - an array of keys and values containing all the form variables we're POSTing
 */

function scraperpost($url,$postvars=NULL,$cookie=NULL) {
    $curl = curl_init($url);
    $fields_string = "";
    if($postvars) {
        foreach($postvars as $key=>$value) {
            $fields_string .= $key.'='.$value.'&';
        }
    }
    rtrim($fields_string,'&');
    curl_setopt($curl,CURLOPT_POST,true);
    curl_setopt($curl,CURLOPT_RETURNTRANSFER,true);
    curl_setopt($curl,CURLOPT_POSTFIELDS,$fields_string);
    curl_setopt($curl,CURLOPT_COOKIESESSION,true);
    curl_setopt($curl,CURLOPT_HEADER, 1);
    if($cookie) {
        curl_setopt($curl,CURLOPT_COOKIE, $cookie);
    }
    $res  = curl_exec($curl);
    curl_close($curl) ;
    return $res  ;
}


function process_page($html) {
    $dom = new simple_html_dom();
    $dom->load($html);
    $apps = array();
    global $authority_code;
    global $nearby_api_key;
    foreach($dom->find("table[class='AppDetailsTable'] tr") as $row) {
        #  Man, this is hacky, but I'm not using dom here in case 'td' shows in plaintext of var
        if (stristr($row,'FINALISED') || stristr($row,'CONDITIONAL') || stristr($row,'APPEALED') || stristr($row,'WITHDRAWN') || stristr($row,'NEW<') || stristr($row,'APPROVED') || stristr($row,'REFUSED')) { 

            $appref = $authority_code . substr($row->children[0]->plaintext,0,2) . "/" . substr($row->children[0]->plaintext,2);
            $rawappref = trim($row->children[0]->plaintext);
            $url = "http://planning.corkcity.ie/InternetEnquiry/rpt_ViewApplicDetails.asp?validFileNum=1&app_num_file=" . $rawappref;
            $rawdate   = substr($row->children[4]->plaintext,0,10);
            $date = substr($rawdate,-4) . "-" . substr($rawdate,3,2) . "-" . substr($rawdate,0,2);
            $applicant = trim($row->children[5]->plaintext);
            $address = str_replace("<br>",",",str_replace("<BR>",",",$row->children[6]->innertext));

            # Now fetch additional information.  Part one, full description of plan

            $fullapphtml = scraperwiki::scrape($url);
            $fullappdom = new simple_html_dom();
            $fullappdom->load($fullapphtml);
            $fullappdetails = $fullappdom->find("table[class='AppDetailsTable'] tr",15)->children(1)->plaintext;

            # Part two, location of application

            $lochtml = scraperwiki::scrape('http://planning.corkcity.ie/InternetEnquiry/rpt_ViewSiteLocDetails.asp?page_num=0&file_number=' . $rawappref);
            if (!(stristr($lochtml,"No Site Location Details Found"))) {
                $locdom = new simple_html_dom();
                $locdom->load($lochtml);
                $locnorthing = round(floatval($locdom->find("table[class='AppDetailsTable'] tr",1)->children(1)->plaintext));
                $loceasting  = round(floatval($locdom->find("table[class='AppDetailsTable'] tr",1)->children(4)->plaintext));

                # Part three, convert E&N to WGS84 using nearby.org.uk's API
                sleep(2);
                $convhtml = scraperwiki::scrape("http://www.nearby.org.uk/api/convert.php?key=$nearby_api_key&p=" . urlencode($loceasting . "," . $locnorthing . " OSI") . "&output=text&want=ll-wgs84");
            
                $latlong = explode(",",$convhtml);
                #print 'http://planning.corkcity.ie/InternetEnquiry/rpt_ViewSiteLocDetails.asp?page_num=0&file_number=' . $rawappref . "\n";
                $lat = $latlong[2];
                $long = trim($latlong[3]);
    
                $apps["$appref"] = array(
                    'url'       => $url,
                    'appref'    => $appref,
                    'date'      => $date,
                    'applicant' => $applicant,
                    'address'   => $address,
                    'details'   => $fullappdetails,
                    'latitude'  => $lat,
                    'longitude' => $long,
                    );
                }
            }
        }
    return $apps;
}

# Initialise POST form data

$postvars = array (
    'txtFileNum' => '',
    'txtSurname' => '',
    'ReportType' => 'RECEIVED',
    'txtLocation' => '',
    'NoDays' => '365',
    'limitResults' => '0',
    'Submit5' => 'Search',
    'btnLookupFileNum' => 'Processing...'
    );

$thispage = 1;
$html = scraperpost("http://planning.corkcity.ie/InternetEnquiry/frmSelCritSearch.asp",$postvars);
preg_match('/^Set-Cookie: (.*?);/m', $html, $m);
$cookie = $m[1];

$applications = process_page($html);

foreach ($applications as $key => $value) {
    scraperwiki::save(array('appref'),$value,$value["date"],array(floatval($value["latitude"]),floatval($value["longitude"])));
}

if(stristr($html,"Currently viewing page")) {   # There's >1 pages of results

    # I'm sorry. I'm so sorry.

    $hackysplice  = explode("Currently viewing page",$html);
    $hackysplice2 = explode("</font>",$hackysplice[1]);
    $hackysplice3 = explode(" of ",$hackysplice2[0]);
    $numpages = intval($hackysplice3[1]);

    while ($thispage < $numpages) {
        $postvars["page_num"] = $thispage;
        #print $thispage . " of " . $numpages . "\n";
        $postvars["Op"] = 1;
        $html = scraperpost("http://planning.corkcity.ie/InternetEnquiry/frmSelCritSearch.asp?page_num=" . $thispage . "&Op=1",NULL,$cookie);

        $applications = process_page($html);

        foreach ($applications as $key => $value) {
            scraperwiki::save(array('appref','url'),$value,$value["date"],array(floatval($value["latitude"]),floatval($value["longitude"])));
        }
        $thispage += 1;
    }
}

?><?php

/*
 * Planning applications for Cork City Council
 *
 * The LGCSB's ePlan app is a POS aspx nightmare which forcibly paginates results
 * and refuses GETs on its search form.  Yay Government.
 * Once we grab all received applications for the last N days, we loop through
 * only those applications in the state of 'New Application' (and ignore 'Incomplete')
 * because the City adds Irish grid references to the 'Site location' detail page.
 *
 * TODO: Add data to datastore after checking we haven't added the same planning ref number
 * previously.
 */

require  'scraperwiki/simple_html_dom.php';

/*
 * Setting any global vars here in order to
 * make reuse easier
 */

$authority_code = "CC";
$authority_name = "Cork City Council";
$authority_short_name = "Cork City";
$nearby_api_key = "64c962e53d1c01"; # Seriously. Don't use this if you're not me. Sign up at nearby.org.uk

/*
 * scraperpost()
 * A function to use instead of scraperwiki::scrape since that function only performs simple GETs
 *
 * Variables:
 * $url - a URL to which we will post form variables
 * $postvars - an array of keys and values containing all the form variables we're POSTing
 */

function scraperpost($url,$postvars=NULL,$cookie=NULL) {
    $curl = curl_init($url);
    $fields_string = "";
    if($postvars) {
        foreach($postvars as $key=>$value) {
            $fields_string .= $key.'='.$value.'&';
        }
    }
    rtrim($fields_string,'&');
    curl_setopt($curl,CURLOPT_POST,true);
    curl_setopt($curl,CURLOPT_RETURNTRANSFER,true);
    curl_setopt($curl,CURLOPT_POSTFIELDS,$fields_string);
    curl_setopt($curl,CURLOPT_COOKIESESSION,true);
    curl_setopt($curl,CURLOPT_HEADER, 1);
    if($cookie) {
        curl_setopt($curl,CURLOPT_COOKIE, $cookie);
    }
    $res  = curl_exec($curl);
    curl_close($curl) ;
    return $res  ;
}


function process_page($html) {
    $dom = new simple_html_dom();
    $dom->load($html);
    $apps = array();
    global $authority_code;
    global $nearby_api_key;
    foreach($dom->find("table[class='AppDetailsTable'] tr") as $row) {
        #  Man, this is hacky, but I'm not using dom here in case 'td' shows in plaintext of var
        if (stristr($row,'FINALISED') || stristr($row,'CONDITIONAL') || stristr($row,'APPEALED') || stristr($row,'WITHDRAWN') || stristr($row,'NEW<') || stristr($row,'APPROVED') || stristr($row,'REFUSED')) { 

            $appref = $authority_code . substr($row->children[0]->plaintext,0,2) . "/" . substr($row->children[0]->plaintext,2);
            $rawappref = trim($row->children[0]->plaintext);
            $url = "http://planning.corkcity.ie/InternetEnquiry/rpt_ViewApplicDetails.asp?validFileNum=1&app_num_file=" . $rawappref;
            $rawdate   = substr($row->children[4]->plaintext,0,10);
            $date = substr($rawdate,-4) . "-" . substr($rawdate,3,2) . "-" . substr($rawdate,0,2);
            $applicant = trim($row->children[5]->plaintext);
            $address = str_replace("<br>",",",str_replace("<BR>",",",$row->children[6]->innertext));

            # Now fetch additional information.  Part one, full description of plan

            $fullapphtml = scraperwiki::scrape($url);
            $fullappdom = new simple_html_dom();
            $fullappdom->load($fullapphtml);
            $fullappdetails = $fullappdom->find("table[class='AppDetailsTable'] tr",15)->children(1)->plaintext;

            # Part two, location of application

            $lochtml = scraperwiki::scrape('http://planning.corkcity.ie/InternetEnquiry/rpt_ViewSiteLocDetails.asp?page_num=0&file_number=' . $rawappref);
            if (!(stristr($lochtml,"No Site Location Details Found"))) {
                $locdom = new simple_html_dom();
                $locdom->load($lochtml);
                $locnorthing = round(floatval($locdom->find("table[class='AppDetailsTable'] tr",1)->children(1)->plaintext));
                $loceasting  = round(floatval($locdom->find("table[class='AppDetailsTable'] tr",1)->children(4)->plaintext));

                # Part three, convert E&N to WGS84 using nearby.org.uk's API
                sleep(2);
                $convhtml = scraperwiki::scrape("http://www.nearby.org.uk/api/convert.php?key=$nearby_api_key&p=" . urlencode($loceasting . "," . $locnorthing . " OSI") . "&output=text&want=ll-wgs84");
            
                $latlong = explode(",",$convhtml);
                #print 'http://planning.corkcity.ie/InternetEnquiry/rpt_ViewSiteLocDetails.asp?page_num=0&file_number=' . $rawappref . "\n";
                $lat = $latlong[2];
                $long = trim($latlong[3]);
    
                $apps["$appref"] = array(
                    'url'       => $url,
                    'appref'    => $appref,
                    'date'      => $date,
                    'applicant' => $applicant,
                    'address'   => $address,
                    'details'   => $fullappdetails,
                    'latitude'  => $lat,
                    'longitude' => $long,
                    );
                }
            }
        }
    return $apps;
}

# Initialise POST form data

$postvars = array (
    'txtFileNum' => '',
    'txtSurname' => '',
    'ReportType' => 'RECEIVED',
    'txtLocation' => '',
    'NoDays' => '365',
    'limitResults' => '0',
    'Submit5' => 'Search',
    'btnLookupFileNum' => 'Processing...'
    );

$thispage = 1;
$html = scraperpost("http://planning.corkcity.ie/InternetEnquiry/frmSelCritSearch.asp",$postvars);
preg_match('/^Set-Cookie: (.*?);/m', $html, $m);
$cookie = $m[1];

$applications = process_page($html);

foreach ($applications as $key => $value) {
    scraperwiki::save(array('appref'),$value,$value["date"],array(floatval($value["latitude"]),floatval($value["longitude"])));
}

if(stristr($html,"Currently viewing page")) {   # There's >1 pages of results

    # I'm sorry. I'm so sorry.

    $hackysplice  = explode("Currently viewing page",$html);
    $hackysplice2 = explode("</font>",$hackysplice[1]);
    $hackysplice3 = explode(" of ",$hackysplice2[0]);
    $numpages = intval($hackysplice3[1]);

    while ($thispage < $numpages) {
        $postvars["page_num"] = $thispage;
        #print $thispage . " of " . $numpages . "\n";
        $postvars["Op"] = 1;
        $html = scraperpost("http://planning.corkcity.ie/InternetEnquiry/frmSelCritSearch.asp?page_num=" . $thispage . "&Op=1",NULL,$cookie);

        $applications = process_page($html);

        foreach ($applications as $key => $value) {
            scraperwiki::save(array('appref','url'),$value,$value["date"],array(floatval($value["latitude"]),floatval($value["longitude"])));
        }
        $thispage += 1;
    }
}

?>