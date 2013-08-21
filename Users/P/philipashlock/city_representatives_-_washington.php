<?php

$run_environment = 'prod'; // either 'dev' or 'prod'
$max_records = 3; // only used for testing

if ($run_environment == 'dev') {
    error_reporting(E_ALL);
    ini_set('display_errors','On');    

    require 'scraperwiki.php';
}

require 'scraperwiki/simple_html_dom.php';

$city_directory = "http://www.mrsc.org/cityprofiles/citylist.aspx";

    
$cities = get_cities($city_directory);

$count = 1;

foreach ($cities as $city) {
    
    if ($run_environment == 'prod') {
        scraperwiki::save_sqlite(array('data_url'), $city, $table_name='city');    
        get_city_data($city['name'], $city['officials_url']); 
    }
    else {
        $reps    =     get_city_data($city['name'], $city['officials_url']); 
        $alldata[] = array('city' => $city, 'reps' => $reps);
    }
        
    $count++;
    if ($run_environment == 'dev' && $count > $max_records) break;
}

if ($run_environment == 'prod') {
    sleep(3); // this is required on scraperwiki.com
}    
    
// if testing
if ($run_environment == 'dev') {
    header('Content-type: application/json');
    print json_encode($alldata);
}



function get_cities($url) {
    
    global $base_url;
    
    $html = scraperWiki::scrape($url);
    
    $dom = new simple_html_dom();
    $dom->load($html);

    $count = 1;

    $table = $dom->find("table[id=dgCities]", 0);
    
    // echo $table->find("tr", 1)->outertext; exit;
    
    foreach($table->find("tr") as $data){
            
        // Skip the header row
        if($count < 2) {
            $count++;
            continue;
        }

        $tds = $data->find("td");

        if ($object = $tds[0]->find("a", 0)) {        
            
            $city['name']                 = trim($object->plaintext);
            $city['data_url']             = 'http://www.mrsc.org/cityprofiles/' .  $object->href;
            $city['population']            = trim($tds[1]->plaintext);
            $city['county']                = trim($tds[2]->plaintext);            
            $city['class']                = trim($tds[3]->plaintext);            
            $city['gov_type']            = trim($tds[4]->plaintext);                                    

            $city['officials_url']         = 'http://www.mrsc.org' . $tds[5]->find("a", 0)->href;
        
            $cities[] = $city;
            $city = null;
        
        }

        $count++;
    }   

    
    return $cities;

}



function get_city_data($city, $url) {
    
    global $run_environment;
        
    $html = scraperWiki::scrape($url);    
    $dom = new simple_html_dom();
    $dom->load($html);

    $count = 1;
    
    $content = $dom->find("div[id=content]", 0);
    $table = $content->find("table", 0);


    foreach($table->find("tr") as $data){
        

        $tds = $data->find("td");

        if(empty($tds[1])) break;
        
        $rep = null;
        $rep['title']     = trim($tds[0]->plaintext);
        $rep['name']     = trim($tds[1]->plaintext);                
        $rep['city']     = $city;
        $rep['source']  = $url;        
        
        
        if ($run_environment == 'dev') {
            $reps[] = $rep;
        }
        else {
            scraperwiki::save_sqlite(array('title','name','city'), $rep, $table_name='rep');    
        }        
                
        $count++;
    }   

    if ($run_environment == 'dev') {
        return $reps;
    } else {
        return true;
    }

}




?><?php

$run_environment = 'prod'; // either 'dev' or 'prod'
$max_records = 3; // only used for testing

if ($run_environment == 'dev') {
    error_reporting(E_ALL);
    ini_set('display_errors','On');    

    require 'scraperwiki.php';
}

require 'scraperwiki/simple_html_dom.php';

$city_directory = "http://www.mrsc.org/cityprofiles/citylist.aspx";

    
$cities = get_cities($city_directory);

$count = 1;

foreach ($cities as $city) {
    
    if ($run_environment == 'prod') {
        scraperwiki::save_sqlite(array('data_url'), $city, $table_name='city');    
        get_city_data($city['name'], $city['officials_url']); 
    }
    else {
        $reps    =     get_city_data($city['name'], $city['officials_url']); 
        $alldata[] = array('city' => $city, 'reps' => $reps);
    }
        
    $count++;
    if ($run_environment == 'dev' && $count > $max_records) break;
}

if ($run_environment == 'prod') {
    sleep(3); // this is required on scraperwiki.com
}    
    
// if testing
if ($run_environment == 'dev') {
    header('Content-type: application/json');
    print json_encode($alldata);
}



function get_cities($url) {
    
    global $base_url;
    
    $html = scraperWiki::scrape($url);
    
    $dom = new simple_html_dom();
    $dom->load($html);

    $count = 1;

    $table = $dom->find("table[id=dgCities]", 0);
    
    // echo $table->find("tr", 1)->outertext; exit;
    
    foreach($table->find("tr") as $data){
            
        // Skip the header row
        if($count < 2) {
            $count++;
            continue;
        }

        $tds = $data->find("td");

        if ($object = $tds[0]->find("a", 0)) {        
            
            $city['name']                 = trim($object->plaintext);
            $city['data_url']             = 'http://www.mrsc.org/cityprofiles/' .  $object->href;
            $city['population']            = trim($tds[1]->plaintext);
            $city['county']                = trim($tds[2]->plaintext);            
            $city['class']                = trim($tds[3]->plaintext);            
            $city['gov_type']            = trim($tds[4]->plaintext);                                    

            $city['officials_url']         = 'http://www.mrsc.org' . $tds[5]->find("a", 0)->href;
        
            $cities[] = $city;
            $city = null;
        
        }

        $count++;
    }   

    
    return $cities;

}



function get_city_data($city, $url) {
    
    global $run_environment;
        
    $html = scraperWiki::scrape($url);    
    $dom = new simple_html_dom();
    $dom->load($html);

    $count = 1;
    
    $content = $dom->find("div[id=content]", 0);
    $table = $content->find("table", 0);


    foreach($table->find("tr") as $data){
        

        $tds = $data->find("td");

        if(empty($tds[1])) break;
        
        $rep = null;
        $rep['title']     = trim($tds[0]->plaintext);
        $rep['name']     = trim($tds[1]->plaintext);                
        $rep['city']     = $city;
        $rep['source']  = $url;        
        
        
        if ($run_environment == 'dev') {
            $reps[] = $rep;
        }
        else {
            scraperwiki::save_sqlite(array('title','name','city'), $rep, $table_name='rep');    
        }        
                
        $count++;
    }   

    if ($run_environment == 'dev') {
        return $reps;
    } else {
        return true;
    }

}




?>