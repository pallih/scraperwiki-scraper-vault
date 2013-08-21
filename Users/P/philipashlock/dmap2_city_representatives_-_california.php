<?php

$run_environment = 'prod'; // either 'dev' or 'prod'
$max_records = 4; // only used for testing

if ($run_environment == 'dev') {
    error_reporting(E_ALL);
    ini_set('display_errors','On');    

    require 'scraperwiki.php';
}

require 'scraperwiki/simple_html_dom.php';

$url = "http://events.cacities.org/CGI-SHL/TWSERVER.EXE/RUN:MEMLOOK";

$post_url = 'http://events.cacities.org/cgi-shl/TWServer.exe?Run:MEMLOOK_1';

$city_list = get_city_list($url);

// Set state of scraper as running in case we crash part way thru
scraperwiki::save_var('scraper_state', 'running');

$count = 1;
foreach ($city_list as $city) {
    
    
    // Check if we failed part way through a run and find where we left off
    if (scraperwiki::get_var('scraper_state') == 'running') {
        
        $last_city = scraperwiki::get_var('last_city');
        
        if (!empty($last_city)) {
            if ($last_city !== $city) {
                continue;
            } 
        } else {
            scraperwiki::save_var('last_city', $city);
        }
                
    }
        
    
    //set POST variables
    $fields = array(
                'Company' => $city
            );

    $result = get_post_response($post_url,$fields);
            
    if ($run_environment == 'prod') {
        get_city_data($result);
    }
    else {
        $alldata[]  =   get_city_data($result);
    }



    $count++;
    if ($run_environment == 'dev' && $count > $max_records) break;

    
    if ($run_environment == 'prod') {
        sleep(2); // this may be needed on scraperwiki.com
    }

    // reset the progress bookmark
    scraperwiki::save_var('last_city', '');    
}    


// Set state of scraper to complete so we know it didn't crash part way thru
scraperwiki::save_var('scraper_state', 'complete');


// if testing
if ($run_environment == 'dev') {
    header('Content-type: application/json');
    print json_encode($alldata);
}


function get_post_response($url,$fields) {
    
    //url-ify the data for the POST
    $fields_string = '';
    foreach($fields as $key=>$value) { $fields_string .= $key.'='.$value.'&'; }
    rtrim($fields_string, '&');


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



function get_city_data($html = null, $url = null, $reps = null) {
    
    global $run_environment;
    global $post_url;
    
    if(!empty($url)) {
        $html = scraperWiki::scrape($url);   
    }
      
    $dom = new simple_html_dom();
    $dom->load($html);

    $count = 1;

    // for debugging
    if(!$dom->find("table", 0)) {
        echo $url; exit;
    }
    
    $table = $dom->find("table", 0);

    foreach($table->find("tr") as $data){
                
        $tds = $data->find("td");
        
        if (trim($tds[0]->plaintext) == 'Full Name') continue;
        
        $rep = null;
        $rep['name_full']     = trim($tds[0]->plaintext);
        $rep['city']            = trim($tds[1]->plaintext);                
        $rep['title']           = trim($tds[2]->plaintext); 
        $rep['source']        = 'http://events.cacities.org' . $tds[0]->find('a',0)->href;       
        

        $rep_details = get_rep_details($rep['source'] );
        if ($run_environment == 'prod') {
            sleep(1); // this may be needed on scraperwiki.com
        }                
        
        //$rep = array_merge($rep, $rep_details);
        if($rep_details) {
            $rep = $rep_details;        

            if ($run_environment == 'dev') {
                $reps[] = $rep;
            }
            else {
                $reps = null;
                scraperwiki::save_sqlite(array('title','name_full','government_name'), $rep, $table_name='officials');    
            }
        }

                
    }  

    
    if($next = $dom->find("div[class=prevNext]", 0)->find("a[class=last]", 0)) {
        
        $page = str_replace(' ', '%20', $next->href);
        
        $url = 'http://events.cacities.org' . $page;
        get_city_data(null, $url, $reps);
    }
    
    
 

    if ($run_environment == 'dev') {
        return $reps;
    } else {
        return true;
    }

}





function get_city_list($url) {
        
    $html = scraperWiki::scrape($url);    
    $dom = new simple_html_dom();
    $dom->load($html);
    
    $content = $dom->find("form", 0);
    $content = $content->find("select", 0);

    foreach($content->find("option") as $city){
        

        $cities[] = $city->plaintext;       
        
    }  

     unset($cities[0]);

    return $cities;

}

function get_rep_details($url) {
        
    $html = scraperWiki::scrape($url);    
    $dom = new simple_html_dom();
    $dom->load($html);

    if ($table = $dom->find("table", 0)) {
        
        $rows = $table->find("tr");
    
        // echo $rows[0]->find("td", 1)->plaintext; exit;
        // echo $table->find("tr", 0)->find("td", 1)->plaintext; exit;
    
        $rep['name_full']         = ($rows[0]->find("td", 1)) ? trim($rows[0]->find("td", 1)->plaintext) : null;    
        $rep['title']             = ($rows[2]->find("td", 1)) ? trim($rows[2]->find("td", 1)->plaintext) : null;    
        $rep['address_1']         = ($rows[3]->find("td", 1)) ? trim($rows[3]->find("td", 1)->plaintext) : null;    
        $rep['address_2']         = ($rows[4]->find("td", 1)) ? trim($rows[4]->find("td", 1)->plaintext) : null;    
    
           $rep['city']             = ($rows[1]->find("td", 1)) ? trim($rows[1]->find("td", 1)->plaintext) : null;    
        $rep['state']            = 'CA';

        // filter zip from string
        $zip                        = ($rows[5]->find("td", 1)) ? trim($rows[5]->find("td", 1)->plaintext) : null;
        $zip                       = ($zip) ? trim(substr($zip, strrpos($zip, ' '))) : null;    
        $rep['zip']                = $zip;
        
        $rep['phone']             = ($rows[6]->find("td", 1)) ? trim($rows[6]->find("td", 1)->plaintext) : null;        // 
        $rep['city_url']         = ($rows[8]->find("td", 1)) ? trim($rows[8]->find("td", 1)->plaintext) : null;        

        $rep['source']             = $url;

        // Map to data model

        $official = official();



        $official['government_name']        = $rep['city'];
        $official['government_level']        = 'municipal';

        $official['type']                    = null;
        $official['title']                  = $rep['title'];
        $official['name_full']                = $rep['name_full'];
        $official['address_1']              = $rep['address_1'];
        $official['address_2']                = $rep['address_2'];
        $official['address_locality']        = $rep['city'];
        $official['address_region']            = $rep['state'];
        $official['address_postcode']        = $rep['zip'];
        $official['address_country']        = 'USA';    
        $official['phone']                  = $rep['phone'];
        $official['sources']                = json_encode(array(array('description' => null, 'url' => $rep['source'])));

        return $official;
    } else {
        return false;
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