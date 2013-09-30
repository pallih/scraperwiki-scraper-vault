<?php

$html = scraperWiki::scrape("http://wiki.fablab.is/wiki/Portal:Labs");       
require 'scraperwiki/simple_html_dom.php';  
$dom = new simple_html_dom();
$dom->load($html);
$i = 0;
$fablabs = array();

print_r(scraperwiki::show_tables()); 

foreach($dom->find("#content .wikitable tr") as $data)
{
    //if($i == 22 || $i == 33)
    //{
    ///print("i: ".$i);
    $tds = $data->find("td");
    if(count($tds) == 0) continue;
    
    $country = $tds[0]->plaintext;
    $city = $tds[1]->plaintext;
    $combinedLocation = $country." ". $city;
    //print("combinedLocation: ".$combinedLocation);
    //$combinedLocation = str_replace(";"," ",$combinedLocation);
    $combinedLocationQuery = preg_replace('/[,;]/i',"",$combinedLocation);    
    $combinedLocationQuery = preg_replace('/[+]/i'," ",$combinedLocationQuery);
    $combinedLocationQuery = preg_replace('/^ | $|  |\r|\n/i',"",$combinedLocationQuery);
    $combinedLocationQuery = str_replace('ü',"u",$combinedLocationQuery);
    $combinedLocationQuery = str_replace('â',"a",$combinedLocationQuery);
    //print("  combinedLocation: ".$combinedLocation);
    $combinedLocationQuery = urlencode($combinedLocationQuery);
    //print("    combinedLocation: ".$combinedLocation);
    $locationName = $tds[2]->plaintext;
    $website = $tds[3]->plaintext;
    $rating = (count($tds) >= 5)? $tds[4]->plaintext : "";
    $contact = (count($tds) >= 6)? $tds[5]->plaintext : "";

    
    /* Google maps
     * - limited to 2,500 requests in a 24 hour period (more details here: http://code.google.com/apis/maps/faq.html#geocoder_limit)
     * TODO: Research using  MapQuest's Nominatim search system (using data from openstreetmaps): http://open.mapquestapi.com/nominatim/ */
    
    $lat = "";
    $lng = "";

    /*$oldFablabData = scraperwiki::select("* from swdata where name='locationName'");*/
    //$oldFablabData = scraperwiki::select("* from swdata");
    $sql = "* from swdata where name='$locationName'";
    print("sql: ".$sql);
    $oldFablabData = scraperwiki::select($sql);
    print_r($oldFablabData);

    if($oldFablabData['location'] != $combinedLocation || $oldFablabData['lat'] == "")
    {
        print("overwrite<br>");
        $geocode_url = 'http://open.mapquestapi.com/nominatim/v1/search?format=json&q=';
        $geoResult = file_get_contents($geocode_url.$combinedLocationQuery);
        $geoJSON = json_decode($geoResult);
        //print("geoJSON: ".$geoJSON." ");
        //print("Count: ".count($geoJSON)." ");
        if(count($geoJSON) > 0)
        {
            $place = $geoJSON[0];
            //print("place: ".$place." ");
            $lat = $place->lat;
            $lng = $place->lon;
            print($i." located ".$locationName." (".$lat." x ".$lng.")");

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

        }
        else
        {
            echo "Can't locate: $locationName ($combinedLocation)";
        }

        
    }

    
    
    
    sleep((1000+rand(0,500))/1000);
    
    $i++;
    //if($i > 3) break;
}
?>
<?php

$html = scraperWiki::scrape("http://wiki.fablab.is/wiki/Portal:Labs");       
require 'scraperwiki/simple_html_dom.php';  
$dom = new simple_html_dom();
$dom->load($html);
$i = 0;
$fablabs = array();

print_r(scraperwiki::show_tables()); 

foreach($dom->find("#content .wikitable tr") as $data)
{
    //if($i == 22 || $i == 33)
    //{
    ///print("i: ".$i);
    $tds = $data->find("td");
    if(count($tds) == 0) continue;
    
    $country = $tds[0]->plaintext;
    $city = $tds[1]->plaintext;
    $combinedLocation = $country." ". $city;
    //print("combinedLocation: ".$combinedLocation);
    //$combinedLocation = str_replace(";"," ",$combinedLocation);
    $combinedLocationQuery = preg_replace('/[,;]/i',"",$combinedLocation);    
    $combinedLocationQuery = preg_replace('/[+]/i'," ",$combinedLocationQuery);
    $combinedLocationQuery = preg_replace('/^ | $|  |\r|\n/i',"",$combinedLocationQuery);
    $combinedLocationQuery = str_replace('ü',"u",$combinedLocationQuery);
    $combinedLocationQuery = str_replace('â',"a",$combinedLocationQuery);
    //print("  combinedLocation: ".$combinedLocation);
    $combinedLocationQuery = urlencode($combinedLocationQuery);
    //print("    combinedLocation: ".$combinedLocation);
    $locationName = $tds[2]->plaintext;
    $website = $tds[3]->plaintext;
    $rating = (count($tds) >= 5)? $tds[4]->plaintext : "";
    $contact = (count($tds) >= 6)? $tds[5]->plaintext : "";

    
    /* Google maps
     * - limited to 2,500 requests in a 24 hour period (more details here: http://code.google.com/apis/maps/faq.html#geocoder_limit)
     * TODO: Research using  MapQuest's Nominatim search system (using data from openstreetmaps): http://open.mapquestapi.com/nominatim/ */
    
    $lat = "";
    $lng = "";

    /*$oldFablabData = scraperwiki::select("* from swdata where name='locationName'");*/
    //$oldFablabData = scraperwiki::select("* from swdata");
    $sql = "* from swdata where name='$locationName'";
    print("sql: ".$sql);
    $oldFablabData = scraperwiki::select($sql);
    print_r($oldFablabData);

    if($oldFablabData['location'] != $combinedLocation || $oldFablabData['lat'] == "")
    {
        print("overwrite<br>");
        $geocode_url = 'http://open.mapquestapi.com/nominatim/v1/search?format=json&q=';
        $geoResult = file_get_contents($geocode_url.$combinedLocationQuery);
        $geoJSON = json_decode($geoResult);
        //print("geoJSON: ".$geoJSON." ");
        //print("Count: ".count($geoJSON)." ");
        if(count($geoJSON) > 0)
        {
            $place = $geoJSON[0];
            //print("place: ".$place." ");
            $lat = $place->lat;
            $lng = $place->lon;
            print($i." located ".$locationName." (".$lat." x ".$lng.")");

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

        }
        else
        {
            echo "Can't locate: $locationName ($combinedLocation)";
        }

        
    }

    
    
    
    sleep((1000+rand(0,500))/1000);
    
    $i++;
    //if($i > 3) break;
}
?>
