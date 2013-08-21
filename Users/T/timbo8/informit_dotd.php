<?php

$html = scraperWiki::scrape("http://informit.com");
print $html . "\n";

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[@class='ebookDetails']") as $data){
    $time = time();
    $as = $data->find("a");
    $record = array(
        'time' => $time,
        'book' => $as[1]->plaintext, 
    );
    scraperwiki::save(array('book'), $record);
}

?>
