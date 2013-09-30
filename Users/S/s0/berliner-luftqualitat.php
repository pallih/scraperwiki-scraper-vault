<?php
###########################
# Berliner Luftqualität v1
# by Fraunhofer Fokus (bbr)
###########################

require  'scraperwiki/simple_html_dom.php';
date_default_timezone_set('CET');


#### GET DATA FROM 1 FILE

function getData( $file )
{
    print("LOADING: http://www.berlin.de/sen/umwelt/luftqualitaet/de/messnetz/tageswerte/download/".$file."\n");
    if (20070126 > intval(substr($file,0,8) ) ) {
        print "*** requested file too old. not possible ***";
        return false;
    }
    $html = scraperwiki::scrape( "http://www.berlin.de/sen/umwelt/luftqualitaet/de/messnetz/tageswerte/download/".$file );
    #print $html;
    $dom = new simple_html_dom();
    $dom->load($html);
    $rowcount = 0;
    $streetnearby = "false";
    $date = substr($file,0,4)."-".substr($file,4,2)."-".substr($file,6,2);
    foreach($dom->find('table.datenhellgrauklein tbody tr') as $tr) #'table tbody tr td table tbody tr td table tbody tr'
    {
        $rowcount += 1;
        if ($rowcount > 2)
        { # frist 2 rows are headers
            if ($tr->first_child()->getAttribute('class') !== 'grau' && !isset($tr->first_child()->colspan) 
                && $tr->first_child()->plaintext !== "Grenz- u. Richtwerte:") 
            { # ignores headlines like 'Messstationen an Straßen'
                #print "row: ".$rowcount."\n";
                $data = array();
                $colcount = 0;
                foreach($tr->find('td') as $td) #find('td p b')
                {
                    $colcount += 1;
                    $value = $td->plaintext;
                    # fixs invalid html bug for files from 2006-2007:
                    if (substr($value,strlen($value)-4,4) == "</B>") $value = substr($value,0,strlen($value)-4);
                    #print "col: ".$colcount." - value: ".$value."\n";
                    if ($colcount == 1) 
                    { #location
                        array_push($data, $value);
                    }
                    else 
                    { # save values
                        if ($td->plaintext != "---") array_push($data, $value);
                        else array_push($data, ""); # war vorher null
                    }
                }
                if ($colcount == 15) {
                    $thisdata = array('location' => $data[0], 'streetnearby'=>$streetnearby,
                        'pm10-avg' => $data[1], 'pm10-y-exc' => $data[2], 
                        'grime-avg' => $data[3], 'grime-max' => $data[4], 
                        'no2-avg' => $data[5], 'no2-max' => $data[6],
                        'benzol-avg' => $data[7], 'benzol-max' => $data[8],
                        'co-avg' => $data[9], 'co-max' => $data[10],
                        'o3-max1h' => $data[11], 'o3-max8h' => $data[12],
                        'so2-avg' => $data[13], 'so2-max' => $data[14]
                    );
                    #print_r($thisdata);
                    scraperwiki::save(array('location'), $thisdata, $date);
                }
                else {
                    print "*** error on row ".$rowcount.". only get:\n";
                    print_r($data);
                    break;
                }
            }
            else if (isset($tr->first_child()->colspan)) $streetnearby = "true";
        }
        #else print "*** ignoring row: ".$rowcount." ***\n";
    }
}
#testing: getData('20070126.html');


#### GET YESTERDAYS DATA (daily at 12 am)

function dateafter ( $a )
{
    $hours = $a * 24;
    $added = ($hours * 3600)+time();
    $month = date("m", $added);
    $day = date("d", $added);
    $year = date("Y", $added);
    $result = "$year$month$day";
    return ($result);
}
getData(dateafter(-1).".html");



#### GET ALL DATA SINCE 26.01.2007 (only run once)

#$html = scraperwiki::scrape("http://www.berlin.de/sen/umwelt/luftqualitaet/de/messnetz/tageswerte/download/");
## get list of files
#$dom = new simple_html_dom();
#$dom->load($html);
#$list = array();
#foreach($dom->find('a') as $data)
#{
#    if ( strpos($data->href,"?") === false && 20070126 <= intval(substr($data->href,0,8)) )
#    {
#        array_push($list, $data->href);
#    }
#}
#print "count: ".count($dom->find('a'))."\n";
#
##saves the data from them
#$list = array_reverse($list);
#$filecounter = 0;
#foreach($list  as $file) {
#    getData($file);
#    if ($filecounter >= 100) break;
#    $filecounter++;
#}
#print "Done. Saved the last ".$filecounter." logs."

