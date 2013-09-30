<?php

//Whoops, seems that doing 600 queries in under 80 seconds isn't a smart idea. This scraper attempts to aggregate coordinates into something usable.


scraperwiki::attach("tfl_bus_routes_scraper", "src");

$routes = scraperwiki::select( "route, stop_name, latitude, longitude from src.tfl_buses where run = 1 order by sequence asc" );

$routemap = array();


foreach ($routes as $route) {
    $routemap[$route['route']]['route'] = $route['route'];
    @$routemap[$route['route']]['coords'] .= $route['latitude'] . ',' . $route['longitude'] . ',2357' . "\n";
}


$theroutes = array();

$count = 0;
foreach ($routemap as $a_route) {
    $count++;
    $r = $a_route['route'];
    $c = $a_route['coords'];

    $theroutes[] = array(
        'id' => $count,
        'route' => $r,
        'coords' => $c
    );
}

scraperwiki::save_sqlite(array("id"), $theroutes); 

?>
<?php

//Whoops, seems that doing 600 queries in under 80 seconds isn't a smart idea. This scraper attempts to aggregate coordinates into something usable.


scraperwiki::attach("tfl_bus_routes_scraper", "src");

$routes = scraperwiki::select( "route, stop_name, latitude, longitude from src.tfl_buses where run = 1 order by sequence asc" );

$routemap = array();


foreach ($routes as $route) {
    $routemap[$route['route']]['route'] = $route['route'];
    @$routemap[$route['route']]['coords'] .= $route['latitude'] . ',' . $route['longitude'] . ',2357' . "\n";
}


$theroutes = array();

$count = 0;
foreach ($routemap as $a_route) {
    $count++;
    $r = $a_route['route'];
    $c = $a_route['coords'];

    $theroutes[] = array(
        'id' => $count,
        'route' => $r,
        'coords' => $c
    );
}

scraperwiki::save_sqlite(array("id"), $theroutes); 

?>
