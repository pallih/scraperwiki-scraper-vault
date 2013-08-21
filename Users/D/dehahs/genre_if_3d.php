<?php

require 'scraperwiki/simple_html_dom.php';
//$genrelink = "http://www.boxofficemojo.com/movies/?id=monstersinc3d.htm";
$genrelink = "http://www.boxofficemojo.com/movies/?id=endofwatch.htm";
$genrehtml = scraperWiki::scrape($genrelink);
$gendom = new simple_html_dom();
$gendom->load($genrehtml);

$offset=0;
//Increment offset by 1 if there is a 'Domestic Lifetime Gross' data
foreach($gendom->find("td[@align='center'] a" ) as $gendata){
    $lgrosstag = $gendata->find("b");
    if(count($lgrosstag)>0){
        $lgross = $lgrosstag[0]->plaintext;
        if(count($lgross)>0){
            $offset=1;
            break;
        }
    }
}

foreach($gendom->find("td[@valign='top']" ) as $gendata){
    //$btag = $gendata->find("b");
    //print $gendata;
    $btag = $gendata->find("b");
    $genre = $btag[4+$offset]->plaintext;
    if(count($genre)>0){
        break;
    }
}
print $genre;
print $lgross;
?>
