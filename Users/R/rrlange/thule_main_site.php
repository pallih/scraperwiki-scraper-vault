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

// Get the HTML.
$html_content = scraperwiki::scrape($base_url);
$html = str_get_html($html_content);

// Counter used to count the parts and create a unique ID for insertion into the table.
$total = 1;

$cats = array(
  "http://www.thule.com/en-us/us/products/carriers-and-racks/bike-carriers/roof-mounted-bike-carriers",
  "http://www.thule.com/en-us/us/products/carriers-and-racks/bike-carriers/hitch-mounted-bike-carriers",
  "http://www.thule.com/en-us/us/products/carriers-and-racks/bike-carriers/rear-door-mounted-bike-carriers",
  "http://www.thule.com/en-us/us/products/carriers-and-racks/bike-carriers/spare-tire-bike-carriers",
  "http://www.thule.com/en-us/us/products/carriers-and-racks/bike-carriers/truck-bed-bike-carriers",
  "http://www.thule.com/en-us/us/products/carriers-and-racks/bike-carriers/bike-carrier-accessories",
  "http://www.thule.com/en-us/us/products/carriers-and-racks/boxes-and-baskets/roof-boxes",
  "http://www.thule.com/en-us/us/products/carriers-and-racks/boxes-and-baskets/cargo-bags",
  "http://www.thule.com/en-us/us/products/carriers-and-racks/boxes-and-baskets/carrier-baskets",
  "http://www.thule.com/en-us/us/products/carriers-and-racks/boxes-and-baskets/rear-mounted-cargo",
  "http://www.thule.com/en-us/us/products/carriers-and-racks/roof-racks/feet",
  "http://www.thule.com/en-us/us/products/carriers-and-racks/roof-racks/complete-all-in-one-racks",
  "http://www.thule.com/en-us/us/products/carriers-and-racks/roof-racks/racks-load-bars",
  "http://www.thule.com/en-us/us/products/carriers-and-racks/roof-racks/load-accessories",
  "http://www.thule.com/en-us/us/products/carriers-and-racks/water-sport-carriers/kayak-and-canoe-carriers",
  "http://www.thule.com/en-us/us/products/carriers-and-racks/water-sport-carriers/surf-boards-carriers",
  "http://www.thule.com/en-us/us/products/carriers-and-racks/water-sport-carriers/water-sports-carrier-accessories",
  "http://www.thule.com/en-us/us/products/carriers-and-racks/winter-sport-carriers/roof-mounted-ski-carriers",
  "http://www.thule.com/en-us/us/products/carriers-and-racks/winter-sport-carriers/roof-boxes",
  "http://www.thule.com/en-us/us/products/carriers-and-racks/winter-sport-carriers/hitch-ski-carriers",
  "http://www.thule.com/en-us/us/products/carriers-and-racks/winter-sport-carriers/winter-sports-carrier-accessories"
);

// Loop over the categories.
foreach($cats as $cat_link){
    
    // Get the HTML.
    $html_content = scraperwiki::scrape($cat_link);
    $html = str_get_html($html_content);

    // Loop over the products and find the links.
    foreach($html->find("article[@class='product-item'] a") as $product_link){
        $product_url = $base_url_scheme . SCHEME_TO_HOST . $base_url_host . $product_link->href;

        // Get the HTML.
        $html_prod_content = scraperwiki::scrape($product_url);
        $html_prod = str_get_html($html_prod_content);

        // Loop over the table rows we have.
        foreach($html_prod->find("a[@id='main_0_mainframed_0_ctl00_sparePartModalButton']") as $part_link){

            $part_url = html_entity_decode($part_link->href);

            $part = $base_url_scheme . SCHEME_TO_HOST . $base_url_host . $part_url;
            $parts_url = $part;

            $html_part_content = scraperwiki::scrape($parts_url);
            $html_part = str_get_html($html_part_content);

            $parent_name_raw = $html_part->find("h3[@class='headline1-product-small']",0);
            $parent_name = trim($parent_name_raw->plaintext);
            $parent_raw_image = $html_part->find("a[@id='ctl00_linkBomImage'] img",0);
            $parent_image = trim($parent_raw_image->src);

            // Loop over the table rows we have.
            foreach($html_part->find("div[@class='responsive-table-container'] table tbody tr") as $data){
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
    }
}

echo "Number of products: " . $total;

?>