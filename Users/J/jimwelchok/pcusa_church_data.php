<?php
require 'scraperwiki/simple_html_dom.php';
// TOC:                                 Scrape PCUSA
// MAIN
//  1 getpbypins($dom)                             scrape list of presbyteries from a page
//        clean_pby($name)                         clean presbytery name
//  2 scrape_synods()                              scrape synod pages to match Pbys to each synod
//  3 scrape_All_pby()                             scrape all of the presbytery for basic church info
//        scrape_pby_pages($pby_id)                scrape one of the presbytery all of its pages for all of the churches
//            scrape_pby_page($pby_id, $page)      scrape one pby page for all churches.
//                getchurch($data, $pby_id)        scrape churches from a presbytry page.
//                    clean_one_church($oldname)   clean up names to std
//  4 scrape_all_church_detail()                   call scrape_church_detail for each church
//        scrape_church_detail($cid)               scrape Phone/Fax/Website/Email - ignore adr1, adr2, state, city, name.
//  5 scrape_stats()                               scrape ALL church CSV files for statistics.
//        scrape_one_stat($cid)                    Scape one church CSV file for statistics.
//            get_value($value)                    remove cents, then thousands sep
//  ************
//  6 sum_all_pby()                                Propagate summary of stats up to presbytery.
//        sum_one_pby($pby_id)                         Propagate summary of church stats up to presbytery
//  7 sum_all_synod()                              Propagate summary of pby stats up to synods
// *************************
//    verify_churches()                            Verify after the fact
//        verify_church_detail($cid)               scrape Phone/Fax/Website/Email - ignore adr1, adr2, state, city, name.
//
//    verify_all_cids()                            scrape all of the presbyteries to verify church ids
//        verify_pby_pages($pby_id)                verify all of the churches of all pages of one presbytery  
//             verify_pby_page($pby_id, $page)     Verify one pby page of churches.
//                getcid($data, $pby_id)           scrape church ID from a presbytry page.
//    scrape_pby_stats($pby_id)                    Scape ALL church CSV files for statistics. Pby by Pby (for testing)
//    getpbypage($pby_id, $page)                   get a presbytery page
//
//save_var:      Some take a lot of time, we have to save our place for restart after time exceded.
//  IndxInfo   - scrape_all_pby, verify_call _cids
//  IndxDetail - scrape_all_church_detail
//  IndxStat   - scrape_stats
//  IndxVer    - verify_churches
$churchcnt = 0;
$debug = 0;

//http://www.pcusa.org/search/congregations/?page=1&distance=15&by-presbytery=on&submit=Search&presbytery=150004&congregation=&criteria=
// *****************************************************
// get a presbytery page
//http://www.pcusa.org/search/congregations/?page=2&distance=15&by-presbytery=on&submit=Search&presbytery=150004&congregation=&criteria=
function getpbypage($pby_id, $page)
{
    if (strlen($pby_id) < 6)
        $pby_id = "0" . $pby_id;
    //print $pby_id;
    $url = "http://www.pcusa.org/search/congregations/?page=" . $page ."&distance=15&by-presbytery=on&submit=Search&presbytery=" . $pby_id . "&congregation=&criteria=";
    //print "pby_id:" . $pby_id . " page:" . $page . "\n";
    //print "url:" . $url ."\n";
    $html = scraperWiki::scrape($url);
    $dom = new simple_html_dom();
    $dom->load($html);
    //print "Dom size=". sizeof($dom) . "\n";
    return $dom;
}

// *****************************************************
// clean presbytery name
function clean_pby($name)
{
    $new_name = str_replace  ("Presbiterio De ", "", $name);
    $new_name = str_replace  ("Presbiterio Del ", "", $new_name );
    $new_name = str_replace  ("St ", "St. ", $new_name );
    $new_name = str_ireplace ("The ", "", $new_name );
    $new_name = str_replace  ("And ", "and ", $new_name );
    $new_name = str_replace  ("Charleston-", "Charleston ", $new_name );
    if (strcmp ($new_name, "Atlantic Korean") == 0)
        $new_name = str_replace  ("Atlantic Korean", "Atlantic Korean-American", $new_name );
    $new_name = str_replace  ("Muskingham", "Muskingum", $new_name );
    $new_name = str_replace  ("Northwest/", "", $new_name );
    $new_name = str_replace  ("Southwest/", "", $new_name );

    //if ($name != $new_name)
        //print "PBY old=\"" . $name . "\" new=\"" . $new_name . "\"\n";

    return $new_name;
}

// *****************************************************
// scrape list of presbyteries from a page.
function getpbypins($dom)
{
    global $debug;
    print "Scrape First page for list of Presbyteries\n";
    // List of presbyteries - PINs
    $pbys = array();
    $data = $dom->find("select[name='presbytery']", 0);
    foreach($data->find("option") as $tds)
    {
        $id = $tds->value;
        array_push($pbys, $id);
        $name = trim($tds->plaintext);
        $new_name = clean_pby($name);

        $record = array('pby_id' => intval($id), 'name' => $new_name , 'denom_id' => 1);

        //if($id == 35500) print "pby_id:" . intval($id) . " name:\"" . $new_name . "\"\n";

        scraperwiki::save_sqlite(array('pby_id'), $record, $table_name="presbyteries", $verbose=0);
    }
print "    Found " . sizeof($pbys) . " presbyteries\n";
}

// *****************************************************
// http://oga.pcusa.org/section/departments/mid-councils/links/
// scrape synod page to match Pbys to each synod.
function scrape_synods()
{
    $pbynames = scraperwiki::select("name from presbyteries");
    $pbyids = scraperwiki::select("pby_id from presbyteries");
    print "Scrape Synods for Pby info Pbys=" . sizeof($pbynames) . "\n" ;

    $url = "http://oga.pcusa.org/section/departments/mid-councils/links/";
    $html = scraperWiki::scrape($url);
    $dom = new simple_html_dom();
    $dom->load($html);
    $syn_id = 1;    // skip zero=not found
    $ok = 0; $fail = 0;
    // get list of synods
    foreach($dom->find("li") as $tds)
    {
        //$id = $tds->value;
        //print "id=" . intval($id) ;
        if (strpos ( $tds->plaintext , "Synod of " ) === false )
            continue;
        $sname = str_ireplace ("the ", "", str_replace ("Synod of", "", $tds->plaintext));
        $a = $tds->find("a", 0);
        $url = "http://oga.pcusa.org" . $a->href;

        $html = scraperWiki::scrape($url);
        $dom = new simple_html_dom();
        $dom->load($html);
        $a = $dom->find('div[id=main]', 0);
        $h = $a->find('h4');
        $xy = $h[0]->find('a');
        if (sizeof($xy) > 0)
            $url = $xy[0]->href . "\n";
        else
            $url = "";

        //print "SYNOD:". $syn_id. " Name=" . ($sname). " HTML: " . "http://oga.pcusa.org" . $a->href . "\n";
        $record = array('syn_id' => intval($syn_id), 'name' => $sname, 'url' => $url, 'denom_id' => 1);
        scraperwiki::save_sqlite(array('syn_id'), $record, $table_name="synods", $verbose=0);
        // match presbytery on page to DB
        $pby_syn = 0;
        foreach($a->find("li") as $tds)
        {
            // cleanup web Presbytery name
            $name = trim($tds->plaintext);
            $new_name = $name;
            $new_name = trim($new_name, ",-");
            $new_name = clean_pby($new_name);

            $a = $tds->find("a", 0);
            if (sizeof($a) === 0)
                continue;
            $url = $a->href;
            $pby_syn++;
            // Search Pby Names for match
            $rec = 0;
            foreach ($pbynames as $pn)
            {
                $old_name = $pn['name'];
                $old_namex = trim($old_name, ",-");
                if (strcasecmp($new_name, $old_namex) == 0)
                    break;
                $rec++;
            }
            if ($rec < sizeof($pbyids) )
            {    // found
                //print $rec . " of " . sizeof($pbyids) ."\n";
                //print "\"" . $pbynames[$rec]['name'] . "\"@" . $rec . "\n";
                $pby_id = $pbyids[$rec]['pby_id'];
                $record = array('pby_id' => $pby_id, 'syn_id' => $syn_id, 'url' => $url, 'name' => $new_name, 'denom_id' => 1);
                $ok++;
                if ($pby_id == 35500)
                    print "Pby_id:" . $pby_id ." Name:\"" . $name . "\n";
                scraperwiki::save_sqlite(array('pby_id'), $record, $table_name="presbyteries", $verbose=0);
            }
            else
            {
                print "can not find:\"" . $new_name . "\"\n";
                $fail++;
            }
        }  // end of foreach li in 'div[id=main]'

    print "SYNOD:". $syn_id. " Name=" . ($sname) . " #pbys=" . $pby_syn . "\n";

    $syn_id++;
    }  // end of foreach li in page

// manual data for input
$pby_id = 180183;
$xsyn_id = 8;
$url = "http://www.ekpusa.org/";
$record = array('pby_id' => $pby_id, 'syn_id' => $xsyn_id, 'url' => $url, 'name' => $name, 'denom_id' => 1);
scraperwiki::save_sqlite(array('pby_id'), $record, $table_name="presbyteries", $verbose=0);
$ok++;

// manual data for input
$pby_id = 115760;
$xsyn_id = 5;
$url = "http://presbyteryofwesternkentucky.yolasite.com/";
$record = array('pby_id' => $pby_id, 'syn_id' => $xsyn_id, 'url' => $url, 'name' => $name, 'denom_id' => 1);
scraperwiki::save_sqlite(array('pby_id'), $record, $table_name="presbyteries", $verbose=0);
$ok++;

print "Found " . $syn_id . " synods\n";
print "Presbyteries matched " . $ok . " out of " .  sizeof($pbyids). " No Match:" . $fail . "\n";
 }

// *****************************************************
// scrape churches from a presbytry page.
function getchurch($data, $pby_id)
{
    global $churchcnt;
    $new = array();
    //print "CH:" . $data. "\n";
    $a = $data->find("a", 0);

    // get the church pin from the html link
    $ref = $a->href;
    $cid = str_replace ("/" ,"",str_replace ("/congregations/","" ,$ref)) ;
    $new['church_id'] = $cid;
    $new['pby_id'] = $pby_id;
    $new['denom_id'] = 1;
    //print "Ch name:" . $a->plaintext . " cid:" . $cid . "\n";
    //$churchdat = scraperwiki::select("* from churches where church_id='" . $cid . "'");

    // Get the address field
    $p = $data->find("p", 0);
    //print "p:" . $p . "\n";
    $adr2 = ""; $adr3 = "";
    $i = 0;
    foreach( $p->find("span")as $value)
    {
        if ($i == 0) $adr1 = trim($value->plaintext, "% ");
        if ($i == 1) $adr2 = $value->plaintext;
        if ($i == 2) $adr3 = $value->plaintext;
        $i = $i + 1;
    }
    if ($i == 2)
    {    // if no extra adr, move city state zip to adr3
        $adr3 = $adr2;
        $adr2 = "";
    }
    //print "a1:" . $adr1 . " a2:" . $adr2 . " a3:" . $adr3 . "\n";
    $new['adr1'] = $adr1;
    $new['adr2'] = $adr2;
    // break out city, state, zip from adr3
    $pos = strpos($adr3, ",");
    $city  = trim(substr ( $adr3, 0, $pos) );
    $state = substr ( $adr3, $pos + 2, 2);
    $zip   = trim(substr ( $adr3, $pos + 5));
    if($state === "S.")
    {
        $state = "SC";
        $zip   = trim(substr($zip, 6));
    }
    //print "city:" . $city . " state:" . $state . " zip:" . $zip . "\n";
    if (strlen($zip) < 6)
        $zip = $zip . "-";
    //print "Ch name:" . $a->plaintext . " cid:" . $cid . " zip:" . $zip . "\n";
    $new['city']  = $city;
    $new['state'] = $state;
    $new['zip']   = $zip;

    // get the lat/lon from the paragraph
    $geo = explode("=", $p);
    $lat = str_replace ("\"", "", str_replace ("\" data-lon", "", $geo[2]));
    $pos = strpos($geo[3], ">");
    $lon = substr ( $geo[3], 0, $pos);
    $lon = str_replace ("\"", "", $lon);
    //print "lat:" . $lat . " lon:" . $lon . "\n";
    $name = clean_one_church($a->plaintext);
    $new['lat']  = $lat;
    $new['lon']  = $lon;
    $new['name'] = $name;
    // details later
    $new['url'] = "";
    $new['phone'] = "";
    $new['fax'] = "";
    $new['email'] = "";

    // store the church data
    scraperwiki::save_sqlite(array('church_id'), $new, $table_name="churches", $verbose=0);
    $churchcnt++;
}

