<?php
require 'scraperwiki/simple_html_dom.php';

/*$html = scraperWiki::scrape("http://www.hemhyra.se/FragaJuristen/Sidor/default.aspx");

$dom = new simple_html_dom();
$dom->load($html);
$counter = 1;
foreach($dom->find("div.askLawyerContainer") as $data){
    $header = $data->find("div.askLawyerHeader");
    $text = $data->find("div.askLawyerText");
    $record = array('id' => $counter, 'header' => $header[0]->plaintext, 'question' => $text[0]->plaintext, 'answer' => $text[1]->plaintext);
    scraperwiki::save(array('id'), $record);
    $counter++;
}*/


$html = scraperWiki::scrape("http://www.hemhyra.se/Sidor/IMD.aspx");

$dom = new simple_html_dom();
$dom->load($html);
$counter = 1;
foreach($dom->find("div.linklistcontainer ul li") as $data){
    $link = $data->find("a");
    print $link[0]."\n";
    //$record = array('id' => $counter, 'header' => $header[0]->plaintext, 'question' => $text[0]->plaintext, 'answer' => $text[1]->plaintext);
    //scraperwiki::save(array('id'), $record);
    //$counter++;
}

?>
