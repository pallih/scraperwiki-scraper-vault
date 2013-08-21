<?php
######################################
# Scrape and geocode all of the houses listed on Philadelphia Sheriff's website
######################################

$html = scraperwiki::scrape("http://www.phillysheriff.com/properties.html");
//print $html;

// The only form of organization on this page is to divide records by <hr /> tags
$hrs = explode('<hr />',$html);

$title_block = array_shift($hrs);

// Throttling limit on test runs
$test_limit = 10;
$test_count = 0;
$testing = false;

foreach($hrs as $hr) {
    $test_count++;    
    if($testing && $test_count > $test_limit) break;
    
    $data = array();

    $brs = explode('<br>',$hr);
    //print_r($brs);
    $split_on_spaces = explode('&nbsp;   &nbsp;',$brs[0]);
    $id_street = trim($split_on_spaces[0]);
    $x = explode('</center>',$id_street);
    // Strip out the ID
    $data['id'] = trim(strip_tags($x[0]));

    // Get the property address and geocode it
    $data['street'] = (isset($x[1])) ? trim(strip_tags($x[1])):'';
    $geocode_url = 'http://maps.googleapis.com/maps/api/geocode/json?address='.urlencode($data['street']).',+Philadelphia,+PA&sensor=false&output=json';
   
    // Retrieve the URL contents
    $geodata = file_get_contents($geocode_url);

    // Parse the returned json
    $geo_json = json_decode($geodata);
    $latlng = ($geo_json->status != 'ZERO_RESULTS') ? $latlng = array($geo_json->results[0]->geometry->location->lat, $geo_json->results[0]->geometry->location->lng) : array(0.0,0.0);
    //print_r($latlng);

    // $misc_info = ward sq.ft. BRT# improvements
    $data['misc_info'] = (isset($split_on_spaces[1])) ? trim(strip_tags($split_on_spaces[1])) : '';
    
    // Pull out the ward first
    $ward_pattern = '/^[A-Za-z0-9]+(.)* Ward/';
    $data['ward'] = preg_match($ward_pattern,$data['misc_info'],$wards) ? $wards[0]: '';
//print_r($ward);

    // Pull out the BRT # next
    $brt_pattern = '/[0-9]{9}/';
    $data['brt'] = preg_match_all($brt_pattern,$data['misc_info'],$brts) ? $brts[0][0]: ''; 
//print_r($brts);

    // Now the improvements
    $improve_pattern = '/Improvements: [A-Za-z0-9].*$/';
    $data['improvement'] = preg_match($improve_pattern,$data['misc_info'],$improvements) ? str_replace('Improvements:','',$improvements[0]): '';
//print_r($improvement . "\n");

    if(isset($brs[1])) {
        $split_on_spaces2 = explode('&nbsp;   &nbsp;',$brs[1]);
        $data['owner'] = (isset($split_on_spaces2[0])) ? trim(strip_tags($split_on_spaces2[0])) : '';
        $data['term'] = (isset($split_on_spaces2[1])) ? trim(strip_tags($split_on_spaces2[1])) : '';
        $p_and_a = (isset($split_on_spaces2[2])) ? explode('&nbsp;  &nbsp;', $split_on_spaces2[2]) : '';
        //print_r($p_and_a);
        $data['price'] = (isset($p_and_a[0])) ? trim(strip_tags($p_and_a[0])) : '';    
        $data['attorney'] = (isset($p_and_a[1])) ? trim(strip_tags($p_and_a[1])) : '';    
        
    } 
    
    scraperwiki::save(array('id'), $data, date('Y-m-d h:i:s'), array($latlng[0] , $latlng[1]));
    //scraperwiki::save(array('id'), $data, date('Y-m-d hh:ii:ss'));
}

?>