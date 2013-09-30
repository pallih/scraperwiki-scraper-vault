<?php
require 'scraperwiki/simple_html_dom.php'; 
set_time_limit(0);

// While $i (the loop counter) is less than or equal to 9999 (the number of times you want to navigate)
$lastpage = scraperwiki::get_var('last_page');
//$lastpage = 60;
print $lastpage;
for ($i=$lastpage; $i <= 9999; $i++) {
     
$html_content = scraperwiki::scrape("https://www.airbnb.co.uk/s?page=".$i."&room_types[]=Entire+home%2Fapt");
$html = str_get_html($html_content);

if (!empty($html)) {
$listingnum = $html->find("li.search_result");
foreach ($listingnum as $el) {    
       
    //print $el-> . "\n";
    $url_listing=array(
    'listingnum'=> $el->getAttribute('data-hosting-id'),
    'neighborhood'=> (isset($el->find('span.neighborhood-link', 0)->plaintext)) ? $el->find('span.neighborhood-link', 0)->plaintext : null,
    'url'=> 'https://www.airbnb.com/rooms/'.$el->getAttribute('data-hosting-id'),
    );


$neigh = $url_listing['neighborhood'];
$hostingid = $url_listing['listingnum'];
$url_listing = $url_listing['url'];
$url_listing = scraperwiki::scrape($url_listing);
$html = str_get_html($url_listing);

if (!empty($html)) {
//Galleria Images
$result = $html->find('div[id=galleria_container]/a');
$galleria = array();
foreach($result as $element) {
    $val = $element->getAttribute('href');
    $galleria[] = $val;
    //print json_encode($galleria) . "\n";
}

//Reviews Messages
$result = $html->find('p.message');
$messages = array();
foreach($result as $element) {
    $val = $element->innertext;
    $messages[] = $element;
    //print json_encode($galleria) . "\n";
}

//Description Details li
$result = $html->find('ul[id=description_details]/li');
$inputs = array();
foreach($result as $element) {
    $key = $element->find('span.property', 0)->plaintext;
    $val = $element->find('span.value', 0)->plaintext;
    $inputs[$key]=$val;
    //print json_encode($inputs) . "\n";
}

//Other Page Attributes
    $attributes = array (
    'id'=> $hostingid,
    'title'=> $html->getElementsByTagName('title')->plaintext,
    'saved_count'=> $html->find('div.saved_count span', 0)->plaintext,
    'price'=> $html->find('h2[id=price_amount]', 0)->plaintext,
    'description'=> $html->find('div[id=description_text_wrapper]', 0)->plaintext,
    'images'=> implode(' ^^',$galleria),
    'review_count'=> $html->find('span[itemprop=reviewCount]', 0)->plaintext,
    'stars'=> $html->find('meta[property=airbedandbreakfast:rating]', 0)->content,
    'og_image'=> $html->find('meta[property=og:image]', 0)->content,
    'postal_code'=> $html->find('meta[property=airbedandbreakfast:postal-code]', 0)->content,
    'locality'=> $html->find('meta[property=airbedandbreakfast:locality]', 0)->content,
    'region'=> (isset($el->find('meta[property=airbedandbreakfast:region]', 0)->plaintext)) ? $el->find('meta[property=airbedandbreakfast:region]', 0)->plaintext : null,
    'country_name'=> $html->find('meta[property=airbedandbreakfast:country-name]', 0)->content,
    'city'=> $html->find('meta[property=airbedandbreakfast:city]', 0)->content,
    'neighborhood'=> $neigh,
    'lat'=> $html->find('meta[property=airbedandbreakfast:location:latitude]', 0)->content,
    'lat'=> $html->find('meta[property=airbedandbreakfast:location:latitude]', 0)->content,
    'currency'=> $html->find('div[id=pricing]/meta', 0)->content,
    'messages'=> implode(' ^^',$messages),
    ); 
    $dbdata = ($attributes+$inputs);
    //$dbdata = mb_check_encoding($dbdata, 'UTF-8') ? $dbdata : utf8_encode($dbdata);
    //print json_encode($dbdata) . "\n";
    scraperwiki::save(array('id'), $dbdata);
    $html->__destruct();
 

    }//End single room load
}    // End the listingnum loop
}    // End if
    scraperwiki::save_var('last_page', $i);  
    $html->__destruct();
};    // End the  for loop

