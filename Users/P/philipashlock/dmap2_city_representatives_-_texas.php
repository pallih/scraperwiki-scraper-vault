<?php

$run_environment = 'prod'; // either 'dev' or 'prod'
$max_records = 4; // only used for testing

if ($run_environment == 'dev') {
    error_reporting(E_ALL);     
    require 'scraperwiki.php';
}

require 'scraperwiki/simple_html_dom.php';


$post_url = "http://members.tml.org/source/Members/TML_DirectoryProcess.cfm";

//http://members.tml.org/source/members/TML_Directory.cfm

//set POST variables
$fields = array(
            'population' => '',
            'CS' => '',
            'FIRST_NAME' => '', 
            'LAST_NAME' => '', 
            'x' => 23,
            'y' => 6, 
        );

$city_list = get_city_list(get_post_response($post_url,$fields));

// $alldata = $city_list; 

$count = 1;
foreach ($city_list as $url) {
    
    if ($run_environment == 'prod') {
        get_city_data($url);
    }
    else {
        $alldata[]  = get_city_data($url);
    }

    $count++;
    if ($run_environment == 'dev' && $count > $max_records) break;

}


// if testing
if ($run_environment == 'dev') {
    header('Content-type: application/json');
    print json_encode($alldata);
}


function get_post_response($url,$fields) {
    
    //url-ify the data for the POST
    $fields_string = '';
    foreach($fields as $key=>$value) { $fields_string .= $key.'='.$value.'&'; }
    $fields_string = rtrim($fields_string, '&');


    //open connection
    $ch = curl_init();

    //set the url, number of POST vars, POST data
    curl_setopt($ch,CURLOPT_URL, $url);
    curl_setopt($ch,CURLOPT_RETURNTRANSFER, true);        
    curl_setopt($ch,CURLOPT_POST, count($fields));
    curl_setopt($ch,CURLOPT_POSTFIELDS, $fields_string);

    //execute post
    $result = curl_exec($ch);

    //close connection
    curl_close($ch);
    
    return $result;
        
}



function get_city_list($html) {
        
    global $run_environment;
    global $max_records;

    //$html = scraperWiki::scrape($url);    
    $dom = new simple_html_dom();
    $dom->load($html);
    
    // table/tr/td/div/table/tr/td[2]/table/tr/td/table/tr[5]
    // $content = $dom->find("table", 0)->find("tr", 0)->find("td", 0)->find("div", 0)->find("table", 0)->find("tr", 0)->find("td", 2)->find("table", 0);
    
    // table/tbody/tr/td/div/section/div/table
    $content = $dom->find("table", 0)->find("tr", 0)->find("td", 0)->find("div", 0)->find("section", 0)->find("div", 0)->find("table", 0);

    $count = 0;
    foreach($content->find("tr") as $row){
        
        // first row of data is this one
        if ($count < 4) { $count++; continue; }
        if (!$row->find("a", 0)) continue;

        $city = $row->find("a", 0);
        
        $url = 'http://www.tml.org/source/Members/' . $city->href; 

        $cities[] = $url; //get_city_data($url);
        
         $count++;

    }  

// Clear memory
$dom->__destruct();
$content->__destruct();

     return $cities;

}



