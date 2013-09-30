<?php 

// Include the library.
require 'scraperwiki/simple_html_dom.php';

// We'll need this unchanging element throughout.
define("SCHEME_TO_HOST", "://");

// The base URLs.
$base_urls = array(
    "http://www.rockymounts.com/Ski_and_Snowboard_Racks_s/154.htm",
    "http://www.rockymounts.com/bike_racks_s/117.htm",
    "http://www.rockymounts.com/truck_bike_racks_s/118.htm",
    "http://www.rockymounts.com/hitch_bike_racks_s/163.htm",
    "http://www.rockymounts.com/category_s/204.htm",
    "http://www.rockymounts.com/category_s/202.htm",
    "http://www.rockymounts.com/racks_lock_cores_s/23.htm",
    "http://www.rockymounts.com/gear_and_clothing_s/34.htm",
    "http://www.rockymounts.com/racks_spareparts_s/35.htm"
);

// Counter used to count the parts and create a unique ID for insertion into the table.
$total = 1;

// Loop over the categories found on the page.
foreach($base_urls as $base_url){

    $cat_content = scraperwiki::scrape($base_url);
    $cat_html = str_get_html($cat_content);

    // Look for the product links
    foreach($cat_html->find("a[@class='productnamecolor']") as $product_link){
        handle_products($product_link->href);
    }
}

echo $total;

function handle_products($product_link)
{
    global $total;
    if(!empty($product_link)){

        $html_content = scraperwiki::scrape($product_link);
        $html = str_get_html($html_content);
        
        $name = utf8_encode(trim($html->find("span[@itemprop='name']",0)->plaintext));
        $price = trim($html->find("span[@itemprop='price']",0)->innertext);
        $code = trim($html->find("span[@class='product_code']",0)->innertext);
        $desc = utf8_encode(trim($html->find("span[@itemprop='description']",0)->plaintext));
        $features = trim($html->find("div[@id='ProductDetail_ProductDetails_div2'] ul",0));
        $brand = "Rockymounts";
        $category_raw = $html->find("td[@class='vCSS_breadcrumb_td'] b a",2);
        $category = (!empty($category_raw)) ? $category_raw->innertext : "";
        $image = "http:" . trim($html->find("img[@id='product_photo']",0)->src);

        // Add it to an array.
        $record = array(
            'id' => $total,
            'code' => substr($code, 0, 4),
            'name' => trim($name),
            'desc' => trim($desc),
            'brand' => $brand,
            'price' => $price,
            'image' => $image,
            'category' => $category,
            'features' => $features
        );

        // Add it to the table.
        scraperwiki::save_sqlite(array('id'), array($record), "rockymounts", 2);

        // Increment the 'id' counter.
        $total++;
 
    }
}

?><?php 

// Include the library.
require 'scraperwiki/simple_html_dom.php';

// We'll need this unchanging element throughout.
define("SCHEME_TO_HOST", "://");

// The base URLs.
$base_urls = array(
    "http://www.rockymounts.com/Ski_and_Snowboard_Racks_s/154.htm",
    "http://www.rockymounts.com/bike_racks_s/117.htm",
    "http://www.rockymounts.com/truck_bike_racks_s/118.htm",
    "http://www.rockymounts.com/hitch_bike_racks_s/163.htm",
    "http://www.rockymounts.com/category_s/204.htm",
    "http://www.rockymounts.com/category_s/202.htm",
    "http://www.rockymounts.com/racks_lock_cores_s/23.htm",
    "http://www.rockymounts.com/gear_and_clothing_s/34.htm",
    "http://www.rockymounts.com/racks_spareparts_s/35.htm"
);

// Counter used to count the parts and create a unique ID for insertion into the table.
$total = 1;

// Loop over the categories found on the page.
foreach($base_urls as $base_url){

    $cat_content = scraperwiki::scrape($base_url);
    $cat_html = str_get_html($cat_content);

    // Look for the product links
    foreach($cat_html->find("a[@class='productnamecolor']") as $product_link){
        handle_products($product_link->href);
    }
}

echo $total;

function handle_products($product_link)
{
    global $total;
    if(!empty($product_link)){

        $html_content = scraperwiki::scrape($product_link);
        $html = str_get_html($html_content);
        
        $name = utf8_encode(trim($html->find("span[@itemprop='name']",0)->plaintext));
        $price = trim($html->find("span[@itemprop='price']",0)->innertext);
        $code = trim($html->find("span[@class='product_code']",0)->innertext);
        $desc = utf8_encode(trim($html->find("span[@itemprop='description']",0)->plaintext));
        $features = trim($html->find("div[@id='ProductDetail_ProductDetails_div2'] ul",0));
        $brand = "Rockymounts";
        $category_raw = $html->find("td[@class='vCSS_breadcrumb_td'] b a",2);
        $category = (!empty($category_raw)) ? $category_raw->innertext : "";
        $image = "http:" . trim($html->find("img[@id='product_photo']",0)->src);

        // Add it to an array.
        $record = array(
            'id' => $total,
            'code' => substr($code, 0, 4),
            'name' => trim($name),
            'desc' => trim($desc),
            'brand' => $brand,
            'price' => $price,
            'image' => $image,
            'category' => $category,
            'features' => $features
        );

        // Add it to the table.
        scraperwiki::save_sqlite(array('id'), array($record), "rockymounts", 2);

        // Increment the 'id' counter.
        $total++;
 
    }
}

