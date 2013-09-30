<?php

# Blank PHP

$csv = file_get_contents("http://map.personaltelco.net/csv.php");           
$rows = explode("\n", trim($csv));

$row_count = count($rows);
for ($i=1; $i<$row_count; $i++) {
//    echo $rows[$i];
    $data = explode(";", trim($rows[$i]));
    $record = array(
        'location_name' => $data[0], 
        'name' => $data[1],
        'address' => $data[2],
        'latitude' => $data[3],
        'longitude' => $data[4]
    );

/*
$csv = file_get_contents('https://nycopendata.socrata.com/api/views/ehc4-fktp/rows.json?accessType=DOWNLOAD');
$again=json_decode($csv);
$againagain = $again->data;
$itemcount=count($againagain);
for ($i=0;$i<$itemcount;$i++) {
    if ($againagain[$i][16] == "Free") {
        $record['location_name'] = $againagain[$i][10]+$againagain[$i][12];
        $record['name'] = $againagain[$i][10];
        $record['street_address'] = $againagain[$i][12];
        $record['latitude'] = $againagain[$i][9][5]->point[0];
        $record['longitude'] = $againagain[$i][9][5]->point[1];
        $record['city'] = $againagain[$i][13];
        $record['zip'] = $againagain[$i][14];
    }
}
*/

scraperwiki::save(array('location_name'), $record); 
}
?>
<?php

# Blank PHP

$csv = file_get_contents("http://map.personaltelco.net/csv.php");           
$rows = explode("\n", trim($csv));

$row_count = count($rows);
for ($i=1; $i<$row_count; $i++) {
//    echo $rows[$i];
    $data = explode(";", trim($rows[$i]));
    $record = array(
        'location_name' => $data[0], 
        'name' => $data[1],
        'address' => $data[2],
        'latitude' => $data[3],
        'longitude' => $data[4]
    );

/*
$csv = file_get_contents('https://nycopendata.socrata.com/api/views/ehc4-fktp/rows.json?accessType=DOWNLOAD');
$again=json_decode($csv);
$againagain = $again->data;
$itemcount=count($againagain);
for ($i=0;$i<$itemcount;$i++) {
    if ($againagain[$i][16] == "Free") {
        $record['location_name'] = $againagain[$i][10]+$againagain[$i][12];
        $record['name'] = $againagain[$i][10];
        $record['street_address'] = $againagain[$i][12];
        $record['latitude'] = $againagain[$i][9][5]->point[0];
        $record['longitude'] = $againagain[$i][9][5]->point[1];
        $record['city'] = $againagain[$i][13];
        $record['zip'] = $againagain[$i][14];
    }
}
*/

scraperwiki::save(array('location_name'), $record); 
}
?>
