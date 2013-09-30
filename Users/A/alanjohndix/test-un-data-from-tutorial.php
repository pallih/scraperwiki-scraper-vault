<?php

$html = scraperWiki::scrape("http://unstats.un.org/unsd/demographic/products/socind/education.htm");
require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
$count=0;
foreach($dom->find("div[@align='left'] tr.tcont") as $data){
    $tds = $data->find("td");
    $record = array( 'country' => $tds[0]->plaintext, 'years_in_school' => intval($tds[4]->plaintext) );
    //print_r($record);
    //$count++;
    //if ( $count > 10 ) break;
    scraperwiki::save(array('country'), $record); 
}

?>
<?php

$html = scraperWiki::scrape("http://unstats.un.org/unsd/demographic/products/socind/education.htm");
require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
$count=0;
foreach($dom->find("div[@align='left'] tr.tcont") as $data){
    $tds = $data->find("td");
    $record = array( 'country' => $tds[0]->plaintext, 'years_in_school' => intval($tds[4]->plaintext) );
    //print_r($record);
    //$count++;
    //if ( $count > 10 ) break;
    scraperwiki::save(array('country'), $record); 
}

?>
