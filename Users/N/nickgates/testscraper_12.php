<?php

// Enter Search String
$searchString = "paris";

$page = 1;

require 'scraperwiki/simple_html_dom.php'; 
  
$html_content = scraperwiki::scrape(processSearchString($searchString));
processImages($html_content);



/*
* Function to turn the search string into a url.
* This function is unique for each site
*
* 500px
*/
function processSearchString($search) {
    $page = 1;

    $s = $search;
    $s = str_replace(" ", "+", $s);
    $s = urlencode($s);

    $link = "http://500px.com/search?order=popularity&page=".$page."&q=".$s."&type=photos&utf8=%E2%9C%93";
    return $link;
}

/*
* Function to process html into an array of imageLinks
* This function is unique for each site
*
* 500px
*/
function  processImages($html){
    $html = str_get_html($html);

    $elements = $html->find("div.photo");
    foreach ($elements as $element) {           
        $link = substr( $element->children(0)->children(0)->src ,0,-5);

        $record['photographer'] = $element->find("div",0)->children(0)->children(0)->innertext;
        $record['reputation'] =   (int)(getReputation('http://www.500px.com' . $element->find("div",0)->children(0)->children(0)->href)); 
        $record['title'] =  $element->find("div",0)->children(1)->innertext; 
        $record['thumb'] = $link . "2.jpg";
        $record['photo'] = $link . "4.jpg";

        scraperwiki::save(array('title'), $record);       
    }
}

 /*
* Function to process html into an array of imageLinksget reputation of user
* This function is unique for each site
*
* 500px
*/ 
function getReputation($userLink){
    $html = str_get_html(scraperwiki::scrape($userLink));   
 
    $affection = $html->find("div#showaffection h1",0)->innertext;
    return $affection;
}


?>
<?php

// Enter Search String
$searchString = "paris";

$page = 1;

require 'scraperwiki/simple_html_dom.php'; 
  
$html_content = scraperwiki::scrape(processSearchString($searchString));
processImages($html_content);



/*
* Function to turn the search string into a url.
* This function is unique for each site
*
* 500px
*/
function processSearchString($search) {
    $page = 1;

    $s = $search;
    $s = str_replace(" ", "+", $s);
    $s = urlencode($s);

    $link = "http://500px.com/search?order=popularity&page=".$page."&q=".$s."&type=photos&utf8=%E2%9C%93";
    return $link;
}

/*
* Function to process html into an array of imageLinks
* This function is unique for each site
*
* 500px
*/
function  processImages($html){
    $html = str_get_html($html);

    $elements = $html->find("div.photo");
    foreach ($elements as $element) {           
        $link = substr( $element->children(0)->children(0)->src ,0,-5);

        $record['photographer'] = $element->find("div",0)->children(0)->children(0)->innertext;
        $record['reputation'] =   (int)(getReputation('http://www.500px.com' . $element->find("div",0)->children(0)->children(0)->href)); 
        $record['title'] =  $element->find("div",0)->children(1)->innertext; 
        $record['thumb'] = $link . "2.jpg";
        $record['photo'] = $link . "4.jpg";

        scraperwiki::save(array('title'), $record);       
    }
}

 /*
* Function to process html into an array of imageLinksget reputation of user
* This function is unique for each site
*
* 500px
*/ 
function getReputation($userLink){
    $html = str_get_html(scraperwiki::scrape($userLink));   
 
    $affection = $html->find("div#showaffection h1",0)->innertext;
    return $affection;
}


?>
