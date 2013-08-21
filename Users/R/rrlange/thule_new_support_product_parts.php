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

$products = array("16296");


// Loop over the products and find the links.
foreach($products as $product_id){
    // Assemble the product URL for products listed in the Support section of the Thule website.
    $product_url = "http://www.thule.com/en-us/us/support/spare-parts?p=" . $product_id;

    // Get the HTML.
    $html_prod_content = scraperwiki::scrape($product_url);
    $html_prod = str_get_html($html_prod_content);

    // Name of the parent product.
    $parent_name_raw = $html_prod->find("h3[@class='headline1-product-small']",0);
    $parent_name = trim($parent_name_raw->plaintext);

    // Get the image associated with the parts.
    $parent_raw_image = $html_prod->find("a[@id='main_0_mainframed_2_ctl04_linkBomImage'] img",0);
    $parent_image = trim($parent_raw_image->src);

    // Loop over the table rows we have.
    foreach($html_prod->find("div[@class='responsive-table-container'] table tbody tr") as $data){
        $tds = $data->find("td");
        if(!empty($tds)){
    
            $seq = trim($tds[0]->plaintext);
    
            // If we don't have a sequence available, it most likely means we are dealing with an ad-hoc part.
            $seq = (strlen($seq) > 0) ? $seq : "--";
    
            $sku_file = $tds[1]->find("a[@class='product-item-name']",0)->href;
            $sku_url = $base_url_scheme . SCHEME_TO_HOST . $base_url_host . $sku_file;
    
            // Need to go to the "Add to Cart" page for the part to determine the Thule SKU.
            $html_part_sku_content = scraperwiki::scrape($sku_url);
            $html_part_sku = str_get_html($html_part_sku_content);
            preg_match("/pr_page_id: '(.*?)',/", $html_part_sku, $skus);
    
            $name_raw = trim($tds[1]->plaintext);
            $names = explode("$", $name_raw);
            $name = trim($names[0]);
            $price_raw = trim($tds[2]->plaintext);
            $price = str_replace("$", "", $price_raw);
            $required_raw = trim($tds[3]->plaintext);
    
            // Add it to an array.
            $record = array(
                'id' => $total,
                'product' => $parent_name,
                'sequence' => $seq,
                'sku' => $skus[1],
                'current_sku' => 0,
                'name' => $name,
                'price' => $price,
                'number_needed' => $required_raw,
                'status' => 'In stock',
                'image' => $parent_image,
                'available' => 1,
                'note' => ''
            );
    
    
            // Add it to the table.
            scraperwiki::save_sqlite(array('id'), array($record), "parts", 2);
    
            // Increment the 'id' counter.
            $total++;
    
        }
    }
}

echo "Number of products: " . $total;

?><?php 

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

$products = array("16296");


// Loop over the products and find the links.
foreach($products as $product_id){
    // Assemble the product URL for products listed in the Support section of the Thule website.
    $product_url = "http://www.thule.com/en-us/us/support/spare-parts?p=" . $product_id;

    // Get the HTML.
    $html_prod_content = scraperwiki::scrape($product_url);
    $html_prod = str_get_html($html_prod_content);

    // Name of the parent product.
    $parent_name_raw = $html_prod->find("h3[@class='headline1-product-small']",0);
    $parent_name = trim($parent_name_raw->plaintext);

    // Get the image associated with the parts.
    $parent_raw_image = $html_prod->find("a[@id='main_0_mainframed_2_ctl04_linkBomImage'] img",0);
    $parent_image = trim($parent_raw_image->src);

    // Loop over the table rows we have.
    foreach($html_prod->find("div[@class='responsive-table-container'] table tbody tr") as $data){
        $tds = $data->find("td");
        if(!empty($tds)){
    
            $seq = trim($tds[0]->plaintext);
    
            // If we don't have a sequence available, it most likely means we are dealing with an ad-hoc part.
            $seq = (strlen($seq) > 0) ? $seq : "--";
    
            $sku_file = $tds[1]->find("a[@class='product-item-name']",0)->href;
            $sku_url = $base_url_scheme . SCHEME_TO_HOST . $base_url_host . $sku_file;
    
            // Need to go to the "Add to Cart" page for the part to determine the Thule SKU.
            $html_part_sku_content = scraperwiki::scrape($sku_url);
            $html_part_sku = str_get_html($html_part_sku_content);
            preg_match("/pr_page_id: '(.*?)',/", $html_part_sku, $skus);
    
            $name_raw = trim($tds[1]->plaintext);
            $names = explode("$", $name_raw);
            $name = trim($names[0]);
            $price_raw = trim($tds[2]->plaintext);
            $price = str_replace("$", "", $price_raw);
            $required_raw = trim($tds[3]->plaintext);
    
            // Add it to an array.
            $record = array(
                'id' => $total,
                'product' => $parent_name,
                'sequence' => $seq,
                'sku' => $skus[1],
                'current_sku' => 0,
                'name' => $name,
                'price' => $price,
                'number_needed' => $required_raw,
                'status' => 'In stock',
                'image' => $parent_image,
                'available' => 1,
                'note' => ''
            );
    
    
            // Add it to the table.
            scraperwiki::save_sqlite(array('id'), array($record), "parts", 2);
    
            // Increment the 'id' counter.
            $total++;
    
        }
    }
}

echo "Number of products: " . $total;

?>