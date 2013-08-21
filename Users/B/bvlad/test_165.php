<?php
require 'scraperwiki/simple_html_dom.php';      

// $html = scraperWiki::scrape("http://unstats.un.org/unsd/demographic/products/socind/education.htm");           
$html = scraperWiki::scrape("http://kochbuch.unix-ag.uni-kl.de/bin/rezept.php?id=1");           
 
    
$dom = new simple_html_dom();
$dom->load($html);


/*
foreach($dom->find("div[@align='left'] tr.tcont") as $data){
    $tds = $data->find("td");
    $record = array(
        'country' => $tds[0]->plaintext, 
        'years_in_school' => intval($tds[4]->plaintext)
    );


*/
$title = $dom->find("head title",0);           
print $title . "\n";

$recipe = $dom->find("body pre",0);           
print $recipe . "\n";


//scraperwiki::save(array('country'), $record);      

?>
