<?php

//geocode sk towns using google api
//limit 2000 a day )-:
//using our server as well

$last_postcode = scraperwiki::get_var('last_postcode','00000');

//read the towns
scraperwiki::attach("sk_towns", "src");
$towns = scraperwiki::select('* from src.swdata where "Post code">='.$last_postcode.' order by "Post code"');

  $region = 'sk';
  $language = 'sk';

foreach ($towns as $town) {

  $urls = array( 
    "http://maps.googleapis.com/maps/api/geocode/json?region={$region}&language={$language}&sensor=false&address=" . urlencode($town['Name'] . ',' .$town['Post code']),
    "http://test.kohovolit.sk/geo/geocode_service.php?region=region={$region}&language={$language}&address=" . urlencode($town['Name'] . ',' .$town['Post code']),
    "http://kohovolit.eu/michal/geocode_service.php?region=region={$region}&language={$language}&address=" . urlencode($town['Name'] . ',' .$town['Post code']),
  );
  foreach ($urls as $url) {
    $geocoded = json_decode(scraperwiki::scrape($url));
    if ($geocoded->status == 'OK') break;
  }
  if ($geocoded->status == 'OK') {
    $out = array(
      'id' => $town['Id'],
       'name' => $town['Name']
    );

    foreach ($geocoded->results[0]->address_components as $component) {
//print_r($component);die();
      $out[$component->types[0] . '-long_name'] = $component->long_name;
      $out[$component->types[0] . '-short_name'] = $component->short_name;
    }
    $out['lat'] = $geocoded->results[0]->geometry->location->lat;
    $out['lng'] = $geocoded->results[0]->geometry->location->lng;
    $out['formatted_address'] = $geocoded->results[0]->formatted_address;

    scraperwiki::save_sqlite(array('id'),$out);
    scraperwiki::save_var('last_postcode',$town['Post code']);
  } else {
    
  }

  //print_r($out);die(); 
}

scraperwiki::save_var('last_postcode','00000');


?>
<?php

//geocode sk towns using google api
//limit 2000 a day )-:
//using our server as well

$last_postcode = scraperwiki::get_var('last_postcode','00000');

//read the towns
scraperwiki::attach("sk_towns", "src");
$towns = scraperwiki::select('* from src.swdata where "Post code">='.$last_postcode.' order by "Post code"');

  $region = 'sk';
  $language = 'sk';

foreach ($towns as $town) {

  $urls = array( 
    "http://maps.googleapis.com/maps/api/geocode/json?region={$region}&language={$language}&sensor=false&address=" . urlencode($town['Name'] . ',' .$town['Post code']),
    "http://test.kohovolit.sk/geo/geocode_service.php?region=region={$region}&language={$language}&address=" . urlencode($town['Name'] . ',' .$town['Post code']),
    "http://kohovolit.eu/michal/geocode_service.php?region=region={$region}&language={$language}&address=" . urlencode($town['Name'] . ',' .$town['Post code']),
  );
  foreach ($urls as $url) {
    $geocoded = json_decode(scraperwiki::scrape($url));
    if ($geocoded->status == 'OK') break;
  }
  if ($geocoded->status == 'OK') {
    $out = array(
      'id' => $town['Id'],
       'name' => $town['Name']
    );

    foreach ($geocoded->results[0]->address_components as $component) {
//print_r($component);die();
      $out[$component->types[0] . '-long_name'] = $component->long_name;
      $out[$component->types[0] . '-short_name'] = $component->short_name;
    }
    $out['lat'] = $geocoded->results[0]->geometry->location->lat;
    $out['lng'] = $geocoded->results[0]->geometry->location->lng;
    $out['formatted_address'] = $geocoded->results[0]->formatted_address;

    scraperwiki::save_sqlite(array('id'),$out);
    scraperwiki::save_var('last_postcode',$town['Post code']);
  } else {
    
  }

  //print_r($out);die(); 
}

scraperwiki::save_var('last_postcode','00000');


?>
