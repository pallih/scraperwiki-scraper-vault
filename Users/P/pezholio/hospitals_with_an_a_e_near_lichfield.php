<?php
require 'scraperwiki/simple_html_dom.php';  

function IsPostcode($postcode) {
$postcode = strtoupper($postcode);
$pattern = "((GIR 0AA)|(TDCU 1ZZ)|(ASCN 1ZZ)|(BIQQ 1ZZ)|(BBND 1ZZ)"
."|(FIQQ 1ZZ)|(PCRN 1ZZ)|(STHL 1ZZ)|(SIQQ 1ZZ)|(TKCA 1ZZ)"
."|[A-PR-UWYZ]([0-9]{1,2}|([A-HK-Y][0-9]"
."|[A-HK-Y][0-9]([0-9]|[ABEHMNPRV-Y]))"
."|[0-9][A-HJKS-UW])( {0,1})[0-9][ABD-HJLNP-UW-Z]{2})"; 
   
    if(preg_match($pattern, $postcode, $matches)) {
        return $matches[0];
    } else {
        return FALSE;
    }
}

$html = scraperWiki::scrape("http://www.nhs.uk/ServiceDirectories/Pages/ServiceResults.aspx?Postcode=WS13%206YY&Coords=3092,4117&ServiceType=AandE&JScript=0"); 

$dom = new simple_html_dom();
$dom->load($html);

$results = $dom->find('ul.results > li');

foreach ($results as $result) {
    $name = $result->find('a', 0)->plaintext;
    $name = explode(" providing", $name);
    $name = $name[0];
    $url = "http://www.nhs.uk".$result->find('a', 0)->href;
    $address = $result->find('.address', 0)->plaintext;
    if (strlen($address) > 0) {
    $postcode = IsPostcode($address);
    $postcode = str_replace(" ", "", strtoupper($postcode));
    $latlng = json_decode(file_get_contents("http://www.uk-postcodes.com/postcode/". $postcode .".json?a=b"));

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
}
?>
