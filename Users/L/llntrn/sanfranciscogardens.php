<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';
$html = scraperwiki::scrape("http://www.sfgro.org/sfgardens.php");

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);

echo $dom->html;

$pages_to_scrape = array();

$entry = array();
$records = array();
foreach($dom->find('div[class=Text] tr td') as $entry){
    $records = explode('<br><br>',$entry);

    foreach($records as $row){
        $row_arr = explode('<br>',$row,3);

        $row_arr_stripped['garden_name'] = trim(strip_tags($row_arr[0]));
        $row_arr_stripped['garden_addr'] = trim(strip_tags($row_arr[1]));
        $row_arr_stripped['garden_comments'] = $row_arr[2];
        $row_arr_stripped['lat'] = NULL;
        $row_arr_stripped['lng'] = NULL;

        print $row_arr_stripped['garden_name'];
        if($row_arr_stripped['garden_name']!=""){

        
            print_r($row_arr_stripped);



            $addy = $row_arr_stripped['garden_addr'];
            if(strpos($addy, 'b/t') !== false) {
                $addy_parts = explode('&',$addy);
                $addy = trim(str_replace('b/t','and', $addy_parts[0]));
            }
            $geocode_url = 'http://maps.googleapis.com/maps/api/geocode/json?address='.urlencode($addy).',+San+Francisco,+CA&sensor=false&output=json';

/*
    $geocode_url = 'http://tasks.arcgisonline.com/ArcGIS/rest/services/Locators/TA_Streets_US_10/GeocodeServer/findAddressCandidates?Single+Line+Input='.urlencode($addy).'+San+Francisco,+CA&outFields=&outSR=&f=json';
print $geocode_url;

            $geodata = file_get_contents($geocode_url);

            // Parse the returned json
           */
/* $geo_json = json_decode($geodata);
           print_r($geo_json);
*/

/*
if len(geocode['candidates']):
    data_lat = geocode['candidates'][0]['location']['y']
    data_lng = geocode['candidates'][0]['location']['x']

print data_lat
print data_lng
*/


           print $geocode_url."\n";

            // Retrieve the URL contents
           $geodata = file_get_contents($geocode_url);

          // Parse the returned json
            $geo_json = json_decode($geodata);
           print_r($geo_json);
            if($geo_json->status == 'OK'){
                $row_arr_stripped['lat'] = $geo_json->results[0]->geometry->location->lat;
                $row_arr_stripped['lng'] = $geo_json->results[0]->geometry->location->lng;
            }
 
            scraperwiki::save(array('garden_name'), $row_arr_stripped);
        }
    }
}
?>
