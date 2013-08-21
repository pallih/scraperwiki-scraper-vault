<?php

$regions = array(
   0 => array(
                    'id' => 11812,
                     'label' => 'North East',
                     'pop' => '2.6',
                     'geo' => ''
                   ),
   1 => array(
                     'id' => 11807,
                     'label' => 'North West',
                     'pop' => '7.1',
                     'geo' =>  ''
                   ),
   2 => array(
                     'id' => 11810,
                     'label' => 'Yorkshire and the Humber',
                     'pop' => '5.3',
                     'geo' =>  ''
                   ),
   3 => array(
                        'id' => 11805,
                        'label' => 'East Midlands',
                        'pop' => '4.5',
                        'geo' =>  ''
                    ),
   4 => array(
                        'id' => 11809,
                        'label' => 'West Midlands',
                        'pop' => '5.6',
                        'geo' =>  ''
                    ),
   5 => array(
                        'id' => 11804,
                        'label' => 'Eastern England',
                        'pop' => '5.8',
                        'geo' =>  ''
                    ),
   6 => array(
                        'id' => 11806,
                        'label' => 'London',
                        'pop' => '8.2',
                        'geo' =>  ''
                    ),
   7 => array(
                        'id' => 11811,
                        'label' => 'South East',
                        'pop' => '8.6',
                        'geo' =>  ''
                    ),
   8 => array(
                        'id' => 11814,
                        'label' => 'South West',
                        'pop' => '5.3',
                        'geo' =>  ''
                    ),
   9 => array(
                        'id' => 11813,
                        'label' => 'Wales',
                        'pop' => '3.1',
                        'geo' =>  ''
                    )
);

//Get GeoJSON of regions

foreach ($regions as $key => $region) {
    $regions[$key]['geo'] = serialize(json_decode(file_get_contents('http://mapit.mysociety.org/area/' . $region['id'] . '.geojson')));
}

//print_r($var);
scraperwiki::save_sqlite(array("id"), $regions);


?>
