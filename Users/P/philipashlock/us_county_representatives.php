<?php

$run_environment = 'prod'; // either 'dev' or 'prod'
$max_records = 10; // only used for testing

if ($run_environment == 'dev') {
    error_reporting(E_ALL);
    ini_set('display_errors','On');    

    require 'scraperwiki.php';
}

require 'scraperwiki/simple_html_dom.php';

// $states = array("AL","AK","AZ","AR","CA","CO","CT","DC","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MO"); // these ones finished
// array("GU", "PR", "MP"); // it choked on these, so I'm removing them

$states = array("MS","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY");

$county_directory_url = "http://www.uscounties.org/cffiles_web/counties/";


foreach ($states as $state) {

    global $county_directory_url;

    $url = $county_directory_url . 'state.cfm?statecode=' . $state;
    
    $counties = get_counties($url);
    
    foreach ($counties as $county) {
        $alldata[] = get_county_data($state, $county['county_name'], $county['county_data_url']);
    }
    
    
    if ($run_environment == 'prod') {
        sleep(10); // this is required on scraperwiki.com
    }    
    
}


// if testing
if ($run_environment == 'dev') {
    header('Content-type: application/json');
    print json_encode($alldata);
}



function get_counties($url) {
    
    global $county_directory_url;    

    $html = scraperWiki::scrape($url);
    
    $dom = new simple_html_dom();
    $dom->load($html);

    $count = 1;
    
    foreach($dom->find("table", 1)->find("tr") as $data){
            
        if($data->find("th")) {
            continue;
        }

        $tds = $data->find("td");

        $object      = $tds[0]->find("a", 0);
        $county_name = trim($object->plaintext);
        $county_data_url = $county_directory_url . $object->href;
        
        $counties[] = array('county_name' => $county_name, 'county_data_url' => $county_data_url);

    }   

    
    return $counties;

}



function get_county_data($state, $county, $url) {
    
    global $run_environment;
        
    $html = scraperWiki::scrape($url);    
    $dom = new simple_html_dom();
    $dom->load($html);

    $count = 1;
    
    $table = $dom->find("table", 2);

    foreach($table->find("tr") as $data){
        

        
        if($count < 3) {
            $count++;
            continue;
        }

        $tds = $data->find("td");

        if ($tds[0]->find("a", 0)) {
            $rep_link      = $tds[0]->find("a", 0);
            $rep_name      = trim($rep_link->plaintext);
            $rep_email     = $rep_link->href;
            
            if (substr($rep_email, 0, 7) == 'mailto:'){
                $rep_email = substr($rep_email, 7);
            }            

        } else {
            $rep_name      = trim($tds[0]->plaintext);
            $rep_email      = null;
        }

        $rep_position = trim($tds[1]->plaintext);
        
        $rep = null;
        $rep = array('state' => $state, 'county' => $county, 'rep' => $rep_name, 'rep_email' => $rep_email, 'rep_position' => $rep_position);
        
        if ($run_environment == 'dev') {
            $reps[] = $rep;
        }
        else {
            scraperwiki::save(array('rep'), $rep);
        }

                
        $count++;
    }   

    if ($run_environment == 'dev') {
        return $reps;
    }

}



function get_phone_numbers($string) {
    
    $phone_list = preg_replace('/[^0-9]/','',$string);

    $pattern = '/(?:\+|00)?(\d[\d\s]{9,10})/';
    preg_match_all($pattern, $phone_list, $matches);
    $numbers = array();
    if (isset($matches[1])) {
        foreach ($matches[1] as $match) {
            $numbers[] = str_replace(' ', '', $match);
        }
    }    
    
    
return $numbers;    
    
}



?><?php

$run_environment = 'prod'; // either 'dev' or 'prod'
$max_records = 10; // only used for testing

if ($run_environment == 'dev') {
    error_reporting(E_ALL);
    ini_set('display_errors','On');    

    require 'scraperwiki.php';
}

require 'scraperwiki/simple_html_dom.php';

// $states = array("AL","AK","AZ","AR","CA","CO","CT","DC","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MO"); // these ones finished
// array("GU", "PR", "MP"); // it choked on these, so I'm removing them

$states = array("MS","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY");

$county_directory_url = "http://www.uscounties.org/cffiles_web/counties/";


foreach ($states as $state) {

    global $county_directory_url;

    $url = $county_directory_url . 'state.cfm?statecode=' . $state;
    
    $counties = get_counties($url);
    
    foreach ($counties as $county) {
        $alldata[] = get_county_data($state, $county['county_name'], $county['county_data_url']);
    }
    
    
    if ($run_environment == 'prod') {
        sleep(10); // this is required on scraperwiki.com
    }    
    
}


// if testing
if ($run_environment == 'dev') {
    header('Content-type: application/json');
    print json_encode($alldata);
}



function get_counties($url) {
    
    global $county_directory_url;    

    $html = scraperWiki::scrape($url);
    
    $dom = new simple_html_dom();
    $dom->load($html);

    $count = 1;
    
    foreach($dom->find("table", 1)->find("tr") as $data){
            
        if($data->find("th")) {
            continue;
        }

        $tds = $data->find("td");

        $object      = $tds[0]->find("a", 0);
        $county_name = trim($object->plaintext);
        $county_data_url = $county_directory_url . $object->href;
        
        $counties[] = array('county_name' => $county_name, 'county_data_url' => $county_data_url);

    }   

    
    return $counties;

}



