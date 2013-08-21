<?php

$run_environment = 'prod'; // either 'dev' or 'prod'
$max_records = 10; // only used for testing

if ($run_environment == 'dev') {
    error_reporting(E_ALL);     
    require 'scraperwiki.php';
}

require 'scraperwiki/simple_html_dom.php';


$url = "http://council.nyc.gov/html/members/members.shtml";
$council_list = get_council_list($url);

$twitter_url = "https://twitter.com/NYCCouncil/nyccouncilmembers/members";
$twitter_list = get_council_twitter($twitter_url);

$council_list = merge_accounts($council_list, $twitter_list);

//$alldata = $twitter_list;
//$alldata = $council_list;

$count = 1;
foreach ($council_list as $district) {
    

    if ($run_environment == 'prod') {
        get_district_data($district);
    }
    else {
        $alldata[] = get_district_data($district);
    }

    $count++;
    if ($run_environment == 'dev' && $count > $max_records) break;

}


// if testing
if ($run_environment == 'dev') {
    header('Content-type: application/json');
    print json_encode($alldata);
}



function get_council_list($url) {
        
    global $run_environment;
    global $max_records;

    $html = scraperWiki::scrape($url);    
    $dom = new simple_html_dom();
    $dom->load($html);
    
    // table/tr/td/div/table/tr/td[2]/table/tr/td/table/tr[5]
    $content = $dom->find("table[id=members_table]", 0);

    $count = 1;
    foreach($content->find("tr") as $row){
        
        if ($count > 1) {
            $councilmember['name']         = $row->find("td", 0)->plaintext;
            $councilmember['source']     = 'http://council.nyc.gov' . $row->find("td", 0)->find("a", 0)->href;
            $councilmember['district']     = $row->find("td", 1)->plaintext;                
            $councilmember['borough']     = $row->find("td", 2)->plaintext;                
            $councilmember['party']     = $row->find("td", 3)->plaintext;                                

            $council[] = $councilmember;
        }

        $count++;

    }  

    // Clear memory
    $dom->__destruct();
    $content->__destruct();

     return $council;

}



function get_district_data($district) {
    
    global $run_environment;
    
    $html = scraperWiki::scrape($district['source']);        
    $dom = new simple_html_dom();
    $dom->load($html);

    $count = 1;




    // ################# Get Photo #################

    $photo = $dom->find("td[class=inside_top_image]", 0)->find("img", 0)->src;
    $district['image_url'] = rel2abs($photo, $district['source']);
    
    
    // ################# Check for Contact URL #################    
    
    
    $navlist = $dom->find("ul[class=members_subnav]", 0)->innertext;
    $navlist = get_between($navlist, 'NAV_NODES_MEMBERS = ', '];') . ']';

    $navlist = str_replace("','", "'###'", $navlist);
    $navlist = str_replace('[', '', $navlist);    
    $navlist = str_replace(']', '', $navlist);    
    $navlist = trim($navlist, ',');
    $navlist = explode(',', $navlist);
    
    foreach ($navlist as $item) {
        $item = explode('###', $item);
        if (strpos($item[0], 'Contact Council') && !empty($item[1])) {
            $link = '../..' . trim($item[1], "'");
            $link = rel2abs($link, $district['source']);
            
            $district['contact_url'] = $link;
        }
    }
    
    if(empty($district['contact_url'])) {
        $district['contact_url'] = null;
    }
        
    
    // ################# Get Contact info #################
    
    $contacts = $dom->find("td[class=nav_text]", 0)->innertext;
    $contacts = explode("<b>", $contacts);
                                            
    foreach ($contacts as $val) {
    
        $val = str_replace("</b>", "", $val);
        $val = trim($val); 
        $val = trim($val, "<br>");
        $val = trim($val);
        $val = explode("<br>", $val);    
        
        array_walk($val, create_function('&$val', '$val = trim($val);'));
        
        if($val[0]) {
            $val[0] = strtolower(str_replace(' ', '_', $val[0]));
            
            // Make sure the field wasn't misspelld :)
            if(strpos($val[0], 'legistlative') !== false) {
                $val[0] = str_replace('legistlative', 'legislative', $val[0]);
            }
            
            $field[$val[0]] = $val[1];
        }
            
    }            
    
    // check if we have a non-empty email address and strip away html
    if(!empty($field['email']) && strpos($field['email'], 'mailto') && strpos($field['email'], '><') === false) {
        $field['email'] = get_between($field['email'], 'mailto:', '">');
    } else {
        $field['email'] = null;
    }
                                

    $district = array_merge($district, $field);
   
    if ($run_environment == 'dev') {
        return $district;
    }
    else {
        scraperwiki::save_sqlite(array('name','source'), $district);    
        return true;

    }


}



