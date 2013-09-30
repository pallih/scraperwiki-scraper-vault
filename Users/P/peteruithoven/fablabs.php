<?php

$html = scraperWiki::scrape("http://wiki.fablab.is/wiki/Portal:Labs");       
require 'scraperwiki/simple_html_dom.php';  
$dom = new simple_html_dom();
$dom->load($html);
//$i = 0;
foreach($dom->find("#content .wikitable tr") as $data)
{
    $tds = $data->find("td");
    if(count($tds) == 0) continue;
    
    $country = $tds[0]-plaintext;
    $city = $tds[1]->plaintext;
    $combinedLocation = $country." ". $city;
    $locationName = $tds[2]->plaintext;
    $website = $tds[3]->plaintext;
    $rating = (count($tds) >= 5)? $tds[4]->plaintext : "";
    $contact = (count($tds) >= 6)? $tds[5]-plaintext : "";

    /* Google maps
     * - limited to 2,500 requests in a 24 hour period (more details here: http://code.google.com/apis/maps/faq.html#geocoder_limit)
     * TODO: Research using  MapQuest's Nominatim search system (using data from openstreetmaps): http://open.mapquestapi.com/nominatim/ */
    $lat = " ";
    $lng = " ";
    $geocode_url = 'http://maps.googleapis.com/maps/api/geocode/json?sensor=false&output=json&address=';
    $geoResult = file_get_contents($geocode_url.urlencode($combinedLocation));
    $geoJSON = json_decode($geoResult);
    print("Status: ".$geoJSON->status." ");
    if($geoJSON->status == "OK")
    {
        $lat = $geoJSON->results[0]->geometry->location->lat;
        $lng = $geoJSON->results[0]->geometry->location->lng;
    }
    else
    {
        echo "Can't locate: $locationName ($combinedLocation)";
    }
    $fablab = array(
        'name' => $locationName,        
        'location' => $combinedLocation,
        'website' => $website,
        'lat' => $lat,
        'lng' => $lng,
        'rating' => $rating,
        'contact' => $contact
    );
    //print_r($fablab);
    scraperwiki::save(array('name','location'), $fablab);

    sleep((2000+rand(0,1000))/1000);

    //$i++;
    //if($i > 3) break;
}

?>
<?php

$html = scraperWiki::scrape("http://wiki.fablab.is/wiki/Portal:Labs");       
require 'scraperwiki/simple_html_dom.php';  
$dom = new simple_html_dom();
$dom->load($html);
//$i = 0;
foreach($dom->find("#content .wikitable tr") as $data)
{
    $tds = $data->find("td");
    if(count($tds) == 0) continue;
    
    $country = $tds[0]-plaintext;
    $city = $tds[1]->plaintext;
    $combinedLocation = $country." ". $city;
    $locationName = $tds[2]->plaintext;
    $website = $tds[3]->plaintext;
    $rating = (count($tds) >= 5)? $tds[4]->plaintext : "";
    $contact = (count($tds) >= 6)? $tds[5]-plaintext : "";

    /* Google maps
     * - limited to 2,500 requests in a 24 hour period (more details here: http://code.google.com/apis/maps/faq.html#geocoder_limit)
     * TODO: Research using  MapQuest's Nominatim search system (using data from openstreetmaps): http://open.mapquestapi.com/nominatim/ */
    $lat = " ";
    $lng = " ";
    $geocode_url = 'http://maps.googleapis.com/maps/api/geocode/json?sensor=false&output=json&address=';
    $geoResult = file_get_contents($geocode_url.urlencode($combinedLocation));
    $geoJSON = json_decode($geoResult);
    print("Status: ".$geoJSON->status." ");
    if($geoJSON->status == "OK")
    {
        $lat = $geoJSON->results[0]->geometry->location->lat;
        $lng = $geoJSON->results[0]->geometry->location->lng;
    }
    else
    {
        echo "Can't locate: $locationName ($combinedLocation)";
    }
    $fablab = array(
        'name' => $locationName,        
        'location' => $combinedLocation,
        'website' => $website,
        'lat' => $lat,
        'lng' => $lng,
        'rating' => $rating,
        'contact' => $contact
    );
    //print_r($fablab);
    scraperwiki::save(array('name','location'), $fablab);

    sleep((2000+rand(0,1000))/1000);

    //$i++;
    //if($i > 3) break;
}

?>
