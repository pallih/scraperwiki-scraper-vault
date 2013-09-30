<?php

// ALEX MULCHINOCK
// CIRRUS IT SOLUTIONS LIMITED

require_once 'scraperwiki/simple_html_dom.php'; // PULLS SCRAPEWIKI STUFF

//////////////////////////////////// EDIT BELOW HERE:
$html_content = scraperwiki::scrape("http://www.accupart.co.uk/quanta__C55.html/results=50/"); // THE PAGE WE'RE SCRAPING
//////////////////////////////////// EDIT ABOVE HERE:

$html = str_get_html($html_content); // CREATING A HANDY VARIABLE TO USE LATER.

foreach ($html->find("div.product_title_long a") as $title) { //DEFINING THE PRODUCT TITLE SEARCH CRITERIA.           
    $title_data = preg_split("/[\s,]+/" ,$title->innertext); //GET THE TEXT FROM THE TITLE AND SPLIT UP.
    $link_data = preg_split("/.html/", $title->href); //GET THE LINKS FOR EACH PRODUCT ON THE PAGE- USED LATER FOR GETTING FURTHER PRODUCT INFORMATION.

    //echo $title_data[0] . "\n"; // ECHO OUT FIELD 1
    //echo $title_data[1] . "\n"; // ECHO OUT FIELD 2
    //echo $title_data[2] . "\n"; // ECHO OUT FIELD 3
    //echo $title_data[3] . "\n"; // ECHO OUT FIELD 4
    //echo preg_replace('/"/','',$title_data[3]) . "\n"; // ECHO OUT SCREEN SIZE

    
    $further_html_content = scraperwiki::scrape($link_data[0].".html"); // THE FURTHER PAGES WE'RE SCRAPING
    $further_html = str_get_html($further_html_content); // CREATING ANOTHER USEFUL VARIABLE TO SAVE TIME TYPING


// GETTING THE PRODUCT REF.    
    foreach ($further_html->find("div.product_ref") as $product_ref) { //DEFINING THE PRODUCT CODE SEARCH CRIETERIA.
    $product_ref_data = $product_ref->innertext; //GET THE TEXT FROM THE PRODUCT REF.
    $product_code_array = preg_split("/[\s,]+/",$product_ref); //SPLIT TEXT UP.
    //echo $product_code_array[4] ."\n"; // ECHO OUT PRODUCT REF
    };


// GETTING THE EX VAT PRICE
    foreach ($further_html->find("div.current_price_ex_vat span#top_product_price") as $product_xvat) { //DEFINING THE PRODUCT CODE SEARCH CRIETERIA.
    $product_xvat_data = $product_xvat->innertext; //GET THE TEXT FROM THE PRODUCT REF.
    $xvat_strip = strip_tags($product_xvat); // GET RID OF <SPAN> TAGS
    $xvat_array = preg_split("/&#163;/",$xvat_strip); // REMOVE POUND SIGN
    //echo $xvat_array[1] . "\n"; // ECHO OUT PRICE X VAT
    };

//STORING THE DATA IN AN ARRAY
if (!isset($title_data[0])) {
    $title_data[0] = 'N/A';
}
if (!isset($title_data[1])) {
    $title_data[1] = 'N/A';
}
if (!isset($title_data[2])) {
    $title_data[2] = 'N/A';
}
if (!isset($title_data[3])) {
    $title_data[3] = 'N/A';
}
if (!isset($title_data[4])) {
    $title_data[4] = 'N/A';
}
if (!isset($title_data[5])) {
    $title_data[5] = 'N/A';
}
if (!isset($title_data[6])) {
    $title_data[6] = 'N/A';
}
if (!isset($title_data[7])) {
    $title_data[7] = 'N/A';
}
if (!isset($title_data[8])) {
    $title_data[8] = 'N/A';
}
if (!isset($title_data[9])) {
    $title_data[9] = 'N/A';
}
    $record = array (
        'field1' => $title_data[0], 
        'field2' => $title_data[1],
        'field3' => $title_data[2],
        'field4' => $title_data[3],
        'field5' => $title_data[4],
        'field6' => $title_data[5],
        'field7' => $title_data[6],
        'field8' => $title_data[7],
        'field9' => $title_data[8],
        'field10' => $title_data[9],
        'sku' => $product_code_array[4],
        'exvatcost' => $xvat_array[1],
    );

scraperwiki::save(array('sku'), $record);

};
<?php