function get_council_twitter($url) {
        
    global $run_environment;
    global $max_records;

    $html = scraperWiki::scrape($url);    
    $dom = new simple_html_dom();
    $dom->load($html);
    
    // See if we can get the cursor for the next page of html
    $cursor = $dom->find("div[class=stream-container]", 0)->outertext;
    $cursor = get_between($cursor, 'class="stream-container "', '<div class="stream list-stream">');
    $cursor = substr($cursor, strpos($cursor, 'data-cursor="') + 13);
    $cursor = substr($cursor, 0, strpos($cursor, '"'));    
    
    $next_page = "https://twitter.com/NYCCouncil/nyccouncilmembers/members/timeline?cursor=$cursor&include_available_features=1&include_entities=1&is_forward=true";
    $next_page = scraperWiki::scrape($next_page);    
    $next_page = json_decode($next_page, true);    
    
    //$next_page = curl_to_json($next_page);
    
    // Get the first page of html
    $content = $dom->find("ol[id=stream-items-id]", 0);

    // Combine it with the second page
    $content = $content->innertext .    $next_page["items_html"];

    $dom = new simple_html_dom();
    $dom->load($content);    

    $count = 1;
    foreach($dom->find("li") as $row){

        $councilmember['name']         = $row->find("div[class=stream-item-header]", 0)->find("strong[class=fullname]", 0)->plaintext;    
        $councilmember['username']     = $row->find("div[class=stream-item-header]", 0)->find("span[class=username]", 0)->plaintext;        
        
        $council[] = $councilmember;
        
        $count++;

    }  

     return $council;

}


function merge_accounts($council_list, $twitter_list) {
    
    global $run_environment;
    global $max_records;
    
    $count = 0;
    foreach ($council_list as $district) {
        
        $fullname = explode(' ', $district['name']);
        
        
        foreach($twitter_list as $account) {
            
            $match_count = 0;
            
        
            foreach ($fullname as $key => $name) {
            
                $name = trim($name, ',');
                $name = trim($name, '.');
                
                if (strlen($name) > 2) { // make sure we're not matching an initial or something
            
                    if(stripos($account['name'], $name) !== false) {
                        $match_count++;
                        if($key > 0) $match_count++; // we give extra credit if the matching name isn't the first name
                    }
                
                }
                
                
            }

            if($match_count > 1) {
                $district['twitter'] = $account['username'];
            } 

        }
        
        if(empty($district['twitter'])) $district['twitter'] = null;
    
        $districts[] = $district;


        $count++;
        //if ($run_environment == 'dev' && $count > $max_records) exit;                
    }
    
    return $districts;
    
}



function rel2abs($rel, $base)
{
    /* return if already absolute URL */
    if (parse_url($rel, PHP_URL_SCHEME) != '') return $rel;

    /* queries and anchors */
    if ($rel[0]=='#' || $rel[0]=='?') return $base.$rel;

    /* parse base URL and convert to local variables:
       $scheme, $host, $path */
    extract(parse_url($base));

    /* remove non-directory element from path */
    $path = preg_replace('#/[^/]*$#', '', $path);

    /* destroy path if relative url points to root */
    if ($rel[0] == '/') $path = '';

    /* dirty absolute URL */
    $abs = "$host$path/$rel";

    /* replace '//' or '/./' or '/foo/../' with '/' */
    $re = array('#(/\.?/)#', '#/(?!\.\.)[^/]+/\.\./#');
    for($n=1; $n>0; $abs=preg_replace($re, '/', $abs, -1, $n)) {}

    /* absolute URL is ready! */
    return $scheme.'://'.$abs;
}


function get_between($input, $start, $end)
{
  $substr = substr($input, strlen($start)+strpos($input, $start), (strlen($input) - strpos($input, $end))*(-1));
  return $substr;
}




?>