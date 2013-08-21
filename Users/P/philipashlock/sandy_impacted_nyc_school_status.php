<?php

//require 'scraperwiki.php';
require 'scraperwiki/simple_html_dom.php';


$directory_url = "http://schools.nyc.gov/Home/InOurSchoolsToday/2012-2013/cancellations";

$records = get_sources($directory_url);

# Our record counter
$count = 1;

# To see where the errors are when attempting
# to deserialize using PHP's miserable excuse
# for a JSON parser, let's break the JSON
# into single lines and process each one.

foreach(explode("{ impacted: ", $records) as $line) {
#foreach ($records as $record) {

    # Skip first record, it's just "[{ impacted: "
    if ($count == 1) {
       $count++;
       continue;
    }

    # Add the "impacted" back in, and trim the end
    $format = "{ \"impacted\": %s";
    $raw_line = rtrim(sprintf($format, $line));
 
    # Remove trailing commas
    $raw_line = rtrim(rtrim($raw_line),",");

    # Remove trailing ] (admittedly this is only on the last record)
    if (substr($raw_line, strlen($raw_line) - 1, strlen($raw_line)) == "]") {
        $json_line = rtrim($raw_line, "]");
    } else {
        $json_line = $raw_line;
    }   

    # Decode the JSON using a function that returns errors
    # Note that the depth of our JSON is 3 levels
    $record = json_decode_debug($json_line, false, 3);
   
    $record = objectToArray( $record );  


    $impacted = $record['impacted'];
    $receiving = $record['receiving'];
     
    $export = array();
    
    $export['program'] = $record['program'];
    $export['category'] = $record['category'];    
    
    $export['bn'] = $impacted['bn'];
    $export['name'] = $impacted['name'];    
    $export['principal'] = $impacted['principal'];    
    $export['staffopen'] = $impacted['staffopen'];    
    $export['studentopen'] = $impacted['studentopen'];        

    $export['receiving_bn'] = $receiving['bn'];
    $export['receiving_name'] = $receiving['name'];    
    $export['receiving_principal'] = $receiving['principal'];    
    $export['receiving_address'] = $receiving['address'];    
    $export['receiving_borough'] = $receiving['borough'];    
    $export['receiving_zip'] = $receiving['zip'];        
    
    
    $export['index'] = $export['bn'] . ' ' . $export['program'];
    
    scraperwiki::save(array('index'), $export);
    
    $count++;
}



//header('Content-type: application/json');
//print json_encode($exportall);

function get_sources($url) {
    
    
    $html = scraperWiki::scrape($url);

    $dom = new simple_html_dom();
    $dom->load($html);

    $list = $dom->find("div[id=topcenter]", 0);

    $script = $list->find("div[class=searchform]", 0)->find("script", 0);
    
    $script = $script->innertext;
    
    # Get data from the first occurrence of the string "impacted:"...
    $data = substr($script, strpos($script, 'impacted:'));
    
    # Until the document.ready function.
    $length = strlen($data) - strpos($data, '$(document).ready(function ()');
    
    # Not sure why we subtract again here, but it works
    $length = strlen($data) - $length;

    $data = substr($data, 0, $length);
    
    # Add the beginning of the json back...
    # Not sure why the lines below are still needed,
    # but I wrote them a while back and it doesn't
    # work without them, so I am leaving well enough alone.
    $data = '[{ ' . $data;
    
    $data = trim($data);
    $data = substr($data, 0, strlen($data) - 2);

    return $data;
    

}



function objectToArray( $object )
{
    if( !is_object( $object ) && !is_array( $object ) )
    {
        return $object;
    }
    if( is_object( $object ) )
    {
        $object = get_object_vars( $object );
    }
    return array_map( 'objectToArray', $object );
}

/*
* Function to decode AND return JSON errors
*/
function json_decode_debug($string, $assoc, $depth) {
    $string = json_clean($string);    
    $result = json_decode($string, $assoc, $depth);

    switch (json_last_error()) {
        case JSON_ERROR_NONE:
#            echo 'No errors: ';
        break;
        case JSON_ERROR_DEPTH:
            echo 'Maximum stack depth exceeded: ';
        break;
        case JSON_ERROR_STATE_MISMATCH:
            echo 'Underflow or the modes mismatch: ';
        break;
        case JSON_ERROR_CTRL_CHAR:
            echo 'Unexpected control character found: ';
        break;
        case JSON_ERROR_SYNTAX:
            echo 'Syntax error, malformed JSON: ';
        break;
        case JSON_ERROR_UTF8:
            echo 'Malformed UTF-8 characters, possibly incorrectly encoded: ';
        break;
        default:
            echo 'Unknown error: ';
        break;
    }
    
    # Only print out an error if we have one
    if (json_last_error()) {
        print $string . "\n";
    }

    return $result;
}


/*
* Stole this function from here:  http://www.php.net/manual/en/function.json-decode.php 
* Thanks to Colin Mollenhour
* Renamed to just clean the json but not decode it
*/
function json_clean($json){
    $json = str_replace(array("\n","\r"),"",$json);
    $json = preg_replace('/([{,])(\s*)([^"]+?)\s*:/','$1"$3":',$json);
    return $json;
}

