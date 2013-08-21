<?php

$run_environment = 'prod'; // either 'dev' or 'prod'
$max_records = 10; // only used for testing

if ($run_environment == 'dev') {
    error_reporting(E_ALL);
    ini_set('display_errors','On');    
}

if ($run_environment == 'dev') {
    require 'scraperwiki.php';
}

require 'scraperwiki/simple_html_dom.php';


$state_directory_url = "http://www.nga.org/cms/governors/bios";

$state_sources = get_state_sources($state_directory_url);



 $count = 1;
 foreach ($state_sources as $state_source) {
         
     $url     = $state_source['url'];
     $state     = $state_source['state'];    
     
     $state_records = get_state_data($url);    
     $state_records['state'] = $state;
     $state_records['source_url'] = $url;
      
     // if testing
    if ($run_environment == 'dev') {
        $alldata[] = $state_records;    
         if($count > $max_records) break;
        
        // for detailed debugged
        //print_r($state_records);
    } 
    
    // if scraperwiki
    else {
        scraperwiki::save(array('state'), $state_records);
    }
 
 $count++;
 }


// if testing
if ($run_environment == 'dev') {
    header('Content-type: application/json');
    print json_encode($alldata);
}

function get_state_sources($url) {
    
    
    $html = scraperWiki::scrape($url);

    $dom = new simple_html_dom();
    $dom->load($html);

    $count = 1;

    $table = $dom->find("div[id=container]", 0)->find("div[class=content-container]", 0)->find("div[class=col-layout-two]", 0)->find("div[class=list-basic]", 0)->find("div[class=columns3]", 0);

    foreach($table->find("div[class=column-item]") as $item){


                $item = $item->find("div[class=list-item]", 0);
                $state = $item->find("div[class=list-item-title]", 0)->plaintext;
                $governor = trim($item->find("div[class=list-item-summary]", 0)->plaintext);
                $url = $item->find('a', 0);
                $url = 'http://www.nga.org' . $url->href;
                

                $source[] = array('state' => $state, 'governor' => $governor, 'url' => $url);


    }

    
    return $source;
        
}


function get_state_data($url) {

    $html = scraperWiki::scrape($url);
    
    $dom = new simple_html_dom();
    $dom->load($html);

    $count = 1;
    
    $content = $dom->find("div[id=contentwrapper]", 0);

    $title = $content->find("div[class=article-title]", 0)->plaintext;
    
    // clean up weird spacing
    $title = trim(preg_replace('!\s+!', ' ', $title));
    $title = substr($title, strpos($title, 'Governor') + 9);
    
    $record['name'] = $title;
    
    
    $table = $content->find("table tr", 0);    
    $column = $table->find('td', 0);
    
    $record['url_photo'] = 'http://www.nga.org' . $column->find('img', 0)->src;
    
    if ($column->find('li', 0)) {
        
        $link_href = $column->find('li', 0)->find('a', 0)->href;
        $link_text = $column->find('li', 0)->find('a', 0)->plaintext;
        
        if ($link_text == "Governor's Website") {
            $record['url_governor'] = $link_href;
        }        
        
        if ($link_text == 'State Website') {
            $record['url_state'] = $link_href;
        }        
        
    }
    
    if ($column->find('li', 1)) {
        $record['url_state'] = $column->find('li', 1)->find('a', 0)->href;    
    }
    
    $column = $table->find('td', 2);
    $address = $column->find("div", 0);
    $address_name = $address->innertext;
    $address_name = trim(substr($address_name, strpos($address_name, '</span>')+7));
    $record['address_1'] = substr($address_name, 0, strpos($address_name, '<br>'));



    $record_1 = trim($address->find("div", 0)->plaintext);
    $record_2 = $address->find("div", 1)->plaintext;
    
    if(empty($record_2)){
        $record['address_2'] = null;            
        $address_full = $record_1;    
    }
    else {
        $record['address_2'] = $record_1;    
        $address_full = $record_2;            
    }
    
    $address_full = str_replace('&nbsp;', ' ', $address_full);    
    $address_full = trim(preg_replace('!\s+!', ' ', $address_full));    
    
    $record['address_city'] = substr($address_full, 0, strrpos($address_full, ', '));
    $record['address_state'] = substr($address_full, strrpos($address_full, ', ')+2, 2);
    $record['address_zip'] = substr($address_full, strrpos($address_full, ' ')+1);        
    
    // Phone number
    foreach($column->find("span[class=bio-stats-title]") as $data) {
        
        $field = trim($data->plaintext);

        if ($field == 'Phone:') {
                
            $phone = $data->parent();
            $phone = $phone->innertext;
            $phone = trim(substr($phone, strpos($phone, '</span>')+7));    
            $phone_clean = get_phone_numbers($phone);            

            if (!empty($phone_clean)) {
                $record['phone'] = $phone_clean[0];
            }
            else {
                $record['phone'] = null;
            }
            
            
        }
        
    }

    
    
    if (isset($record)) {
        return $record;
    }
    else {
        return 'hello';
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