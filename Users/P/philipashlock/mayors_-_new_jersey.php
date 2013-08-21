<?php

$run_environment = 'prod'; // either 'dev' or 'prod'
$max_records = 20; // only used for testing

if ($run_environment == 'dev') {
    error_reporting(E_ALL);
    ini_set('display_errors','On');    

    require 'scraperwiki.php';

} 


require 'scraperwiki/simple_html_dom.php';

$url = 'http://www.state.nj.us/dca/home/20120809mayors.csv';

$output = get_sources($url);


if ($run_environment == 'dev') {
    header('Content-type: application/json');
    print json_encode($output);
}

function get_sources($url) {
    
    global $run_environment;
    global $max_records;


    $csv = scraperWiki::scrape($url);    


    $lines = explode("\n", $csv); 
    $count = 1;

    // Each Row
    foreach($lines as $line) {

        $line = str_getcsv($line);

        // Reset rep array
        $rep = array();

        // Each column
        foreach ($line as $key => $value) {
            
    
            // If we're at the first line, set column headings
            if($count == 1) {
                
                if($value) {
                    $headings[$key] = strtolower(str_replace(' ', '_', $value));
                }
            // Otherwise use column headings to set new values in the array                
            } else {
                
                if($headings[$key] == 'zip')                     $value = trim($value, "'");
                if(empty($value))                                 $value = null;
                if(strpos($headings[$key], 'term') !== FALSE)    $value = date("Y-m-d", strtotime($value));
                
                if($headings[$key] == 'address_1' && $value) {
                    
                    $addr_words = explode(' ', $value);
                    
                    // Check to see if this line of the address includes numbers or anything to ensure it's an address
                    if (preg_match('/[0-9]/', $value) == 1 || num_word_search($addr_words[0]) || stripos($value, 'Post Office Box') !== FALSE) {
                        $rep['address_name'] = null;
                        $lineswap[$count] = FALSE;
                    } else {
                        $rep['address_name'] = $value;
                        $lineswap[$count] = TRUE;
                        continue;
                    }
                }
                
                if($headings[$key] == 'address_2' && $lineswap[$count] && $value) {
                        $rep['address_1'] = $value;    
                        $rep['address_2'] = NULL;                
                } else {
                    $rep[$headings[$key]] = $value;                    
                }
                            

            }                
        
        }    
        
        if($count > 1) {

            if ($run_environment == 'dev') {
                $reps[] = $rep;
                if($count > $max_records) break;                
            }

            if ($run_environment == 'prod') {            
                scraperwiki::save(array('muni_code'), $rep);
            }
            
        }
                    
        $count++;
        
    }


    if ($run_environment == 'dev') {    
        return $reps;    
    } else {
        return true;
    }
    

}


function strposa($haystack, $needles=array(), $offset=0) {
    

        $chr = array();
        foreach($needles as $needle) {
                $res = stripos($haystack, $needle, $offset);
                if ($res !== false) $chr[$needle] = $res;
        }

        if(empty($chr)) return false;
        return min($chr);
}


function num_word_search($string) {
    
    
    $array  = array('one', 
                    'two', 
                    'three', 
                    'four', 
                    'five', 
                    'six', 
                    'seven',
                    'eight', 
                    'nine',
                    'ten');

    if (strposa($string, $array) !== FALSE) {
        return true;
    } else {
        return false;
    }    
    
    
}



?><?php

$run_environment = 'prod'; // either 'dev' or 'prod'
$max_records = 20; // only used for testing

if ($run_environment == 'dev') {
    error_reporting(E_ALL);
    ini_set('display_errors','On');    

    require 'scraperwiki.php';

} 


require 'scraperwiki/simple_html_dom.php';

$url = 'http://www.state.nj.us/dca/home/20120809mayors.csv';

$output = get_sources($url);


if ($run_environment == 'dev') {
    header('Content-type: application/json');
    print json_encode($output);
}

function get_sources($url) {
    
    global $run_environment;
    global $max_records;


    $csv = scraperWiki::scrape($url);    


    $lines = explode("\n", $csv); 
    $count = 1;

    // Each Row
    foreach($lines as $line) {

        $line = str_getcsv($line);

        // Reset rep array
        $rep = array();

        // Each column
        foreach ($line as $key => $value) {
            
    
            // If we're at the first line, set column headings
            if($count == 1) {
                
                if($value) {
                    $headings[$key] = strtolower(str_replace(' ', '_', $value));
                }
            // Otherwise use column headings to set new values in the array                
            } else {
                
                if($headings[$key] == 'zip')                     $value = trim($value, "'");
                if(empty($value))                                 $value = null;
                if(strpos($headings[$key], 'term') !== FALSE)    $value = date("Y-m-d", strtotime($value));
                
                if($headings[$key] == 'address_1' && $value) {
                    
                    $addr_words = explode(' ', $value);
                    
                    // Check to see if this line of the address includes numbers or anything to ensure it's an address
                    if (preg_match('/[0-9]/', $value) == 1 || num_word_search($addr_words[0]) || stripos($value, 'Post Office Box') !== FALSE) {
                        $rep['address_name'] = null;
                        $lineswap[$count] = FALSE;
                    } else {
                        $rep['address_name'] = $value;
                        $lineswap[$count] = TRUE;
                        continue;
                    }
                }
                
                if($headings[$key] == 'address_2' && $lineswap[$count] && $value) {
                        $rep['address_1'] = $value;    
                        $rep['address_2'] = NULL;                
                } else {
                    $rep[$headings[$key]] = $value;                    
                }
                            

            }                
        
        }    
        
        if($count > 1) {

            if ($run_environment == 'dev') {
                $reps[] = $rep;
                if($count > $max_records) break;                
            }

            if ($run_environment == 'prod') {            
                scraperwiki::save(array('muni_code'), $rep);
            }
            
        }
                    
        $count++;
        
    }


    if ($run_environment == 'dev') {    
        return $reps;    
    } else {
        return true;
    }
    

}


function strposa($haystack, $needles=array(), $offset=0) {
    

        $chr = array();
        foreach($needles as $needle) {
                $res = stripos($haystack, $needle, $offset);
                if ($res !== false) $chr[$needle] = $res;
        }

        if(empty($chr)) return false;
        return min($chr);
}


function num_word_search($string) {
    
    
    $array  = array('one', 
                    'two', 
                    'three', 
                    'four', 
                    'five', 
                    'six', 
                    'seven',
                    'eight', 
                    'nine',
                    'ten');

    if (strposa($string, $array) !== FALSE) {
        return true;
    } else {
        return false;
    }    
    
    
}



?>