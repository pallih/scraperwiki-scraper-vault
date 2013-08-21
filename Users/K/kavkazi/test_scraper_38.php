<?php

require 'scraperwiki/simple_html_dom.php';

print "Welcome to Deal Genius Scraper!";

$html = scraperWiki::scrape("http://www.dealgenius.ca/business-productivity-software/sc/195");

$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find("div[@id='items_container'] div[starts-with(@class='item_grid_')] div") as $data){
    $product = $data->find("div[@class='prod_name'] a");
    $price = $data->find("div[@class='base_price font-14 bold'] a");
    $discount = $data->find("div[@class='grid_discount dark_red uppercase']");
    
    if(count($product)==1){
            $record = array(
                "itemId" => $product,
                "price" => $price,
                "discount" => $discount
            );
            print ($record). "\n";
    }
}

?>