?><?php
require 'scraperwiki/simple_html_dom.php'; 
set_time_limit(0);

// While $i (the loop counter) is less than or equal to 9999 (the number of times you want to navigate)
$lastpage = scraperwiki::get_var('last_page');
//$lastpage = 60;
print $lastpage;
for ($i=$lastpage; $i <= 9999; $i++) {
     
$html_content = scraperwiki::scrape("https://www.airbnb.co.uk/s?page=".$i."&room_types[]=Entire+home%2Fapt");
$html = str_get_html($html_content);

if (!empty($html)) {
$listingnum = $html->find("li.search_result");
foreach ($listingnum as $el) {    
       
    //print $el-> . "\n";
    $url_listing=array(
    'listingnum'=> $el->getAttribute('data-hosting-id'),
    'neighborhood'=> (isset($el->find('span.neighborhood-link', 0)->plaintext)) ? $el->find('span.neighborhood-link', 0)->plaintext : null,
    'url'=> 'https://www.airbnb.com/rooms/'.$el->getAttribute('data-hosting-id'),
    );


$neigh = $url_listing['neighborhood'];
$hostingid = $url_listing['listingnum'];
$url_listing = $url_listing['url'];
$url_listing = scraperwiki::scrape($url_listing);
$html = str_get_html($url_listing);

if (!empty($html)) {
//Galleria Images
$result = $html->find('div[id=galleria_container]/a');
$galleria = array();
foreach($result as $element) {
    $val = $element->getAttribute('href');
    $galleria[] = $val;
    //print json_encode($galleria) . "\n";
}

//Reviews Messages
$result = $html->find('p.message');
$messages = array();
foreach($result as $element) {
    $val = $element->innertext;
    $messages[] = $element;
    //print json_encode($galleria) . "\n";
}

//Description Details li
$result = $html->find('ul[id=description_details]/li');
$inputs = array();
foreach($result as $element) {
    $key = $element->find('span.property', 0)->plaintext;
    $val = $element->find('span.value', 0)->plaintext;
    $inputs[$key]=$val;
    //print json_encode($inputs) . "\n";
}

//Other Page Attributes
    $attributes = array (
    'id'=> $hostingid,
    'title'=> $html->getElementsByTagName('title')->plaintext,
    'saved_count'=> $html->find('div.saved_count span', 0)->plaintext,
    'price'=> $html->find('h2[id=price_amount]', 0)->plaintext,
    'description'=> $html->find('div[id=description_text_wrapper]', 0)->plaintext,
    'images'=> implode(' ^^',$galleria),
    'review_count'=> $html->find('span[itemprop=reviewCount]', 0)->plaintext,
    'stars'=> $html->find('meta[property=airbedandbreakfast:rating]', 0)->content,
    'og_image'=> $html->find('meta[property=og:image]', 0)->content,
    'postal_code'=> $html->find('meta[property=airbedandbreakfast:postal-code]', 0)->content,
    'locality'=> $html->find('meta[property=airbedandbreakfast:locality]', 0)->content,
    'region'=> (isset($el->find('meta[property=airbedandbreakfast:region]', 0)->plaintext)) ? $el->find('meta[property=airbedandbreakfast:region]', 0)->plaintext : null,
    'country_name'=> $html->find('meta[property=airbedandbreakfast:country-name]', 0)->content,
    'city'=> $html->find('meta[property=airbedandbreakfast:city]', 0)->content,
    'neighborhood'=> $neigh,
    'lat'=> $html->find('meta[property=airbedandbreakfast:location:latitude]', 0)->content,
    'lat'=> $html->find('meta[property=airbedandbreakfast:location:latitude]', 0)->content,
    'currency'=> $html->find('div[id=pricing]/meta', 0)->content,
    'messages'=> implode(' ^^',$messages),
    ); 
    $dbdata = ($attributes+$inputs);
    //$dbdata = mb_check_encoding($dbdata, 'UTF-8') ? $dbdata : utf8_encode($dbdata);
    //print json_encode($dbdata) . "\n";
    scraperwiki::save(array('id'), $dbdata);
    $html->__destruct();
 

    }//End single room load
}    // End the listingnum loop
}    // End if
    scraperwiki::save_var('last_page', $i);  
    $html->__destruct();
};    // End the  for loop

?>