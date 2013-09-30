<?php 

// Include the library.
require 'scraperwiki/simple_html_dom.php';

// We'll need these unchanging elements throughout.
define("SCHEME_TO_HOST", "://");
define("PARTS_APPEND", "?view=spareparts");

// Are we in 'dev' mode? Boolean.
$dev = 1;

// The base URL.
$base_url = "http://www.autozone.com/autozone/ymme/selector.jsp?which=overlay";

// Get the necessary components.
$base_url_scheme = parse_url($base_url, PHP_URL_SCHEME);
$base_url_host = parse_url($base_url, PHP_URL_HOST);

// Get the HTML.
$html_content = scraperwiki::scrape($base_url);
$html = str_get_html($html_content);

// Counter used to count the parts and create a unique ID for insertion into the table.
$total = 1;

// Loop over the categories.
foreach($html->find("ul[@id='categorySubmenuLeft'] li a") as $menu_link){

    // Define what we dive into.
    $link = $base_url_scheme . SCHEME_TO_HOST . $base_url_host . $menu_link->href;

    my_echo("Category: " . $link);

    $html_content_1 = scraperwiki::scrape($link);
    $html_1 = str_get_html($html_content_1);

    // Categories can have both prducts and/or subcategories.
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

            my_echo("Subcategory: " . $link_2);

            $html_content_2 = scraperwiki::scrape($link_2);
            $html_2 = str_get_html($html_content_2);

            // Look for the product links
            foreach($html_2->find("div[@class='productLinkArea'] a") as $product_link){

                handle_products($product_link);

            }
        }
    }

}

function my_echo($string)
{
    global $dev;
    if(empty($string)){
        if ($dev == 1) {
            echo "DEBUG: ";
            echo $message;
            echo "\n";
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
            $link_elements = parse_url($link_3);
            $link_path = explode("/", $link_elements['path']);
            $product_name = str_replace("-", " ", end($link_path));

            my_echo("Product Link: " . $link_3);
            my_echo("Product Name: " . $product_name);

            $html_content_3 = scraperwiki::scrape($link_3 . PARTS_APPEND);
            $html_3 = str_get_html($html_content_3);

            // Get the name.
            $par_name_raw = trim($html_3->find("div[@class='parts_page_column'] h2",0));
            $par_name = (!empty($par_name_raw)) ? strip_tags($par_name_raw) : "";

            // Get the parts image.
            $a_link = $html_3->find("a[@id='phcontent_0_ctl00_lbBomImage']");
            $img_raw = (!empty($a_link)) ? $a_link[0]->find("img",0)->src : "";

            // Loop over the table rows we have.
            foreach($html_3->find("div[@id='phcontent_0_ctl00_pnlPartsList'] table tr[id]") as $data){
                $tds = $data->find("td");
                $seq = trim($tds[0]->plaintext);
                $name = trim($tds[1]->find("h4",0)->plaintext);
                $sku = trim($tds[1]->find("span.partno",0)->plaintext);
                $price = trim($tds[2]->plaintext);
                $needed = trim($tds[3]->plaintext);
                $status = trim($tds[5]->plaintext);

                // If we don't have a sequence available, it most likely means we are dealing with an ad-hoc part.
                if(strlen($seq) > 0){

                    // Ad-hoc parts have commas in their prices; we'll substitute them with 'periods.'
                    $price = str_replace(",", ".", $price);

                    // Add it to an array.
                    $record = array(
                        'id' => $total,
                        'sku' => $sku,
                        'name' => $name,
                        'price' => $price,
                        'parent_name' => $par_name,
                        'img' => $img_raw,
                        'sequence' => $seq,
                        'needed' => $needed,
                        'status' => $status
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

my_echo("Number of parts: " . $total);

?><?php 

// Include the library.
require 'scraperwiki/simple_html_dom.php';

// We'll need these unchanging elements throughout.
define("SCHEME_TO_HOST", "://");
define("PARTS_APPEND", "?view=spareparts");

// Are we in 'dev' mode? Boolean.
$dev = 1;

// The base URL.
$base_url = "http://www.autozone.com/autozone/ymme/selector.jsp?which=overlay";

// Get the necessary components.
$base_url_scheme = parse_url($base_url, PHP_URL_SCHEME);
$base_url_host = parse_url($base_url, PHP_URL_HOST);

// Get the HTML.
$html_content = scraperwiki::scrape($base_url);
$html = str_get_html($html_content);

// Counter used to count the parts and create a unique ID for insertion into the table.
$total = 1;

// Loop over the categories.
foreach($html->find("ul[@id='categorySubmenuLeft'] li a") as $menu_link){

    // Define what we dive into.
    $link = $base_url_scheme . SCHEME_TO_HOST . $base_url_host . $menu_link->href;

    my_echo("Category: " . $link);

    $html_content_1 = scraperwiki::scrape($link);
    $html_1 = str_get_html($html_content_1);

    // Categories can have both prducts and/or subcategories.
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

            my_echo("Subcategory: " . $link_2);

            $html_content_2 = scraperwiki::scrape($link_2);
            $html_2 = str_get_html($html_content_2);

            // Look for the product links
            foreach($html_2->find("div[@class='productLinkArea'] a") as $product_link){

                handle_products($product_link);

            }
        }
    }

}

function my_echo($string)
{
    global $dev;
    if(empty($string)){
        if ($dev == 1) {
            echo "DEBUG: ";
            echo $message;
            echo "\n";
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
            $link_elements = parse_url($link_3);
            $link_path = explode("/", $link_elements['path']);
            $product_name = str_replace("-", " ", end($link_path));

            my_echo("Product Link: " . $link_3);
            my_echo("Product Name: " . $product_name);

            $html_content_3 = scraperwiki::scrape($link_3 . PARTS_APPEND);
            $html_3 = str_get_html($html_content_3);

            // Get the name.
            $par_name_raw = trim($html_3->find("div[@class='parts_page_column'] h2",0));
            $par_name = (!empty($par_name_raw)) ? strip_tags($par_name_raw) : "";

            // Get the parts image.
            $a_link = $html_3->find("a[@id='phcontent_0_ctl00_lbBomImage']");
            $img_raw = (!empty($a_link)) ? $a_link[0]->find("img",0)->src : "";

            // Loop over the table rows we have.
            foreach($html_3->find("div[@id='phcontent_0_ctl00_pnlPartsList'] table tr[id]") as $data){
                $tds = $data->find("td");
                $seq = trim($tds[0]->plaintext);
                $name = trim($tds[1]->find("h4",0)->plaintext);
                $sku = trim($tds[1]->find("span.partno",0)->plaintext);
                $price = trim($tds[2]->plaintext);
                $needed = trim($tds[3]->plaintext);
                $status = trim($tds[5]->plaintext);

                // If we don't have a sequence available, it most likely means we are dealing with an ad-hoc part.
                if(strlen($seq) > 0){

                    // Ad-hoc parts have commas in their prices; we'll substitute them with 'periods.'
                    $price = str_replace(",", ".", $price);

                    // Add it to an array.
                    $record = array(
                        'id' => $total,
                        'sku' => $sku,
                        'name' => $name,
                        'price' => $price,
                        'parent_name' => $par_name,
                        'img' => $img_raw,
                        'sequence' => $seq,
                        'needed' => $needed,
                        'status' => $status
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

my_echo("Number of parts: " . $total);

?>