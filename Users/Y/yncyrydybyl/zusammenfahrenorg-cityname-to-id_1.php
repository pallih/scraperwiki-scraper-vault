<?php
$url = "http://www.zusammenfahren.org/suchen.php";
$html = scraperWiki::scrape($url);
$html = utf8_encode($html);

require 'scraperwiki/simple_html_dom.php'; 
$dom = new simple_html_dom(); $dom->load($html); 

foreach($dom->find("select[@name=los] option") as $data){ 
    $city = $data->plaintext;
    
    $record = array( 'city' => $city, 'id' => $data->value);
    scraperwiki::save(array('city'), $record);
} 

?>