// ALEX MULCHINOCK
// CIRRUS IT SOLUTIONS LIMITED

require_once 'scraperwiki/simple_html_dom.php'; // PULLS SCRAPEWIKI STUFF

//////////////////////////////////// EDIT BELOW HERE:
$html_content = scraperwiki::scrape("http://www.accupart.co.uk/quanta__C55.html/results=50/"); // THE PAGE WE'RE SCRAPING
//////////////////////////////////// EDIT ABOVE HERE:

$html = str_get_html($html_content); // CREATING A HANDY VARIABLE TO USE LATER.

foreach ($html->find("div.product_title_long a") as $title) { //DEFINING THE PRODUCT TITLE SEARCH CRITERIA.           
    $title_data = preg_split("/[\s,]+/" ,$title->innertext); //GET THE TEXT FROM THE TITLE AND SPLIT UP.
    $link_data = preg_split("/.html/", $title->href); //GET THE LINKS FOR EACH PRODUCT ON THE PAGE- USED LATER FOR GETTING FURTHER PRODUCT INFORMATION.

    //echo $title_data[0] . "\n"; // ECHO OUT FIELD 1
    //echo $title_data[1] . "\n"; // ECHO OUT FIELD 2
    //echo $title_data[2] . "\n"; // ECHO OUT FIELD 3
    //echo $title_data[3] . "\n"; // ECHO OUT FIELD 4
    //echo preg_replace('/"/','',$title_data[3]) . "\n"; // ECHO OUT SCREEN SIZE

    
    $further_html_content = scraperwiki::scrape($link_data[0].".html"); // THE FURTHER PAGES WE'RE SCRAPING
    $further_html = str_get_html($further_html_content); // CREATING ANOTHER USEFUL VARIABLE TO SAVE TIME TYPING


// GETTING THE PRODUCT REF.    
    foreach ($further_html->find("div.product_ref") as $product_ref) { //DEFINING THE PRODUCT CODE SEARCH CRIETERIA.
    $product_ref_data = $product_ref->innertext; //GET THE TEXT FROM THE PRODUCT REF.
    $product_code_array = preg_split("/[\s,]+/",$product_ref); //SPLIT TEXT UP.
    //echo $product_code_array[4] ."\n"; // ECHO OUT PRODUCT REF
    };


// GETTING THE EX VAT PRICE
    foreach ($further_html->find("div.current_price_ex_vat span#top_product_price") as $product_xvat) { //DEFINING THE PRODUCT CODE SEARCH CRIETERIA.
    $product_xvat_data = $product_xvat->innertext; //GET THE TEXT FROM THE PRODUCT REF.
    $xvat_strip = strip_tags($product_xvat); // GET RID OF <SPAN> TAGS
    $xvat_array = preg_split("/&#163;/",$xvat_strip); // REMOVE POUND SIGN
    //echo $xvat_array[1] . "\n"; // ECHO OUT PRICE X VAT
    };

//STORING THE DATA IN AN ARRAY
if (!isset($title_data[0])) {
    $title_data[0] = 'N/A';
}
if (!isset($title_data[1])) {
    $title_data[1] = 'N/A';
}
if (!isset($title_data[2])) {
    $title_data[2] = 'N/A';
}
if (!isset($title_data[3])) {
    $title_data[3] = 'N/A';
}
if (!isset($title_data[4])) {
    $title_data[4] = 'N/A';
}
if (!isset($title_data[5])) {
    $title_data[5] = 'N/A';
}
if (!isset($title_data[6])) {
    $title_data[6] = 'N/A';
}
if (!isset($title_data[7])) {
    $title_data[7] = 'N/A';
}
if (!isset($title_data[8])) {
    $title_data[8] = 'N/A';
}
if (!isset($title_data[9])) {
    $title_data[9] = 'N/A';
}
    $record = array (
        'field1' => $title_data[0], 
        'field2' => $title_data[1],
        'field3' => $title_data[2],
        'field4' => $title_data[3],
        'field5' => $title_data[4],
        'field6' => $title_data[5],
        'field7' => $title_data[6],
        'field8' => $title_data[7],
        'field9' => $title_data[8],
        'field10' => $title_data[9],
        'sku' => $product_code_array[4],
        'exvatcost' => $xvat_array[1],
    );

scraperwiki::save(array('sku'), $record);

};
