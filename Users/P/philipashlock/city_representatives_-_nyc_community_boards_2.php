<?php

$run_environment = 'prod'; // either 'dev' or 'prod'
$max_records = 5; // only used for testing

if ($run_environment == 'dev') {
    error_reporting(E_ALL);     
    require 'scraperwiki.php';
}

require 'scraperwiki/simple_html_dom.php';


$url = "http://www.nyc.gov/html/cau/html/cb/cb.shtml";

$link_list = get_link_list($url);

//$alldata = $link_list; 

$count = 1;
 foreach ($link_list as $link) {
     
    //if($count < 3) {
    //    $count++;
    //    continue;
    //}

     $url = $link['source'];
     $city = $link['name'];
     
     if ($run_environment == 'prod') {
         get_cb_data($city, $url);
     }
     else {
         $alldata[] = get_cb_data($city, $url);
     }

    $count++;
      if ($run_environment == 'dev' && $count > $max_records) break;
 
 }


// if testing
if ($run_environment == 'dev') {
    header('Content-type: application/json');
    print json_encode($alldata);
}



function get_link_list($url) {
        
    global $run_environment;
    global $max_records;

    $html = scraperWiki::scrape($url);    
    $dom = new simple_html_dom();
    $dom->load($html);
    
    $content = $dom->find("td[id=main_content]", 0)->find("table", 0)->find("span[class=bodytext]", 1);

    $count = 1;
    foreach($content->find("a") as $link){
        
        if($link->href && strpos($link->plaintext, 'CBs') !== FALSE) {

            $url = rel2abs($link->href, $url);
            $name = substr($link->plaintext, 0, strpos($link->plaintext, ' CBs'));
            

            $borough['source']     = $url;
            $borough['name']     = $name;

            $links[] = $borough;
    
             $count++;
        
        }


    }  

    // Clear memory
    $dom->__destruct();
    $content->__destruct();

     return $links;

}



