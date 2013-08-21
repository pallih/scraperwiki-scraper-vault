<?php

$html_content = scraperWiki::scrape("http://www.currys.co.uk/gbuk/search-keywords/xx_xx_xx_xx_xx/Humax/xx-criteria.html");
require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();

$html = str_get_html($html_content);
foreach ($html->find("div.productPrices") as $html_it) {
    foreach ($html_it->find('input') as $html_id) {
        $prod_id = trim($html_id->value);
    }
    foreach ($html_it->find("span.currentPrice") as $html_pr) {
        foreach ($html_pr->children() as $child1) {
            $prod_price = trim($child1->plaintext);
        }
    }
    $record = array('id' => $prod_id, 'price' => $prod_price);
    //print json_encode($record) . "\n";
    scraperwiki::save(array('id'), $record);   
}

//foreach($dom->find('article class="product') as $data){
//    $articles = $data->find("currentPrice");
    //if(count($articles)==12){
        //$record = array(
        //    'country' => $articles[0]->plaintext, 
        //    'years_in_school' => intval($tds[4]->plaintext)
        //);
//        print "Hello" . json_encode($articles) . "\n";
    
//}

?>