// *****************************************************
// scrape one pby page for all churches.
function scrape_pby_page($pby_id, $page)
{
    global $debug;
    if ($debug) print "Pby:" . $pby_id . " Page:" . $page . "\n";

    $nextref = "";
    $dom  = getpbypage($pby_id, $page);

    $next = $dom->find("a[class='next']", 0);
    //print "Next:" . $next . "/" . sizeof($next) ."\n";

    // list of churches on this page.
    foreach( $dom->find('li[class^=result]') as $data)
        getchurch($data, $pby_id);
    $page++;
    return $next;
}

// *****************************************************
// scrape one of the presbytery all of its pages for all of the churches
function scrape_pby_pages($pby_id, $pbyi)
{
    global $churchcnt;
    $page = 1;
    do {  // each page
        $next = scrape_pby_page($pby_id, $page);
        $page++;
    } while ($next);
    print "Pby_id=" . $pby_id . " pages=" . $page . " Churches=" . $churchcnt . " #" . $pbyi . "\n";
}

// *****************************************************
// scrape all of the presbytery for basic church info
// starting with the first pby not scraped last time.
function scrape_All_pby()
{
    global $debug;
    $pbyids = scraperwiki::select("pby_id from presbyteries");
    $pbyi = scraperwiki::get_var('IndxInfo', "0");
    print "Scrape Pby@" . $pbyi . " for basic church info\n";

    do {   // each presbytery
        if ($pbyi < sizeof($pbyids ) )
            $pby_id = $pbyids[$pbyi]['pby_id'];

        scrape_pby_pages($pby_id, $pbyi);

        $pbyi++;
        if ($debug) print "next presby:". $pbyi . " of " . sizeof($pbyids) . "\n";
        scraperwiki::save_var('IndxInfo', $pbyi);

    } while ($pbyi < sizeof($pbyids));

    print "Finished scraping pbys for basic church info\n";
    $pbyi = 0;
    scraperwiki::save_var('IndxInfo', $pbyi);
    return $pbyi;
}

// *****************************************************
function scrape_all_church_detail()
{
    $CHI = scraperwiki::get_var('IndxDetail', "0");
    scraperwiki::attach("pcusa_church_data");
    $churches = scraperwiki::select("church_id from churches");
    print "Scrape Church Detail @". $CHI . " of " . sizeof($churches). " " . intval($CHI / sizeof($churches) * 100) . "%\n";
    while ($CHI < sizeof($churches)) {
        $church_id = $churches[$CHI];
        $cid = $church_id['church_id'];
        if (($CHI % 20) == 0)
            {
            print "Detail church:" . $cid . " " . $CHI . "/" . sizeof($churches) . " " . intval($CHI / sizeof($churches) * 100) . "%\n";
            }
        if ($cid != 886)
            scrape_church_detail($cid);
        $CHI++;
        scraperwiki::save_var('IndxDetail', $CHI);
    }
    print "Finished Church Detail\n";
    $CHI = 0;
    scraperwiki::save_var('IndxDetail', $CHI);
}

// *****************************************************
// http://www.pcusa.org/congregations/22990/
// scrape Phone/Fax/Website/Email
// ignore adr1, adr2, state, city, name.
function scrape_church_detail($cid)
{
    $churchdat = scraperwiki::select("* from churches where church_id='" . $cid . "'");
    $url = "http://www.pcusa.org/congregations/" .  $cid . "/";
    //print "url:" . $url ."\n";
    $html = scraperWiki::scrape($url);
    $dom = new simple_html_dom();
    $dom->load($html);
    //print "Dom size=". sizeof($dom) . "\n";

        $div = $dom->find('div[id=results-list]', 0);
        //print $dom->plaintext;
        $url = ""; $email = ""; $phone = ""; $fax = "";

        if (sizeof($div) == 0)
            {
            print "Church has no data@" . $cid . "\n";
            $err = scraperwiki::get_var('errors', "0");
            $err++;
            scraperwiki::save_var('errors', $err);
            return;
            }
        foreach($div->find("p") as $data)
        {
            //print "p size=" . sizeof($data) . ":" . $data->innertext . "\n";
            $s = $data->find("strong", 0);
            if (sizeof($s) !== 0)
            {
                $a = $s->plaintext;
                if ($a == "Phone:")
                    $churchdat[0]['phone'] = trim(str_replace("Phone:", "", $data->plaintext));
                elseif ($a == "Fax:")
                    $churchdat[0]['fax'] = trim(str_replace("Fax:", "", $data->plaintext));
                elseif ($a == "Website:")
                    {
                    $x = $data->find("a", 0);
                    $churchdat[0]['url'] = trim( $x->href);
                    }
                elseif ($a == "Email:")
                    {
                    $x = $data->find("a", 0);
                    $churchdat[0]['email'] = trim( str_replace("mailto:", "", $x->href));
                    }
            }
        }

     scraperwiki::save_sqlite(array('church_id'), $churchdat, $table_name="churches", $verbose=0);
     //print "CID=" . $cid . " url:" . $churchdat[0]['url'] . " email:" . $churchdat[0]['email'] . " Phone:" . $churchdat[0]['phone'] . " fax:" . $churchdat[0]['fax'] . "\n";
}

// *****************************************************
// scrape one pby page for all churches.
function verify_pby_page($pby_id, $page)
{
    global $debug;
    if ($debug) print "Pby:" . $pby_id . " Page:" . $page . "\n";

    $nextref = "";
    $dom  = getpbypage($pby_id, $page);

    $next = $dom->find("a[class='next']", 0);
    //print "Next:" . $next . "/" . sizeof($next) ."\n";

    // list of churches on this page.
    foreach( $dom->find('li[class^=result]') as $data)
        {
        $cid = getcid($data, $pby_id);
        $churchdat = scraperwiki::select("* from churches where church_id='" . $cid . "'");
        //print "church=" . $cid . " Pby=" . $pby_id . "\n";
        $churchdat[0]['verify'] = 2012;
        $churchdat[0]['church_id'] = $cid;
        scraperwiki::save_sqlite(array('church_id'), $churchdat, $table_name="churches", $verbose=0);
        }
    $page++;

    return $next;
}

// *****************************************************
// verify one of the presbytery all of its pages for all of the churches
function verify_pby_pages($pby_id)
{
    global $churchcnt;
    $start = $churchcnt;
    $page = 1;
 
    do {  // each page
        $next = verify_pby_page($pby_id, $page);
        $page++;
    } while ($next);
    $pbych = $churchcnt - $start;
    //print "Pby:" . $pby_id . " Churches=" . $pbych . " Pages=" . $page - 1 . "\n";
 
   return $pbych;
}

// *****************************************************
// scrape church ID from a presbytry page.
function getcid($data, $pby_id)
{
    global $churchcnt;
    //print "CH:" . $data. "\n";
    $a = $data->find("a", 0);

    // get the church pin from the html link
    $ref = $a->href;
    $cid = str_replace ("/" ,"",str_replace ("/congregations/","" ,$ref)) ;
    //print "Ch name:" . $a->plaintext . " cid:" . $cid . "\n";
    $churchcnt++;

    return $cid;
}

// *****************************************************
// scrape all of the presbytery to verify church ids r
function verify_all_cids()
{
    global $debug;
    global $churchcnt;

    $pbyids = scraperwiki::select("pby_id from presbyteries");
    $pbyi = scraperwiki::get_var('IndxVer', "0");
    //$pbyi = 0;
    print "Verify Pby@" . $pbyi . " for church cids\n";

    do {   // each presbytery
        if ($pbyi < sizeof($pbyids ) )
            $pby_id = $pbyids[$pbyi]['pby_id'];

        $pbych = verify_pby_pages($pby_id);

        $pbyi++;
        if ($debug) print "next presby:". $pbyi . " of " . sizeof($pbyids) . "\n";
        scraperwiki::save_var('IndxVer', $pbyi);
        $per = intval($pbyi / sizeof($pbyids) * 100);
        print "Pby:" . $pby_id . " Churches=" . $pbych . "/" . $churchcnt . " Pby=" . $pbyi . " of " . sizeof($pbyids) . " " . $per . "%\n";

    } while ($pbyi < sizeof($pbyids));

    print "Finished verify pbys for church cids\n";
    $pbyi = 0;
    scraperwiki::save_var('IndxVer', $pbyi);
    return $pbyi;
}

// *****************************************************
// Verify after the fact
function verify_churches()
{
    $churches = scraperwiki::select("church_id from churches");
    print "Verify Churches " . sizeof($churches) . "\n" ;
    $fixed = 0;
    $size = sizeof($churches);
    $CHI = scraperwiki::get_var('IndxVer', "0");
    for( ; $CHI < $size; $CHI++)
    {
        $church_id = $churches[$CHI];
        $cid = $church_id['church_id'];
        if ($cid == "")
            continue;

        if (verify_church_detail($cid) == 0)
        {
        $fixed++;
        }
        scraperwiki::save_var('IndxVer', $CHI);

        if (($CHI % 100) == 0)
            {
            print "Verify church:" . $fixed . " " . $CHI . " of " . sizeof($churches) . "\n";
            }
    }
$pbyi = 0;
scraperwiki::save_var('IndxVer', $CHI);
print "Mismatch Check " . $fixed . " churches of " . $size . "\n";
}

