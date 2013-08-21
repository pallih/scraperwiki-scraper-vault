<?php
# Blank PHP
    $sourcescraper = 'central_scotland_fire_incidents'; 
    //$keys = scraperwiki::getKeys($sourcescraper); 
    //print_r($keys);
    $keyindex = getenv("URLQUERY");
    //print_r($keyindex);
    $all_data = scraperwiki::getData($sourcescraper, $limit=40); 
    //print_r($all_data);

    $location = array();


    foreach ($all_data as $items){

    $location[] = $items->location;

     };
 //print_r($location);
 $counter=0;
 $json_string='';
 while ( $counter < count($location ) ) {
 if (isset($location[$counter]) && $location[$counter] !='' ) {
   $url='http://maps.googleapis.com/maps/api/geocode/json?address='.urlencode($location[$counter]).'&sensor=true' ;
   // print $url;
   $json_string.=' '.file_get_contents($url).' ';
 }
 $counter++;
}
//print_r($json_string);
?>

