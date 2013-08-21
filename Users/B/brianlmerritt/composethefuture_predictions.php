<?php

// require scraperwiki's HTML parsing script
require 'scraperwiki/simple_html_dom.php';  

// define the URL you want to scrape
$html = scraperWiki::scrape("http://www.composethefuture.com/predictionNews.php?menuid=MQ==");                  
$dom = new simple_html_dom();
$dom->load($html);

// select the left hand side story divs
foreach($dom->find('.borderline') as $record){
    $title = $record->find('.hd');
    $imageurl = $record->find('.image') ;
    $author = $record->find('.fl') ;
    $startdate= $record->find('.startDate') ;
    $predictiontype = $record->find('.ptype') ;
    $details= $record->find('.table') ;
    $text= $record->last_child() ;


    
// create the array
    $record = array(
       
        'author' => substr(strip_tags($author[0]),3),
        'title' => strip_tags($title[0]),
//        'imageurl' => strip_tags($imageurl[0]),
        'prediction_year' => strip_tags($startdate[0]),
        'predictiontype' => substr(strip_tags($predictiontype[0]),1,-1),
        'details' => strip_tags($details[0]),
//        'text' => $text ,
        
    );


// 
// save array to scraperwiki, based on the 'Title' array, which will be checked every time scraperwiki updates
 scraperwiki::save_sqlite(array('author'), $record);


}

// spare loop
/*
for ($i = 1; $i <= sizeof($record); $i++)
*/

?>