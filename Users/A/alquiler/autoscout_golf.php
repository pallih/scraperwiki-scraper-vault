<?php
require 'scraperwiki/simple_html_dom.php';
$page_counter = 0;
$cars_parsed = 0;
$cars_saved = 0;
do { // loop through pages
    $page_counter++;
    $pageurl = "http://www.autoscout24.es/ListGN.aspx?vis=1&state=A&atype=C&make=74&model=2084&fuel=D&kmto=500000&fregfrom=2010&pricefrom=1000&cy=E&page={$page_counter}&results=20&desc=True&ustate=N,U&sort=pubstart&mmvco=1&mmvmk0=74&mmvmd0=2084";
//    $pageurl = "http://www.autoscout24.es/ListGN.aspx?vis=1&state=A&atype=C&make=74&model=2084&fuel=D&kmto=500000&fregfrom=2010&pricefrom=1000&cy=E&page=200&results=20&desc=True&ustate=N,U&sort=pubstart&mmvco=1&mmvmk0=74&mmvmd0=2084";
    $html_data = scraperwiki::scrape($pageurl);

    if (preg_match('#<li class="next" onclick="location\.href=&\#39;(.+?)&\#39;">#',$html_data, $next_page)) {
        $next_page = $next_page[1];
    }

    if (preg_match_all('#cars\[.+?\]=new Car\((.+?)\);#',$html_data, $cars)) {
        $cars = $cars[1];
    }
    foreach ($cars as &$car) { # iterate through cars
        $cars_parsed++;
        $car = str_replace(",-", "", $car); # remove ",-" from price
        $car = str_replace("€ ", "", $car); # remove "€ " from price
        $car = str_replace("false", "''", $car); # remove false from strings
        $car = str_replace("true", "''", $car); # remove true from strings
        $car = explode("','",$car); # break into single items
        if (strpos(strtolower($car[11]),"var.") > 0 ) continue; //skip variant
        if (strpos(strtolower($car[11]),"variant") > 0 ) continue; //skip variant
        if (strpos(strtolower($car[11]),"cabrio") > 0 ) continue; //skip cabrio
        if (strpos(strtolower($car[11]),"plus") > 0 ) continue; //skip plus
        //if (strpos(strtolower($car[11]),"sport") == 0 ) continue; //skip all except sport
        if ($car[22] != "Diésel") continue; //skip non Diesels
        $cars_saved++;
        $car[4] = str_replace(".", "", $car[4]);
        $car[7] = str_replace(".", "", $car[7]);
        print "[{$car[24]}] {$car[11]} {$car[4]}€ {$car[7]}km\n";
    
    
        scraperwiki::save(   // and save to database
            array('id'),
            array(
                'id' => $car[24],
                'url' => $car[2],
                'price' => $car[4] + 0,
                'mileage' => $car[7] + 0,
                'year' => $car[8],
                'kw' => $car[9] + 0,
                'cv' => $car[10] + 0 ,
                'description' => $car[11],
                'zip' => $car[15],
                'city' => $car[16],
                'color' => $car[19],
                'fuel' => $car[22],
                'created' => $car[40],
                'type' => $car[41],
                'photo' => $car[42],
                'gearbox' => $car[25]
            ) //endarray
        ); //endsave
    
    }
    #print_r ($cars[0]);
    #print_r ($cars);
//} while (isset($more_pages));
} while (!empty($next_page));
print "parsed pages: {$page_counter}\nparsed cars: {$cars_parsed}\nsaved cars: {$cars_saved}"
?>
