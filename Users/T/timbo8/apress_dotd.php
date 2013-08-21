<?php

$html = scraperWiki::scrape("http://apress.com");
print $html . "\n";

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[@class='block block-dotd']") as $data){

    $as = $data->find("a");

    $ps = $data->find("p");
    $time = time();
    $record = array(
        'time' => $time,

        'image' => $as[0]->plaintext,

        'book' => $ps[0]->plaintext, 
        'wasprice' => $ps[1]->plaintext, 
        'isprice' => $ps[2]->plaintext,
    );
    scraperwiki::save(array('book'), $record);
}

?>

