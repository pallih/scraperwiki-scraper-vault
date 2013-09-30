<?php
require "scraperwiki/simple_html_dom.php";
define("BASE_URL", "http://www.gifbin.com/");
$base_url = "http://www.gifbin.com";

// Save a record to the data store.
function saveData($unique, $tag_link ) {
      scraperWiki::save_sqlite($unique, $tag_link );
}
// Get rid of whitespace and spaces
function removeSpaces($text) {
    return str_replace("&nbsp;","%20", $text);
}

$tag_source = scraperWiki::scrape("http://www.gifbin.com/tags");
$html = new simple_html_dom();
$html->load($tag_source);
$tag_cloud = $html->find("div[@class='tag_cloud']");
$tags = $tag_cloud[0]->find('a');    
$tag_id = 0;
foreach($tags as $tag) { 
    $tag_id = $tag_id+1; 

    $tag_url= removeSpaces($tag->href); 
    $tag_name= $tag->plaintext;

    $tag_link = array(
                "tag_name"=>$tag_name,                             
                "tag_url"=>$base_url.$tag_url     
                );
       
}

$html->clear();  
unset($html);  

foreach ($tag_link as $link)
        {
            function getArticles($page)
            {
            $source = scraperWiki::scrape($page);
            $html = new simple_html_dom();
            $html->load($source);
            $box= $html->find("div[@class='box']");
                foreach($box->find("div[@class='thumb-cell']") as $thumb); 
                {
                 $links= $thumb->find('a');   
                 $url = $links->href;
                 $url=$base_url.$url;


            $tag_id = 0;

            }
            getArticles($link[tag_url]);  
        } 







?>
<?php
require "scraperwiki/simple_html_dom.php";
define("BASE_URL", "http://www.gifbin.com/");
$base_url = "http://www.gifbin.com";

// Save a record to the data store.
function saveData($unique, $tag_link ) {
      scraperWiki::save_sqlite($unique, $tag_link );
}
// Get rid of whitespace and spaces
function removeSpaces($text) {
    return str_replace("&nbsp;","%20", $text);
}

$tag_source = scraperWiki::scrape("http://www.gifbin.com/tags");
$html = new simple_html_dom();
$html->load($tag_source);
$tag_cloud = $html->find("div[@class='tag_cloud']");
$tags = $tag_cloud[0]->find('a');    
$tag_id = 0;
foreach($tags as $tag) { 
    $tag_id = $tag_id+1; 

    $tag_url= removeSpaces($tag->href); 
    $tag_name= $tag->plaintext;

    $tag_link = array(
                "tag_name"=>$tag_name,                             
                "tag_url"=>$base_url.$tag_url     
                );
       
}

$html->clear();  
unset($html);  

foreach ($tag_link as $link)
        {
            function getArticles($page)
            {
            $source = scraperWiki::scrape($page);
            $html = new simple_html_dom();
            $html->load($source);
            $box= $html->find("div[@class='box']");
                foreach($box->find("div[@class='thumb-cell']") as $thumb); 
                {
                 $links= $thumb->find('a');   
                 $url = $links->href;
                 $url=$base_url.$url;


            $tag_id = 0;

            }
            getArticles($link[tag_url]);  
        } 







?>
