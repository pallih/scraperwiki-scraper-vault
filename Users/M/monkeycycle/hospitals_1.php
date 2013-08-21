<?php

print "Hello, coding in the cloud!";

$html = scraperWiki::scrape("http://www.hospitalsworldwide.com/listings/2191.php");

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("h2") as $data){

    $facilityName = $data->plaintext;


    print_r($facilityName);
}

scraperwiki::save(array('country'), $record);


?>