// *****************************************************
// http://www.pcusa.org/congregations/22990/
// scrape Phone/Fax/Website/Email
// ignore adr1, adr2, state, city, name.
function verify_church_detail($cid)
{
    $name= ""; $adr1= ""; $adr2= ""; $adr3= "";
    $churchdat = scraperwiki::select("* from churches where church_id='" . $cid . "'");
    $url = "http://www.pcusa.org/congregations/" .  $cid;
    //print "url:" . $url ."\n";
    $html = scraperWiki::scrape($url);
    $dom = new simple_html_dom();
    $dom->load($html);
    //print "Dom size=". sizeof($dom) . "\n";

    $div  = $dom->find('div.result-info', 0);
    //print $div->outertext . "\n";
    $h = $div->find('h2');
    $name = clean_one_church($h[0]->plaintext);
    $i = 0;
    foreach($div->find("span") as $s)
    {
        if (sizeof($s))
        {
            if     ($i==0)  $adr1 = $s->plaintext;
            elseif ($i==1)  $adr2 = $s->plaintext;
            elseif ($i==2)  $adr3 = $s->plaintext;
        }
        $i++;
    }
    if (strlen($adr3) == 0) $adr3 = $adr2;
    //print "\"" .$adr1 . "\",\"" . $adr2 . "\",\"" . $adr3 . "\"\n" ;
    $pos = strpos($adr3, ",");
    $city  = trim(substr ( $adr3, 0, $pos) );
    $state = substr ( $adr3, $pos + 2, 2);
    $zip   = trim(substr ( $adr3, $pos + 5));
    $adr1  = trim(trim($adr1, "%"));

    $n = strcmp($churchdat[0]['name'],     $name)     != 0;
    $a = strcmp($churchdat[0]['adr1'],     $adr1)     != 0;
    $z = strncmp($churchdat[0]['zip'], $zip, 5) != 0;
    $s = strcmp($churchdat[0]['state'],    $state)    != 0;
    if ($n || $a || $z || $s)
    {
        print "MISMATCH CID=" . $cid . " N" .  $n  . " A" .  $a . " Z" . $z . " S" . $s . "\n";
        print "NEW name:\"" . $name . "\" adr1:\"" . $adr1 . "\" city:\"" . $city . "\" State:\"" . $state. "\" Zip:\"" . $zip . "\"\n";
        print "OLD name:\"" . $churchdat[0]['name'] . "\" adr1:\"" . $churchdat[0]['adr1'] . "\" city:\"" . $churchdat[0]['city'] . "\" State:\"" . $churchdat[0]['state']. "\" Zip:\"" . $churchdat[0]['zip'] . "\"\n";
        return 0;
    }
return 1;
}
// *****************************************************
//Scape ALL church CSV files for statistics. Pby by Pby (for testing)
function scrape_pby_stats($pby_id)
{
    global $debug;
    $CHI = 0;
    $badCnt = 0;
    $churches = scraperwiki::select("church_id from churches where pby_id=" . $pby_id);
    print "Scrape Stats Pby:" . $pby_id . " Churches:" . sizeof($churches) . "\n";

    while ($CHI < sizeof($churches)) {
        $church_id = $churches[$CHI];
        $cid = $church_id['church_id'];
        //if($debug)
        //if ($debug || ($CHI % 100) == 0)
        print "Stats church Empty=" . $badCnt . " " . $CHI . " of " . sizeof($churches) . " " . intval($CHI / sizeof($churches) * 100) . "%\n";
        if (scrape_one_stat($cid) == 0)
            $badCnt++;
        $CHI++;
    }
    print "Scrape Stats Done Churches=" . $CHI . " empty=" . $badCnt . "\n";
}

// *****************************************************
//Scape ALL church CSV files for statistics.
function scrape_stats()
{
    global $debug;
    $CHI = 0;
    $badCnt = 0;
    $CHI = scraperwiki::get_var('IndxStat', $CHI, "0");
    $churches = scraperwiki::select("church_id from churches");
    //print "Scrape Church Stats @" . $CHI . " of " . sizeof($churches). " " . intval($CHI / sizeof($churches) * 100) . "%\n" ;

    while ($CHI < sizeof($churches)) {
        $church = $churches[$CHI];
        $cid = $church['church_id'];
        if ($debug || ($CHI % 100) == 0)
           print "Stats church Empty=" . $badCnt. " " . $CHI . " of " . sizeof($churches) . " " . intval($CHI / sizeof($churches) * 100) . "%\n";
        if (scrape_one_stat($cid) == 0)
            $badCnt++;
        //print "Stats@" . $CHI . "/" . $cid . "\n";
        $CHI++;
        scraperwiki::save_var('IndxStat', $CHI);
    }
    print "Scrape Stats Done Churches=" . $CHI . " empty=" . $badCnt . "\n";
    scraperwiki::save_var('IndxStat', 0);
}

// *****************************************************
// remove cents, then thousands sep
function get_value($value)
{
    if( strlen($value) == 0)
        $value = "0";
    else
        $value = str_replace( ",", "",str_replace(".00", "", $value));
    return $value;
}

// *****************************************************
//Scape one church CSV file for statistics.
//http://apps.pcusa.org/tenyeartrends/report/22990/data_export.csv

function scrape_one_stat($cid)
{
    $yearcnt=0;
    $hdr=0;

//    $churchdat = scraperwiki::select("* from churches where church_id='" . $cid . "'");
    $data = scraperWiki::scrape('http://apps.pcusa.org/tenyeartrends/report/' . $cid . "/data_export.csv" );
    $stat = array();
    $stat[0]['church_id'] = $cid;

    $lines = explode("\n", $data);
    $rowcnt  = 0;
    //print_r($lines);

    //print "Scrape stat church=" . $cid . " lines=" . sizeof($lines) . "\n";
    foreach($lines as $row)
    {
        $row = str_getcsv($row);
        $rowcnt++;
        if ($rowcnt === 5)
            $hdr = $row;

        //print $rowcnt . ":" ;
        //$colcnt = 0;
        //foreach($row as $col)
            //{
            //print $col . ",";
            //++$colcnt;
            //}
        //print "\n";

        $colcnt = 0;
        foreach($row as $col)
            {
            if ($colcnt === 0)
               {
                $title = $col;
                ++$colcnt;
                continue;
               }
                if ($rowcnt <= 5)// no data until row 5
                break;

            $yr = $hdr[$colcnt];
            if ($yr === "")
                continue;
            $yearcnt++;

            if ($title === "Members")
                $stat[0]['mbr'.$yr] = get_value($col);

            if ($title === "Worship Attendance")
                $stat[0]['wor'.$yr] = get_value($col);

            if ($title === "Contributions ($)")
                $stat[0]['ctb'.$yr] = get_value($col);

            if ($title === "Baptized Members")
                $stat[0]['chd'.$yr] = get_value($col);

            if ($title === "Inactives")
                $stat[0]['ina'.$yr] = get_value($col);

            if ($title === "Death")
                $stat[0]['death'.$yr] = get_value($col);

            if ($title === "Infant Baptisms")
                $stat[0]['born'.$yr] = get_value($col);

            if ($title === "Per Capita Apportionment ($)")
                $stat[0]['per'.$yr] = get_value($col);

            ++$colcnt;
            }
     }
    if ($yearcnt)
        {
        scraperwiki::save_sqlite(array('church_id'), $stat, $table_name="stats", $verbose=0);
        //print "Cid:" . $cid . " Attendance:" . $stat[0]['wor2011'] . " Adherents:" . $stat[0]['mbr2011'] . " Contributions:" . $stat[0]['ctb2011'] . "\n";
        }
    else
        print "Church=" . $cid . " No Data in Source\n";
    //print_r($stat);
    return $yearcnt;
}

// *****************************************************
// Propagate summary of church stats up to presbytery
function sum_one_pby($pby_id)
{
    global $debug;
    $ch_cnt = 0;

    $mbr  = array();
    $wor  = array();
    $cont = array();

    //print "Sum Pby=" . $pby_id . "\n";

    $churches= scraperwiki::select("church_id from churches where pby_id=" . $pby_id);
    $pbydata = scraperwiki::select("* from presbyteries where pby_id=". $pby_id);

    foreach( $churches as $church )
        {
        $cid = $church['church_id'];
        //print "Sum Pby=" . $pby_id . " church=" . $cid . "\n";
        $stats = scraperwiki::select("* from stats where church_id=" . $cid);
        //print " #Stats=" . sizeof($stats) . "\n";
        if (sizeof($stats) == 0)
            {
            print "Sum Pby=" . $pby_id . " church=" . $cid . " No STATS \n";
            $ch_cnt++;
            continue;
            }
        $stat = $stats[0];
        if ($ch_cnt == 0)
            {        // first row set totals to zero.
            foreach($stat as $k => $col)
                {

                if (substr($k, 0, 3) == "mbr")
                    $mbr[$k] = 0;
                if (substr($k, 0, 3) == "wor")
                    $wor[$k] = 0;
                if (substr($k, 0, 3) == "ctb")
                    $cont[$k] = 0;
                }
            }
        foreach($stat as $k => $col)
            {
            if (substr($k, 0, 3) == "mbr")
                $mbr[$k] += $col;
            if (substr($k, 0, 3) == "wor")
                $wor[$k] += $col;
            if (substr($k, 0, 3) == "ctb")
                $cont[$k] += $col;
            }
        $ch_cnt++;
        }
    $cnt = 0;
    // add totals to the pby
    foreach($mbr as $k => $col)
        {
        $cnt++;
        $pbydata[0][$k] = $col;
        }
    foreach($wor as $k => $col)
        {
        $cnt++;
        $pbydata[0][$k] = $col;
        }
    foreach($cont as $k => $col)
        {
        $cnt++;
        $pbydata[0][$k] = $col;
        }

    $pbydata[0]['churches'] = $ch_cnt;
    $pbydata[0]['denom_id'] = 1;
    //print "Sum Pby@" . $pby_id . " #church=" . $ch_cnt. " #stats=" . $cnt . "\n";
    scraperwiki::save_sqlite(array('pby_id'), $pbydata, $table_name="presbyteries", $verbose=0);
}

// *****************************************************
// Propagate summary of church stats up to presbytery.
function sum_all_pby()
{
    global $debug;
    print "Sum All Presbyteries\n";
    $PBI= 0;
    $pbydata = scraperwiki::select("pby_id from presbyteries");
    foreach($pbydata as $pby)
    {
        $pby_id = $pby['pby_id'];
        sum_one_pby($pby_id);
        $per = $PBI / sizeof($pbydata) * 100;
        if (($per > 0) && ( ($per % 10) == 0) )
            print "Sum Pby@" . $pby_id . " " . $PBI . " " . intval($per) . "%\n";
        $PBI++;
    }
    print "Sum Pby " . $PBI . " of " . sizeof($pbydata) . "\n";
}

