<?php

$run_environment = 'prod'; // either 'dev' or 'prod'
$max_records = 4; // only used for testing

if ($run_environment == 'dev') {
    error_reporting(E_ALL);     
    require 'scraperwiki.php';
}

require 'scraperwiki/simple_html_dom.php';


$url = "http://www.floridaleagueofcities.com/directory.aspx";

$city_list = get_city_list($url);

// $alldata = $city_list; 

$count = 1;
foreach ($city_list as $link) {
    
    $url = $link['source'];
    $city = $link['name'];
    
    if ($run_environment == 'prod') {
        get_city_data($city, $url);
    }
    else {
        $alldata[] = get_city_data($city, $url);
    }

    $count++;
    if ($run_environment == 'dev' && $count > $max_records) break;

}


// if testing
if ($run_environment == 'dev') {
    header('Content-type: application/json');
    print json_encode($alldata);
}



function get_city_list($url) {
        
    global $run_environment;
    global $max_records;

    $html = scraperWiki::scrape($url);    
    $dom = new simple_html_dom();
    $dom->load($html);
    
    // table/tr/td/div/table/tr/td[2]/table/tr/td/table/tr[5]
    $content = $dom->find("div[id=ctl00_cphmain_pnlIndex]", 0)->find("table", 1);

    $count = 0;
    foreach($content->find("a") as $link){
        
        if ($link->href) {

            $city['source'] = 'http://www.floridaleagueofcities.com' . $link->href;
            $city['name'] = $link->plaintext;

            $cities[] = $city;
        
             $count++;
        }

    }  

    // Clear memory
    $dom->__destruct();
    $content->__destruct();

     return $cities;

}



function get_city_data($name, $url) {
    
    global $run_environment;
    
    $html = scraperWiki::scrape($url);        
    $dom = new simple_html_dom();
    $dom->load($html);

    $count = 1;

    // for debugging
    if(!$dom->find("table", 0)) {
        echo $url; exit;
    }
    
    
    
    
    $content = $dom->find("div[id=ctl00_cphmain_pnlCityInfo]", 0)->find("table", 0);

    $city['source']                 = $url;
    $city['name']                     = $name;
                                
    $city['address']                 = trim($content->find("tr", 1)->find("td", 1)->plaintext);            
    $city['address_shipping']        = trim($content->find("tr", 2)->find("td", 1)->plaintext);                

    $city['phone']                     = trim($content->find("tr", 4)->find("td", 1)->plaintext);                
    $city['fax']                     = trim($content->find("tr", 5)->find("td", 1)->plaintext);                        
    
    $city['url']                     = ($content->find("tr", 7)->find("td", 1)->find("a", 0)) ? $content->find("tr", 7)->find("td", 1)->find("a", 0)->href : null;
    $city['email']                     = ($content->find("tr", 8)->find("td", 1)->find("a", 0)) ? $content->find("tr", 8)->find("td", 1)->find("a", 0)->href : null;

    $city['year_incorporated']         = trim($content->find("tr", 10)->find("td", 1)->plaintext);                        
    $city['population']             = trim($content->find("tr", 11)->find("td", 1)->plaintext);                        
    $city['county']                 = trim($content->find("tr", 12)->find("td", 1)->plaintext);        

    $city['city_history']             = ($content->find("tr", 14)->find("td", 1)) ? trim($content->find("tr", 14)->find("td", 1)->plaintext) : null;            
   
    // Get reps
    $rep_details = get_rep_details($dom, $url, $city['name']);
   
   
    // Clear memory
    $dom->__destruct();
    $content->__destruct();
   
    if ($run_environment == 'dev') {
        $city['reps'] = $rep_details;
        return $city;
    }
    else {
        scraperwiki::save_sqlite(array('name','source'), $city, $table_name='city');    
        return true;

    }


}



function get_rep_details($dom, $source, $city) {
        
     global $run_environment;

    //$html = scraperWiki::scrape($url);    
    //$dom = new simple_html_dom();
    //$dom->load($html);

    $content = $dom->find("div[id=ctl00_cphmain_pnlStaff]", 0)->find("table", 0);
    
    foreach($content->find("tr") as $row){
    
        
    
        $rep['title']     = trim($row->find("td", 0)->plaintext);
        $rep['name']    = trim($row->find("td", 1)->plaintext);

        $rep['city']    = $city;
        $rep['source']     = $source;
    
    
           if ($run_environment == 'dev') {
                $reps[] = $rep;
           } 
           else {
                scraperwiki::save_sqlite(array('name','title','city'), $rep, $table_name='reps');    
           }
    
    
    }
    
    if ($run_environment == 'dev') {            
        return $reps;
    }
    else {
        return true;
    }

}


