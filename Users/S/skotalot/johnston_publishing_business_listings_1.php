<?php

require_once 'scraperwiki/simple_html_dom.php';

for($i=0; $i<11; $i++) {

    $html = scraperWiki::scrape("http://www.webworldcam.com/results_webcam.php&_sacat=1249&page=" . $i);           
    $dom = new simple_html_dom();
    $dom->load($html);

    foreach($dom->find("div.reviewFull") as $data){

        $name = $data->find("h3");
        $name = trim(preg_replace('/\d+\./', '', $name[0]->plaintext));

        $address = $data->find("div.addressArea");
        $address = trim(preg_replace('/[\t]+/', ' ', $address[0]->plaintext));

        $phone = array();
        preg_match('/\d{5}\s?\d{6}/', $address, $phone);
        $phone = $phone[0];

        $address = trim(str_replace($phone, '', $address));

        $record = array(
            'name' => $name, 
            'address' => $address,
            'phone' => $phone
        );

        scraperwiki::save(array('name'), $record);
    }
}<?php

require_once 'scraperwiki/simple_html_dom.php';

for($i=0; $i<11; $i++) {

    $html = scraperWiki::scrape("http://www.webworldcam.com/results_webcam.php&_sacat=1249&page=" . $i);           
    $dom = new simple_html_dom();
    $dom->load($html);

    foreach($dom->find("div.reviewFull") as $data){

        $name = $data->find("h3");
        $name = trim(preg_replace('/\d+\./', '', $name[0]->plaintext));

        $address = $data->find("div.addressArea");
        $address = trim(preg_replace('/[\t]+/', ' ', $address[0]->plaintext));

        $phone = array();
        preg_match('/\d{5}\s?\d{6}/', $address, $phone);
        $phone = $phone[0];

        $address = trim(str_replace($phone, '', $address));

        $record = array(
            'name' => $name, 
            'address' => $address,
            'phone' => $phone
        );

        scraperwiki::save(array('name'), $record);
    }
}