// *****************************************************
// Propagate summary of pby stats up to synods
function sum_all_synod()
{
    global $debug;
    print "Summing All Synods\n";

    $Gch_cnt = 0;
    $Gpby_cnt = 0;
    $Gsyn_cnt = 0;

    $Gmbr  = array();
    $Gwor  = array();
    $Gcont = array();

    $syndata = scraperwiki::select("syn_id from synods");
    foreach($syndata as $syn)
    {
        $syn_id = $syn['syn_id'];
        print "Sum Synod:" . $syn_id . "\n";

        $ch_cnt = 0;   // num of churches in synod

        $mbr  = array();
        $wor  = array();
        $cont = array();

        $syndata = scraperwiki::select("* from synods where syn_id=" . $syn_id);
        $pbydata = scraperwiki::select("* from presbyteries where syn_id=". $syn_id);

        if ($Gsyn_cnt == 0)
                {    // init totals to zero, and gather names (changes once a year)
                $pby = $pbydata[0];
                foreach($pby as $k => $col)
                    {
                    //print "PBY=" . $pby['pby_id'] . "\n";
                    if (substr($k, 0, 3) == "mbr")
                        $Gmbr[$k] = 0;
                    if (substr($k, 0, 3) == "wor")
                        $Gwor[$k] = 0;
                    if (substr($k, 0, 3) == "ctb")
                        $Gcont[$k] = 0;
                    }
                }
        $Gsyn_cnt++;

        $pby_cnt = 0;  // num of pbys in synod
        foreach($pbydata as $pby)
            {
            //print "Pby=" . $pby['pby_id']. "\n";
            if ($pby_cnt == 0)
                {    // init totals to zero, and gather names (changes once a year)
                foreach($pby as $k => $col)
                    {
                    if (substr($k, 0, 3) == "mbr")
                        $mbr[$k] = 0;
                    if (substr($k, 0, 3) == "wor")
                        $wor[$k] = 0;
                    if (substr($k, 0, 3) == "ctb")
                        $cont[$k] = 0;
                    }
                }
            else
                {    // total each pby into synod and denom totals
                foreach($pby as $k => $col)
                    {
                    if (substr($k, 0, 3) == "mbr")
                        $mbr[$k] += $col;
                    if (substr($k, 0, 3) == "wor")
                       $wor[$k] += $col;
                    if (substr($k, 0, 3) == "ctb")
                        $cont[$k] += $col;
                    }
                }
            $ch_cnt    += $pby['churches'];

            $pby_cnt++;
            }
        $Gch_cnt  += $ch_cnt;
        $Gpby_cnt += $pby_cnt;

        // copy totals to each synod DB, and totalize for denom
        foreach($mbr as $k => $col)
            {
            $syndata[0][$k] = $col;
            $Gmbr[$k] += $col;
            }
        foreach($wor as $k => $col)
            {
            $syndata[0][$k] = $col;
            $Gwor[$k] += $col;
            }
        foreach($cont as $k => $col)
            {
            $syndata[0][$k] = $col;
            $Gcont[$k] += $col;
            }

        $syndata[0]['churches']     = $ch_cnt;
        $syndata[0]['pbys']         = $pby_cnt;
        $syndata[0]['denom_id']     = 1;
        scraperwiki::save_sqlite(array('syn_id'), $syndata, $table_name="synods", $verbose=0);
    }
    $denom= array();
    print "Synods:" . $Gsyn_cnt . " pbys:" . $Gpby_cnt . " churches:" . $Gch_cnt . " members:" . $Gmbr['mbr2011']. " Worhsip:" . $Gwor['wor2011']. " Contributions:" . $Gcont['ctb2011'] . "\n";
    $denom[0]['name']         = 'pcusa';
    $denom[0]['denom_id']     = '1';
    $denom[0]['churches']     = $Gch_cnt;
    $denom[0]['presbyteries'] = $Gpby_cnt;
    $denom[0]['synods']       = $Gsyn_cnt;

    // copy totals to denom
    foreach($Gmbr as $k => $col)
        {
        $denom[0][$k] = $col;
        }
    foreach($Gwor as $k => $col)
        {
        $denom[0][$k] = $col;
        }
    foreach($Gcont as $k => $col)
        {
        $denom[0][$k] = $col;
        }
    //print_r($denom);
    scraperwiki::save_sqlite(array('denom_id'), $denom, $table_name="denom", $verbose=0);
}

// *****************************************************
// clean up names to std
function clean_one_church($oldname)
{
    $name = $oldname;
    $name = str_replace ("Presbyterian Church", "PC", $oldname);
    $name = str_replace ("United PC", "UPC", $name);
    // fix up abreviations and mis-spellings
    $name = str_replace ("3ast", "East", $name);
    $name = str_replace ("ChristChurch", "Christ Church", $name);
    $name = str_replace ("United Ch ", "United Church", $name);
    $name = str_replace ("Un ", "United ", $name);
    $name = str_replace ("Flsp", "Fellowship", $name);
    $name = str_replace ("Flshp", "Fellowship", $name);
    $name = str_replace ("St Lukes", "St Luke's", $name);
    $name = str_replace ("St Marks", "St Mark's", $name);
    $name = str_replace ("St Johns", "St John's", $name);
    $name = str_replace ("St Andrews", "St Andrew's", $name);
    $name = str_replace ("St Pauls", "St Paul's", $name);
    $name = str_replace ("St Stephens", "St Stephen's", $name);
    $name = str_replace ("St Marys", "St Mary's", $name);
    $name = str_replace ("Ch of", "Church of", $name);
    $name = str_replace (" Vlg", " Vilage", $name);
    $name = str_replace (" Vlge", " Vilage", $name);
    $name = str_replace (" Vlage", " Village", $name);
    $name = str_replace (" Vly", " Valley", $name);
    $name = str_replace ("Cong ", "Congregation ", $name);
    $name = str_replace ("Comm ", "Community ", $name);
    $name = str_replace ("Blmfld", "Bloomfield", $name);

    // change "PC of xxx PC" to "PC of xxxx"
    if (substr($name, 0, 5 ) == "PC " && substr($name, -2 ) == "PC" & strlen($name) > 6)
    {
        $name = substr($name, 0, -3);
       // print "Correct:" . $oldname . " to:" . $name . "\n";
    }

    // change "The PC xxxxx PC" to "The PC xxxxx"
    if (substr($name, 0, 5 ) == "The PC" && substr($name, -2 ) == "PC" & strlen($name) > 6)
    {
        $name = substr($name, 0, -3);
        //print "Correct:" . $oldname . " to:" . $name . "\n";
    }
    if (strpos($name, "PC of") !== false && substr($name, -2 ) == "PC")
    {
        $name = substr($name, 0, -3);
        //print "Correct:" . $oldname . " to:" . $name . "\n";
    }
    $name = trim($name);
    return $name;
}

// *****************************************************
function fix_stats()        // change null to zero stats
{
    $stats = scraperwiki::select("* from stats");
    $Cnt = 0;
    $Bad = 0;
    print "Fixing Stats " . sizeof($stats) . "\n";

    foreach($stats as $stat)
        {
        $dirty = 0;
        foreach($stat as $k => $v)
            {
            if (!isset($v))
                {
                $Bad++;
                $dirty = 1;
                //print "Bad k=" . $k . "\n";
                $stat[$k] = 0;
                }
            }
        if($dirty)
            scraperwiki::save_sqlite(array('church_id'), $stat, $table_name="stats", $verbose=0);
        $dirty = 0;
        if ( ($Cnt % 1000) == 0)
            print " Stats #" . $Cnt . " Bad=" . $Bad . "\n";
        $Cnt++;
        }
    print " Stats #" . $Cnt . " Bad=" . $Bad . "\n";
}

// *****************************************************
// *** MAIN ***
$init =  0;
$stop = 0;

// INIT variables
if ($stop)
{    // Must be run in this order.
    scraperwiki::save_var('GetPbyPins', 0);
    scraperwiki::save_var('GetSynods', 0);
    scraperwiki::save_var('GetChurchInfo', 0);
    scraperwiki::save_var('GetChurchDetail', 0);
    scraperwiki::save_var('GetChurchStats', 0);
    scraperwiki::save_var('SumPby', 0);
    scraperwiki::save_var('SumSyn', 0);
}
    // test stuff
//scraperwiki::save_var('IndxVer', 0);  // start over
//    scraperwiki::save_var('VerCh', 0);
//scraperwiki::save_var('IndxVer', 137);    // start over
//scraperwiki::save_var('VerCID', 1);// Test lines

//scraperwiki::save_var('GetPbyPins', 1);
//scraperwiki::save_var('GetSynods', 1);
//scraperwiki::save_var('IndxInfo', 0);    // start over
//scraperwiki::save_var('GetChurchInfo', 1);
//scraperwiki::save_var('IndxDetail', 0);
//scraperwiki::save_var('GetChurchDetail', 1);
scraperwiki::save_var('IndxStat', 0);  // start over
//scraperwiki::save_var('IndxStat',6000);
scraperwiki::save_var('GetChurchStats', 1);

    fix_stats();
//scraperwiki::save_var('SumPby', 1);
//scraperwiki::save_var('SumSyn', 1);

// INIT variables
if ($init)
{    // Must be run in this order.
    scraperwiki::save_var('GetPbyPins', 1);
    scraperwiki::save_var('GetSynods', 1);
    scraperwiki::save_var('GetChurchInfo', 1);
    scraperwiki::save_var('GetChurchDetail', 1);
    scraperwiki::save_var('GetChurchStats', 1);
    scraperwiki::save_var('SumPby', 1);
    scraperwiki::save_var('SumSyn', 1);

    // test stuff
    scraperwiki::save_var('VerCh', 0);
    scraperwiki::save_var('VerCID', 0);

    // these take a lot of time, we have to save our place for restart after time exceded.
    scraperwiki::save_var('IndxInfo', 0);    // scrape_all_pby, verify_call _cids
    scraperwiki::save_var('IndxDetail', 0);  // scrape_all_church_detail
    scraperwiki::save_var('IndxStat', 0);    // scrape_stats
    scraperwiki::save_var('IndxVer', 0);     // verify_churches
}

// Get List of Presbyteries from first page (It has magic code(pby_id) for pby pages)
if (scraperwiki::get_var('GetPbyPins', "0"))
{
    $dom  = getpbypage(150004, 1); // get any page
    $pbys = getpbypins($dom);
    scraperwiki::save_var('GetPbyPins', 0);
}

// Scrape Synod page for details of each presbytery
if (scraperwiki::get_var('GetSynods', "0"))
{
    scrape_synods();
    scraperwiki::save_var('GetSynods', 0);
}

//scrape Pby pages for church info.
if (scraperwiki::get_var('GetChurchInfo', "0"))
{
    scrape_All_pby();
    scraperwiki::save_var('GetChurchInfo', 0);
}

//scrape Church stat pages for church details.
if (scraperwiki::get_var('GetChurchDetail', "0"))
{
    scrape_all_church_detail();
    scraperwiki::save_var('GetChurchDetail', 0);
}

// scrape statistics page for each church
if (scraperwiki::get_var('GetChurchStats', "0"))
{
    scrape_stats();
    scraperwiki::save_var('GetChurchStats', 0);
}

// sum statistics from each church into each presbytery and synod
if (scraperwiki::get_var('SumPby', "0"))
{
    sum_all_pby();
    scraperwiki::save_var('SumPby', 0);
}

// sum statistics from each church into each presbytery and synod
if (scraperwiki::get_var('SumSyn', "0"))
{
    sum_all_synod();
    scraperwiki::save_var('SumSyn', 0);
}

// verify church page against pby page
if (scraperwiki::get_var('VerCID', "0"))
{
    verify_all_cids();

    scraperwiki::save_var('VerCID', 0);
}

// verify church page against pby page
if (scraperwiki::get_var('VerCh', "0"))
{
    verify_churches();
    scraperwiki::save_var('VerCh', 0);
}

// SINGLE TESTING CALLS

//$pby_id = "30012";
//scrape_pby_stats($pby_id);

//$pby_id = "180700";
//sum_one_pby($pby_id);

//scrape_pby_pages("30012", 1);    // scrape one pby all pages.

//$cid = 886;
//scrape_church_detail($cid);// scape one church detail

//$cid = 6935;
//scrape_one_stat($cid);// scrape single church statistics

//$cid = 6197;
//verify_church_detail($cid);

//$churchcnt = 0;
//$pby_id = 40628;
//verify_pby_pages($pby_id);

// delete bad data
//scraperwiki::sqliteexecute("delete from synods where syn_id=0");
//scraperwiki::sqliteexecute("drop table if exists churches");

