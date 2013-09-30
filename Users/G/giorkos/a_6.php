<?php 
$html = scraperWiki::scrape("https://play.google.com/store/apps/collection/topselling_free");           

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find("ul.container-snippet-list li") as $data){

    $name = $data->find("div.details a");
    $image = $data->find("div.thumbnail-wrapper img");

    $record = array(
            'name' => $name[0]->plaintext,
            'thumbnail' => $image[0]->src
        );
    scraperwiki::save(array('name'), $record);  
}
?>

