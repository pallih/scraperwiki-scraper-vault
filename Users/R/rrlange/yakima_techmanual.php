<?php 

// Include the library.
require 'scraperwiki/simple_html_dom.php';

// The base URL.
$base_url = "http://techmanual.yakima.com/";
$allowed_tags = "<br>,<strong>,<b>";

$active_skus = get_products("active");
$discontinued_skus = get_products("discontinued");

process_data($active_skus, 1);
process_data($discontinued_skus, 0);

// To process the data.
function process_data($skus, $avail = 1){
    global $allowed_tags;
    if(!empty($skus) && is_array($skus)){
        foreach($skus as $sku){
            // Get the description.
            $description = strip_tags(get_description($sku), $allowed_tags);
            // Add it to an array.
            $record = array(
                'sku' => $sku,
                'avail' => $avail,
                'desc' => $description
            );
            // Add it to the table.
            scraperwiki::save_sqlite(array('sku'), array($record), "techmanual", 2);
        }
    }
}


// To retrieve the in-depth description for the part.
function get_description($part){
    global $base_url;
    if($part){
        // Instantiate the scraper.
        $html_content = scraperwiki::scrape($base_url . "default.aspx?product_num=" . $part);

        // Get the HTML.
        $html = str_get_html($html_content);
 
        // Description from ID.
        $desc_raw = $html->find("span[@id='txtPartDesc']");
        $desc = $desc_raw[0]->innertext;
        return $desc;
    }
}


// To retrieve the SKUs from the page, active or discontinued.
function get_products($which = "active"){
    global $base_url;

    // Empty array we are populating later.
    $skus = array();

    // The id of the select HTML element we are using.
    $select_id = ($which == "active") ? "ddlProductActive" : "ddlProductDiscontinued";

    // Instantiate the scraper.
    $html_content = scraperwiki::scrape($base_url);

    // Get the HTML.
    $html = str_get_html($html_content);

    // Loop over the categories.
    foreach($html->find("select[@id='" . $select_id . "'] option") as $option){

        // Grab what is between parenthesis.
        $ids = preg_match('#\((.*?)\)#', $option->innertext, $match);

        // Make sure it matches the 7-digit we need from Yakima.
        if(array_key_exists('1', $match)){
            if(preg_match('#\d{7}#',$match[1],$matches)){
                if(array_key_exists('0', $matches)){
                    $skus[] = $matches[0];
                }
            }
        }
    }

    return $skus;
}
?>