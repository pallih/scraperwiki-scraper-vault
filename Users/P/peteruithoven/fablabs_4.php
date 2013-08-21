<?php

$html = scraperWiki::scrape("http://wiki.fablab.is/wiki/Portal:Labs");       
require 'scraperwiki/simple_html_dom.php';  
$dom = new simple_html_dom();
$dom->load($html);
$i = 0;
$notLocated = array();
foreach($dom->find("#content .wikitable tr") as $data)
{
    /*if($i >= 0)
    {
    echo("i: $i \n");*/
    $tds = $data->find("td");
    if(count($tds) == 0) continue;
    
    $country = $tds[1]->plaintext;
    $city = $tds[2]->plaintext;
    $combinedLocation = $country." ". $city;
    //print("combinedLocation: ".$combinedLocation);
    //$combinedLocation = str_replace(";"," ",$combinedLocation);
        
    $combinedLocationQuery = str_replace('+'," ",$combinedLocation);
    $combinedLocationQuery = str_replace('ü',"u",$combinedLocationQuery);
    $combinedLocationQuery = str_replace('â',"a",$combinedLocationQuery);
    
    if(preg_match('/.*?United Kingdom.*?/i',$combinedLocationQuery)){
        /*print("    combinedLocation: ".$combinedLocationQuery);*/
        $combinedLocationQuery = str_replace('United Kingdom',"England",$combinedLocationQuery);
        if (strpos($combinedLocationQuery, 'Doncaster') !== FALSE) {
            $combinedLocationQuery = "Doncaster";
        }
        if (strpos($combinedLocationQuery, 'Scotland') !== FALSE) {
            $combinedLocationQuery = str_replace('Scotland',"",$combinedLocationQuery);
            $combinedLocationQuery = str_replace('England',"Scotland",$combinedLocationQuery);
        }
    }

    if(preg_match('/United States/i',$combinedLocationQuery)){
        /*print("city: ".$city."\n");
        $combinedLocationQuery = preg_replace('/.*?(United States).*?,(.*)/i',"$2",$combinedLocationQuery);
        print("  combinedLocationQuery: ".$combinedLocationQuery."\n");*/
        $combinedLocationQuery = preg_replace('/.*?,(.*)/i',"$1",$city);
    }
    $combinedLocationQuery = preg_replace('/^ | $|  |\r|\n/i',"",$combinedLocationQuery);
    $combinedLocationQuery = preg_replace('/[,;]/i',"",$combinedLocationQuery);    
    $combinedLocationQuery = urlencode($combinedLocationQuery);
    /*print(">    combinedLocation: ".$combinedLocation);*/
    $locationName = $tds[2]->plaintext;
    $website = $tds[3]->plaintext;
    $rating = (count($tds) >= 5)? $tds[4]->plaintext : "";
    $contact = (count($tds) >= 6)? $tds[5]->plaintext : "";
    
    $lat = "";
    $lng = "";
    //echo "$locationName\n";
    switch($locationName)
    {
        case " ProtoSpace ":
            $lat = 52.103105;
            $lng = 5.083709;
            print($i." located ".$locationName." (".$lat." x ".$lng.")\n");
        break;
        case " FabLabTruck (mobile) ":
            $lat = 52.390561;
            $lng = 4.938251;
            print($i." located ".$locationName." (".$lat." x ".$lng.")\n");
            break;
        case " Technistub ":
            $lat = 47.7200873062889;
            $lng = 7.31648040776553;
            print($i." located ".$locationName." (".$lat." x ".$lng.")\n");
        break;
        case " DAD-Workshop ":
        case " Woźna 9c/5 ":
            $lat = 52.408005;
            $lng = 16.936514;
            print($i." located ".$locationName." (".$lat." x ".$lng.")\n");
        break;
        default:
            $geocode_url = 'http://open.mapquestapi.com/nominatim/v1/search?format=json&q=';
            /*print("\n    geocode_url: ".$geocode_url.$combinedLocationQuery);*/
            $geoResult = file_get_contents($geocode_url.$combinedLocationQuery);
            $geoJSON = json_decode($geoResult);
            if(count($geoJSON) > 0)
            {
                $place = $geoJSON[0];
                /*print("\nplace: \n");
                  print_r($place);*/
                $lat = $place->lat;
                $lng = $place->lon;
                /*print($i." located ".$locationName." (".$lat." x ".$lng.")\n");*/
            }
            else
            {
                echo "Can't locate: $locationName ($combinedLocation) ($combinedLocationQuery)\n";
                $notLocated[] = "$locationName ($combinedLocation) ($combinedLocationQuery)";
            }
        break;
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

    scraperwiki::save(array('name','location'), $fablab);
    
    sleep((1000+rand(0,5000))/1000);

    $i++;
    //if($i > 3) break;
}
print("Can't locate:\n");
$notLocatedString = implode("\n",$notLocated);
print($notLocatedString);
?>
