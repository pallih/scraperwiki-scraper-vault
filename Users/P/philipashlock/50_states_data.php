<?php

//require 'scraperwiki.php';
require 'scraperwiki/simple_html_dom.php';


$state_directory_url = "http://answers.usa.gov/system/selfservice.controller?CONFIGURATION=1000&PARTITION_ID=1&CMD=VIEW_ARTICLE&ARTICLE_ID=9902&USERTYPE=1&LANGUAGE=en&COUNTRY=US";

$state_sources = get_state_sources($state_directory_url);


// Sort the array of states alphabetically
foreach ($state_sources as $key => $row) { $state[$key] = $row['state']; }
array_multisort($state, SORT_ASC, $state_sources);

$count = 1;
foreach ($state_sources as $state_source) {
        
    $url     = $state_source['url'];
    $state     = $state_source['state'];    
    
    $state_records = get_state_data($url);    
    $state_records['state'] = $state;
    $state_records['source_url'] = $url;
    
    scraperwiki::save(array('state'), $state_records);
     
    // used for testing, comment out for prod
    //$alldata[] = $state_records;    
    //if($count > 5) break;

$count++;
}


// used for testing, comment out for prod
//header('Content-type: application/json');
//print json_encode($alldata);


function get_state_sources($url) {
    
    
    $html = scraperWiki::scrape($url);

    $dom = new simple_html_dom();
    $dom->load($html);

    $count = 1;

    $table = $dom->find("div[id=dashboard_main_content] table", 0);

    foreach($table->find("tr") as $tr){

        foreach($tr->find("td") as $tds){

                $heading = $tds->plaintext;
                $url = $tds->find('a', 0);
                $url = $url->href;
                $url = htmlspecialchars_decode($url);


                $source[] = array ('state' => $heading, 'url' => $url);


        }


    }
    
    return $source;
        
}


