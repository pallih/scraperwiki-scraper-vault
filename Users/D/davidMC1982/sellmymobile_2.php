<?php
require 'scraperwiki/simple_html_dom.php';

//Get the page with links to all manufacturers
$html = scraperWiki::scrape("http://www.sellmymobile.com/search/");

//Get a simple_html_dom instance
$dom = new simple_html_dom();

//Load the page into the dom
$dom->load($html);

//get the link and text of the manufacturer
foreach($dom->find("li.loading p") as $data) {
    $a = $data->find("a");
    $manu = $a[0]->plaintext;
    $link = $a[0]->href;
    //Get to the manufacturer product listings page    
    $html2 = scraperWiki::scrape($link);

    //Create a simple_html_dom instance
    $dom2 = new simple_html_dom();

    //Load the page into the dom
    $dom2->load($html2);
    
    //Get the model and price of the product
    foreach ($dom2->find("li.loading a.long") as $data){

        //Get the model name
        $model = $data->plaintext;

        //Get the link
        $product_link = $data->href;

        //Remove the manufacturer name
        $model = substr($model, strlen($manu) + 1);

        //Get the position of the price
        $price_pos = strrpos($model, '£');

        //Extract the price from the model name
        $price = substr($model, $price_pos);

        //Remove the comparing text
        $comp_pos = strrpos($model, "comparing ");
        $length = strlen($model);
        $model = substr($model, 0, $comp_pos-$length);
        //$mpx_working = "";
        //$fb_working = "";
 
        //If we have a price, save the product to the db
        if ($price) {
            scraperwiki::save_sqlite(array("model"), array("manufacturer"=>$manu, 
                                                           "model"=>$model, 
                                                           "price"=>$price, 
                                                           "link"=>$product_link),'swdata',0); 
        }
    }
        if ($manu === "Samsung") {
            break;
        }  
   
}

//Now load the links for the manufacturers we'd like extra rate info for
$rows = scraperwiki::select("* from swdata where manufacturer LIKE 'Apple' OR manufacturer LIKE 'HTC' OR manufacturer LIKE 'Samsung' OR manufacturer LIKE 'Blackberry' ");

foreach ($rows as $row) {

    $mpx_working = $row['mpx_working'];
    $fb_working = $row['fb_working'];

    if (empty($mpx_working)) { $mpx_working = ""; }
    if (empty($fb_working)) { $fb_working = ""; }

    //Scrape the product page
    $html3 = scraperWiki::scrape($row['link']);

    //Load it into a dom object
    $dom3 = new simple_html_dom();
    $dom3->load($html3);

    //Get all merchant logo table cells. The title attribute tells us which manufacturer we're looking at
    $merchant_logos = $dom3->find("td.merchantlogo a");
    foreach ($merchant_logos as $merchant_logo) {
            
        $title = $merchant_logo->title;
            if (stripos($title, "Mobile Phone Xchange") !== false) {
                $mpx_working = $merchant_logo->parent()->next_sibling()->plaintext;
            }

            if (stripos($title, "FoneBank") !== false) {
                $fb_working = $merchant_logo->parent()->next_sibling()->plaintext;
            }
    }
    scraperwiki::save_sqlite(array("model"), array("model"=>$row['model'],
                                                   "manufacturer"=>$row['manufacturer'],
                                                   "link"=>$row['link'],
                                                   "price"=>$row['price'],
                                                   "mpx_working"=>$mpx_working,
                                                   "fb_working"=>$fb_working),"swdata",0); 
}


?>
<?php
require 'scraperwiki/simple_html_dom.php';

//Get the page with links to all manufacturers
$html = scraperWiki::scrape("http://www.sellmymobile.com/search/");

//Get a simple_html_dom instance
$dom = new simple_html_dom();

//Load the page into the dom
$dom->load($html);

//get the link and text of the manufacturer
foreach($dom->find("li.loading p") as $data) {
    $a = $data->find("a");
    $manu = $a[0]->plaintext;
    $link = $a[0]->href;
    //Get to the manufacturer product listings page    
    $html2 = scraperWiki::scrape($link);

    //Create a simple_html_dom instance
    $dom2 = new simple_html_dom();

    //Load the page into the dom
    $dom2->load($html2);
    
    //Get the model and price of the product
    foreach ($dom2->find("li.loading a.long") as $data){

        //Get the model name
        $model = $data->plaintext;

        //Get the link
        $product_link = $data->href;

        //Remove the manufacturer name
        $model = substr($model, strlen($manu) + 1);

        //Get the position of the price
        $price_pos = strrpos($model, '£');

        //Extract the price from the model name
        $price = substr($model, $price_pos);

        //Remove the comparing text
        $comp_pos = strrpos($model, "comparing ");
        $length = strlen($model);
        $model = substr($model, 0, $comp_pos-$length);
        //$mpx_working = "";
        //$fb_working = "";
 
        //If we have a price, save the product to the db
        if ($price) {
            scraperwiki::save_sqlite(array("model"), array("manufacturer"=>$manu, 
                                                           "model"=>$model, 
                                                           "price"=>$price, 
                                                           "link"=>$product_link),'swdata',0); 
        }
    }
        if ($manu === "Samsung") {
            break;
        }  
   
}

//Now load the links for the manufacturers we'd like extra rate info for
$rows = scraperwiki::select("* from swdata where manufacturer LIKE 'Apple' OR manufacturer LIKE 'HTC' OR manufacturer LIKE 'Samsung' OR manufacturer LIKE 'Blackberry' ");

foreach ($rows as $row) {

    $mpx_working = $row['mpx_working'];
    $fb_working = $row['fb_working'];

    if (empty($mpx_working)) { $mpx_working = ""; }
    if (empty($fb_working)) { $fb_working = ""; }

    //Scrape the product page
    $html3 = scraperWiki::scrape($row['link']);

    //Load it into a dom object
    $dom3 = new simple_html_dom();
    $dom3->load($html3);

    //Get all merchant logo table cells. The title attribute tells us which manufacturer we're looking at
    $merchant_logos = $dom3->find("td.merchantlogo a");
    foreach ($merchant_logos as $merchant_logo) {
            
        $title = $merchant_logo->title;
            if (stripos($title, "Mobile Phone Xchange") !== false) {
                $mpx_working = $merchant_logo->parent()->next_sibling()->plaintext;
            }

            if (stripos($title, "FoneBank") !== false) {
                $fb_working = $merchant_logo->parent()->next_sibling()->plaintext;
            }
    }
    scraperwiki::save_sqlite(array("model"), array("model"=>$row['model'],
                                                   "manufacturer"=>$row['manufacturer'],
                                                   "link"=>$row['link'],
                                                   "price"=>$row['price'],
                                                   "mpx_working"=>$mpx_working,
                                                   "fb_working"=>$fb_working),"swdata",0); 
}


?>