function get_county_data($state, $county, $url) {
    
    global $run_environment;
        
    $html = scraperWiki::scrape($url);    
    $dom = new simple_html_dom();
    $dom->load($html);

    $count = 1;
    
    $table = $dom->find("table", 2);

    foreach($table->find("tr") as $data){
        

        
        if($count < 3) {
            $count++;
            continue;
        }

        $tds = $data->find("td");

        if ($tds[0]->find("a", 0)) {
            $rep_link      = $tds[0]->find("a", 0);
            $rep_name      = trim($rep_link->plaintext);
            $rep_email     = $rep_link->href;
            
            if (substr($rep_email, 0, 7) == 'mailto:'){
                $rep_email = substr($rep_email, 7);
            }            

        } else {
            $rep_name      = trim($tds[0]->plaintext);
            $rep_email      = null;
        }

        $rep_position = trim($tds[1]->plaintext);
        
        $rep = null;
        $rep = array('state' => $state, 'county' => $county, 'rep' => $rep_name, 'rep_email' => $rep_email, 'rep_position' => $rep_position);
        
        if ($run_environment == 'dev') {
            $reps[] = $rep;
        }
        else {
            scraperwiki::save(array('rep'), $rep);
        }

                
        $count++;
    }   

    if ($run_environment == 'dev') {
        return $reps;
    }

}



function get_phone_numbers($string) {
    
    $phone_list = preg_replace('/[^0-9]/','',$string);

    $pattern = '/(?:\+|00)?(\d[\d\s]{9,10})/';
    preg_match_all($pattern, $phone_list, $matches);
    $numbers = array();
    if (isset($matches[1])) {
        foreach ($matches[1] as $match) {
            $numbers[] = str_replace(' ', '', $match);
        }
    }    
    
    
return $numbers;    
    
}



?><?php

$run_environment = 'prod'; // either 'dev' or 'prod'
$max_records = 10; // only used for testing

if ($run_environment == 'dev') {
    error_reporting(E_ALL);
    ini_set('display_errors','On');    

    require 'scraperwiki.php';
}

require 'scraperwiki/simple_html_dom.php';

// $states = array("AL","AK","AZ","AR","CA","CO","CT","DC","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MO"); // these ones finished
// array("GU", "PR", "MP"); // it choked on these, so I'm removing them

$states = array("MS","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY");

$county_directory_url = "http://www.uscounties.org/cffiles_web/counties/";


foreach ($states as $state) {

    global $county_directory_url;

    $url = $county_directory_url . 'state.cfm?statecode=' . $state;
    
    $counties = get_counties($url);
    
    foreach ($counties as $county) {
        $alldata[] = get_county_data($state, $county['county_name'], $county['county_data_url']);
    }
    
    
    if ($run_environment == 'prod') {
        sleep(10); // this is required on scraperwiki.com
    }    
    
}


// if testing
if ($run_environment == 'dev') {
    header('Content-type: application/json');
    print json_encode($alldata);
}



function get_counties($url) {
    
    global $county_directory_url;    

    $html = scraperWiki::scrape($url);
    
    $dom = new simple_html_dom();
    $dom->load($html);

    $count = 1;
    
    foreach($dom->find("table", 1)->find("tr") as $data){
            
        if($data->find("th")) {
            continue;
        }

        $tds = $data->find("td");

        $object      = $tds[0]->find("a", 0);
        $county_name = trim($object->plaintext);
        $county_data_url = $county_directory_url . $object->href;
        
        $counties[] = array('county_name' => $county_name, 'county_data_url' => $county_data_url);

    }   

    
    return $counties;

}



function get_county_data($state, $county, $url) {
    
    global $run_environment;
        
    $html = scraperWiki::scrape($url);    
    $dom = new simple_html_dom();
    $dom->load($html);

    $count = 1;
    
    $table = $dom->find("table", 2);

    foreach($table->find("tr") as $data){
        

        
        if($count < 3) {
            $count++;
            continue;
        }

        $tds = $data->find("td");

        if ($tds[0]->find("a", 0)) {
            $rep_link      = $tds[0]->find("a", 0);
            $rep_name      = trim($rep_link->plaintext);
            $rep_email     = $rep_link->href;
            
            if (substr($rep_email, 0, 7) == 'mailto:'){
                $rep_email = substr($rep_email, 7);
            }            

        } else {
            $rep_name      = trim($tds[0]->plaintext);
            $rep_email      = null;
        }

        $rep_position = trim($tds[1]->plaintext);
        
        $rep = null;
        $rep = array('state' => $state, 'county' => $county, 'rep' => $rep_name, 'rep_email' => $rep_email, 'rep_position' => $rep_position);
        
        if ($run_environment == 'dev') {
            $reps[] = $rep;
        }
        else {
            scraperwiki::save(array('rep'), $rep);
        }

                
        $count++;
    }   

    if ($run_environment == 'dev') {
        return $reps;
    }

}



function get_phone_numbers($string) {
    
    $phone_list = preg_replace('/[^0-9]/','',$string);

    $pattern = '/(?:\+|00)?(\d[\d\s]{9,10})/';
    preg_match_all($pattern, $phone_list, $matches);
    $numbers = array();
    if (isset($matches[1])) {
        foreach ($matches[1] as $match) {
            $numbers[] = str_replace(' ', '', $match);
        }
    }    
    
    
return $numbers;    
    
}



?>