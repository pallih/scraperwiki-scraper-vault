<?php

// Include the library.
require 'scraperwiki/simple_html_dom.php';

// We'll need these unchanging elements throughout.
define("SCHEME_TO_HOST", "://");

// The base URL.
$base_url = "http://www.thule.com/en-us/us";

// Get the necessary components.
$base_url_scheme = parse_url($base_url, PHP_URL_SCHEME);
$base_url_host = parse_url($base_url, PHP_URL_HOST);

// Counter used to count the parts and create a unique ID for insertion into the table.
$total = 1;

$products = array("16296","13806");

// Loop over the products and find the links.
foreach($products as $product_id){

    // Assemble the product URL for products listed in the Support section of the Thule website.
    $product_url = "http://www.thule.com/en-us/us/support/spare-parts?p=" . $product_id;

    // Get the HTML.
    $html_prod_content = scraperwiki::scrape($product_url);
    $html_prod = str_get_html($html_prod_content);

    // Get the image.
    $image =  = $html_prod->find("img[@id='main_0_mainframed_2_ctl04_imgBomImage']",0)->src;

    // Name of the parent product.
    $product_link = $html_prod->find("a[@id='main_0_mainframed_2_ctl04_hlViewProduct']",0)->href;

    $main_product_link = $base_url_scheme . SCHEME_TO_HOST . $base_url_host . $product_link;

    // Get the main product HTML.
    $html_main_prod_content = scraperwiki::scrape($main_product_link);
    $html_main_prod = str_get_html($html_main_prod_content);

    // Find the category.
    $category = $html_main_prod->find("li[@class='active'] a",0)->plaintext;

    // Get the name.
    $name = $html_main_prod->find("h1[@id='main_0_mainframed_0_ctl00_productName']",0)->plaintext;

    // Get the price.
    $price = $html_main_prod->find("span[@class='price price-large']",0)->plaintext;
    $price = trim(str_replace("$", "", $price));

    // Get the description.
    $desc = $html_main_prod->find("p[@id='main_0_mainframed_0_ctl00_productDescripton']",0)->plaintext;
    $desc = trim($desc);

    // Add it to an array.
    $record = array(
        'id' => $total,
        'name' => $name,
        'description' => $desc,
        'price' => $price,
        'image_url' => $image,
        'category' => $category,
    );
    // Add it to the table.
    scraperwiki::save_sqlite(array('id'), array($record), "products", 2);

    // Increment the 'id' counter.
    $total++;
}

echo "\n\nNumber of products: " . $total;
<?php

// Include the library.
require 'scraperwiki/simple_html_dom.php';

// We'll need these unchanging elements throughout.
define("SCHEME_TO_HOST", "://");

// The base URL.
$base_url = "http://www.thule.com/en-us/us";

// Get the necessary components.
$base_url_scheme = parse_url($base_url, PHP_URL_SCHEME);
$base_url_host = parse_url($base_url, PHP_URL_HOST);

// Counter used to count the parts and create a unique ID for insertion into the table.
$total = 1;

$products = array("16296","13806");

// Loop over the products and find the links.
foreach($products as $product_id){

    // Assemble the product URL for products listed in the Support section of the Thule website.
    $product_url = "http://www.thule.com/en-us/us/support/spare-parts?p=" . $product_id;

    // Get the HTML.
    $html_prod_content = scraperwiki::scrape($product_url);
    $html_prod = str_get_html($html_prod_content);

    // Get the image.
    $image =  = $html_prod->find("img[@id='main_0_mainframed_2_ctl04_imgBomImage']",0)->src;

    // Name of the parent product.
    $product_link = $html_prod->find("a[@id='main_0_mainframed_2_ctl04_hlViewProduct']",0)->href;

    $main_product_link = $base_url_scheme . SCHEME_TO_HOST . $base_url_host . $product_link;

    // Get the main product HTML.
    $html_main_prod_content = scraperwiki::scrape($main_product_link);
    $html_main_prod = str_get_html($html_main_prod_content);

    // Find the category.
    $category = $html_main_prod->find("li[@class='active'] a",0)->plaintext;

    // Get the name.
    $name = $html_main_prod->find("h1[@id='main_0_mainframed_0_ctl00_productName']",0)->plaintext;

    // Get the price.
    $price = $html_main_prod->find("span[@class='price price-large']",0)->plaintext;
    $price = trim(str_replace("$", "", $price));

    // Get the description.
    $desc = $html_main_prod->find("p[@id='main_0_mainframed_0_ctl00_productDescripton']",0)->plaintext;
    $desc = trim($desc);

    // Add it to an array.
    $record = array(
        'id' => $total,
        'name' => $name,
        'description' => $desc,
        'price' => $price,
        'image_url' => $image,
        'category' => $category,
    );
    // Add it to the table.
    scraperwiki::save_sqlite(array('id'), array($record), "products", 2);

    // Increment the 'id' counter.
    $total++;
}

echo "\n\nNumber of products: " . $total;
