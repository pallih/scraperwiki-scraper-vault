<?php
require 'scraperwiki/simple_html_dom.php';     
scraperWiki::sqliteexecute('drop table if exists ttt');
$url = 'http://www.rugbydump.blogspot.com/';
$html = scraperWiki::scrape($url);

$dom = new simple_html_dom();
$dom->load($html);

$movies = $dom->find('object param[name="movie"]');
$i=0;
foreach($movies as $movie){
    $i++;
    $movieurl = $movie->value;
   
    $data = array( 'id'=>  "code:New_Script_Resolve('".$movieurl."')", 'title'=> 'Video '.$i );
    scraperWiki::save_sqlite(array('id'), $data);

}


?>
