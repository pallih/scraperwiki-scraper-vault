<?php

$html = scraperWiki::scrape("http://gallery.artron.net/Gallery_Map_ResultsW.php?action=SelectGallery&city=%E5%8C%97%E4%BA%AC&AreaCode=&Name=&first=&Order=&page=1");           

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div.gallAreaBox dl") as $data){
    $dt = $data->find("dt");
    $dds = $data->find("dd");
    $record = array(
        'description' => $dt[0]->plaintext,
        'address' => $dds[0]->plaintext, 
        'phone' => $dds[1]->plaintext
    );
    scraperwiki::save(array('description'), $record); 
}


?>
