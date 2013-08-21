<?php
/* NOTE: Crawlers are automatically sent to the mobile site, so use that for figuring out scrapers.
Also will only grab todays routes, so if running on the weekend it won't grab service numbers for weekday services (mainly just the P routes)

*/
require 'scraperwiki/simple_html_dom.php';     
 
#debug mode, turn on (=1) to just scrape the first 2 routes, trips and stops
$debug =0;      

# URLS
$bus_route_url = "http://mobile.jp.translink.com.au/travel-information/network-information/buses/all-timetables";

//$route_url + bus code
$route_url = "http://mobile.jp.translink.com.au/travel-information/network-information/buses/";   

//$trip_url + direction / timetable_code / trip_code
$trip_url = "http://mobile.jp.translink.com.au/travel-information/network-information/service-information/";

//$stop_url + stop_id
$stop_url = "http://mobile.jp.translink.com.au/travel-information/network-information/stops-and-stations/stop/";


# Tables
scraperwiki::sqliteexecute("CREATE TABLE IF NOT EXISTS 'routes' ('route' text UNIQUE ON CONFLICT REPLACE, 'routeName' text, 'status' text)"); 

scraperwiki::sqliteexecute("CREATE TABLE IF NOT EXISTS 'services' ('trip_code' integer UNIQUE ON CONFLICT REPLACE, 'route' text, 'direction' text, 'timetable_code' text, 'start' text, 'end' text)");  

 scraperwiki::sqliteexecute("CREATE TABLE IF NOT EXISTS 'timetable' ('timetable_code' integer UNIQUE ON CONFLICT REPLACE, 'day' text)");  

scraperwiki::sqliteexecute("CREATE TABLE IF NOT EXISTS 'trip' ('trip_code' integer, 'direction' text, 'timetable_code' text, 'stop_id' text, 'time' text)");  

scraperwiki::sqliteexecute("CREATE TABLE IF NOT EXISTS 'stop' ('stop_id' integer UNIQUE ON CONFLICT REPLACE, 'name' text, 'desc' text, 'zone' text, 'lat' text, 'long' text)");  


$html = scraperWiki::scrape($bus_route_url);           

//Grab all available bus routes
$dom = new simple_html_dom();
$dom->load($html);
$records = array();
foreach($dom->find("table.content-table tr") as $data){

    $tds = $data->find("td");
    if(count($tds) ==0){
      continue;
    }
    $route = array(
            'route' => $tds[0]->plaintext, 
            'routeName' => $tds[1]->plaintext,
            'status' => 'scraping'
        );
    $result = scraperwiki::sqliteexecute("select * from routes where route ='".$route['route']."'"); 
    if(isset( $result->data[0][2]) && $result->data[0][2] == 'complete'){ 
     //already scraped
}else{

    $routes[] = $route;
}

}
 scraperwiki::save_sqlite(array('route'), $routes, "routes", 0);  

#Fetch trips along a route



if($debug ==1){
  $recTemp[] = $routes[0];
  $recTemp[] = $routes[1];
  $routes = $recTemp;
}

foreach($routes as $route){

  getTrips($route);
  $route['status'] = 'complete';
  scraperwiki::save_sqlite(array('route'), $route, "routes", 0);   

}


function getTrips($route){  
   
   //check if route exists and is complete
   $route_id = $route['route'];
  
   global $trips, $route_url, $debug;
   $route_url_full = $route_url . $route['route'];

   $html = scraperWiki::scrape($route_url_full);
    $dom = new simple_html_dom();
    $dom->load($html);  
    $directions = array('Inbound', 'Outbound');

    foreach($directions as $direction){

   foreach($dom->find('table.'.$direction.' tbody tr') as $timetable){
     $tds = $timetable->find('td');

    if(count($tds)==0){
        continue;

    }
    $start = $timetable->find('td > b');

    $start_time = $start[0]->plaintext; 
    $end_time = $start[1]->plaintext;

    /*  Timetable codes, buses seem to have the same code for services M-F, then different ones for both Saturday & Sunday (& public holidays maybe?)*/
    $link = $timetable->find('td a'); 
    $link_chunks = explode("/", $link[0]->href);

    $timetable_code = $link_chunks[5];
    $trip_code = $link_chunks[6];

    $trip_record = array(
        'route' => $route['route'],
        'trip_code' => $trip_code,
        'direction' => $direction,
        'timetable_code' => $timetable_code,
        'start' => $start_time,
        'end' => $end_time
        
    );
    $trips[] = $trip_record;

   }
}          
 scraperwiki::save_sqlite(array('trip_code'), $trips, "services", 0);    
  

  if($debug ==1){
    $tripsTemp[] = $trips[0];
    $tripsTemp[] = $trips[1];
    $trips = $tripsTemp;
  }



  foreach($trips as $trip){
    getTripTimes($trip['trip_code'], $trip['timetable_code'], $trip['direction']);
    $trip['status'] = 'complete';
    scraperwiki::save_sqlite(array('trip_code'), $trip, "services", 0);     
  } 

}




