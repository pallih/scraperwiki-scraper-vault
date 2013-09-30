<?php
echo "Get prices for protein powder on BodyBuilding.com";
$html = scraperWiki::scrape("http://www.bodybuilding.com/store/protein-powder.html");

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[@class='store-layout-product-item']") as $data){
    $prodName = $data->find("h3");
    $price = $data->find("div[@class='store-layout-price']");
    $record = array(
        'productName' => $prodName[0]->plaintext,
        'price' => $price[0]->plaintext, 
         );
    print_r($record);
}
  
   

?>
<?php
echo "Get prices for protein powder on BodyBuilding.com";
$html = scraperWiki::scrape("http://www.bodybuilding.com/store/protein-powder.html");

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[@class='store-layout-product-item']") as $data){
    $prodName = $data->find("h3");
    $price = $data->find("div[@class='store-layout-price']");
    $record = array(
        'productName' => $prodName[0]->plaintext,
        'price' => $price[0]->plaintext, 
         );
    print_r($record);
}
  
   

?>
