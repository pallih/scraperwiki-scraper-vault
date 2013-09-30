<?php
require 'scraperwiki/simple_html_dom.php';

$html = scraperWiki::scrape("http://www.mazumamobile.com/sell_mobile_phones.php");

$dom = new simple_html_dom();
$dom->load($html);

#print($html);
scraperwiki::sqliteexecute("DROP TABLE `swdata`");
scraperwiki::sqliteexecute("CREATE TABLE `swdata` (`Model` text, `Price` text)");
print("Created swdata");



foreach($dom->find("div[id=tiledManufacturers] a") as $data){
    $a = $data->plaintext;
    $link = $data->href;
    
    $html2 = scraperWiki::scrape("http://www.mazumamobile.com/" . $link);
    $dom2 = new simple_html_dom();
    $dom2->load($html2);
    
    foreach ($dom2->find("div.model") as $data){
       print($data.PHP_EOL);

       $href = $data->find("a");
       $model_link = $href[0]->href;
       $model_link = str_replace("&amp;","&",$model_link);
       print("http://www.mazumamobile.com/" . $model_link.PHP_EOL);
       $html3 = scraperWiki::scrape("http://www.mazumamobile.com/" . $model_link);
       $dom3 = new simple_html_dom();
       $dom3->load($html3);

       $price_span = $dom3->find("span[id=chequeValue]");
       $price = $price_span[0]->plaintext;
       $price = str_replace("&pound;", "", $price);
        print($price.PHP_EOL);
       $manu_div = $dom3->find("h1[id=yourHandsetWidget] div h4");

       print("ManuDiv=".$manu_div->plaintext.PHP_EOL);
       print("ManuDiv[0]->plaintext=".$manu_div[0]->plaintext);


       $model_div = $dom3->find("div[id=handsetDetailGroup] h4");
       print("ModelDiv=".$model_div[0]->plaintext.PHP_EOL);
       $model = str_replace(" -", "", $manu_div[0]->plaintext) . $model_div[0]->plaintext;
       print("Model=".$model.PHP_EOL);
       
       if($price){
            scraperwiki::save_sqlite(array("Model"), array("Model"=>$model, "Price"=>$price));
       }

    }
}


    
?>