?>
<?php
require 'scraperwiki/simple_html_dom.php';
// TOC:                                 Scrape PCUSA
// MAIN
//  1 getpbypins($dom)                             scrape list of presbyteries from a page
//        clean_pby($name)                         clean presbytery name
//  2 scrape_synods()                              scrape synod pages to match Pbys to each synod
//  3 scrape_All_pby()                             scrape all of the presbytery for basic church info
//        scrape_pby_pages($pby_id)                scrape one of the presbytery all of its pages for all of the churches
//            scrape_pby_page($pby_id, $page)      scrape one pby page for all churches.
//                getchurch($data, $pby_id)        scrape churches from a presbytry page.
//                    clean_one_church($oldname)   clean up names to std
//  4 scrape_all_church_detail()                   call scrape_church_detail for each church
//        scrape_church_detail($cid)               scrape Phone/Fax/Website/Email - ignore adr1, adr2, state, city, name.
//  5 scrape_stats()                               scrape ALL church CSV files for statistics.
//        scrape_one_stat($cid)                    Scape one church CSV file for statistics.
//            get_value($value)                    remove cents, then thousands sep
//  ************
//  6 sum_all_pby()                                Propagate summary of stats up to presbytery.
//        sum_one_pby($pby_id)                         Propagate summary of church stats up to presbytery
//  7 sum_all_synod()                              Propagate summary of pby stats up to synods
// *************************
//    verify_churches()                            Verify after the fact
//        verify_church_detail($cid)               scrape Phone/Fax/Website/Email - ignore adr1, adr2, state, city, name.
//
//    verify_all_cids()                            scrape all of the presbyteries to verify church ids
//        verify_pby_pages($pby_id)                verify all of the churches of all pages of one presbytery  
//             verify_pby_page($pby_id, $page)     Verify one pby page of churches.
//                getcid($data, $pby_id)           scrape church ID from a presbytry page.
//    scrape_pby_stats($pby_id)                    Scape ALL church CSV files for statistics. Pby by Pby (for testing)
//    getpbypage($pby_id, $page)                   get a presbytery page
//
//save_var:      Some take a lot of time, we have to save our place for restart after time exceded.
//  IndxInfo   - scrape_all_pby, verify_call _cids
//  IndxDetail - scrape_all_church_detail
//  IndxStat   - scrape_stats
//  IndxVer    - verify_churches
$churchcnt = 0;
$debug = 0;

//http://www.pcusa.org/search/congregations/?page=1&distance=15&by-presbytery=on&submit=Search&presbytery=150004&congregation=&criteria=
// *****************************************************
// get a presbytery page
//http://www.pcusa.org/search/congregations/?page=2&distance=15&by-presbytery=on&submit=Search&presbytery=150004&congregation=&criteria=
function getpbypage($pby_id, $page)
{
    if (strlen($pby_id) < 6)
        $pby_id = "0" . $pby_id;
    //print $pby_id;
    $url = "http://www.pcusa.org/search/congregations/?page=" . $page ."&distance=15&by-presbytery=on&submit=Search&presbytery=" . $pby_id . "&congregation=&criteria=";
    //print "pby_id:" . $pby_id . " page:" . $page . "\n";
    //print "url:" . $url ."\n";
    $html = scraperWiki::scrape($url);
    $dom = new simple_html_dom();
    $dom->load($html);
    //print "Dom size=". sizeof($dom) . "\n";
    return $dom;
}

// *****************************************************
// clean presbytery name
function clean_pby($name)
{
    $new_name = str_replace  ("Presbiterio De ", "", $name);
    $new_name = str_replace  ("Presbiterio Del ", "", $new_name );
    $new_name = str_replace  ("St ", "St. ", $new_name );
    $new_name = str_ireplace ("The ", "", $new_name );
    $new_name = str_replace  ("And ", "and ", $new_name );
    $new_name = str_replace  ("Charleston-", "Charleston ", $new_name );
    if (strcmp ($new_name, "Atlantic Korean") == 0)
        $new_name = str_replace  ("Atlantic Korean", "Atlantic Korean-American", $new_name );
    $new_name = str_replace  ("Muskingham", "Muskingum", $new_name );
    $new_name = str_replace  ("Northwest/", "", $new_name );
    $new_name = str_replace  ("Southwest/", "", $new_name );

    //if ($name != $new_name)
        //print "PBY old=\"" . $name . "\" new=\"" . $new_name . "\"\n";

    return $new_name;
}

// *****************************************************
// scrape list of presbyteries from a page.
function getpbypins($dom)
{
    global $debug;
    print "Scrape First page for list of Presbyteries\n";
    // List of presbyteries - PINs
    $pbys = array();
    $data = $dom->find("select[name='presbytery']", 0);
    foreach($data->find("option") as $tds)
    {
        $id = $tds->value;
        array_push($pbys, $id);
        $name = trim($tds->plaintext);
        $new_name = clean_pby($name);

        $record = array('pby_id' => intval($id), 'name' => $new_name , 'denom_id' => 1);

        //if($id == 35500) print "pby_id:" . intval($id) . " name:\"" . $new_name . "\"\n";

        scraperwiki::save_sqlite(array('pby_id'), $record, $table_name="presbyteries", $verbose=0);
    }
print "    Found " . sizeof($pbys) . " presbyteries\n";
}

// *****************************************************
// http://oga.pcusa.org/section/departments/mid-councils/links/
// scrape synod page to match Pbys to each synod.
function scrape_synods()
{
    $pbynames = scraperwiki::select("name from presbyteries");
    $pbyids = scraperwiki::select("pby_id from presbyteries");
    print "Scrape Synods for Pby info Pbys=" . sizeof($pbynames) . "\n" ;

    $url = "http://oga.pcusa.org/section/departments/mid-councils/links/";
    $html = scraperWiki::scrape($url);
    $dom = new simple_html_dom();
    $dom->load($html);
    $syn_id = 1;    // skip zero=not found
    $ok = 0; $fail = 0;
    // get list of synods
    foreach($dom->find("li") as $tds)
    {
        //$id = $tds->value;
        //print "id=" . intval($id) ;
        if (strpos ( $tds->plaintext , "Synod of " ) === false )
            continue;
        $sname = str_ireplace ("the ", "", str_replace ("Synod of", "", $tds->plaintext));
        $a = $tds->find("a", 0);
        $url = "http://oga.pcusa.org" . $a->href;

        $html = scraperWiki::scrape($url);
        $dom = new simple_html_dom();
        $dom->load($html);
        $a = $dom->find('div[id=main]', 0);
        $h = $a->find('h4');
        $xy = $h[0]->find('a');
        if (sizeof($xy) > 0)
            $url = $xy[0]->href . "\n";
        else
            $url = "";

        //print "SYNOD:". $syn_id. " Name=" . ($sname). " HTML: " . "http://oga.pcusa.org" . $a->href . "\n";
        $record = array('syn_id' => intval($syn_id), 'name' => $sname, 'url' => $url, 'denom_id' => 1);
        scraperwiki::save_sqlite(array('syn_id'), $record, $table_name="synods", $verbose=0);
        // match presbytery on page to DB
        $pby_syn = 0;
        foreach($a->find("li") as $tds)
        {
            // cleanup web Presbytery name
            $name = trim($tds->plaintext);
            $new_name = $name;
            $new_name = trim($new_name, ",-");
            $new_name = clean_pby($new_name);

            $a = $tds->find("a", 0);
            if (sizeof($a) === 0)
                continue;
            $url = $a->href;
            $pby_syn++;
            // Search Pby Names for match
            $rec = 0;
            foreach ($pbynames as $pn)
            {
                $old_name = $pn['name'];
                $old_namex = trim($old_name, ",-");
                if (strcasecmp($new_name, $old_namex) == 0)
                    break;
                $rec++;
            }
            if ($rec < sizeof($pbyids) )
            {    // found
                //print $rec . " of " . sizeof($pbyids) ."\n";
                //print "\"" . $pbynames[$rec]['name'] . "\"@" . $rec . "\n";
                $pby_id = $pbyids[$rec]['pby_id'];
                $record = array('pby_id' => $pby_id, 'syn_id' => $syn_id, 'url' => $url, 'name' => $new_name, 'denom_id' => 1);
                $ok++;
                if ($pby_id == 35500)
                    print "Pby_id:" . $pby_id ." Name:\"" . $name . "\n";
                scraperwiki::save_sqlite(array('pby_id'), $record, $table_name="presbyteries", $verbose=0);
            }
            else
            {
                print "can not find:\"" . $new_name . "\"\n";
                $fail++;
            }
        }  // end of foreach li in 'div[id=main]'

    print "SYNOD:". $syn_id. " Name=" . ($sname) . " #pbys=" . $pby_syn . "\n";

    $syn_id++;
    }  // end of foreach li in page

// manual data for input
$pby_id = 180183;
$xsyn_id = 8;
$url = "http://www.ekpusa.org/";
$record = array('pby_id' => $pby_id, 'syn_id' => $xsyn_id, 'url' => $url, 'name' => $name, 'denom_id' => 1);
scraperwiki::save_sqlite(array('pby_id'), $record, $table_name="presbyteries", $verbose=0);
$ok++;

// manual data for input
$pby_id = 115760;
$xsyn_id = 5;
$url = "http://presbyteryofwesternkentucky.yolasite.com/";
$record = array('pby_id' => $pby_id, 'syn_id' => $xsyn_id, 'url' => $url, 'name' => $name, 'denom_id' => 1);
scraperwiki::save_sqlite(array('pby_id'), $record, $table_name="presbyteries", $verbose=0);
$ok++;

print "Found " . $syn_id . " synods\n";
print "Presbyteries matched " . $ok . " out of " .  sizeof($pbyids). " No Match:" . $fail . "\n";
 }

// *****************************************************
// scrape churches from a presbytry page.
function getchurch($data, $pby_id)
{
    global $churchcnt;
    $new = array();
    //print "CH:" . $data. "\n";
    $a = $data->find("a", 0);

    // get the church pin from the html link
    $ref = $a->href;
    $cid = str_replace ("/" ,"",str_replace ("/congregations/","" ,$ref)) ;
    $new['church_id'] = $cid;
    $new['pby_id'] = $pby_id;
    $new['denom_id'] = 1;
    //print "Ch name:" . $a->plaintext . " cid:" . $cid . "\n";
    //$churchdat = scraperwiki::select("* from churches where church_id='" . $cid . "'");

    // Get the address field
    $p = $data->find("p", 0);
    //print "p:" . $p . "\n";
    $adr2 = ""; $adr3 = "";
    $i = 0;
    foreach( $p->find("span")as $value)
    {
        if ($i == 0) $adr1 = trim($value->plaintext, "% ");
        if ($i == 1) $adr2 = $value->plaintext;
        if ($i == 2) $adr3 = $value->plaintext;
        $i = $i + 1;
    }
    if ($i == 2)
    {    // if no extra adr, move city state zip to adr3
        $adr3 = $adr2;
        $adr2 = "";
    }
    //print "a1:" . $adr1 . " a2:" . $adr2 . " a3:" . $adr3 . "\n";
    $new['adr1'] = $adr1;
    $new['adr2'] = $adr2;
    // break out city, state, zip from adr3
    $pos = strpos($adr3, ",");
    $city  = trim(substr ( $adr3, 0, $pos) );
    $state = substr ( $adr3, $pos + 2, 2);
    $zip   = trim(substr ( $adr3, $pos + 5));
    if($state === "S.")
    {
        $state = "SC";
        $zip   = trim(substr($zip, 6));
    }
    //print "city:" . $city . " state:" . $state . " zip:" . $zip . "\n";
    if (strlen($zip) < 6)
        $zip = $zip . "-";
    //print "Ch name:" . $a->plaintext . " cid:" . $cid . " zip:" . $zip . "\n";
    $new['city']  = $city;
    $new['state'] = $state;
    $new['zip']   = $zip;

    // get the lat/lon from the paragraph
    $geo = explode("=", $p);
    $lat = str_replace ("\"", "", str_replace ("\" data-lon", "", $geo[2]));
    $pos = strpos($geo[3], ">");
    $lon = substr ( $geo[3], 0, $pos);
    $lon = str_replace ("\"", "", $lon);
    //print "lat:" . $lat . " lon:" . $lon . "\n";
    $name = clean_one_church($a->plaintext);
    $new['lat']  = $lat;
    $new['lon']  = $lon;
    $new['name'] = $name;
    // details later
    $new['url'] = "";
    $new['phone'] = "";
    $new['fax'] = "";
    $new['email'] = "";

    // store the church data
    scraperwiki::save_sqlite(array('church_id'), $new, $table_name="churches", $verbose=0);
    $churchcnt++;
}