function get_city_data($url) {
    
    global $run_environment;
    
    $html = scraperWiki::scrape($url);        
    $dom = new simple_html_dom();
    $dom->load($html);

    $count = 1;

    // for debugging
    if(!$dom->find("table", 0)) {
        echo $url; exit;
    }
    
    // /html/body/table/tbody/tr/td/div/section/div/table
    // $content = $dom->find("table", 0)->find("tr", 0)->find("td", 0)->find("div", 0)->find("table", 0)->find("tr", 0)->find("td", 2)->find("table", 0);
    
    $content = $dom->find("table", 0)->find("tr", 0)->find("td", 0)->find("div", 0)->find("section", 0)->find("div", 0)->find("table", 0);

    $city['source'] = $url;
    $city['name_full'] = $content->find("h2", 0)->plaintext;
    $city['name'] = substr($city['name_full'], strpos($city['name_full'], ' of ') + 4);    
    $city['type'] = strtolower(substr($city['name_full'], 0, strpos($city['name_full'], ' of ')));

    $city['url'] = ($content->find("tr", 5)->find("td", 1)->find("a", 0)) ? $content->find("tr", 5)->find("td", 1)->find("a", 0)->href : null;
    $city['region'] = trim($content->find("tr", 6)->find("td", 1)->plaintext);
    $city['county'] = trim($content->find("tr", 7)->find("td", 1)->plaintext);        
    $city['address1'] = trim($content->find("tr", 8)->find("td", 1)->plaintext);            
    $city['address2'] = trim($content->find("tr", 9)->find("td", 1)->plaintext);                
    $city['phone'] = trim($content->find("tr", 10)->find("td", 1)->plaintext);                
    $city['fax'] = trim($content->find("tr", 11)->find("td", 1)->plaintext);                        
    $city['council_meeting_time'] = trim($content->find("tr", 12)->find("td", 1)->plaintext);                        
    $city['year_incorporated'] = trim($content->find("tr", 13)->find("td", 1)->plaintext);                        
    $city['fiscal_year_start'] = trim($content->find("tr", 14)->find("td", 1)->plaintext);                        
    $city['population'] = trim($content->find("tr", 15)->find("td", 1)->plaintext);                        
    $city['government_type'] = trim($content->find("tr", 16)->find("td", 1)->plaintext);                            
    $city['civil_service'] = trim($content->find("tr", 17)->find("td", 1)->plaintext);                        
    

    $rep_details = get_rep_details($content, $url, $city['name']);


    // Clear memory
    $dom->__destruct();
    $content->__destruct();

    if ($run_environment == 'dev') {
        $city['reps'] = $rep_details;
        return $city;
    }
    else {
        scraperwiki::save_sqlite(array('name_full','source'), $city, $table_name='jurisdiction');    
        return true;

    }


}



function get_rep_details($content, $source, $city) {
        
     global $run_environment;

    //$html = scraperWiki::scrape($url);    
    //$dom = new simple_html_dom();
    //$dom->load($html);

    foreach($content->find("tr", 19)->find("td", 1)->find("table", 0)->find("tr") as $row){
    
        
    
        $rep['title']     = trim($row->find("td", 0)->plaintext);
        
        // Skip any empty columns (often the first one)
        if($rep['title'] == '&nbsp;') continue;
        $rep['title']    = str_replace(':', '', $rep['title']);
        
        
        $rep['name']    = trim($row->find("td", 1)->plaintext);
        $rep['name']    = str_replace('&nbsp;', '', $rep['name']);

    
        $official = official();
        $official['government_name']        = $city;
        $official['government_level']        = 'municipal';

        $official['type']                    = null;
        $official['title']                  = $rep['title'];
        $official['name_full']                = $rep['name'];

        $official['address_locality']        = $city;
        $official['address_region']            = 'TX';
        $official['address_country']        = 'USA';

        $official['sources']                = json_encode(array(array('description' => null, 'url' => $source, "timestamp" => gmdate("Y-m-d H:i:s"))));    
    
    
    
    
           if ($run_environment == 'dev') {
                $officials[] = $official;
           } 
           else {
                scraperwiki::save_sqlite(array('name_full','title','government_name'), $official, $table_name='officials');    
           }
    
    
    }
    
    if ($run_environment == 'dev') {            
        return $officials;
    }
    else {
        return true;
    }

}




function official() {
    
    $official = array(
        'government_name'        => NULL,                         
        'government_level'        => NULL,                         
        'type'                     => NULL,                         
        'title'                 => NULL,                        
        'description'             => NULL,                  
        'name_given'             => NULL,                   
        'name_family'             => NULL,                      
        'name_full'             => NULL,                        
        'url'                     => NULL,                  
        'url_photo'             => NULL,            
        'url_schedule'             => NULL,         
        'url_contact'             => NULL,          
        'email'                 => NULL,                
        'phone'                 => NULL,                
        'address_name'             => NULL,         
        'address_1'             => NULL,            
        'address_2'             => NULL,            
        'address_locality'         => NULL,         
        'address_region'         => NULL,        
        'address_postcode'         => NULL,          
        'current_term_enddate'     => NULL, 
        'last_updated'             => NULL,                     
        'social_media'             => NULL,                     
        'other_data'             => NULL,
        'conflicting_data'        => NULL,
        'sources'                 => NULL                                     

    );
    
    return $official;
    
}





?>