?><?php

$run_environment = 'prod'; // either 'dev' or 'prod'
$max_records = 4; // only used for testing

if ($run_environment == 'dev') {
    error_reporting(E_ALL);     
    require 'scraperwiki.php';
}

require 'scraperwiki/simple_html_dom.php';


$url = "http://www.floridaleagueofcities.com/directory.aspx";

$city_list = get_city_list($url);

// $alldata = $city_list; 

$count = 1;
foreach ($city_list as $link) {
    
    $url = $link['source'];
    $city = $link['name'];
    
    if ($run_environment == 'prod') {
        get_city_data($city, $url);
    }
    else {
        $alldata[] = get_city_data($city, $url);
    }

    $count++;
    if ($run_environment == 'dev' && $count > $max_records) break;

}


// if testing
if ($run_environment == 'dev') {
    header('Content-type: application/json');
    print json_encode($alldata);
}



function get_city_list($url) {
        
    global $run_environment;
    global $max_records;

    $html = scraperWiki::scrape($url);    
    $dom = new simple_html_dom();
    $dom->load($html);
    
    // table/tr/td/div/table/tr/td[2]/table/tr/td/table/tr[5]
    $content = $dom->find("div[id=ctl00_cphmain_pnlIndex]", 0)->find("table", 1);

    $count = 0;
    foreach($content->find("a") as $link){
        
        if ($link->href) {

            $city['source'] = 'http://www.floridaleagueofcities.com' . $link->href;
            $city['name'] = $link->plaintext;

            $cities[] = $city;
        
             $count++;
        }

    }  

    // Clear memory
    $dom->__destruct();
    $content->__destruct();

     return $cities;

}



function get_city_data($name, $url) {
    
    global $run_environment;
    
    $html = scraperWiki::scrape($url);        
    $dom = new simple_html_dom();
    $dom->load($html);

    $count = 1;

    // for debugging
    if(!$dom->find("table", 0)) {
        echo $url; exit;
    }
    
    
    
    
    $content = $dom->find("div[id=ctl00_cphmain_pnlCityInfo]", 0)->find("table", 0);

    $city['source']                 = $url;
    $city['name']                     = $name;
                                
    $city['address']                 = trim($content->find("tr", 1)->find("td", 1)->plaintext);            
    $city['address_shipping']        = trim($content->find("tr", 2)->find("td", 1)->plaintext);                

    $city['phone']                     = trim($content->find("tr", 4)->find("td", 1)->plaintext);                
    $city['fax']                     = trim($content->find("tr", 5)->find("td", 1)->plaintext);                        
    
    $city['url']                     = ($content->find("tr", 7)->find("td", 1)->find("a", 0)) ? $content->find("tr", 7)->find("td", 1)->find("a", 0)->href : null;
    $city['email']                     = ($content->find("tr", 8)->find("td", 1)->find("a", 0)) ? $content->find("tr", 8)->find("td", 1)->find("a", 0)->href : null;

    $city['year_incorporated']         = trim($content->find("tr", 10)->find("td", 1)->plaintext);                        
    $city['population']             = trim($content->find("tr", 11)->find("td", 1)->plaintext);                        
    $city['county']                 = trim($content->find("tr", 12)->find("td", 1)->plaintext);        

    $city['city_history']             = ($content->find("tr", 14)->find("td", 1)) ? trim($content->find("tr", 14)->find("td", 1)->plaintext) : null;            
   
    // Get reps
    $rep_details = get_rep_details($dom, $url, $city['name']);
   
   
    // Clear memory
    $dom->__destruct();
    $content->__destruct();
   
    if ($run_environment == 'dev') {
        $city['reps'] = $rep_details;
        return $city;
    }
    else {
        scraperwiki::save_sqlite(array('name','source'), $city, $table_name='city');    
        return true;

    }


}



function get_rep_details($dom, $source, $city) {
        
     global $run_environment;

    //$html = scraperWiki::scrape($url);    
    //$dom = new simple_html_dom();
    //$dom->load($html);

    $content = $dom->find("div[id=ctl00_cphmain_pnlStaff]", 0)->find("table", 0);
    
    foreach($content->find("tr") as $row){
    
        
    
        $rep['title']     = trim($row->find("td", 0)->plaintext);
        $rep['name']    = trim($row->find("td", 1)->plaintext);

        $rep['city']    = $city;
        $rep['source']     = $source;
    
    
           if ($run_environment == 'dev') {
                $reps[] = $rep;
           } 
           else {
                scraperwiki::save_sqlite(array('name','title','city'), $rep, $table_name='reps');    
           }
    
    
    }
    
    if ($run_environment == 'dev') {            
        return $reps;
    }
    else {
        return true;
    }

}


?>