?><?php 

// Include the library.
require 'scraperwiki/simple_html_dom.php';

// We'll need this unchanging element throughout.
define("SCHEME_TO_HOST", "://");

// The base URLs.
$base_urls = array(
    "http://www.rockymounts.com/Ski_and_Snowboard_Racks_s/154.htm",
    "http://www.rockymounts.com/bike_racks_s/117.htm",
    "http://www.rockymounts.com/truck_bike_racks_s/118.htm",
    "http://www.rockymounts.com/hitch_bike_racks_s/163.htm",
    "http://www.rockymounts.com/category_s/204.htm",
    "http://www.rockymounts.com/category_s/202.htm",
    "http://www.rockymounts.com/racks_lock_cores_s/23.htm",
    "http://www.rockymounts.com/gear_and_clothing_s/34.htm",
    "http://www.rockymounts.com/racks_spareparts_s/35.htm"
);

// Counter used to count the parts and create a unique ID for insertion into the table.
$total = 1;

// Loop over the categories found on the page.
foreach($base_urls as $base_url){

    $cat_content = scraperwiki::scrape($base_url);
    $cat_html = str_get_html($cat_content);

    // Look for the product links
    foreach($cat_html->find("a[@class='productnamecolor']") as $product_link){
        handle_products($product_link->href);
    }
}

echo $total;

function handle_products($product_link)
{
    global $total;
    if(!empty($product_link)){

        $html_content = scraperwiki::scrape($product_link);
        $html = str_get_html($html_content);
        
        $name = utf8_encode(trim($html->find("span[@itemprop='name']",0)->plaintext));
        $price = trim($html->find("span[@itemprop='price']",0)->innertext);
        $code = trim($html->find("span[@class='product_code']",0)->innertext);
        $desc = utf8_encode(trim($html->find("span[@itemprop='description']",0)->plaintext));
        $features = trim($html->find("div[@id='ProductDetail_ProductDetails_div2'] ul",0));
        $brand = "Rockymounts";
        $category_raw = $html->find("td[@class='vCSS_breadcrumb_td'] b a",2);
        $category = (!empty($category_raw)) ? $category_raw->innertext : "";
        $image = "http:" . trim($html->find("img[@id='product_photo']",0)->src);

        // Add it to an array.
        $record = array(
            'id' => $total,
            'code' => substr($code, 0, 4),
            'name' => trim($name),
            'desc' => trim($desc),
            'brand' => $brand,
            'price' => $price,
            'image' => $image,
            'category' => $category,
            'features' => $features
        );

        // Add it to the table.
        scraperwiki::save_sqlite(array('id'), array($record), "rockymounts", 2);

        // Increment the 'id' counter.
        $total++;
 
    }
}

?><?php 

// Include the library.
require 'scraperwiki/simple_html_dom.php';

// We'll need this unchanging element throughout.
define("SCHEME_TO_HOST", "://");

// The base URLs.
$base_urls = array(
    "http://www.rockymounts.com/Ski_and_Snowboard_Racks_s/154.htm",
    "http://www.rockymounts.com/bike_racks_s/117.htm",
    "http://www.rockymounts.com/truck_bike_racks_s/118.htm",
    "http://www.rockymounts.com/hitch_bike_racks_s/163.htm",
    "http://www.rockymounts.com/category_s/204.htm",
    "http://www.rockymounts.com/category_s/202.htm",
    "http://www.rockymounts.com/racks_lock_cores_s/23.htm",
    "http://www.rockymounts.com/gear_and_clothing_s/34.htm",
    "http://www.rockymounts.com/racks_spareparts_s/35.htm"
);

// Counter used to count the parts and create a unique ID for insertion into the table.
$total = 1;

// Loop over the categories found on the page.
foreach($base_urls as $base_url){

    $cat_content = scraperwiki::scrape($base_url);
    $cat_html = str_get_html($cat_content);

    // Look for the product links
    foreach($cat_html->find("a[@class='productnamecolor']") as $product_link){
        handle_products($product_link->href);
    }
}

echo $total;

function handle_products($product_link)
{
    global $total;
    if(!empty($product_link)){

        $html_content = scraperwiki::scrape($product_link);
        $html = str_get_html($html_content);
        
        $name = utf8_encode(trim($html->find("span[@itemprop='name']",0)->plaintext));
        $price = trim($html->find("span[@itemprop='price']",0)->innertext);
        $code = trim($html->find("span[@class='product_code']",0)->innertext);
        $desc = utf8_encode(trim($html->find("span[@itemprop='description']",0)->plaintext));
        $features = trim($html->find("div[@id='ProductDetail_ProductDetails_div2'] ul",0));
        $brand = "Rockymounts";
        $category_raw = $html->find("td[@class='vCSS_breadcrumb_td'] b a",2);
        $category = (!empty($category_raw)) ? $category_raw->innertext : "";
        $image = "http:" . trim($html->find("img[@id='product_photo']",0)->src);

        // Add it to an array.
        $record = array(
            'id' => $total,
            'code' => substr($code, 0, 4),
            'name' => trim($name),
            'desc' => trim($desc),
            'brand' => $brand,
            'price' => $price,
            'image' => $image,
            'category' => $category,
            'features' => $features
        );

        // Add it to the table.
        scraperwiki::save_sqlite(array('id'), array($record), "rockymounts", 2);

        // Increment the 'id' counter.
        $total++;
 
    }
}

?>