<?php

function geocode($addr) {

    $addrParts = splitAddress($addr);
    $a = urlencode($addrParts[0]);
    $c = urlencode($addrParts[1]);

    $geocodeURL = "http://www.urbanspoon.com/n/332/";
    //$geocodeURL = "http://maps.googleapis.com/maps/api/geocode/json?address=$a&sensor=false";
    $ch = curl_init($geocodeURL);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    $result = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($httpCode == 200) {
        $geocode = json_decode($result);
        if (count($geocode->candidates) > 0) {
            $candidate = $geocode->candidates[0];
            $formatted_address = $candidate->address;
            $lat = $candidate->location->y;
            $lng  = $candidate->location->x;
            return array($lat, $lng, $formatted_address);
        }
    }

    return array();
}

function splitAddress($addr) {
    $lines = explode("<br>", $addr);
    $street = strip_tags($lines[0]);
    $city = preg_replace('/[^a-z ]/i', '', strip_tags($lines[1]));

    return array($street, $city);
}

$html = scraperWiki::scrape("urbanspoon.com/n/332/");

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();

$dom->load($html);
foreach($dom->find(".listResult") as $restaurant) {

    $name = $restaurant->find(".name h3", 0);
    $link = $name->find("a", 0);
    $addr = $restaurant->find(".name .place", 0);
    $logo = $restaurant->find(".thumb img", 0);
    $cuisines = $restaurant->find(".type .spec");
    $cert = $restaurant->find(".surveillance", 0);

    $cleanCuisines = array_map(function($c) { return utf8_encode(trim($c->plaintext)); }, $cuisines);

    if ($link->href != '') {

        $latLng = geocode($addr);

        if (!empty($latLng)) {

            $address = utf8_encode($addr->plaintext);
    
            $record = array(
                'url' => 'http://www.kosherinfrance.com/' . $link->href,
                'name' => utf8_encode(array_pop(explode('Kosher Restaurant ', $name->plaintext))),
                'originalAddress' => $address,
                'address' => $latLng[2],
                'lat' => $latLng[0],
                'lng' => $latLng[1],
                'logo' => 'http://www.kosherinfrance.com/' . $logo->src,
                'cuisine' => implode(", ", $cleanCuisines),
                'certification' => utf8_encode($cert->plaintext)
            );
        
            scraperwiki::save(array('url'), $record);     
        }
    }

}

?>
<?php

function geocode($addr) {

    $addrParts = splitAddress($addr);
    $a = urlencode($addrParts[0]);
    $c = urlencode($addrParts[1]);

    $geocodeURL = "http://www.urbanspoon.com/n/332/";
    //$geocodeURL = "http://maps.googleapis.com/maps/api/geocode/json?address=$a&sensor=false";
    $ch = curl_init($geocodeURL);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    $result = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($httpCode == 200) {
        $geocode = json_decode($result);
        if (count($geocode->candidates) > 0) {
            $candidate = $geocode->candidates[0];
            $formatted_address = $candidate->address;
            $lat = $candidate->location->y;
            $lng  = $candidate->location->x;
            return array($lat, $lng, $formatted_address);
        }
    }

    return array();
}

function splitAddress($addr) {
    $lines = explode("<br>", $addr);
    $street = strip_tags($lines[0]);
    $city = preg_replace('/[^a-z ]/i', '', strip_tags($lines[1]));

    return array($street, $city);
}

$html = scraperWiki::scrape("urbanspoon.com/n/332/");

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();

$dom->load($html);
foreach($dom->find(".listResult") as $restaurant) {

    $name = $restaurant->find(".name h3", 0);
    $link = $name->find("a", 0);
    $addr = $restaurant->find(".name .place", 0);
    $logo = $restaurant->find(".thumb img", 0);
    $cuisines = $restaurant->find(".type .spec");
    $cert = $restaurant->find(".surveillance", 0);

    $cleanCuisines = array_map(function($c) { return utf8_encode(trim($c->plaintext)); }, $cuisines);

    if ($link->href != '') {

        $latLng = geocode($addr);

        if (!empty($latLng)) {

            $address = utf8_encode($addr->plaintext);
    
            $record = array(
                'url' => 'http://www.kosherinfrance.com/' . $link->href,
                'name' => utf8_encode(array_pop(explode('Kosher Restaurant ', $name->plaintext))),
                'originalAddress' => $address,
                'address' => $latLng[2],
                'lat' => $latLng[0],
                'lng' => $latLng[1],
                'logo' => 'http://www.kosherinfrance.com/' . $logo->src,
                'cuisine' => implode(", ", $cleanCuisines),
                'certification' => utf8_encode($cert->plaintext)
            );
        
            scraperwiki::save(array('url'), $record);     
        }
    }

}

?>