function get_state_data($url) {

    $html = scraperWiki::scrape($url);
    
    $dom = new simple_html_dom();
    $dom->load($html);

    $count = 1;
    
    foreach($dom->find("div[id=dashboard_main_content] tr") as $data){
        
    
        $ths = $data->find("th");
        $tds = $data->find("td");

        $heading = $ths[0]->plaintext;
        $object = $tds[0];
        $value = $object->plaintext;

            if(!$heading) {
                $heading = "Extra Field $count:";
                $count++;            
            }

            $heading = substr($heading, 0, strpos($heading, ":"));
            $clean_heading = str_replace(' ', '_', strtolower($heading));

            $record[$clean_heading] = $value;

            if ($clean_heading == 'official_name' ||
                $clean_heading == 'information'      ||
                $clean_heading == 'governor') {
                    foreach ($object->find("a") as $link) {
                        $link = $link->href;
                        $new_heading = $clean_heading . "_url";

                        if (substr($link, 0, 7) == 'mailto:'){
                            $record['email'] = substr($link, 7, strlen($link)-7);
                        }
                        else {
                            $heading = "$heading URL";
                            $record[$new_heading] = $link;
                        }
                    }
                    
            }
            
            if ($clean_heading == 'information') {
                    $phone_numbers = get_phone_numbers($value);
                     $record['phone_primary'] = ($phone_numbers[0]) ? $phone_numbers[0] : '';
                     $record['phone_secondary'] = ($phone_numbers[1]) ? $phone_numbers[1] : '';
            }

    }   

    if(!isset($record['email'])) {
        $record['email'] = null    ;
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



?><?php

//require 'scraperwiki.php';
require 'scraperwiki/simple_html_dom.php';


$state_directory_url = "http://answers.usa.gov/system/selfservice.controller?CONFIGURATION=1000&PARTITION_ID=1&CMD=VIEW_ARTICLE&ARTICLE_ID=9902&USERTYPE=1&LANGUAGE=en&COUNTRY=US";

$state_sources = get_state_sources($state_directory_url);


// Sort the array of states alphabetically
foreach ($state_sources as $key => $row) { $state[$key] = $row['state']; }
array_multisort($state, SORT_ASC, $state_sources);

$count = 1;
foreach ($state_sources as $state_source) {
        
    $url     = $state_source['url'];
    $state     = $state_source['state'];    
    
    $state_records = get_state_data($url);    
    $state_records['state'] = $state;
    $state_records['source_url'] = $url;
    
    scraperwiki::save(array('state'), $state_records);
     
    // used for testing, comment out for prod
    //$alldata[] = $state_records;    
    //if($count > 5) break;

$count++;
}


// used for testing, comment out for prod
//header('Content-type: application/json');
//print json_encode($alldata);


function get_state_sources($url) {
    
    
    $html = scraperWiki::scrape($url);

    $dom = new simple_html_dom();
    $dom->load($html);

    $count = 1;

    $table = $dom->find("div[id=dashboard_main_content] table", 0);

    foreach($table->find("tr") as $tr){

        foreach($tr->find("td") as $tds){

                $heading = $tds->plaintext;
                $url = $tds->find('a', 0);
                $url = $url->href;
                $url = htmlspecialchars_decode($url);


                $source[] = array ('state' => $heading, 'url' => $url);


        }


    }
    
    return $source;
        
}


function get_state_data($url) {

    $html = scraperWiki::scrape($url);
    
    $dom = new simple_html_dom();
    $dom->load($html);

    $count = 1;
    
    foreach($dom->find("div[id=dashboard_main_content] tr") as $data){
        
    
        $ths = $data->find("th");
        $tds = $data->find("td");

        $heading = $ths[0]->plaintext;
        $object = $tds[0];
        $value = $object->plaintext;

            if(!$heading) {
                $heading = "Extra Field $count:";
                $count++;            
            }

            $heading = substr($heading, 0, strpos($heading, ":"));
            $clean_heading = str_replace(' ', '_', strtolower($heading));

            $record[$clean_heading] = $value;

            if ($clean_heading == 'official_name' ||
                $clean_heading == 'information'      ||
                $clean_heading == 'governor') {
                    foreach ($object->find("a") as $link) {
                        $link = $link->href;
                        $new_heading = $clean_heading . "_url";

                        if (substr($link, 0, 7) == 'mailto:'){
                            $record['email'] = substr($link, 7, strlen($link)-7);
                        }
                        else {
                            $heading = "$heading URL";
                            $record[$new_heading] = $link;
                        }
                    }
                    
            }
            
            if ($clean_heading == 'information') {
                    $phone_numbers = get_phone_numbers($value);
                     $record['phone_primary'] = ($phone_numbers[0]) ? $phone_numbers[0] : '';
                     $record['phone_secondary'] = ($phone_numbers[1]) ? $phone_numbers[1] : '';
            }

    }   

    if(!isset($record['email'])) {
        $record['email'] = null    ;
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



?><?php

//require 'scraperwiki.php';
require 'scraperwiki/simple_html_dom.php';


$state_directory_url = "http://answers.usa.gov/system/selfservice.controller?CONFIGURATION=1000&PARTITION_ID=1&CMD=VIEW_ARTICLE&ARTICLE_ID=9902&USERTYPE=1&LANGUAGE=en&COUNTRY=US";

$state_sources = get_state_sources($state_directory_url);


// Sort the array of states alphabetically
foreach ($state_sources as $key => $row) { $state[$key] = $row['state']; }
array_multisort($state, SORT_ASC, $state_sources);

$count = 1;
foreach ($state_sources as $state_source) {
        
    $url     = $state_source['url'];
    $state     = $state_source['state'];    
    
    $state_records = get_state_data($url);    
    $state_records['state'] = $state;
    $state_records['source_url'] = $url;
    
    scraperwiki::save(array('state'), $state_records);
     
    // used for testing, comment out for prod
    //$alldata[] = $state_records;    
    //if($count > 5) break;

$count++;
}


// used for testing, comment out for prod
//header('Content-type: application/json');
//print json_encode($alldata);


function get_state_sources($url) {
    
    
    $html = scraperWiki::scrape($url);

    $dom = new simple_html_dom();
    $dom->load($html);

    $count = 1;

    $table = $dom->find("div[id=dashboard_main_content] table", 0);

    foreach($table->find("tr") as $tr){

        foreach($tr->find("td") as $tds){

                $heading = $tds->plaintext;
                $url = $tds->find('a', 0);
                $url = $url->href;
                $url = htmlspecialchars_decode($url);


                $source[] = array ('state' => $heading, 'url' => $url);


        }


    }
    
    return $source;
        
}


function get_state_data($url) {

    $html = scraperWiki::scrape($url);
    
    $dom = new simple_html_dom();
    $dom->load($html);

    $count = 1;
    
    foreach($dom->find("div[id=dashboard_main_content] tr") as $data){
        
    
        $ths = $data->find("th");
        $tds = $data->find("td");

        $heading = $ths[0]->plaintext;
        $object = $tds[0];
        $value = $object->plaintext;

            if(!$heading) {
                $heading = "Extra Field $count:";
                $count++;            
            }

            $heading = substr($heading, 0, strpos($heading, ":"));
            $clean_heading = str_replace(' ', '_', strtolower($heading));

            $record[$clean_heading] = $value;

            if ($clean_heading == 'official_name' ||
                $clean_heading == 'information'      ||
                $clean_heading == 'governor') {
                    foreach ($object->find("a") as $link) {
                        $link = $link->href;
                        $new_heading = $clean_heading . "_url";

                        if (substr($link, 0, 7) == 'mailto:'){
                            $record['email'] = substr($link, 7, strlen($link)-7);
                        }
                        else {
                            $heading = "$heading URL";
                            $record[$new_heading] = $link;
                        }
                    }
                    
            }
            
            if ($clean_heading == 'information') {
                    $phone_numbers = get_phone_numbers($value);
                     $record['phone_primary'] = ($phone_numbers[0]) ? $phone_numbers[0] : '';
                     $record['phone_secondary'] = ($phone_numbers[1]) ? $phone_numbers[1] : '';
            }

    }   

    if(!isset($record['email'])) {
        $record['email'] = null    ;
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



?><?php

//require 'scraperwiki.php';
require 'scraperwiki/simple_html_dom.php';


$state_directory_url = "http://answers.usa.gov/system/selfservice.controller?CONFIGURATION=1000&PARTITION_ID=1&CMD=VIEW_ARTICLE&ARTICLE_ID=9902&USERTYPE=1&LANGUAGE=en&COUNTRY=US";

$state_sources = get_state_sources($state_directory_url);


// Sort the array of states alphabetically
foreach ($state_sources as $key => $row) { $state[$key] = $row['state']; }
array_multisort($state, SORT_ASC, $state_sources);

$count = 1;
foreach ($state_sources as $state_source) {
        
    $url     = $state_source['url'];
    $state     = $state_source['state'];    
    
    $state_records = get_state_data($url);    
    $state_records['state'] = $state;
    $state_records['source_url'] = $url;
    
    scraperwiki::save(array('state'), $state_records);
     
    // used for testing, comment out for prod
    //$alldata[] = $state_records;    
    //if($count > 5) break;

$count++;
}


// used for testing, comment out for prod
//header('Content-type: application/json');
//print json_encode($alldata);


function get_state_sources($url) {
    
    
    $html = scraperWiki::scrape($url);

    $dom = new simple_html_dom();
    $dom->load($html);

    $count = 1;

    $table = $dom->find("div[id=dashboard_main_content] table", 0);

    foreach($table->find("tr") as $tr){

        foreach($tr->find("td") as $tds){

                $heading = $tds->plaintext;
                $url = $tds->find('a', 0);
                $url = $url->href;
                $url = htmlspecialchars_decode($url);


                $source[] = array ('state' => $heading, 'url' => $url);


        }


    }
    
    return $source;
        
}


function get_state_data($url) {

    $html = scraperWiki::scrape($url);
    
    $dom = new simple_html_dom();
    $dom->load($html);

    $count = 1;
    
    foreach($dom->find("div[id=dashboard_main_content] tr") as $data){
        
    
        $ths = $data->find("th");
        $tds = $data->find("td");

        $heading = $ths[0]->plaintext;
        $object = $tds[0];
        $value = $object->plaintext;

            if(!$heading) {
                $heading = "Extra Field $count:";
                $count++;            
            }

            $heading = substr($heading, 0, strpos($heading, ":"));
            $clean_heading = str_replace(' ', '_', strtolower($heading));

            $record[$clean_heading] = $value;

            if ($clean_heading == 'official_name' ||
                $clean_heading == 'information'      ||
                $clean_heading == 'governor') {
                    foreach ($object->find("a") as $link) {
                        $link = $link->href;
                        $new_heading = $clean_heading . "_url";

                        if (substr($link, 0, 7) == 'mailto:'){
                            $record['email'] = substr($link, 7, strlen($link)-7);
                        }
                        else {
                            $heading = "$heading URL";
                            $record[$new_heading] = $link;
                        }
                    }
                    
            }
            
            if ($clean_heading == 'information') {
                    $phone_numbers = get_phone_numbers($value);
                     $record['phone_primary'] = ($phone_numbers[0]) ? $phone_numbers[0] : '';
                     $record['phone_secondary'] = ($phone_numbers[1]) ? $phone_numbers[1] : '';
            }

    }   

    if(!isset($record['email'])) {
        $record['email'] = null    ;
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