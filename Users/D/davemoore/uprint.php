<?php
require 'scraperwiki/simple_html_dom.php';
$baseUrl = 'http://unitedprint.com';
$dom = new simple_html_dom();

// Step 1 - Get Product Urls
$html = scraperWiki::scrape($baseUrl);
$dom->load($html);

$productTypes = array();
foreach($dom->find("a.productbox") as $link){
    $productLinks[] = array( 'href' => $link->href, 'link' => $link->plaintext);
}


// Step 2 - Get Individual Product Info
foreach($productLinks as $productLink){
    $productHtml = scraperWiki::scrape($baseUrl.$productLink['href']);
    $dom->load($productHtml);
    foreach($dom->find("div.prop") as $select){
        $record = array('name' => $select->name);
        scraperwiki::save(array('name'), $record);
    }
    break;
}

?>