<?php



require 'scraperwiki/simple_html_dom.php';    

$location = 'kashmir';
// add to end of url and scrape all the photos
$flickr_url = "http://flickrhivemind.net/flickr_hvmnd.cgi?search_type=Tags&photo_number=50&photo_type=250&noform=t&quicksearch=1&sort=Interestingness&textinput=Glasgow";

$page = scraperWiki::scrape($flickr_url);
print_r($page);

$dom = new simple_html_dom(); 
$dom->load($page);

//add each element to an array

$pics = array();

foreach($dom->find('img') as $img) {
        echo $img->src;            
       };