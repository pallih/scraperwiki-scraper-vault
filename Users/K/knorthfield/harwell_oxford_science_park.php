<?php
require 'scraperwiki/simple_html_dom.php';
$page = new simple_html_dom();

for( $i = 0; $i < 1000; $i++ ){

    $html = scraperWiki::scrape("http://harwelloxford.com/node/$i");
    $page->load($html);

    $record = array(
        'name' => trim( $page->find(".field-field-contact .field-item",0)->plaintext ),
        'company' => trim( $page->find("h1",0)->plaintext ),
        'address' => trim( $page->find(".field-field-location .field-item",0)->plaintext ),
        'phone' => trim( $page->find(".field-field-telephone .field-item",0)->plaintext ),
        'email' => trim( $page->find(".field-field-email .field-item",0)->plaintext ),
        'website' => $page->find(".field-field-weblink .field-item a",0)->href,
        'source' => "http://harwelloxford.com/node/$i"
    );

    scraperwiki::save(array('company'), $record);
    //print json_encode($record) . "\n";

}

?>