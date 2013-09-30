<?php
require 'scraperwiki/simple_html_dom.php';

$html = scraperWiki::scrape("http://marketplace.civiccommons.org");

$dom = new simple_html_dom();
$dom->load($html);

    foreach($dom->find("div.view-interactions span.field-content") as $data){
    $tds = $data->find("span");
    $dates = $data->find("em");
    $urls = $data->find("a");
    $record = array(
        'url' => 'http://marketplace.civiccommons.org'.$urls[0]->href,
        'maker' => $tds[0]->plaintext, 
        'action' => $tds[1]->plaintext,
        'app' => $tds[2]->plaintext,
        'day' => date_create(trim($dates[0]->plaintext, 'added')),
        'title' => $tds[0]->plaintext.' '.$tds[1]->plaintext.' '.$tds[2]->plaintext,

    );
    print_r($record);
    scraperwiki::save(array('url'), $record); 

}


?><?php
require 'scraperwiki/simple_html_dom.php';

$html = scraperWiki::scrape("http://marketplace.civiccommons.org");

$dom = new simple_html_dom();
$dom->load($html);

    foreach($dom->find("div.view-interactions span.field-content") as $data){
    $tds = $data->find("span");
    $dates = $data->find("em");
    $urls = $data->find("a");
    $record = array(
        'url' => 'http://marketplace.civiccommons.org'.$urls[0]->href,
        'maker' => $tds[0]->plaintext, 
        'action' => $tds[1]->plaintext,
        'app' => $tds[2]->plaintext,
        'day' => date_create(trim($dates[0]->plaintext, 'added')),
        'title' => $tds[0]->plaintext.' '.$tds[1]->plaintext.' '.$tds[2]->plaintext,

    );
    print_r($record);
    scraperwiki::save(array('url'), $record); 

}


?>