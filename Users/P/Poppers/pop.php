<?php
$base = "http://www.4poppers.com/";  // Initial url to start scraping
require 'scraperwiki/simple_html_dom.php';



$ScrapeList = array();
$output = array();
// Get all URLS
// Find all links




function findURLs($url) {
     
    global $output;
    global $base;
    echo $base . "\n";
    $urls = array();
    $dom  = new simple_html_dom();
    $html = scraperWiki::scrape($url);
    $dom->load($html);
    foreach ($dom->find('a') as $element) {
            if ((strpos($element->href, 'javascript') === false) && (strpos($element->href, 'cart.php') === false)){
                $temp =  $base . $element->href;
                //echo $base . $element->href . "\n";

                //if (!in_array($temp, $urls)){
                //    $urls[] = $temp;
                //}   
                $record = array('url' => $temp);

                scraperwiki::save(array('url'), $record);
                $urls = addArray($temp, $urls);
            }  
    //echo $base . $element->href . "\n";


    if (count($urls) > 4353453454) return $urls;  // temp stop loop.
    }
    return $urls;
}

function getMetaData($url){
    $tags = get_meta_tags($url);
    unset($tags['google-site-verification']);
    return $tags;
}


// SCRAPE URLS

// main loop

//main($base);
//print_r($output);
 $urls = findURLs($base);
 

function main($startURL){
    global $dom;
    global $output;
    $dom  = new simple_html_dom();
    $urls = findURLs($startURL);


    foreach ($urls as $url ){
        $html = scraperWiki::scrape($url);
        $dom->load($html);
        $title = $dom->find('title',0);
        $output['title'][$url] = $title->plaintext;
        //$h1 = $html->find('div[id=main]',0);

        foreach($dom->find('div[id=main]') as $main)
        {
            foreach($main->find('h1') as $header)
            {
                $output['h1'][$url] = $header->plaintext;
            }  // End Header

            foreach($main->find('img') as $img)
            {
                $output['img'][$url] = $img;
            }
            $output['body'] = $main->plaintext;

            foreach($main->find('div[class=addtocart]') as $price)
            {
                if (!empty($price)) {
                $output['price'][$url] = $price->innertext;
                foreach($price as $buyurl)
                {
                    if (!empty($buyurl)) {
                    $output['buy'][$url] = $buyurl->innertext;
                   }
                }
                }
            }
        }
    }
}

/*
Title tag
H1
Img URL
Img atr
description
price
add to url

*/

// Find all images
function findAllImg($url){
    $dom  = new simple_html_dom();
    $images = array();
    $html = scraperWiki::scrape($url);
    $dom->load($html);
    foreach ($dom->find('img') as $element) {
        if (strpos($element->src, 'images/catalog/') !== false) {
           $images = addArray($element->src, $images);
        }
    }
    return $images;
}


// Helpers

function addArray($item, $list){
    if (!in_array($item, $list)){
        $list[] = $item;
        return $list;
    }
    return $list;
}
