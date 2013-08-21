<?php

require 'scraperwiki/simple_html_dom.php';
$genrelink = "http://www.boxofficemojo.com/movies/?id=avengers11.htm";
$genrehtml = scraperWiki::scrape($genrelink);
$gendom = new simple_html_dom();
$gendom->load($genrehtml);


foreach($gendom->find("td[@valign='top']" ) as $gendata){
    //$btag = $gendata->find("b");
    //print $gendata;
    $btag = $gendata->find("b");
    $genre = $btag[4]->plaintext;
    if(count($genre)>0){
        break;
    } 
}
print $genre;
?>
