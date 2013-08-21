<?php

$html = scraperWiki::scrape("http://www.kulturbolaget.se/?section=calendarium");           
print $html . "\n";
require 'https://scraperwiki.com/scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find('<div id="noinfo') as $data){
    $tds = $data->find("td");
    $record = array(
        'band' => $tds[0]->plaintext, 
        'date' => $tds[1]->plaintext)
    ;
    scraperwiki::save(array('band', 'date'), $record);
}


?>
