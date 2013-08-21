<?php

/*
require 'scraperwiki/simple_html_dom.php';
                 $dom = new simple_html_dom();

$link = 'http://www.ask.com/pictureslanding?o=0&l=dir&qsrc=321';


$html = scraperwiki::scrape($link);

//Search for extentions
$videos = array('mpg', 'avi', 'mp4', 'wma', 'wmv', 'flv');
$images = array('jpg', 'jpeg');
$maxX = 250;
$maxY = 250;
$video_format = '.flv';


$dom->load($html);

foreach ($dom->find('a > img') as $img) {

   scraperwiki::save(
    array('table_cell','table'),
    array(
        'table_cell' => $img->getAttribute('alt'),
        'table' => $img->getAttribute('src')
        )
    );

 }
*/
$data = scraperwiki::select( "* from swdata desc limit 1000" ); 
foreach ($data as $record) {
    echo'<img src="' . $record['table'] .'"/>';
}

?>
