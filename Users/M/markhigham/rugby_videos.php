<?php
require 'scraperwiki/simple_html_dom.php';     

$url = 'http://www.rugbydump.blogspot.com/';
$html = scraperWiki::scrape($url);

$dom = new simple_html_dom();
$dom->load($html);

$movies = $dom->find('object param[name="movie"]');

foreach($movies as $movie){
    $movieurl = $movie->value;
   
    $data = array( 'video'=>  $movieurl);
    scraperWiki::save_sqlite(array('video'), $data);

}


?>
<?php
require 'scraperwiki/simple_html_dom.php';     

$url = 'http://www.rugbydump.blogspot.com/';
$html = scraperWiki::scrape($url);

$dom = new simple_html_dom();
$dom->load($html);

$movies = $dom->find('object param[name="movie"]');

foreach($movies as $movie){
    $movieurl = $movie->value;
   
    $data = array( 'video'=>  $movieurl);
    scraperWiki::save_sqlite(array('video'), $data);

}


?>
