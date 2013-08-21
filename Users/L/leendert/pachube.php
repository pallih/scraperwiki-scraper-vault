<?php

header('Content-type: application/json');
header('Content-Disposition: attachment; filename="abwl.json"');

if ($_GET) {
  $stationID = $_GET['stationID'];
}
if (!$stationID) {
  // default to North Saskatchewan rivel level at Edmonton
  $stationID = 'RNSASEDM';
}


$sourcescraper = 'north_saskatchewan_river_level_at_edmonton';
scraperwiki::attach($sourcescraper);

$meta = scraperwiki::select("* from {$sourcescraper}.abwl_meta WHERE stationID=\"{$stationID}\"");

$levels = scraperwiki::select("* from {$sourcescraper}.{$stationID} order by Date desc, Time desc");

 
$abwl_pachube['title'] = $meta[0]['location'];
$abwl_pachube['description'] = "Selected river water levels and flows from Alberta river basins. Data scraped from Alberta Environment. Note that this project is not affiliated with Alberta Environment. Currently selection station: {$stationID}";
$abwl_pachube['feed'] = $meta[0]['feed'];
$abwl_pachube['website'] = $meta[0]['website'];
$abwl_pachube['version'] = "1.0.0";
$abwl_pachube['updated'] = $meta[0]['lastDate'] . 'T' . $meta[0]['lastTime'] . '-7:00';
$abwl_pachube['location']['name'] = $meta[0]['location'];
$abwl_pachube['location']['lat'] = $meta[0]['lat'];
$abwl_pachube['location']['lon'] = $meta[0]['lon'];
$abwl_pachube['location']['disposition'] = 'fixed';
$abwl_pachube['location']['exposure'] = 'outdoor';
$abwl_pachube['location']['domain'] = 'physical';

$abwl_pachube['tags'] = array('Alberta','river','basin','water','flow rate','level',$stationID);

foreach ($levels as $key => $value) {
    $abwl_flows[$key] = array('at' => $levels[$key]['Date'] . 'T' . $levels[$key]['Time'] . '-7:00', 'value' => $levels[$key]['Flow']);
    $abwl_levels[$key] = array('at' => $levels[$key]['Date'] . 'T' . $levels[$key]['Time'] . '-7:00', 'value' => $levels[$key]['Level']);
}
$latestTime = $levels[0]['Date'] . 'T' . $levels[0]['Time'] . '-7:00';
$latestFlow = $levels[0]['Flow'];
$latestLevel = $levels[0]['Level'];
$abwl_pachube['datastreams'][0] = array('id' => "{$stationID}_flow", 'tags' => array('flow rate'), 'current_value' => $latestFlow, 'unit' => array('type' => 'derivedSI', 'label' => 'Cubic metres per second', 'symbol' => 'm^3/s'), 'datapoints' => $abwl_flows);
$abwl_pachube['datastreams'][1] = array('id' => "{$stationID}_level", 'tags' => array('level'),'current_value' => $latestLevel, 'unit' => array('type' => 'basicSI', 'label' => 'Metres', 'symbol' => 'm'), 'datapoints' => $abwl_levels);

print json_encode($abwl_pachube);

?>
