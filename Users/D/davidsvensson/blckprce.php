<?php
require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();

$html = scraperWiki::scrape("http://www.blocket.se/goteborg?q=&cg=2040&w=1&st=s&c=2043&ca=15&is=1&l=0&md=th");

$dom->load($html);
foreach($dom->find("div.item_row") as $data){

    $price = $data->find(".list_price");
    $date = $data->find(".list_date");
    $record = array( 'id' => $data->id, 'added' => '"' . $date[0]->innertext . '"', 'price' => $price[0]->innertext);
    scraperwiki::save(array('blck'), $record);
}
?>