function getTripTimes($trip_code, $timetable_code, $direction){
  $result = scraperwiki::sqliteexecute("select * from trip where trip_code ='".$trip_code."' AND timetable_code ='".$timetable_code."' AND direction = '".$direction."'");

  if(isset( $result->data[0][1]) && $result->data[0][1] != '') {
   //stop already in database, no need to parse
   return;
  }else{ 
  global $trip_url;
  $full_trip_url = $trip_url .$direction .'/'.$timetable_code.'/'. $trip_code;

  $html = scraperWiki::scrape($full_trip_url);
  $dom = new simple_html_dom();
  $dom->load($html);   
  //#trip-details
  foreach($dom->find('table#trip-details tbody tr') as $stop){
     $tds = $stop->find('td.indented');

    if(count($tds)==0){
        continue;

    } 
    //get stop ID 
    $stop_link = $stop->find('td a');
    $link_chunks = explode("/", $stop_link[0]->href); 
    $stop_id = $link_chunks[5]; 

  //get time
    $time = $tds[0]->plaintext;
 // 'trip_code' integer, 'direction' text, 'timetable_code' text, 'stop_id' text, 'time' text 
  //save 
   $trip_stops = array(
     'trip_code' => $trip_code,
     'timetable_code' => $timetable_code,
     'direction' => $direction,
     'stop_id' => $stop_id,
     'time' => $time
   );
   getStopInfo($stop_id);

   $day = date('D');
   $timetable = array(
     'timetable_code' =>$timetable_code,
     'day' => $day
   );

   scraperwiki::save_sqlite(array('timetable_code'), $timetable, "timetable", 0); 
   scraperwiki::save_sqlite(array('trip_code','direction', 'timetable_code', 'stop_id', 'time'), $trip_stops, "trip", 0);    



  }

  }
}

function getStopInfo($stop_id) {
  $result = scraperwiki::sqliteexecute("select * from stop where stop_id ='".$stop_id."'");

  if(isset( $result->data[0][3]) && $result->data[0][3] != '') {
   //stop already in database, no need to parse

  }else{
  global $stop_url;
  $full_stop_url = $stop_url .$stop_id;

  $html = scraperWiki::scrape($full_stop_url);
  $dom = new simple_html_dom();
  $dom->load($html);    
  $title = $dom->find('title');
  if(stripos($title[0]->plaintext, 'not found')){
   //404 log and carry on
   return;
  }

  $name_dom = $dom->find('h1');
  $name = $name_dom[0]->plaintext; 
  
  $zone_dom = $dom->find('table.header-column td');
  $zone = $zone_dom[0]->plaintext;
  $desc = $zone_dom[1]->plaintext; 

  $map_dom = $dom->find('a#map-link');
  $map_link = $map_dom[0]->href;
  // OLD FORMAT
  // http://maps.google.com/maps/api/staticmap?size=320x250&amp;sensor=false&amp;markers=color:red|label:A|-27.925015,153.338751&amp; 
  //New form, seems someone at Translink buggered the encoding.
  //http://maps.google.com/maps/api/staticmap?size=320x250&sensor=false&markers=color:red%7Clabel:A%7C-27.464013,153.029148&&client=gme-translinktransit&signature=5_hQHrTJhHBlK8Aur1LLoNBNkIk=
 /* For old format, uncomment if encoding gets fixed  
  $latlon =  substr( $map_link, strrpos ($map_link , '|')+1, -5); 
 
 */
  //new format
 // print 'mapLink: '. $map_link;
  $map_start =  strrpos($map_link, '%7C')+3;
  $map_end =   strlen($map_link) - strrpos($map_link, '&amp;&amp;')  ;
  //print 'map start: '.$map_start. ', map end: '.$map_end;
  $latlon = substr($map_link, $map_start, $map_end * -1);
  //print 'latlong:'. $latlon;
  $latlon_ar = preg_split("/,/", $latlon); 
  
  $lat = $latlon_ar[0];
  $long = $latlon_ar[1];
  
  $stop = array(
    'stop_id' => $stop_id,
    'name' => $name,
    'desc' => $desc,
    'zone' => $zone,
    'lat' => $lat,
    'long' => $long
  ); 
 
  scraperwiki::save_sqlite(array('stop_id'), $stop, "stop", 0);     
  }

}


?>
