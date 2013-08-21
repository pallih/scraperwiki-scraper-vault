<?php

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$html = scraperWiki::scrape("http://www.letsplaysoccer.com/main/locations/northwest/std/nw1schedule.htm");
$dom->load($html);


foreach($dom->find("table tr") as $data){
    $tds = $data->find("td");
    $temptd = array();
    foreach($tds as $td) {
        $temptd[] = $td->plaintext;
    }
    $trs[]= $temptd;
}


$c = 1;
for ($i=2; $i<count($trs); $i+=2) {
    $daynum = 0;
    for ($k=0; $k<count($trs[$i]); $k+=3) {

        if ($trs[$i][$k] != "" && $trs[$i][$k] != "&nbsp;") {

            $game = array(
                'id' => $c,
                'date' => $trs[0][$daynum],
                'time' => $trs[$i][$k],
                'division' => $trs[$i+1][$k],
                'team1' => htmlentities($trs[$i][$k+1]),
                'team2' => htmlentities($trs[$i+1][$k+1]),
                'timestamp' => strtotime($trs[0][$daynum] . " " . $trs[$i][$k])
            );
            #print $c . "\n";
            print_r($game);
            scraperwiki::save(array('timestamp'), $game);
            $c++;
        }
        $daynum+=2;
    }
}




$html = scraperWiki::scrape("http://www.letsplaysoccer.com/main/locations/northwest/std/nw1Nschedule.htm");
$dom->load($html);

$trs = array();
foreach($dom->find("table tr") as $data){
    $tds = $data->find("td");
    $temptd = array();
    foreach($tds as $td) {
        $temptd[] = $td->plaintext;
    }
    $trs[]= $temptd;
}


$c = 1;
for ($i=2; $i<count($trs); $i+=2) {
    $daynum = 0;
    for ($k=0; $k<count($trs[$i]); $k+=3) {

        if ($trs[$i][$k] != "" && $trs[$i][$k] != "&nbsp;") {

            $game = array(
                'id' => $c,
                'date' => $trs[0][$daynum],
                'time' => $trs[$i][$k],
                'division' => $trs[$i+1][$k],
                'team1' => htmlentities($trs[$i][$k+1]),
                'team2' => htmlentities($trs[$i+1][$k+1]),
                'timestamp' => strtotime($trs[0][$daynum] . " " . $trs[$i][$k])
            );
            #print $c . "\n";
            print_r($game);
            scraperwiki::save(array('timestamp'), $game);
            $c++;
        }
        $daynum+=2;
    }
}



?>
