<?php

require 'scraperwiki/simple_html_dom.php';

$html = scraperWiki::scrape("http://www.geonames.org/search.html?q=university&country=AT");           

$dom = new simple_html_dom();
$dom->load($html);

$index = 0;
foreach($dom->find("table.restable tr") as $data){
    $index ++;
    if($index < 3) continue;
    $tds = $data->find("td");
    //foreach($tds as $td){
        //print cleanText($td->plaintext)."\n";
    //}
    if(!isset($tds[1])){
        continue;
    }
    $a = $tds[1]->find("a");
    $name = $a[0]->plaintext;

    $spanlo = $tds[1]->find("span.longitude");
    $longi = $spanlo[0]->plaintext;

    $spanla = $tds[1]->find("span.latitude");
    $lati = $spanla[0]->plaintext;
    
    $record = array();
    $record['name'] = $name;
    $record['longitude'] = $longi;
    $record['latitude'] = $lati;
    
    scraperwiki::save(array('name'), $record);
}

function cleanText($text){
    return str_replace('&nbsp;', '', $text);
}
?>