// *****************************************************
// scrape one pby page for all churches.
function scrape_pby_page($pby_id, $page)
{
    global $debug;
    if ($debug) print "Pby:" . $pby_id . " Page:" . $page . "\n";

    $nextref = "";
    $dom  = getpbypage($pby_id, $page);

    $next = $dom->find("a[class='next']", 0);
    //print "Next:" . $next . "/" . sizeof($next) ."\n";

    // list of churches on this page.
    foreach( $dom->find('li[class^=result]') as $data)
        getchurch($data, $pby_id);
    $page++;
    return $next;
}

// *****************************************************
// scrape one of the presbytery all of its pages for all of the churches
function scrape_pby_pages($pby_id, $pbyi)
{
    global $churchcnt;
    $page = 1;
    do {  // each page
        $next = scrape_pby_page($pby_id, $page);
        $page++;
    } while ($next);
    print "Pby_id=" . $pby_id . " pages=" . $page . " Churches=" . $churchcnt . " #" . $pbyi . "\n";
}

// *****************************************************
// scrape all of the presbytery for basic church info
// starting with the first pby not scraped last time.
function scrape_All_pby()
{
    global $debug;
    $pbyids = scraperwiki::select("pby_id from presbyteries");
    $pbyi = scraperwiki::get_var('IndxInfo', "0");
    print "Scrape Pby@" . $pbyi . " for basic church info\n";

    do {   // each presbytery
        if ($pbyi < sizeof($pbyids ) )
            $pby_id = $pbyids[$pbyi]['pby_id'];

        scrape_pby_pages($pby_id, $pbyi);

        $pbyi++;
        if ($debug) print "next presby:". $pbyi . " of " . sizeof($pbyids) . "\n";
        scraperwiki::save_var('IndxInfo', $pbyi);

    } while ($pbyi < sizeof($pbyids));

    print "Finished scraping pbys for basic church info\n";
    $pbyi = 0;
    scraperwiki::save_var('IndxInfo', $pbyi);
    return $pbyi;
}

// *****************************************************
function scrape_all_church_detail()
{
    $CHI = scraperwiki::get_var('IndxDetail', "0");
    scraperwiki::attach("pcusa_church_data");
    $churches = scraperwiki::select("church_id from churches");
    print "Scrape Church Detail @". $CHI . " of " . sizeof($churches). " " . intval($CHI / sizeof($churches) * 100) . "%\n";
    while ($CHI < sizeof($churches)) {
        $church_id = $churches[$CHI];
        $cid = $church_id['church_id'];
        if (($CHI % 20) == 0)
            {
            print "Detail church:" . $cid . " " . $CHI . "/" . sizeof($churches) . " " . intval($CHI / sizeof($churches) * 100) . "%\n";
            }
        if ($cid != 886)
            scrape_church_detail($cid);
        $CHI++;
        scraperwiki::save_var('IndxDetail', $CHI);
    }
    print "Finished Church Detail\n";
    $CHI = 0;
    scraperwiki::save_var('IndxDetail', $CHI);
}

// *****************************************************
// http://www.pcusa.org/congregations/22990/
// scrape Phone/Fax/Website/Email
// ignore adr1, adr2, state, city, name.
function scrape_church_detail($cid)
{
    $churchdat = scraperwiki::select("* from churches where church_id='" . $cid . "'");
    $url = "http://www.pcusa.org/congregations/" .  $cid . "/";
    //print "url:" . $url ."\n";
    $html = scraperWiki::scrape($url);
    $dom = new simple_html_dom();
    $dom->load($html);
    //print "Dom size=". sizeof($dom) . "\n";

        $div = $dom->find('div[id=results-list]', 0);
        //print $dom->plaintext;
        $url = ""; $email = ""; $phone = ""; $fax = "";

        if (sizeof($div) == 0)
            {
            print "Church has no data@" . $cid . "\n";
            $err = scraperwiki::get_var('errors', "0");
            $err++;
            scraperwiki::save_var('errors', $err);
            return;
            }
        foreach($div->find("p") as $data)
        {
            //print "p size=" . sizeof($data) . ":" . $data->innertext . "\n";
            $s = $data->find("strong", 0);
            if (sizeof($s) !== 0)
            {
                $a = $s->plaintext;
                if ($a == "Phone:")
                    $churchdat[0]['phone'] = trim(str_replace("Phone:", "", $data->plaintext));
                elseif ($a == "Fax:")
                    $churchdat[0]['fax'] = trim(str_replace("Fax:", "", $data->plaintext));
                elseif ($a == "Website:")
                    {
                    $x = $data->find("a", 0);
                    $churchdat[0]['url'] = trim( $x->href);
                    }
                elseif ($a == "Email:")
                    {
                    $x = $data->find("a", 0);
                    $churchdat[0]['email'] = trim( str_replace("mailto:", "", $x->href));
                    }
            }
        }

     scraperwiki::save_sqlite(array('church_id'), $churchdat, $table_name="churches", $verbose=0);
     //print "CID=" . $cid . " url:" . $churchdat[0]['url'] . " email:" . $churchdat[0]['email'] . " Phone:" . $churchdat[0]['phone'] . " fax:" . $churchdat[0]['fax'] . "\n";
}

// *****************************************************
// scrape one pby page for all churches.
function verify_pby_page($pby_id, $page)
{
    global $debug;
    if ($debug) print "Pby:" . $pby_id . " Page:" . $page . "\n";

    $nextref = "";
    $dom  = getpbypage($pby_id, $page);

    $next = $dom->find("a[class='next']", 0);
    //print "Next:" . $next . "/" . sizeof($next) ."\n";

    // list of churches on this page.
    foreach( $dom->find('li[class^=result]') as $data)
        {
        $cid = getcid($data, $pby_id);
        $churchdat = scraperwiki::select("* from churches where church_id='" . $cid . "'");
        //print "church=" . $cid . " Pby=" . $pby_id . "\n";
        $churchdat[0]['verify'] = 2012;
        $churchdat[0]['church_id'] = $cid;
        scraperwiki::save_sqlite(array('church_id'), $churchdat, $table_name="churches", $verbose=0);
        }
    $page++;

    return $next;
}

// *****************************************************
// verify one of the presbytery all of its pages for all of the churches
function verify_pby_pages($pby_id)
{
    global $churchcnt;
    $start = $churchcnt;
    $page = 1;
 
    do {  // each page
        $next = verify_pby_page($pby_id, $page);
        $page++;
    } while ($next);
    $pbych = $churchcnt - $start;
    //print "Pby:" . $pby_id . " Churches=" . $pbych . " Pages=" . $page - 1 . "\n";
 
   return $pbych;
}

// *****************************************************
// scrape church ID from a presbytry page.
function getcid($data, $pby_id)
{
    global $churchcnt;
    //print "CH:" . $data. "\n";
    $a = $data->find("a", 0);

    // get the church pin from the html link
    $ref = $a->href;
    $cid = str_replace ("/" ,"",str_replace ("/congregations/","" ,$ref)) ;
    //print "Ch name:" . $a->plaintext . " cid:" . $cid . "\n";
    $churchcnt++;

    return $cid;
}

// *****************************************************
// scrape all of the presbytery to verify church ids r
function verify_all_cids()
{
    global $debug;
    global $churchcnt;

    $pbyids = scraperwiki::select("pby_id from presbyteries");
    $pbyi = scraperwiki::get_var('IndxVer', "0");
    //$pbyi = 0;
    print "Verify Pby@" . $pbyi . " for church cids\n";

    do {   // each presbytery
        if ($pbyi < sizeof($pbyids ) )
            $pby_id = $pbyids[$pbyi]['pby_id'];

        $pbych = verify_pby_pages($pby_id);

        $pbyi++;
        if ($debug) print "next presby:". $pbyi . " of " . sizeof($pbyids) . "\n";
        scraperwiki::save_var('IndxVer', $pbyi);
        $per = intval($pbyi / sizeof($pbyids) * 100);
        print "Pby:" . $pby_id . " Churches=" . $pbych . "/" . $churchcnt . " Pby=" . $pbyi . " of " . sizeof($pbyids) . " " . $per . "%\n";

    } while ($pbyi < sizeof($pbyids));

    print "Finished verify pbys for church cids\n";
    $pbyi = 0;
    scraperwiki::save_var('IndxVer', $pbyi);
    return $pbyi;
}

// *****************************************************
// Verify after the fact
function verify_churches()
{
    $churches = scraperwiki::select("church_id from churches");
    print "Verify Churches " . sizeof($churches) . "\n" ;
    $fixed = 0;
    $size = sizeof($churches);
    $CHI = scraperwiki::get_var('IndxVer', "0");
    for( ; $CHI < $size; $CHI++)
    {
        $church_id = $churches[$CHI];
        $cid = $church_id['church_id'];
        if ($cid == "")
            continue;

        if (verify_church_detail($cid) == 0)
        {
        $fixed++;
        }
        scraperwiki::save_var('IndxVer', $CHI);

        if (($CHI % 100) == 0)
            {
            print "Verify church:" . $fixed . " " . $CHI . " of " . sizeof($churches) . "\n";
            }
    }
$pbyi = 0;
scraperwiki::save_var('IndxVer', $CHI);
print "Mismatch Check " . $fixed . " churches of " . $size . "\n";
}

