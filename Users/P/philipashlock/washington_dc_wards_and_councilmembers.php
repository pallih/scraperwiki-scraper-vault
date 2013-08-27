<?php

//require 'scraperwiki.php';
require 'scraperwiki/simple_html_dom.php';


$directory_url = "http://www.dccouncil.washington.dc.us/council";

$wards = get_ward_sources($directory_url);


foreach ($wards as $ward) {
    
    $records = get_ward_data($ward);
    
    scraperwiki::save(array('name'), $records);
    
}




//header('Content-type: application/json');
//print json_encode($records);


function get_ward_sources($url) {
    
    
    $html = scraperWiki::scrape($url);

    $dom = new simple_html_dom();
    $dom->load($html);

    $list = $dom->find("a[class=readmore-blue]");

    foreach($list as $link){
    
        $name = $link->plaintext;
        $url = $link->href;
    
        $wards[] = $url; // array('url' => $url, 'name' => $name);

    }
    
    return $wards;
        
}



function get_ward_data($url) {

    $html = scraperWiki::scrape($url);
    
    $dom = new simple_html_dom();
    $dom->load($html);

    $count = 1;
    
    $content = $dom->find("div[id=interior-main-content]", 0)->find("div[class=content-column]", 0)->find("div[class=content-section]", 0);
        

        $descriptor = $content->find("p[class=head-descriptor]", 0);
        $record['member_type'] = $descriptor->plaintext;
        
        $record['name'] = $content->find("h2", 0)->plaintext;
        
        $record['url_photo'] = 'http://www.dccouncil.washington.dc.us' . $content->find("div[id=member-thumb] img", 0)->src;
        
        $email = $content->find("div[id=member-thumb] a", 0)->href;
        
        if (substr($email, 0, 7) == 'mailto:'){
            $record['email'] = substr($email, 7, strlen($email)-7);
        } else {
            $record['email'] = null;
        }        
        
        // if no website listed, should use current url as website
        $website = $content->find("div[id=member-thumb] a", 1)->href;    
        if(empty($website)) $website = $url;
        $record['website'] = $website;
        
        // limit our scope to remaining content        
        foreach ($content->find("div[id=member-info] p") as $field) {
            $field_name = $field->find("strong", 0)->innertext;
            
            if (strpos($field_name, 'Term') !== false) {
                $field_data = $field->innertext;
                $field_data = substr($field_data, strpos($field_data, '</strong>')+10);                
                
                $term_start = substr($field_data, 0, strpos($field_data, ' - '));
                $term_end = substr($field_data, strpos($field_data, ' - ')+3);        
                $record['term_start'] = date("Y-m-d", strtotime($term_start));
                $record['term_end'] = date("Y-m-d", strtotime($term_end));                
            }
            
            if (strpos($field_name, 'Affiliation') !== false) {
                $field_data = $field->innertext;                
                $record['affiliation'] = substr($field_data, strpos($field_data, '</strong>')+10);                                                
            }            
            
            if (strpos($field_name, 'Office') !== false) {
                $field_data = $field->innertext;                
                $record['address'] = trim(substr($field_data, strpos($field_data, '</strong>')+10));                                                
            }                        
            
            if (strpos($field_name, 'Tel') !== false) {
                $phone = $field->find("a", 0)->innertext;
                $record['phone'] = trim($phone);                                
            }    
            
            if (strpos($field_name, 'Represents') !== false) {
                $ward = $field->find("a", 0);
                
                $record['ward_name'] = $ward->innertext;
                $record['ward_url'] = $ward->href;                            
            }                    
            
            
        }



    if (isset($record)) {
        return $record;
    }
    else {
        return 'hello';
    }
    
}







?><?php

//require 'scraperwiki.php';
require 'scraperwiki/simple_html_dom.php';


$directory_url = "http://www.dccouncil.washington.dc.us/council";

$wards = get_ward_sources($directory_url);


foreach ($wards as $ward) {
    
    $records = get_ward_data($ward);
    
    scraperwiki::save(array('name'), $records);
    
}




//header('Content-type: application/json');
//print json_encode($records);


function get_ward_sources($url) {
    
    
    $html = scraperWiki::scrape($url);

    $dom = new simple_html_dom();
    $dom->load($html);

    $list = $dom->find("a[class=readmore-blue]");

    foreach($list as $link){
    
        $name = $link->plaintext;
        $url = $link->href;
    
        $wards[] = $url; // array('url' => $url, 'name' => $name);

    }
    
    return $wards;
        
}