function get_cb_data($name, $url) {
    
    global $run_environment;
    global $max_records;

    
    $html = scraperWiki::scrape($url);        
    $dom = new simple_html_dom();
    $dom->load($html);

    $count = 1;


    foreach($dom->find("table[class=cb_table]") as $board) {
        $cb = null;

        $cb['source']                     = $url;
        $cb['borough']                     = $name;

        $cb['community_board']             = trim($board->find("td[class=cb_title]", 0)->plaintext);    
        
        $cb['community_board_number']    = trim(substr($cb['community_board'], strlen('Community Board ')));
                

        $cb['city_id'] = get_city_id($cb['borough'], $cb['community_board_number']);

        $cb['neighborhoods']         = trim($board->find("tr", 1)->find("td", 2)->plaintext);                        
        $cb['precincts']             = trim($board->find("tr", 4)->find("td", 1)->plaintext);        
        $cb['precinct_phones']         = trim($board->find("tr", 5)->find("td", 1)->plaintext);        


        // Try to parse the unstructured contact info text
        $cb_info     = trim($board->find("tr", 3)->find("td", 1)->innertext);    
        $cb_info     = str_replace('<strong>', '<b>', $cb_info);
        $cb_info     = str_replace('</strong>', '</b>', $cb_info);        
        
        $contacts     = explode("<b>", $cb_info);

        foreach ($contacts as $val) {

            $val = str_replace("<br />", ",", $val);
            $val = trim($val); 
            $val = explode("</b>", $val);    

            array_walk($val, create_function('&$val', '$val = trim($val);'));

            if(!empty($val[1])) {
                $heading = trim($val[0], ",");
                $heading = trim($heading, ":");
                $heading = strtolower(str_replace(' ', '_', $heading));

                // Clean up stray html tags
                if(stripos($val[1], '<span>')) {
                    $val[1] = get_between($val[1], '<span>', '</span>');
                }
                
                $val[1] = trim($val[1], '</p>');
                $val[1] = trim($val[1], ',');
                $val[1] = trim($val[1], ',');                
                
                

                $cb[$heading] = $val[1];
            }

        }            

        // check if we have data in the email field that needs to be parsed like the website url
        if(!empty($cb['address'])) {
                
            $cb['address'] = trim($cb['address']);
            $cb['address'] = trim($cb['address'], ',');    
            $cb['address'] = str_replace(",,", ",", $cb['address']);        
            $cb['address'] = trim($cb['address']);                            
                

            $lines = explode(',', $cb['address']);
            $line_num = count($lines) - 1;
            
            if ($line_num >= 4) {
                $cb['address_title']     = $lines[$line_num - 4]; 
            } else {
                $cb['address_title']     = $cb['borough'] . ' ' . $cb['community_board'];
            }            
            
            if ($cb['address_title'] == $lines[$line_num - 3]) {
                $cb['address_1'] = $lines[$line_num - 2];
                $cb['address_2'] = null;
            } else {
                $cb['address_1'] = $lines[$line_num - 3];
                $cb['address_2'] = $lines[$line_num - 2];                
            }
            
            $zip = trim($lines[$line_num], ', NY '); 

            $cb['address_zip']         = $zip;
            $cb['address_city']     = $lines[$line_num - 1]; 
            $cb['address_state']     = 'NY';        


        }


        // check if we have data in the email field that needs to be parsed like the website url
        if(!empty($cb['email'])) {
            
            $snippet = new simple_html_dom();
            $snippet->load($cb['email']);
            
            if($snippet->find('a',0)) {
                
                // Isolate the email address from the other html
                if (stripos($cb['email'], '<a') > 0) {
                    $cb['email'] = trim(substr($cb['email'], 0, stripos($cb['email'], '<a')));
                    
                    if(count($emails = explode(',', $cb['email'])) > 1) {    
                        $cb['all_email'] = $cb['email'];
                        $cb['email']      = trim($emails[0]);
                        $cb['email']      = trim($cb['email'], '&#160;');
                        
                        
                                                
                    }

                } else {
                    $cb['email'] = null;
                    $cb['website'] = null;
                }
                            
                $cb['website'] = $snippet->find('a',0)->href;
                
                // External URLs have a proxy URL on nyc.gov, let's parse that off
                if (stripos($cb['website'], 'exit.pl')) {                
                    $cb['website'] = substr($cb['website'], stripos($cb['website'], 'exit.pl?') + 12);
                }
                
            } else {
                $cb['website'] = null;                
            }
            
        } else {
            $cb['email'] = null;
        }
        
        // Make this field universal, even if we don't have any data
        if(empty($cb['all_email'])) $cb['all_email'] = null;

        // verify we didn't mix up website and email
        if(!empty($cb['website']) && stripos($cb['website'], 'mailto') !== FALSE) {
            $cb['email'] = substr($cb['website'], stripos($cb['website'], 'mailto:') + 7);
            $cb['website'] = null;
        }

        // Be sure to clear any stray commas
        if(!empty($cb['email']))  $cb['email'] = trim($cb['email'], ',');                   

        // normalize field names
        if(!empty($cb['chairperson'])) {
            $cb['chair'] = $cb['chairperson'];
            unset($cb['chairperson']);
        }


       if ($run_environment == 'dev') {
            $cbs[] = $cb;
        }
        else {
            scraperwiki::save_sqlite(array('source','borough','community_board_number'), $cb, $table_name='community_board');    
        }

        $count++;
         //if ($run_environment == 'dev' && $count > $max_records) break;

       // Clear memory
        $board->__destruct();

    }

    // Clear memory
    $dom->__destruct();
   
    if ($run_environment == 'dev') {
        return $cbs;
    }
    else {
        return true;

    }


}