// *****************************************************
// http://www.pcusa.org/congregations/22990/
// scrape Phone/Fax/Website/Email
// ignore adr1, adr2, state, city, name.
function verify_church_detail($cid)
{
    $name= ""; $adr1= ""; $adr2= ""; $adr3= "";
    $churchdat = scraperwiki::select("* from churches where church_id='" . $cid . "'");
    $url = "http://www.pcusa.org/congregations/" .  $cid;
    //print "url:" . $url ."\n";
    $html = scraperWiki::scrape($url);
    $dom = new simple_html_dom();
    $dom->load($html);
    //print "Dom size=". sizeof($dom) . "\n";

    $div  = $dom->find('div.result-info', 0);
    //print $div->outertext . "\n";
    $h = $div->find('h2');
    $name = clean_one_church($h[0]->plaintext);
    $i = 0;
    foreach($div->find("span") as $s)
    {
        if (sizeof($s))
        {
            if     ($i==0)  $adr1 = $s->plaintext;
            elseif ($i==1)  $adr2 = $s->plaintext;
            elseif ($i==2)  $adr3 = $s->plaintext;
        }
        $i++;
    }
    if (strlen($adr3) == 0) $adr3 = $adr2;
    //print "\"" .$adr1 . "\",\"" . $adr2 . "\",\"" . $adr3 . "\"\n" ;
    $pos = strpos($adr3, ",");
    $city  = trim(substr ( $adr3, 0, $pos) );
    $state = substr ( $adr3, $pos + 2, 2);
    $zip   = trim(substr ( $adr3, $pos + 5));
    $adr1  = trim(trim($adr1, "%"));

    $n = strcmp($churchdat[0]['name'],     $name)     != 0;
    $a = strcmp($churchdat[0]['adr1'],     $adr1)     != 0;
    $z = strncmp($churchdat[0]['zip'], $zip, 5) != 0;
    $s = strcmp($churchdat[0]['state'],    $state)    != 0;
    if ($n || $a || $z || $s)
    {
        print "MISMATCH CID=" . $cid . " N" .  $n  . " A" .  $a . " Z" . $z . " S" . $s . "\n";
        print "NEW name:\"" . $name . "\" adr1:\"" . $adr1 . "\" city:\"" . $city . "\" State:\"" . $state. "\" Zip:\"" . $zip . "\"\n";
        print "OLD name:\"" . $churchdat[0]['name'] . "\" adr1:\"" . $churchdat[0]['adr1'] . "\" city:\"" . $churchdat[0]['city'] . "\" State:\"" . $churchdat[0]['state']. "\" Zip:\"" . $churchdat[0]['zip'] . "\"\n";
        return 0;
    }
return 1;
}
// *****************************************************
//Scape ALL church CSV files for statistics. Pby by Pby (for testing)
function scrape_pby_stats($pby_id)
{
    global $debug;
    $CHI = 0;
    $badCnt = 0;
    $churches = scraperwiki::select("church_id from churches where pby_id=" . $pby_id);
    print "Scrape Stats Pby:" . $pby_id . " Churches:" . sizeof($churches) . "\n";

    while ($CHI < sizeof($churches)) {
        $church_id = $churches[$CHI];
        $cid = $church_id['church_id'];
        //if($debug)
        //if ($debug || ($CHI % 100) == 0)
        print "Stats church Empty=" . $badCnt . " " . $CHI . " of " . sizeof($churches) . " " . intval($CHI / sizeof($churches) * 100) . "%\n";
        if (scrape_one_stat($cid) == 0)
            $badCnt++;
        $CHI++;
    }
    print "Scrape Stats Done Churches=" . $CHI . " empty=" . $badCnt . "\n";
}

// *****************************************************
//Scape ALL church CSV files for statistics.
function scrape_stats()
{
    global $debug;
    $CHI = 0;
    $badCnt = 0;
    $CHI = scraperwiki::get_var('IndxStat', $CHI, "0");
    $churches = scraperwiki::select("church_id from churches");
    //print "Scrape Church Stats @" . $CHI . " of " . sizeof($churches). " " . intval($CHI / sizeof($churches) * 100) . "%\n" ;

    while ($CHI < sizeof($churches)) {
        $church = $churches[$CHI];
        $cid = $church['church_id'];
        if ($debug || ($CHI % 100) == 0)
           print "Stats church Empty=" . $badCnt. " " . $CHI . " of " . sizeof($churches) . " " . intval($CHI / sizeof($churches) * 100) . "%\n";
        if (scrape_one_stat($cid) == 0)
            $badCnt++;
        //print "Stats@" . $CHI . "/" . $cid . "\n";
        $CHI++;
        scraperwiki::save_var('IndxStat', $CHI);
    }
    print "Scrape Stats Done Churches=" . $CHI . " empty=" . $badCnt . "\n";
    scraperwiki::save_var('IndxStat', 0);
}

// *****************************************************
// remove cents, then thousands sep
function get_value($value)
{
    if( strlen($value) == 0)
        $value = "0";
    else
        $value = str_replace( ",", "",str_replace(".00", "", $value));
    return $value;
}

// *****************************************************
//Scape one church CSV file for statistics.
//http://apps.pcusa.org/tenyeartrends/report/22990/data_export.csv

function scrape_one_stat($cid)
{
    $yearcnt=0;
    $hdr=0;

//    $churchdat = scraperwiki::select("* from churches where church_id='" . $cid . "'");
    $data = scraperWiki::scrape('http://apps.pcusa.org/tenyeartrends/report/' . $cid . "/data_export.csv" );
    $stat = array();
    $stat[0]['church_id'] = $cid;

    $lines = explode("\n", $data);
    $rowcnt  = 0;
    //print_r($lines);

    //print "Scrape stat church=" . $cid . " lines=" . sizeof($lines) . "\n";
    foreach($lines as $row)
    {
        $row = str_getcsv($row);
        $rowcnt++;
        if ($rowcnt === 5)
            $hdr = $row;

        //print $rowcnt . ":" ;
        //$colcnt = 0;
        //foreach($row as $col)
            //{
            //print $col . ",";
            //++$colcnt;
            //}
        //print "\n";

        $colcnt = 0;
        foreach($row as $col)
            {
            if ($colcnt === 0)
               {
                $title = $col;
                ++$colcnt;
                continue;
               }
                if ($rowcnt <= 5)// no data until row 5
                break;

            $yr = $hdr[$colcnt];
            if ($yr === "")
                continue;
            $yearcnt++;

            if ($title === "Members")
                $stat[0]['mbr'.$yr] = get_value($col);

            if ($title === "Worship Attendance")
                $stat[0]['wor'.$yr] = get_value($col);

            if ($title === "Contributions ($)")
                $stat[0]['ctb'.$yr] = get_value($col);

            if ($title === "Baptized Members")
                $stat[0]['chd'.$yr] = get_value($col);

            if ($title === "Inactives")
                $stat[0]['ina'.$yr] = get_value($col);

            if ($title === "Death")
                $stat[0]['death'.$yr] = get_value($col);

            if ($title === "Infant Baptisms")
                $stat[0]['born'.$yr] = get_value($col);

            if ($title === "Per Capita Apportionment ($)")
                $stat[0]['per'.$yr] = get_value($col);

            ++$colcnt;
            }
     }
    if ($yearcnt)
        {
        scraperwiki::save_sqlite(array('church_id'), $stat, $table_name="stats", $verbose=0);
        //print "Cid:" . $cid . " Attendance:" . $stat[0]['wor2011'] . " Adherents:" . $stat[0]['mbr2011'] . " Contributions:" . $stat[0]['ctb2011'] . "\n";
        }
    else
        print "Church=" . $cid . " No Data in Source\n";
    //print_r($stat);
    return $yearcnt;
}

// *****************************************************
// Propagate summary of church stats up to presbytery
function sum_one_pby($pby_id)
{
    global $debug;
    $ch_cnt = 0;

    $mbr  = array();
    $wor  = array();
    $cont = array();

    //print "Sum Pby=" . $pby_id . "\n";

    $churches= scraperwiki::select("church_id from churches where pby_id=" . $pby_id);
    $pbydata = scraperwiki::select("* from presbyteries where pby_id=". $pby_id);

    foreach( $churches as $church )
        {
        $cid = $church['church_id'];
        //print "Sum Pby=" . $pby_id . " church=" . $cid . "\n";
        $stats = scraperwiki::select("* from stats where church_id=" . $cid);
        //print " #Stats=" . sizeof($stats) . "\n";
        if (sizeof($stats) == 0)
            {
            print "Sum Pby=" . $pby_id . " church=" . $cid . " No STATS \n";
            $ch_cnt++;
            continue;
            }
        $stat = $stats[0];
        if ($ch_cnt == 0)
            {        // first row set totals to zero.
            foreach($stat as $k => $col)
                {

                if (substr($k, 0, 3) == "mbr")
                    $mbr[$k] = 0;
                if (substr($k, 0, 3) == "wor")
                    $wor[$k] = 0;
                if (substr($k, 0, 3) == "ctb")
                    $cont[$k] = 0;
                }
            }
        foreach($stat as $k => $col)
            {
            if (substr($k, 0, 3) == "mbr")
                $mbr[$k] += $col;
            if (substr($k, 0, 3) == "wor")
                $wor[$k] += $col;
            if (substr($k, 0, 3) == "ctb")
                $cont[$k] += $col;
            }
        $ch_cnt++;
        }
    $cnt = 0;
    // add totals to the pby
    foreach($mbr as $k => $col)
        {
        $cnt++;
        $pbydata[0][$k] = $col;
        }
    foreach($wor as $k => $col)
        {
        $cnt++;
        $pbydata[0][$k] = $col;
        }
    foreach($cont as $k => $col)
        {
        $cnt++;
        $pbydata[0][$k] = $col;
        }

    $pbydata[0]['churches'] = $ch_cnt;
    $pbydata[0]['denom_id'] = 1;
    //print "Sum Pby@" . $pby_id . " #church=" . $ch_cnt. " #stats=" . $cnt . "\n";
    scraperwiki::save_sqlite(array('pby_id'), $pbydata, $table_name="presbyteries", $verbose=0);
}

// *****************************************************
// Propagate summary of church stats up to presbytery.
function sum_all_pby()
{
    global $debug;
    print "Sum All Presbyteries\n";
    $PBI= 0;
    $pbydata = scraperwiki::select("pby_id from presbyteries");
    foreach($pbydata as $pby)
    {
        $pby_id = $pby['pby_id'];
        sum_one_pby($pby_id);
        $per = $PBI / sizeof($pbydata) * 100;
        if (($per > 0) && ( ($per % 10) == 0) )
            print "Sum Pby@" . $pby_id . " " . $PBI . " " . intval($per) . "%\n";
        $PBI++;
    }
    print "Sum Pby " . $PBI . " of " . sizeof($pbydata) . "\n";
}