function get_ward_data($url) {

    $html = scraperWiki::scrape($url);
    
    $dom = new simple_html_dom();
    $dom->load($html);

    $count = 1;
    
    $content = $dom->find("div[id=interior-main-content]", 0)->find("div[class=content-column]", 0)->find("div[class=content-section]", 0);
        

        $descriptor = $content->find("p[class=head-descriptor]", 0);
        $record['member_type'] = $descriptor->plaintext;
        
        $record['name'] = $content->find("h2", 0)->plaintext;
        
        $record['url_photo'] = 'http://www.dccouncil.washington.dc.us' . $content->find("div[id=member-thumb] img", 0)->src;
        
        $email = $content->find("div[id=member-thumb] a", 0)->href;
        
        if (substr($email, 0, 7) == 'mailto:'){
            $record['email'] = substr($email, 7, strlen($email)-7);
        } else {
            $record['email'] = null;
        }        
        
        // if no website listed, should use current url as website
        $website = $content->find("div[id=member-thumb] a", 1)->href;    
        if(empty($website)) $website = $url;
        $record['website'] = $website;
        
        // limit our scope to remaining content        
        foreach ($content->find("div[id=member-info] p") as $field) {
            $field_name = $field->find("strong", 0)->innertext;
            
            if (strpos($field_name, 'Term') !== false) {
                $field_data = $field->innertext;
                $field_data = substr($field_data, strpos($field_data, '</strong>')+10);                
                
                $term_start = substr($field_data, 0, strpos($field_data, ' - '));
                $term_end = substr($field_data, strpos($field_data, ' - ')+3);        
                $record['term_start'] = date("Y-m-d", strtotime($term_start));
                $record['term_end'] = date("Y-m-d", strtotime($term_end));                
            }
            
            if (strpos($field_name, 'Affiliation') !== false) {
                $field_data = $field->innertext;                
                $record['affiliation'] = substr($field_data, strpos($field_data, '</strong>')+10);                                                
            }            
            
            if (strpos($field_name, 'Office') !== false) {
                $field_data = $field->innertext;                
                $record['address'] = trim(substr($field_data, strpos($field_data, '</strong>')+10));                                                
            }                        
            
            if (strpos($field_name, 'Tel') !== false) {
                $phone = $field->find("a", 0)->innertext;
                $record['phone'] = trim($phone);                                
            }    
            
            if (strpos($field_name, 'Represents') !== false) {
                $ward = $field->find("a", 0);
                
                $record['ward_name'] = $ward->innertext;
                $record['ward_url'] = $ward->href;                            
            }                    
            
            
        }



    if (isset($record)) {
        return $record;
    }
    else {
        return 'hello';
    }
    
}







?><?php

//require 'scraperwiki.php';
require 'scraperwiki/simple_html_dom.php';


$directory_url = "http://www.dccouncil.washington.dc.us/council";

$wards = get_ward_sources($directory_url);


foreach ($wards as $ward) {
    
    $records = get_ward_data($ward);
    
    scraperwiki::save(array('name'), $records);
    
}




//header('Content-type: application/json');
//print json_encode($records);


function get_ward_sources($url) {
    
    
    $html = scraperWiki::scrape($url);

    $dom = new simple_html_dom();
    $dom->load($html);

    $list = $dom->find("a[class=readmore-blue]");

    foreach($list as $link){
    
        $name = $link->plaintext;
        $url = $link->href;
    
        $wards[] = $url; // array('url' => $url, 'name' => $name);

    }
    
    return $wards;
        
}



function get_ward_data($url) {

    $html = scraperWiki::scrape($url);
    
    $dom = new simple_html_dom();
    $dom->load($html);

    $count = 1;
    
    $content = $dom->find("div[id=interior-main-content]", 0)->find("div[class=content-column]", 0)->find("div[class=content-section]", 0);
        

        $descriptor = $content->find("p[class=head-descriptor]", 0);
        $record['member_type'] = $descriptor->plaintext;
        
        $record['name'] = $content->find("h2", 0)->plaintext;
        
        $record['url_photo'] = 'http://www.dccouncil.washington.dc.us' . $content->find("div[id=member-thumb] img", 0)->src;
        
        $email = $content->find("div[id=member-thumb] a", 0)->href;
        
        if (substr($email, 0, 7) == 'mailto:'){
            $record['email'] = substr($email, 7, strlen($email)-7);
        } else {
            $record['email'] = null;
        }        
        
        // if no website listed, should use current url as website
        $website = $content->find("div[id=member-thumb] a", 1)->href;    
        if(empty($website)) $website = $url;
        $record['website'] = $website;
        
        // limit our scope to remaining content        
        foreach ($content->find("div[id=member-info] p") as $field) {
            $field_name = $field->find("strong", 0)->innertext;
            
            if (strpos($field_name, 'Term') !== false) {
                $field_data = $field->innertext;
                $field_data = substr($field_data, strpos($field_data, '</strong>')+10);                
                
                $term_start = substr($field_data, 0, strpos($field_data, ' - '));
                $term_end = substr($field_data, strpos($field_data, ' - ')+3);        
                $record['term_start'] = date("Y-m-d", strtotime($term_start));
                $record['term_end'] = date("Y-m-d", strtotime($term_end));                
            }
            
            if (strpos($field_name, 'Affiliation') !== false) {
                $field_data = $field->innertext;                
                $record['affiliation'] = substr($field_data, strpos($field_data, '</strong>')+10);                                                
            }            
            
            if (strpos($field_name, 'Office') !== false) {
                $field_data = $field->innertext;                
                $record['address'] = trim(substr($field_data, strpos($field_data, '</strong>')+10));                                                
            }                        
            
            if (strpos($field_name, 'Tel') !== false) {
                $phone = $field->find("a", 0)->innertext;
                $record['phone'] = trim($phone);                                
            }    
            
            if (strpos($field_name, 'Represents') !== false) {
                $ward = $field->find("a", 0);
                
                $record['ward_name'] = $ward->innertext;
                $record['ward_url'] = $ward->href;                            
            }                    
            
            
        }



    if (isset($record)) {
        return $record;
    }
    else {
        return 'hello';
    }
    
}







?>