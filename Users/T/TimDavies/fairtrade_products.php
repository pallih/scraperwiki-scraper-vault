<?php
require 'scraperwiki/simple_html_dom.php';        

$mapping = array("Beauty"=>"Health and Beauty",
"Beer & Ale"=>"Food and Drink",
"Biscuits"=>"Food and Drink",
"Cakes & Brownies"=>"Food and Drink",
"Cereals & Bars"=>"Food and Drink",
"Chocolate"=>"Food and Drink",
"Cocoa"=>"Food and Drink",
"Coffee"=>"Food and Drink",
"Cotton"=>"Clothing and Textiles",
"Dried Fruit"=>"Food and Drink",
"Flowers"=>"Flowers",
"Fresh Fruits"=>"Food and Drink",
"Fresh Veg"=>"Food and Drink",
"Herbs & Spices"=>"Food and Drink",
"Honey"=>"Food and Drink",
"Hot Chocolate"=>"Food and Drink",
"Ice Cream"=>"Food and Drink",
"Jams & Spreads"=>"Food and Drink",
"Juice & Soft Drinks"=>"Food and Drink",
"Molasses"=>"Food and Drink",
"Nuts/nut Oil"=>"Food and Drink",
"Olives & Olive Oil"=>"Food and Drink",
"Pulses"=>"Food and Drink",
"Quinoa"=>"Food and Drink",
"Rice"=>"Food and Drink",
"Spirits"=>"Food and Drink",
"Sports Balls"=>"Clothing and Textiles",
"Sugar"=>"Food and Drink",
"Sweets"=>"Food and Drink",
"Syrup"=>"Food and Drink",
"Tea"=>"Food and Drink",
"Tea & Herbal Tea"=>"Food and Drink",
"Wine"=>"Food and Drink",
"Yoghurt"=>"Food and Drink");

function make_key($string) {
    return strtolower(str_replace(array(" & "," ","/","'","&"),"_",$string));
}

function save_generic($category,$title) {
    scraperwiki::save_sqlite(array("key"),array("key"=>make_key($title."-generic"), "name"=>$title,"manufacturer"=>"N/A","url"=>"","description"=>"","category"=>make_key($category)."/".make_key($title)));
    
}

$html = scraperWiki::scrape("http://www.fairtrade.org.uk/products/retail_products/default.aspx");
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find("li.level2_off a") as $link) {
    $product_type = trim($link->plaintext);
    $category_string = make_key($mapping[$product_type])."/".make_key($product_type);
    save_generic($category_string,$product_type);

        $products_html = scraperWiki::scrape("http://www.fairtrade.org.uk".$link->href);
        $proddom = new simple_html_dom();
        $proddom->load($products_html);

        foreach($proddom->find("div.info_text2") as $infotext) {
            $producer = trim(strip_tags($infotext->find("strong",0)));
            foreach($infotext->find("li.productlist") as $product) {
                $product_name = strip_tags(substr($product,0,strpos($product,"<br />")));
                $product_url = $product->find("a",0)->href;
                scraperwiki::save_sqlite(array("key"),array("key"=>make_key($product_name), "name"=>$product_name,"manufacturer"=>$producer,"url"=>$product_url,"description"=>"","category"=>$category_string));

            }
        }
}

save_generic("Health and Beauty","Cosmetics");
save_generic("Crafts and Gifts","Childrens Toys");
save_generic("Crafts and Gifts","Woodwork");
save_generic("Crafts and Gifts","Glassware");
save_generic("Crafts and Gifts","Candles");
save_generic("Crafts and Gifts","Jewelery");
save_generic("Crafts and Gifts","Basketware");
save_generic("Household","Homewares");
save_generic("Household","Cleaning Products");

?>
