<?php
require 'scraperwiki/simple_html_dom.php';

$html = scraperWiki::scrape("http://www.sellmymobile.com/search/");

$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("li.loading p") as $data){
    $a = $data->find("a");
    $manu = $a[0]->plaintext;
    $link = $a[0]->href;
    print $link  . "\n";
    
    $html2 = scraperWiki::scrape($link);
    $dom2 = new simple_html_dom();
    $dom2->load($html2);
    
    foreach ($dom2->find("li.loading a") as $data){

       $model = $data->plaintext;
       $price_pos = strrpos($model, '£');
       $price = substr($model, $price_pos);
       $comp_pos = strrpos($model, "comparing ");
       $length = strlen($model);
       $model = substr($model, 0, $comp_pos-$length);

       if($price){
            scraperwiki::save_sqlite(array("Model"), array("Model"=>$model, "Price"=>$price)); 
       }
    }
}




?>