?>
<?php
###########################
# Berliner Luftqualität v1
# by Fraunhofer Fokus (bbr)
###########################

require  'scraperwiki/simple_html_dom.php';
date_default_timezone_set('CET');


#### GET DATA FROM 1 FILE

function getData( $file )
{
    print("LOADING: http://www.berlin.de/sen/umwelt/luftqualitaet/de/messnetz/tageswerte/download/".$file."\n");
    if (20070126 > intval(substr($file,0,8) ) ) {
        print "*** requested file too old. not possible ***";
        return false;
    }
    $html = scraperwiki::scrape( "http://www.berlin.de/sen/umwelt/luftqualitaet/de/messnetz/tageswerte/download/".$file );
    #print $html;
    $dom = new simple_html_dom();
    $dom->load($html);
    $rowcount = 0;
    $streetnearby = "false";
    $date = substr($file,0,4)."-".substr($file,4,2)."-".substr($file,6,2);
    foreach($dom->find('table.datenhellgrauklein tbody tr') as $tr) #'table tbody tr td table tbody tr td table tbody tr'
    {
        $rowcount += 1;
        if ($rowcount > 2)
        { # frist 2 rows are headers
            if ($tr->first_child()->getAttribute('class') !== 'grau' && !isset($tr->first_child()->colspan) 
                && $tr->first_child()->plaintext !== "Grenz- u. Richtwerte:") 
            { # ignores headlines like 'Messstationen an Straßen'
                #print "row: ".$rowcount."\n";
                $data = array();
                $colcount = 0;
                foreach($tr->find('td') as $td) #find('td p b')
                {
                    $colcount += 1;
                    $value = $td->plaintext;
                    # fixs invalid html bug for files from 2006-2007:
                    if (substr($value,strlen($value)-4,4) == "</B>") $value = substr($value,0,strlen($value)-4);
                    #print "col: ".$colcount." - value: ".$value."\n";
                    if ($colcount == 1) 
                    { #location
                        array_push($data, $value);
                    }
                    else 
                    { # save values
                        if ($td->plaintext != "---") array_push($data, $value);
                        else array_push($data, ""); # war vorher null
                    }
                }
                if ($colcount == 15) {
                    $thisdata = array('location' => $data[0], 'streetnearby'=>$streetnearby,
                        'pm10-avg' => $data[1], 'pm10-y-exc' => $data[2], 
                        'grime-avg' => $data[3], 'grime-max' => $data[4], 
                        'no2-avg' => $data[5], 'no2-max' => $data[6],
                        'benzol-avg' => $data[7], 'benzol-max' => $data[8],
                        'co-avg' => $data[9], 'co-max' => $data[10],
                        'o3-max1h' => $data[11], 'o3-max8h' => $data[12],
                        'so2-avg' => $data[13], 'so2-max' => $data[14]
                    );
                    #print_r($thisdata);
                    scraperwiki::save(array('location'), $thisdata, $date);
                }
                else {
                    print "*** error on row ".$rowcount.". only get:\n";
                    print_r($data);
                    break;
                }
            }
            else if (isset($tr->first_child()->colspan)) $streetnearby = "true";
        }
        #else print "*** ignoring row: ".$rowcount." ***\n";
    }
}
#testing: getData('20070126.html');


#### GET YESTERDAYS DATA (daily at 12 am)

function dateafter ( $a )
{
    $hours = $a * 24;
    $added = ($hours * 3600)+time();
    $month = date("m", $added);
    $day = date("d", $added);
    $year = date("Y", $added);
    $result = "$year$month$day";
    return ($result);
}
getData(dateafter(-1).".html");



#### GET ALL DATA SINCE 26.01.2007 (only run once)

#$html = scraperwiki::scrape("http://www.berlin.de/sen/umwelt/luftqualitaet/de/messnetz/tageswerte/download/");
## get list of files
#$dom = new simple_html_dom();
#$dom->load($html);
#$list = array();
#foreach($dom->find('a') as $data)
#{
#    if ( strpos($data->href,"?") === false && 20070126 <= intval(substr($data->href,0,8)) )
#    {
#        array_push($list, $data->href);
#    }
#}
#print "count: ".count($dom->find('a'))."\n";
#
##saves the data from them
#$list = array_reverse($list);
#$filecounter = 0;
#foreach($list  as $file) {
#    getData($file);
#    if ($filecounter >= 100) break;
#    $filecounter++;
#}
#print "Done. Saved the last ".$filecounter." logs."

?>
