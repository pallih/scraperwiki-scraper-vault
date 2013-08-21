<?php

$run_environment = 'prod'; // either 'dev' or 'prod'
$max_records = 50; // only used for testing

if ($run_environment == 'dev') {
    error_reporting(E_ALL);
    ini_set('display_errors','On');    

    require 'scraperwiki.php';

    $csv_file_path = '/Users/philipashlock/Sites/_unused/dmap-misc/cities_or_data.csv';

} 

if ($run_environment == 'prod') {
    $csv_file_path = '/tmp/city_or.csv';        
}

require 'scraperwiki/simple_html_dom.php';


/// -------------------------------- First download the file --------------------------------

// faking this now, real location involves a more complicated POST request to:
// http://www.orcities.org/CityResources/LOCCityDirectory/CityReportViewer/tabid/6214/language/en-US/Default.aspx

$url  = 'http://dropbox.ashlock.us/opengov/democracymap/cities_or_data.csv';


if ($run_environment == 'prod') {
 $ch = curl_init($url);
 curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
 curl_setopt($ch, CURLOPT_ENCODING, 'UTF-8');
 
 $data = curl_exec($ch);
 
 curl_close($ch);
 
// solving for weird encoding issues
// $data = iconv('utf-16le', 'utf-8', $data);

 file_put_contents($csv_file_path, $data);

 unset($data);

}
                                          
/// ------------------------------------------------------------------------------------------



$output = get_sources($csv_file_path);


if ($run_environment == 'dev') {
    header('Content-type: application/json');
    print json_encode($output);
}

function get_sources($csv_file_path) {
    
global $run_environment;
global $max_records;

    if(($handle = fopen($csv_file_path, 'r')) !== false)
    {

        $count = 1;
        $cityrow_count = 1;
        $city = array();

        // loop through the file line-by-line
        while(($data = fgetcsv($handle)) !== false)
        {
            
            // Name of the city
            if ($cityrow_count == 1) {
                $city['name'] = substr($data[0], 0, strpos($data[0], " - "));
                $city['county'] = substr($data[0], strpos($data[0], " - ") +3);            
            }
            
            // Mailing address of the city
            if ($cityrow_count == 4) {

                $address = address_splice($data[0]);
                $city = array_merge($city, $address);
                $city['website'] = $data[4];
            }    
            
            
            // Population
            if ($cityrow_count == 5) {
                $city['population'] = $data[4];
            }
            
            // Incorporation
            if ($cityrow_count == 6) {
                $city['incorporation_date'] = $data[4];
            }                                
            
            // Newspapers
            if ($cityrow_count == 7) {
                $city['newspaper'] = $data[4];                
            }    
            
            // Contact and meetings
            if ($cityrow_count == 11) {
                $city['phone'] = $data[1];        
                $city['council_meetings'] = $data[4];                                
            }                    
            
            // Contact and meetings
            if ($cityrow_count == 12) {
                $city['fax'] = $data[1];        
                $city['planning_meetings'] = $data[4];                                
            }    
            
            if ($cityrow_count > 13) {
                    
                if (!$data[1] && !$data[2]) {
                    
                    if ($run_environment == 'dev') {
                        $city['reps'] = $reps;
                        unset($reps);                                                
                        $rows[] = $city;
                        unset($city);
                        if($count > $max_records) break;// { var_dump($rows); exit;}        
                    }                        

                    if ($run_environment == 'prod') {            
                        scraperwiki::save_sqlite(array('name', 'county'), $city, $table_name='city');
                        unset($city);
                    }                    
                    
                    $cityrow_count = 1;
                    $city['name'] = substr($data[0], 0, strpos($data[0], " - "));
                    $city['county'] = substr($data[0], strpos($data[0], " - ") +3);            
                    
                } else {
                    $rep['city']     = $city['name'];
                    $rep['title']     = $data[0];
                    $rep['name']     = $data[1];                
                    $rep['email']     = $data[2];                                        
                    $rep['phone']     = $data[4];                                                            
                    
                    $address = address_splice($data[3]);
                    $rep = array_merge($rep, $address);                    
                    
                    if ($run_environment == 'prod') {            
                        scraperwiki::save_sqlite(array('city', 'title', 'name'), $rep, $table_name='reps');
                    }    else {
                        $reps[] = $rep;
                    }            

                    unset($rep);
                }
                    
            }

            $cityrow_count++;
            $count++;

            unset($row);
        }
        fclose($handle);
    
    }
    
    // In case we're at the last row and didn't have a chance to loop around
    if (!empty($city)) {
        if ($run_environment == 'dev') {
            $city['reps'] = $reps;
            unset($reps);                                                
            $rows[] = $city;
            unset($city);
        }                        

        if ($run_environment == 'prod') {            
            scraperwiki::save_sqlite(array('name'), $city, $table_name='city');
            unset($city);
        }
    }    

    

if ($run_environment == 'dev') {    
    return $rows;    
} else {
    return true;
}
    
}


function address_splice($address_string){
    
    $address = substr($address_string, 0, strpos($address_string, "\r\n"));
    $address_extra = substr($address_string, strpos($address_string, "\r\n") + 2);
    $output['address1'] = $address;
    $output['address_city'] = substr($address_extra, 0, strpos($address_extra, ','));                 
    $output['address_state'] = substr($address_extra, strpos($address_extra, ',') + 2, 2);                                 
    $output['address_zip'] = substr($address_extra, strripos($address_extra, ',') + 2);    
    
    return $output;
}


function rmBOM($data){
    if(substr($data, 0, 3) == pack('CCC', 239, 187, 191)) {
        return substr($data, 3);
    }
    return $data;
}



?>