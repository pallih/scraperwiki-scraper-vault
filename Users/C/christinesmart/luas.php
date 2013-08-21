<?php
$html = scraperWiki::scrape("http://www.luas.ie/luaspid.html?get=Fortunestown");
print $html . "\n";
require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div class='Inbound' ") as $inbound){
    $tds = $inbound->find("div class='location' ");
    $record = array(
        'location' => $tds[0]->plaintext);
    print_r($record);

 $tdss = $inbound->find("div class='time' ");
    $records = array(
        'time' => $tds[1]->plaintext);
    print_r($records);
    
}

?>