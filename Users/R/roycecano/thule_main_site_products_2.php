<?php 

// Include the library.
require 'scraperwiki/simple_html_dom.php';

// We'll need this unchanging element throughout.
define("SCHEME_TO_HOST", "://");

// The base URL.
$base_url = "http://www.thule.com/en-US/US/Products";

// Get the necessary components.
$base_url_scheme = parse_url($base_url, PHP_URL_SCHEME);
$base_url_host = parse_url($base_url, PHP_URL_HOST);

// Get the HTML from the page and turn it into a string.
$html_content = scraperwiki::scrape($base_url);
$html = str_get_html($html_content);

// Counter used to count the parts and create a unique ID for insertion into the table.
$total = 1;

// Loop over the categories found on the page.
foreach($html->find("ul[@id='categorySubmenuLeft'] li a") as $menu_link){

    // Define what we dive into.
    $link = $base_url_scheme . SCHEME_TO_HOST . $base_url_host . $menu_link->href;

    // echo "Category: " . $link . "\n";

    $html_content_1 = scraperwiki::scrape($link);
    $html_1 = str_get_html($html_content_1);

    // Categories can have both products and/or subcategories.
    $product_string = $html_1->find("div[@class='productLinkArea'] a");
    $sub_category_string = $html_1->find("div[@class='product_category'] h2 a");
    if(!empty($product_string)){
        // Look for the product links
        foreach($product_string as $product_link){
            handle_products($product_link);
        }
    }
    elseif(!empty($sub_category_string)){
        // Look for the subcategories
        foreach($sub_category_string as $menu_link_2){

            $link_2 = $base_url_scheme . SCHEME_TO_HOST . $base_url_host . $menu_link_2->href;

            // echo "Subcategory: " . $link_2 . "\n";

            $html_content_2 = scraperwiki::scrape($link_2);
            $html_2 = str_get_html($html_content_2);

            // Look for the product links
            foreach($html_2->find("div[@class='productLinkArea'] a") as $product_link){
                handle_products($product_link);
            }
        }
    }

}

function handle_products($product_link)
{
    global $base_url_host, $base_url_scheme, $total;
    if(!empty($product_link)){

        // There are times when Thule will list discontinued products as part of their catalog - test for this...
        $found = stripos($product_link, "discontinued");

        if ($found === false) {

            $link_3 = $base_url_scheme . SCHEME_TO_HOST . $base_url_host . $product_link->href;
            $cat_raw = str_replace("/en-US/US/Products/", "", $product_link->href);

            $cats = dirname($cat_raw);
            
            $cat_terms = array("Base-Racks/Feet", "Base-Racks/LoadAccessories", "Base-Racks/LoadBars", "Bike-Carriers/Accessories", "Bike-Carriers/Hitch", "Bike-Carriers/RearDoor", "Bike-Carriers/RoofCarriers", "Bike-Carriers/SpareTire", "Bike-Carriers/TruckBed", "Cargo-Carriers/Bags", "Cargo-Carriers/Baskets", "Cargo-Carriers/Boxes", "Cargo-Carriers/HitchCargo", "Luggage/DaypacksAndMessengers", "Luggage/LaptopAndTablet", "Luggage/LuggageAndDuffels", "Snow-Chains/SnowChains", "Snowsports/Accessories", "Snowsports/HitchSki", "Snowsports/SkiBoxes", "Snowsports/SkiCarriers", "Watersports/Accessories", "Watersports/WatersportCarriers");

            $cat_cleaned = array("Base Racks/Feet", "Base Racks/Load Accessories", "Base Racks/Load Bars", "Bike Carriers/Accessories", "Bike Carriers/Hitch", "Bike Carriers/Rear Door", "Bike Carriers/Roof Carriers", "Bike Carriers/Spare Tire", "Bike Carriers/Truck Bed", "Cargo Carriers/Bags", "Cargo Carriers/Baskets", "Cargo Carriers/Boxes", "Cargo Carriers/Hitch Cargo", "Luggage/Daypacks And Messengers", "Luggage/Laptop And Tablet", "Luggage/Luggage And Duffels", "Snow Chains/Snow Chains", "Snowsports/Accessories", "Snowsports/Hitch Ski", "Snowsports/Ski Boxes", "Snowsports/Ski Carriers", "Watersports/Accessories", "Watersports/Watersport Carriers");

            $cat = str_replace($cat_terms, $cat_cleaned, $cats);

            $html_content = scraperwiki::scrape($link_3);
            $html = str_get_html($html_content);
            
            $name_raw = trim($html->find("div[@class='column details_overview'] h2 span",0));
            $name = (!empty($name_raw)) ? strip_tags($name_raw) : "";
            
            $desc_raw = trim($html->find("div[@class='column details_overview'] h3 span",0));
            $desc = (!empty($desc_raw)) ? strip_tags($desc_raw) : "";

            $price_raw = trim($html->find("div[@class='pricing'] span[@id='phcontent_0_ctl00_lblPriceText']",0));
            $price = strip_tags($price_raw);
            $price = str_replace("MSRP $", "", $price);
            $price = trim(str_replace(" (USD)", "", $price));
            $image = trim($html->find("div[@class='promo_photo'] div img",0)->src);

            // Add it to an array.
            $record = array(
                'id' => $total,
                'product_name' => trim($name),
                'desciption' => trim($desc),
                'price' => $price,
                'img' => $image,
                'category' => $cat
            );

            // Add it to the table.
            scraperwiki::save_sqlite(array('id'), array($record), "products", 2);

            // Increment the 'id' counter.
            $total++;

        }        
    }
}

function cleanProductName($string)
{
    if($string){
        $string = str_replace("-", " ", $string);
        $str = preg_replace("/[^A-Za-z0-9\s]/", "", $string);
        return $str;
    }
}

echo "Number of parts: " . $total;

?>