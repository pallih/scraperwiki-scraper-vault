<?php

# Blank PHP
print "Hello, coding in the cloud!";

$html = scraperWiki::scrape("http://travel.org/agents.html");
print $html . "\n";

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[@align='left']") as $data){
    $tds = $data->find("</a>");
    $record = array(
        'url' => $tds[0]->plaintext, 
        'years_in_school' => intval($tds[4]->plaintext)
    );
    print_r($record);
}    

scraperwiki::save(array('country'), $record);







?>