function get_city_id($borough, $board_id) {
    
    switch ($borough) {
        case 'Manhattan':
            $borough_id = '1';
            break;
        case 'Bronx':
            $borough_id = '2';
            break;
        case 'Brooklyn':
            $borough_id = '3';
            break;
        case 'Queens':
            $borough_id = '4';
            break;        
        case 'Staten Island':
            $borough_id = '5';
            break;    
    }    
    
    if ($board_id < 10) {
        $board_id = '0' . $board_id;
    }

    return $borough_id . $board_id;
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


?><?php

$run_environment = 'prod'; // either 'dev' or 'prod'
$max_records = 5; // only used for testing

if ($run_environment == 'dev') {
    error_reporting(E_ALL);     
    require 'scraperwiki.php';
}

require 'scraperwiki/simple_html_dom.php';


$url = "http://www.nyc.gov/html/cau/html/cb/cb.shtml";

$link_list = get_link_list($url);

//$alldata = $link_list; 

$count = 1;
 foreach ($link_list as $link) {
     
    //if($count < 3) {
    //    $count++;
    //    continue;
    //}

     $url = $link['source'];
     $city = $link['name'];
     
     if ($run_environment == 'prod') {
         get_cb_data($city, $url);
     }
     else {
         $alldata[] = get_cb_data($city, $url);
     }

    $count++;
      if ($run_environment == 'dev' && $count > $max_records) break;
 
 }


// if testing
if ($run_environment == 'dev') {
    header('Content-type: application/json');
    print json_encode($alldata);
}



function get_link_list($url) {
        
    global $run_environment;
    global $max_records;

    $html = scraperWiki::scrape($url);    
    $dom = new simple_html_dom();
    $dom->load($html);
    
    $content = $dom->find("td[id=main_content]", 0)->find("table", 0)->find("span[class=bodytext]", 1);

    $count = 1;
    foreach($content->find("a") as $link){
        
        if($link->href && strpos($link->plaintext, 'CBs') !== FALSE) {

            $url = rel2abs($link->href, $url);
            $name = substr($link->plaintext, 0, strpos($link->plaintext, ' CBs'));
            

            $borough['source']     = $url;
            $borough['name']     = $name;

            $links[] = $borough;
    
             $count++;
        
        }


    }  

    // Clear memory
    $dom->__destruct();
    $content->__destruct();

     return $links;

}



function get_cb_data($name, $url) {
    
    global $run_environment;
    global $max_records;

    
    $html = scraperWiki::scrape($url);        
    $dom = new simple_html_dom();
    $dom->load($html);

    $count = 1;


    foreach($dom->find("table[class=cb_table]") as $board) {
        $cb = null;

        $cb['source']                     = $url;
        $cb['borough']                     = $name;

        $cb['community_board']             = trim($board->find("td[class=cb_title]", 0)->plaintext);    
        
        $cb['community_board_number']    = trim(substr($cb['community_board'], strlen('Community Board ')));
                

        $cb['city_id'] = get_city_id($cb['borough'], $cb['community_board_number']);

        $cb['neighborhoods']         = trim($board->find("tr", 1)->find("td", 2)->plaintext);                        
        $cb['precincts']             = trim($board->find("tr", 4)->find("td", 1)->plaintext);        
        $cb['precinct_phones']         = trim($board->find("tr", 5)->find("td", 1)->plaintext);        


        // Try to parse the unstructured contact info text
        $cb_info     = trim($board->find("tr", 3)->find("td", 1)->innertext);    
        $cb_info     = str_replace('<strong>', '<b>', $cb_info);
        $cb_info     = str_replace('</strong>', '</b>', $cb_info);        
        
        $contacts     = explode("<b>", $cb_info);

        foreach ($contacts as $val) {

            $val = str_replace("<br />", ",", $val);
            $val = trim($val); 
            $val = explode("</b>", $val);    

            array_walk($val, create_function('&$val', '$val = trim($val);'));

            if(!empty($val[1])) {
                $heading = trim($val[0], ",");
                $heading = trim($heading, ":");
                $heading = strtolower(str_replace(' ', '_', $heading));

                // Clean up stray html tags
                if(stripos($val[1], '<span>')) {
                    $val[1] = get_between($val[1], '<span>', '</span>');
                }
                
                $val[1] = trim($val[1], '</p>');
                $val[1] = trim($val[1], ',');
                $val[1] = trim($val[1], ',');                
                
                

                $cb[$heading] = $val[1];
            }

        }            

        // check if we have data in the email field that needs to be parsed like the website url
        if(!empty($cb['address'])) {
                
            $cb['address'] = trim($cb['address']);
            $cb['address'] = trim($cb['address'], ',');    
            $cb['address'] = str_replace(",,", ",", $cb['address']);        
            $cb['address'] = trim($cb['address']);                            
                

            $lines = explode(',', $cb['address']);
            $line_num = count($lines) - 1;
            
            if ($line_num >= 4) {
                $cb['address_title']     = $lines[$line_num - 4]; 
            } else {
                $cb['address_title']     = $cb['borough'] . ' ' . $cb['community_board'];
            }            
            
            if ($cb['address_title'] == $lines[$line_num - 3]) {
                $cb['address_1'] = $lines[$line_num - 2];
                $cb['address_2'] = null;
            } else {
                $cb['address_1'] = $lines[$line_num - 3];
                $cb['address_2'] = $lines[$line_num - 2];                
            }
            
            $zip = trim($lines[$line_num], ', NY '); 

            $cb['address_zip']         = $zip;
            $cb['address_city']     = $lines[$line_num - 1]; 
            $cb['address_state']     = 'NY';        


        }


        // check if we have data in the email field that needs to be parsed like the website url
        if(!empty($cb['email'])) {
            
            $snippet = new simple_html_dom();
            $snippet->load($cb['email']);
            
            if($snippet->find('a',0)) {
                
                // Isolate the email address from the other html
                if (stripos($cb['email'], '<a') > 0) {
                    $cb['email'] = trim(substr($cb['email'], 0, stripos($cb['email'], '<a')));
                    
                    if(count($emails = explode(',', $cb['email'])) > 1) {    
                        $cb['all_email'] = $cb['email'];
                        $cb['email']      = trim($emails[0]);
                        $cb['email']      = trim($cb['email'], '&#160;');
                        
                        
                                                
                    }

                } else {
                    $cb['email'] = null;
                    $cb['website'] = null;
                }
                            
                $cb['website'] = $snippet->find('a',0)->href;
                
                // External URLs have a proxy URL on nyc.gov, let's parse that off
                if (stripos($cb['website'], 'exit.pl')) {                
                    $cb['website'] = substr($cb['website'], stripos($cb['website'], 'exit.pl?') + 12);
                }
                
            } else {
                $cb['website'] = null;                
            }
            
        } else {
            $cb['email'] = null;
        }
        
        // Make this field universal, even if we don't have any data
        if(empty($cb['all_email'])) $cb['all_email'] = null;

        // verify we didn't mix up website and email
        if(!empty($cb['website']) && stripos($cb['website'], 'mailto') !== FALSE) {
            $cb['email'] = substr($cb['website'], stripos($cb['website'], 'mailto:') + 7);
            $cb['website'] = null;
        }

        // Be sure to clear any stray commas
        if(!empty($cb['email']))  $cb['email'] = trim($cb['email'], ',');                   

        // normalize field names
        if(!empty($cb['chairperson'])) {
            $cb['chair'] = $cb['chairperson'];
            unset($cb['chairperson']);
        }


       if ($run_environment == 'dev') {
            $cbs[] = $cb;
        }
        else {
            scraperwiki::save_sqlite(array('source','borough','community_board_number'), $cb, $table_name='community_board');    
        }

        $count++;
         //if ($run_environment == 'dev' && $count > $max_records) break;

       // Clear memory
        $board->__destruct();

    }

    // Clear memory
    $dom->__destruct();
   
    if ($run_environment == 'dev') {
        return $cbs;
    }
    else {
        return true;

    }


}


function get_city_id($borough, $board_id) {
    
    switch ($borough) {
        case 'Manhattan':
            $borough_id = '1';
            break;
        case 'Bronx':
            $borough_id = '2';
            break;
        case 'Brooklyn':
            $borough_id = '3';
            break;
        case 'Queens':
            $borough_id = '4';
            break;        
        case 'Staten Island':
            $borough_id = '5';
            break;    
    }    
    
    if ($board_id < 10) {
        $board_id = '0' . $board_id;
    }

    return $borough_id . $board_id;
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