?><?php

//require 'scraperwiki.php';
require 'scraperwiki/simple_html_dom.php';


$directory_url = "http://schools.nyc.gov/Home/InOurSchoolsToday/2012-2013/cancellations";

$records = get_sources($directory_url);

# Our record counter
$count = 1;

# To see where the errors are when attempting
# to deserialize using PHP's miserable excuse
# for a JSON parser, let's break the JSON
# into single lines and process each one.

foreach(explode("{ impacted: ", $records) as $line) {
#foreach ($records as $record) {

    # Skip first record, it's just "[{ impacted: "
    if ($count == 1) {
       $count++;
       continue;
    }

    # Add the "impacted" back in, and trim the end
    $format = "{ \"impacted\": %s";
    $raw_line = rtrim(sprintf($format, $line));
 
    # Remove trailing commas
    $raw_line = rtrim(rtrim($raw_line),",");

    # Remove trailing ] (admittedly this is only on the last record)
    if (substr($raw_line, strlen($raw_line) - 1, strlen($raw_line)) == "]") {
        $json_line = rtrim($raw_line, "]");
    } else {
        $json_line = $raw_line;
    }   

    # Decode the JSON using a function that returns errors
    # Note that the depth of our JSON is 3 levels
    $record = json_decode_debug($json_line, false, 3);
   
    $record = objectToArray( $record );  


    $impacted = $record['impacted'];
    $receiving = $record['receiving'];
     
    $export = array();
    
    $export['program'] = $record['program'];
    $export['category'] = $record['category'];    
    
    $export['bn'] = $impacted['bn'];
    $export['name'] = $impacted['name'];    
    $export['principal'] = $impacted['principal'];    
    $export['staffopen'] = $impacted['staffopen'];    
    $export['studentopen'] = $impacted['studentopen'];        

    $export['receiving_bn'] = $receiving['bn'];
    $export['receiving_name'] = $receiving['name'];    
    $export['receiving_principal'] = $receiving['principal'];    
    $export['receiving_address'] = $receiving['address'];    
    $export['receiving_borough'] = $receiving['borough'];    
    $export['receiving_zip'] = $receiving['zip'];        
    
    
    $export['index'] = $export['bn'] . ' ' . $export['program'];
    
    scraperwiki::save(array('index'), $export);
    
    $count++;
}



//header('Content-type: application/json');
//print json_encode($exportall);

function get_sources($url) {
    
    
    $html = scraperWiki::scrape($url);

    $dom = new simple_html_dom();
    $dom->load($html);

    $list = $dom->find("div[id=topcenter]", 0);

    $script = $list->find("div[class=searchform]", 0)->find("script", 0);
    
    $script = $script->innertext;
    
    # Get data from the first occurrence of the string "impacted:"...
    $data = substr($script, strpos($script, 'impacted:'));
    
    # Until the document.ready function.
    $length = strlen($data) - strpos($data, '$(document).ready(function ()');
    
    # Not sure why we subtract again here, but it works
    $length = strlen($data) - $length;

    $data = substr($data, 0, $length);
    
    # Add the beginning of the json back...
    # Not sure why the lines below are still needed,
    # but I wrote them a while back and it doesn't
    # work without them, so I am leaving well enough alone.
    $data = '[{ ' . $data;
    
    $data = trim($data);
    $data = substr($data, 0, strlen($data) - 2);

    return $data;
    

}



function objectToArray( $object )
{
    if( !is_object( $object ) && !is_array( $object ) )
    {
        return $object;
    }
    if( is_object( $object ) )
    {
        $object = get_object_vars( $object );
    }
    return array_map( 'objectToArray', $object );
}

/*
* Function to decode AND return JSON errors
*/
function json_decode_debug($string, $assoc, $depth) {
    $string = json_clean($string);    
    $result = json_decode($string, $assoc, $depth);

    switch (json_last_error()) {
        case JSON_ERROR_NONE:
#            echo 'No errors: ';
        break;
        case JSON_ERROR_DEPTH:
            echo 'Maximum stack depth exceeded: ';
        break;
        case JSON_ERROR_STATE_MISMATCH:
            echo 'Underflow or the modes mismatch: ';
        break;
        case JSON_ERROR_CTRL_CHAR:
            echo 'Unexpected control character found: ';
        break;
        case JSON_ERROR_SYNTAX:
            echo 'Syntax error, malformed JSON: ';
        break;
        case JSON_ERROR_UTF8:
            echo 'Malformed UTF-8 characters, possibly incorrectly encoded: ';
        break;
        default:
            echo 'Unknown error: ';
        break;
    }
    
    # Only print out an error if we have one
    if (json_last_error()) {
        print $string . "\n";
    }

    return $result;
}


/*
* Stole this function from here:  http://www.php.net/manual/en/function.json-decode.php 
* Thanks to Colin Mollenhour
* Renamed to just clean the json but not decode it
*/
function json_clean($json){
    $json = str_replace(array("\n","\r"),"",$json);
    $json = preg_replace('/([{,])(\s*)([^"]+?)\s*:/','$1"$3":',$json);
    return $json;
}

?>