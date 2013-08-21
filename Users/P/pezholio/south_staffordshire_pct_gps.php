<?php
require 'scraperwiki/simple_html_dom.php';  

$html = scraperWiki::scrape("http://www.nhs.uk/Services/Trusts/HospitalsAndClinics/DefaultView.aspx?id=3583"); 

$dom = new simple_html_dom();
$dom->load($html);

$panels = $dom->find('.box');

foreach ($panels as $panel) {
    $name = $panel->find('h3', 0);
    $url = $name->find('a', 0)->href;
    $name = $name->plaintext;
    $address = $panel->find('.addrss', 0)->plaintext;
    $postcode = array_pop(explode("\r\n", $address));
    $postcode = str_replace(" ", "", strtoupper($postcode));
    $latlng = json_decode(file_get_contents("http://www.uk-postcodes.com/postcode/". $postcode .".json"));

    $data = array (
            'name' => $name,
            'url' => $url,
            'address' => $address,
            'postcode' => $postcode,
            'lat' => $latlng->geo->lat,
            'lng' => $latlng->geo->lng
    );
            
    scraperwiki::save_sqlite(array('url'), $data); 
}
?>
