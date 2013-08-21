<?php
//Takes a file from my web server and puts it into a database. Yaaay!

if (!file_exists('phpcoord-2.3.php')){ //first need to download phpCoord
        $data2 = file_get_contents("http://www.jstott.me.uk/phpcoord/phpcoord-2.3.tar.gz");
        file_put_contents("phpcoord-2.3.tar.gz", $data2);
        exec('tar -xzvf phpcoord-2.3.tar.gz');

    //exec('wget -O phpcoord-2.3.php "http://dev.aendrew.com/phpcoord.phps"');
}
require_once('phpcoord-2.3.php');

$row = 0;
$row2 = 0;
$csv = array();
$routes = array();

if (($handle = fopen('http://dev.aendrew.com/busgobbler.php', 'r')) !== FALSE) { //if you want busgobbler's source, visit http://dev.aendrew.com/busgobbler.phps
    while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
        if (($row > 0) && !empty($data[0])) { //ignore header row
           $csv[$row - 1]['row'] = $row;
           $csv[$row - 1]['route'] = $data[0];
           $csv[$row - 1]['run'] = $data[1];
           $csv[$row - 1]['sequence'] = $data[2];
           $csv[$row - 1]['stop_code_lbsl'] = $data[3];
           $csv[$row - 1]['bus_stop_code'] = $data[4];
           $csv[$row - 1]['naptan_atco'] = $data[5];
           $csv[$row - 1]['stop_name'] = $data[6];
           $csv[$row - 1]['location_easting'] = $data[7];
           $csv[$row - 1]['location_northing'] = $data[8];
           $csv[$row - 1]['heading'] = $data[9];
           $csv[$row - 1]['virtual_bus_stop'] = $data[10];

           $os1 = new OSRef($csv[$row - 1]['location_easting'], $csv[$row - 1]['location_northing']); //here's where we use phpCoord from above. I hate eastings/northings...
           $latlng = $os1->toLatLng();
           $latlng->OSGB36ToWGS84();

           $csv[$row - 1]['latitude'] = @$latlng->lat;
           $csv[$row - 1]['longitude'] = @$latlng->lng;
        }
        $row++;
    }
    fclose($handle);
}

//print_r($routes);
 
scraperwiki::save_sqlite(array('row'), $csv, $table_name="tfl_buses"); 
//scraperwiki::save_sqlite(array('route'), $routes, "tfl_routes"); 
//not bad for <44 lines, eh?

?>