// *****************************************************
// Propagate summary of pby stats up to synods
function sum_all_synod()
{
    global $debug;
    print "Summing All Synods\n";

    $Gch_cnt = 0;
    $Gpby_cnt = 0;
    $Gsyn_cnt = 0;

    $Gmbr  = array();
    $Gwor  = array();
    $Gcont = array();

    $syndata = scraperwiki::select("syn_id from synods");
    foreach($syndata as $syn)
    {
        $syn_id = $syn['syn_id'];
        print "Sum Synod:" . $syn_id . "\n";

        $ch_cnt = 0;   // num of churches in synod

        $mbr  = array();
        $wor  = array();
        $cont = array();

        $syndata = scraperwiki::select("* from synods where syn_id=" . $syn_id);
        $pbydata = scraperwiki::select("* from presbyteries where syn_id=". $syn_id);

        if ($Gsyn_cnt == 0)
                {    // init totals to zero, and gather names (changes once a year)
                $pby = $pbydata[0];
                foreach($pby as $k => $col)
                    {
                    //print "PBY=" . $pby['pby_id'] . "\n";
                    if (substr($k, 0, 3) == "mbr")
                        $Gmbr[$k] = 0;
                    if (substr($k, 0, 3) == "wor")
                        $Gwor[$k] = 0;
                    if (substr($k, 0, 3) == "ctb")
                        $Gcont[$k] = 0;
                    }
                }
        $Gsyn_cnt++;

        $pby_cnt = 0;  // num of pbys in synod
        foreach($pbydata as $pby)
            {
            //print "Pby=" . $pby['pby_id']. "\n";
            if ($pby_cnt == 0)
                {    // init totals to zero, and gather names (changes once a year)
                foreach($pby as $k => $col)
                    {
                    if (substr($k, 0, 3) == "mbr")
                        $mbr[$k] = 0;
                    if (substr($k, 0, 3) == "wor")
                        $wor[$k] = 0;
                    if (substr($k, 0, 3) == "ctb")
                        $cont[$k] = 0;
                    }
                }
            else
                {    // total each pby into synod and denom totals
                foreach($pby as $k => $col)
                    {
                    if (substr($k, 0, 3) == "mbr")
                        $mbr[$k] += $col;
                    if (substr($k, 0, 3) == "wor")
                       $wor[$k] += $col;
                    if (substr($k, 0, 3) == "ctb")
                        $cont[$k] += $col;
                    }
                }
            $ch_cnt    += $pby['churches'];

            $pby_cnt++;
            }
        $Gch_cnt  += $ch_cnt;
        $Gpby_cnt += $pby_cnt;

        // copy totals to each synod DB, and totalize for denom
        foreach($mbr as $k => $col)
            {
            $syndata[0][$k] = $col;
            $Gmbr[$k] += $col;
            }
        foreach($wor as $k => $col)
            {
            $syndata[0][$k] = $col;
            $Gwor[$k] += $col;
            }
        foreach($cont as $k => $col)
            {
            $syndata[0][$k] = $col;
            $Gcont[$k] += $col;
            }

        $syndata[0]['churches']     = $ch_cnt;
        $syndata[0]['pbys']         = $pby_cnt;
        $syndata[0]['denom_id']     = 1;
        scraperwiki::save_sqlite(array('syn_id'), $syndata, $table_name="synods", $verbose=0);
    }
    $denom= array();
    print "Synods:" . $Gsyn_cnt . " pbys:" . $Gpby_cnt . " churches:" . $Gch_cnt . " members:" . $Gmbr['mbr2011']. " Worhsip:" . $Gwor['wor2011']. " Contributions:" . $Gcont['ctb2011'] . "\n";
    $denom[0]['name']         = 'pcusa';
    $denom[0]['denom_id']     = '1';
    $denom[0]['churches']     = $Gch_cnt;
    $denom[0]['presbyteries'] = $Gpby_cnt;
    $denom[0]['synods']       = $Gsyn_cnt;

    // copy totals to denom
    foreach($Gmbr as $k => $col)
        {
        $denom[0][$k] = $col;
        }
    foreach($Gwor as $k => $col)
        {
        $denom[0][$k] = $col;
        }
    foreach($Gcont as $k => $col)
        {
        $denom[0][$k] = $col;
        }
    //print_r($denom);
    scraperwiki::save_sqlite(array('denom_id'), $denom, $table_name="denom", $verbose=0);
}

// *****************************************************
// clean up names to std
function clean_one_church($oldname)
{
    $name = $oldname;
    $name = str_replace ("Presbyterian Church", "PC", $oldname);
    $name = str_replace ("United PC", "UPC", $name);
    // fix up abreviations and mis-spellings
    $name = str_replace ("3ast", "East", $name);
    $name = str_replace ("ChristChurch", "Christ Church", $name);
    $name = str_replace ("United Ch ", "United Church", $name);
    $name = str_replace ("Un ", "United ", $name);
    $name = str_replace ("Flsp", "Fellowship", $name);
    $name = str_replace ("Flshp", "Fellowship", $name);
    $name = str_replace ("St Lukes", "St Luke's", $name);
    $name = str_replace ("St Marks", "St Mark's", $name);
    $name = str_replace ("St Johns", "St John's", $name);
    $name = str_replace ("St Andrews", "St Andrew's", $name);
    $name = str_replace ("St Pauls", "St Paul's", $name);
    $name = str_replace ("St Stephens", "St Stephen's", $name);
    $name = str_replace ("St Marys", "St Mary's", $name);
    $name = str_replace ("Ch of", "Church of", $name);
    $name = str_replace (" Vlg", " Vilage", $name);
    $name = str_replace (" Vlge", " Vilage", $name);
    $name = str_replace (" Vlage", " Village", $name);
    $name = str_replace (" Vly", " Valley", $name);
    $name = str_replace ("Cong ", "Congregation ", $name);
    $name = str_replace ("Comm ", "Community ", $name);
    $name = str_replace ("Blmfld", "Bloomfield", $name);

    // change "PC of xxx PC" to "PC of xxxx"
    if (substr($name, 0, 5 ) == "PC " && substr($name, -2 ) == "PC" & strlen($name) > 6)
    {
        $name = substr($name, 0, -3);
       // print "Correct:" . $oldname . " to:" . $name . "\n";
    }

    // change "The PC xxxxx PC" to "The PC xxxxx"
    if (substr($name, 0, 5 ) == "The PC" && substr($name, -2 ) == "PC" & strlen($name) > 6)
    {
        $name = substr($name, 0, -3);
        //print "Correct:" . $oldname . " to:" . $name . "\n";
    }
    if (strpos($name, "PC of") !== false && substr($name, -2 ) == "PC")
    {
        $name = substr($name, 0, -3);
        //print "Correct:" . $oldname . " to:" . $name . "\n";
    }
    $name = trim($name);
    return $name;
}

// *****************************************************
function fix_stats()        // change null to zero stats
{
    $stats = scraperwiki::select("* from stats");
    $Cnt = 0;
    $Bad = 0;
    print "Fixing Stats " . sizeof($stats) . "\n";

    foreach($stats as $stat)
        {
        $dirty = 0;
        foreach($stat as $k => $v)
            {
            if (!isset($v))
                {
                $Bad++;
                $dirty = 1;
                //print "Bad k=" . $k . "\n";
                $stat[$k] = 0;
                }
            }
        if($dirty)
            scraperwiki::save_sqlite(array('church_id'), $stat, $table_name="stats", $verbose=0);
        $dirty = 0;
        if ( ($Cnt % 1000) == 0)
            print " Stats #" . $Cnt . " Bad=" . $Bad . "\n";
        $Cnt++;
        }
    print " Stats #" . $Cnt . " Bad=" . $Bad . "\n";
}

// *****************************************************
// *** MAIN ***
$init =  0;
$stop = 0;

// INIT variables
if ($stop)
{    // Must be run in this order.
    scraperwiki::save_var('GetPbyPins', 0);
    scraperwiki::save_var('GetSynods', 0);
    scraperwiki::save_var('GetChurchInfo', 0);
    scraperwiki::save_var('GetChurchDetail', 0);
    scraperwiki::save_var('GetChurchStats', 0);
    scraperwiki::save_var('SumPby', 0);
    scraperwiki::save_var('SumSyn', 0);
}
    // test stuff
//scraperwiki::save_var('IndxVer', 0);  // start over
//    scraperwiki::save_var('VerCh', 0);
//scraperwiki::save_var('IndxVer', 137);    // start over
//scraperwiki::save_var('VerCID', 1);// Test lines

//scraperwiki::save_var('GetPbyPins', 1);
//scraperwiki::save_var('GetSynods', 1);
//scraperwiki::save_var('IndxInfo', 0);    // start over
//scraperwiki::save_var('GetChurchInfo', 1);
//scraperwiki::save_var('IndxDetail', 0);
//scraperwiki::save_var('GetChurchDetail', 1);
scraperwiki::save_var('IndxStat', 0);  // start over
//scraperwiki::save_var('IndxStat',6000);
scraperwiki::save_var('GetChurchStats', 1);

    fix_stats();
//scraperwiki::save_var('SumPby', 1);
//scraperwiki::save_var('SumSyn', 1);

// INIT variables
if ($init)
{    // Must be run in this order.
    scraperwiki::save_var('GetPbyPins', 1);
    scraperwiki::save_var('GetSynods', 1);
    scraperwiki::save_var('GetChurchInfo', 1);
    scraperwiki::save_var('GetChurchDetail', 1);
    scraperwiki::save_var('GetChurchStats', 1);
    scraperwiki::save_var('SumPby', 1);
    scraperwiki::save_var('SumSyn', 1);

    // test stuff
    scraperwiki::save_var('VerCh', 0);
    scraperwiki::save_var('VerCID', 0);

    // these take a lot of time, we have to save our place for restart after time exceded.
    scraperwiki::save_var('IndxInfo', 0);    // scrape_all_pby, verify_call _cids
    scraperwiki::save_var('IndxDetail', 0);  // scrape_all_church_detail
    scraperwiki::save_var('IndxStat', 0);    // scrape_stats
    scraperwiki::save_var('IndxVer', 0);     // verify_churches
}

// Get List of Presbyteries from first page (It has magic code(pby_id) for pby pages)
if (scraperwiki::get_var('GetPbyPins', "0"))
{
    $dom  = getpbypage(150004, 1); // get any page
    $pbys = getpbypins($dom);
    scraperwiki::save_var('GetPbyPins', 0);
}

// Scrape Synod page for details of each presbytery
if (scraperwiki::get_var('GetSynods', "0"))
{
    scrape_synods();
    scraperwiki::save_var('GetSynods', 0);
}

//scrape Pby pages for church info.
if (scraperwiki::get_var('GetChurchInfo', "0"))
{
    scrape_All_pby();
    scraperwiki::save_var('GetChurchInfo', 0);
}

//scrape Church stat pages for church details.
if (scraperwiki::get_var('GetChurchDetail', "0"))
{
    scrape_all_church_detail();
    scraperwiki::save_var('GetChurchDetail', 0);
}

// scrape statistics page for each church
if (scraperwiki::get_var('GetChurchStats', "0"))
{
    scrape_stats();
    scraperwiki::save_var('GetChurchStats', 0);
}

// sum statistics from each church into each presbytery and synod
if (scraperwiki::get_var('SumPby', "0"))
{
    sum_all_pby();
    scraperwiki::save_var('SumPby', 0);
}

// sum statistics from each church into each presbytery and synod
if (scraperwiki::get_var('SumSyn', "0"))
{
    sum_all_synod();
    scraperwiki::save_var('SumSyn', 0);
}

// verify church page against pby page
if (scraperwiki::get_var('VerCID', "0"))
{
    verify_all_cids();

    scraperwiki::save_var('VerCID', 0);
}

// verify church page against pby page
if (scraperwiki::get_var('VerCh', "0"))
{
    verify_churches();
    scraperwiki::save_var('VerCh', 0);
}

// SINGLE TESTING CALLS

//$pby_id = "30012";
//scrape_pby_stats($pby_id);

//$pby_id = "180700";
//sum_one_pby($pby_id);

//scrape_pby_pages("30012", 1);    // scrape one pby all pages.

//$cid = 886;
//scrape_church_detail($cid);// scape one church detail

//$cid = 6935;
//scrape_one_stat($cid);// scrape single church statistics

//$cid = 6197;
//verify_church_detail($cid);

//$churchcnt = 0;
//$pby_id = 40628;
//verify_pby_pages($pby_id);

// delete bad data
//scraperwiki::sqliteexecute("delete from synods where syn_id=0");
//scraperwiki::sqliteexecute("drop table if exists churches");

?>
