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

$count = 1;
foreach ($city_list as $city) {
    
// this is just to continue a disconnected session, comment out for full run.
     if ($count < 393) {
     $count ++;
     continue;
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
        sleep(3); // this may be needed on scraperwiki.com
    }

    
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
        $rep = $rep_details;        

        if ($run_environment == 'dev') {
            $reps[] = $rep;
        }
        else {
            $reps = null;
            scraperwiki::save_sqlite(array('title','name_full','city'), $rep, $table_name='rep');    
        }

                
    }  

    
    if($dom->find("div[class=prevNext]", 0) && $next = $dom->find("div[class=prevNext]", 0)->find("a[class=last]", 0)) {
        
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


    $table = $dom->find("table", 0);
    
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

    return $rep;

}






?><?php

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

$count = 1;
foreach ($city_list as $city) {
    
// this is just to continue a disconnected session, comment out for full run.
     if ($count < 393) {
     $count ++;
     continue;
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
        sleep(3); // this may be needed on scraperwiki.com
    }

    
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
        $rep = $rep_details;        

        if ($run_environment == 'dev') {
            $reps[] = $rep;
        }
        else {
            $reps = null;
            scraperwiki::save_sqlite(array('title','name_full','city'), $rep, $table_name='rep');    
        }

                
    }  

    
    if($dom->find("div[class=prevNext]", 0) && $next = $dom->find("div[class=prevNext]", 0)->find("a[class=last]", 0)) {
        
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


    $table = $dom->find("table", 0);
    
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

    return $rep;

}






?><?php

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

$count = 1;
foreach ($city_list as $city) {
    
// this is just to continue a disconnected session, comment out for full run.
     if ($count < 393) {
     $count ++;
     continue;
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
        sleep(3); // this may be needed on scraperwiki.com
    }

    
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
        $rep = $rep_details;        

        if ($run_environment == 'dev') {
            $reps[] = $rep;
        }
        else {
            $reps = null;
            scraperwiki::save_sqlite(array('title','name_full','city'), $rep, $table_name='rep');    
        }

                
    }  

    
    if($dom->find("div[class=prevNext]", 0) && $next = $dom->find("div[class=prevNext]", 0)->find("a[class=last]", 0)) {
        
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


    $table = $dom->find("table", 0);
    
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

    return $rep;

}






?>