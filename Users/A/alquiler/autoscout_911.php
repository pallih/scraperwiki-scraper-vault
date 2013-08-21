<?php
$debug = false;
require 'scraperwiki/simple_html_dom.php';
$page_counter = 0;
//$cars_parsed = 0;
$cars_saved = 0;
//scraperwiki::sqliteexecute("update swdata set photo = 'http://s.autoscout24.net/Images/_cache/8c42d7111b648958.gif' where photo = ''");
//scraperwiki::sqliteexecute("update swdata set gearbox = 'manual' where gearbox = ''");
//scraperwiki::sqlitecommit(); 
//scraperwiki::sqliteexecute("drop table if exists '0'"); // empty table
//    $now = time();
//$sql = "update swdata set deleted = '1' where lastseen <> {$now}";
//print $sql;
//exit;
$start = time();
do { // loop through pages
    $page_counter++;
    $pageurl = "http://www.autoscout24.es/ListGN.aspx?vis=1&state=A&atype=C&make=74&model=2084&fuel=D&kmto=500000&fregfrom=2010&pricefrom=1000&cy=E&page={$page_counter}&results=20&desc=True&ustate=N,U&sort=pubstart&mmvco=1&mmvmk0=74&mmvmd0=2084";
$pageurl = "http://www.autoscout24.es/ListGN.aspx?page={$page_counter}&atype=C&make=57&mmvco=1&model=-70&mmvmk0=57&mmvmd0=-70&pricefrom=1000&priceto=60000&fregfrom=2004&fregto=2009&cy=E&ustate=N%2CU";
$pageurl = "http://www.autoscout24.es/ListGN.aspx?page={$page_counter}&atype=C&make=57&mmvco=1&model=-70&mmvmk0=57&mmvmd0=-70&cy=E&ustate=N%2CU";
    $html_data = scraperwiki::scrape($pageurl);

    if (preg_match('#<li class="next" onclick="location\.href=&\#39;(.+?)&\#39;">#',$html_data, $next_page)) {
        $next_page = $next_page[1];
    }
//unset($next_page); // uncomment to scan first page only

    if (preg_match_all('#cars\[.+?\]=new Car\((.+?)\);#',$html_data, $cars)) {
        $cars = $cars[1];
    }
    foreach ($cars as &$car) { # iterate through cars
//        $cars_parsed++;
        $car = str_replace(",-", "", $car); # remove ",-" from price
        $car = str_replace("€ ", "", $car); # remove "€ " from price
        $car = str_replace("false", "''", $car); # remove false from strings
        $car = str_replace("true", "''", $car); # remove true from strings
        $car = explode("','",$car); # break into single items
        //if (strpos(strtolower($car[11]),"var.") > 0 ) continue; //skip variant
        //if (strpos(strtolower($car[11]),"variant") > 0 ) continue; //skip variant
        //if (strpos(strtolower($car[11]),"cabrio") > 0 ) continue; //skip cabrio
        //if (strpos(strtolower($car[11]),"plus") > 0 ) continue; //skip plus
        //if (strpos(strtolower($car[11]),"sport") == 0 ) continue; //skip all except sport
        //if ($car[22] != "Diésel") continue; //skip non Diesels
//        $car[4] = str_replace(".", "", $car[4]); //remove decimal point from price
//        $car[7] = str_replace(".", "", $car[7]); //remove decimal point from mileage
        if ($car[41] == "") $car[41] = 'http://wiki.artisansasylum.com/images/thumb/7/7d/No_image.jpeg/250px-No_image.jpeg'; //place photo for blank         
        if ($car[8] == "-/-") $car[8] = substr($car[39], 6, 2) . "/" . substr($car[39], 9, 4); //cars with no age info default to ad date
        if ($car[25] == "") $car[25] = "manual"; //cars with no gearbox info default to manual
//        $createdtimestamp = mktime(0, 0, 0, substr($car[39], 6, 2), substr($car[39], 3, 2), substr($car[39], 9, 4));
//        $month = substr($car[8], 0, 2);
//        $year = substr($car[8], -4);
//        print "[{$car[24]}] {$car[11]} {$car[4]}€ {$car[7]}km\n";
//        print "[{$car[8]}] [{$car[39]}]\n";
//        print_r ($car); // print parsed car
//        exit; // exit without saving
    
        if (!$debug) {
            scraperwiki::save_sqlite(   // and save to database
                array('id'),
                array(
                    'id' => $car[24],
                    'url' => $car[2],
                    'price' => str_replace(".", "", $car[4]) + 0,
                    'mileage' => str_replace(".", "", $car[7]) + 0,
                    'month' => substr($car[8], 0, 2),
                    'year' => substr($car[8], -4),
                    'kw' => $car[9] + 0,
                    'cv' => $car[10] + 0 ,
                    'description' => ucwords(strtolower($car[11])),
                    'zip' => $car[15],
                    'city' => ucwords(strtolower($car[16])),
                    'color' => ucwords(strtolower($car[19])),
                    'fuel' => ucwords(strtolower($car[22])),
                    'photo' => $car[41],
                    'gearbox' => ucwords(strtolower($car[25])),
                    'created' => $car[39],
                    'createdtimestamp' => mktime(substr($car[39], 15, 2), substr($car[39], 18, 2), 0, substr($car[39], 6, 2), substr($car[39], 3, 2), substr($car[39], 9, 4)),
                    'lastseen' => $start,
                    'deleted' => '0'
    
                ), //end array
                $table_name="swdata",
                $verbose=0
            ); //end save_sqlite
//            print "{$car[24]} saved!\n";
            $cars_saved++;
        }
    }
    print "[{$page_counter}] {$cars_saved}\n";
//    print_r ($cars[0]);
//    print_r ($cars);
if ($debug) exit; //only one iteration
} while (!empty($next_page));
$sql = "update swdata set deleted = '1' where lastseen <> {$start}";
scraperwiki::sqliteexecute($sql);
scraperwiki::sqlitecommit(); 
//print "parsed pages: {$page_counter}  \nparsed cars: {$cars_parsed}  \nsaved cars: {$cars_saved}";
print "parsed pages: {$page_counter}  \nsaved cars: {$cars_saved}";
?>
