import scraperwiki
import curl

<?php

/*
# Define the file you want to download
$target = "http://www.schrenk.com/nostarch/webbots/hello_world.html";
$file_handle = fopen($target, "r");

# Fetch the file
while (!feof($file_handle))
    echo fgets($file_handle, 4096);
fclose($file_handle);
*/


$target = "http://www.schrenk.com/publications.php"; 
$ref = "http://www.schrenk.com";


# Define how your webbot will appear in server logs
define("WEBBOT_NAME", "Test Webbot");

# Length of time cURL will wait for a response (seconds)
define("CURL_TIMEOUT", 25);

# Location of your cookie file. (Must be fully resolved local address)
define("COOKIE_FILE", "c:\cookie.txt");

# DEFINE METHOD CONSTANTS
define("HEAD", "HEAD");
define("GET",  "GET");
define("POST", "POST");

# DEFINE HEADER INCLUSION
define("EXCL_HEAD", FALSE);
define("INCL_HEAD", TRUE);



function http($target, $ref, $method, $data_array, $incl_head)
    {
    # Initialize PHP/CURL handle
    $ch = curl_init();

    # Prcess data, if presented
    if(is_array($data_array))
        {
        # Convert data array into a query string (ie animal=dog&sport=baseball)
        foreach ($data_array as $key => $value) 
            {
            if(strlen(trim($value))>0)
                $temp_string[] = $key . "=" . urlencode($value);
            else
                $temp_string[] = $key;
            }
        $query_string = join('&', $temp_string);
        }
        
    # HEAD method configuration
    if($method == HEAD)
        {
        curl_setopt($ch, CURLOPT_HEADER, TRUE);                // No http head
        curl_setopt($ch, CURLOPT_NOBODY, TRUE);                // Return body
        }
    else
        {
        # GET method configuration
        if($method == GET)
            {
            if(isset($query_string))
                $target = $target . "?" . $query_string;
            curl_setopt ($ch, CURLOPT_HTTPGET, TRUE); 
            curl_setopt ($ch, CURLOPT_POST, FALSE); 
            }
        # POST method configuration
        if($method == POST)
            {
            if(isset($query_string))
                curl_setopt ($ch, CURLOPT_POSTFIELDS, $query_string);
            curl_setopt ($ch, CURLOPT_POST, TRUE); 
            curl_setopt ($ch, CURLOPT_HTTPGET, FALSE); 
            }
        curl_setopt($ch, CURLOPT_HEADER, $incl_head);   // Include head as needed
        curl_setopt($ch, CURLOPT_NOBODY, FALSE);        // Return body
        }
        
    curl_setopt($ch, CURLOPT_COOKIEJAR, COOKIE_FILE);   // Cookie management.
    curl_setopt($ch, CURLOPT_COOKIEFILE, COOKIE_FILE);
    curl_setopt($ch, CURLOPT_TIMEOUT, CURL_TIMEOUT);    // Timeout
    curl_setopt($ch, CURLOPT_USERAGENT, WEBBOT_NAME);   // Webbot name
    curl_setopt($ch, CURLOPT_URL, $target);             // Target site
    curl_setopt($ch, CURLOPT_REFERER, $ref);            // Referer value
    curl_setopt($ch, CURLOPT_VERBOSE, FALSE);           // Minimize logs
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, FALSE);    // No certificate
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, TRUE);     // Follow redirects
    curl_setopt($ch, CURLOPT_MAXREDIRS, 4);             // Limit redirections to four
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);     // Return in string
    
    # Create return array
    $return_array['FILE']   = curl_exec($ch); 
    $return_array['STATUS'] = curl_getinfo($ch);
    $return_array['ERROR']  = curl_error($ch);
    
    # Close PHP/CURL handle
      curl_close($ch);
    
    # Return results
      return $return_array;
    }


$website = http($target, $ref, $method="GET", $data_array="", INCL_HEAD);

echo "Website \n";
echo $target;

/*
echo "File Content \n";
var_dump($website['FILE']);
*/
var_dump($website['STATUS']);


?>







import scraperwiki
import curl

<?php

/*
# Define the file you want to download
$target = "http://www.schrenk.com/nostarch/webbots/hello_world.html";
$file_handle = fopen($target, "r");

# Fetch the file
while (!feof($file_handle))
    echo fgets($file_handle, 4096);
fclose($file_handle);
*/


$target = "http://www.schrenk.com/publications.php"; 
$ref = "http://www.schrenk.com";


# Define how your webbot will appear in server logs
define("WEBBOT_NAME", "Test Webbot");

# Length of time cURL will wait for a response (seconds)
define("CURL_TIMEOUT", 25);

# Location of your cookie file. (Must be fully resolved local address)
define("COOKIE_FILE", "c:\cookie.txt");

# DEFINE METHOD CONSTANTS
define("HEAD", "HEAD");
define("GET",  "GET");
define("POST", "POST");

# DEFINE HEADER INCLUSION
define("EXCL_HEAD", FALSE);
define("INCL_HEAD", TRUE);



function http($target, $ref, $method, $data_array, $incl_head)
    {
    # Initialize PHP/CURL handle
    $ch = curl_init();

    # Prcess data, if presented
    if(is_array($data_array))
        {
        # Convert data array into a query string (ie animal=dog&sport=baseball)
        foreach ($data_array as $key => $value) 
            {
            if(strlen(trim($value))>0)
                $temp_string[] = $key . "=" . urlencode($value);
            else
                $temp_string[] = $key;
            }
        $query_string = join('&', $temp_string);
        }
        
    # HEAD method configuration
    if($method == HEAD)
        {
        curl_setopt($ch, CURLOPT_HEADER, TRUE);                // No http head
        curl_setopt($ch, CURLOPT_NOBODY, TRUE);                // Return body
        }
    else
        {
        # GET method configuration
        if($method == GET)
            {
            if(isset($query_string))
                $target = $target . "?" . $query_string;
            curl_setopt ($ch, CURLOPT_HTTPGET, TRUE); 
            curl_setopt ($ch, CURLOPT_POST, FALSE); 
            }
        # POST method configuration
        if($method == POST)
            {
            if(isset($query_string))
                curl_setopt ($ch, CURLOPT_POSTFIELDS, $query_string);
            curl_setopt ($ch, CURLOPT_POST, TRUE); 
            curl_setopt ($ch, CURLOPT_HTTPGET, FALSE); 
            }
        curl_setopt($ch, CURLOPT_HEADER, $incl_head);   // Include head as needed
        curl_setopt($ch, CURLOPT_NOBODY, FALSE);        // Return body
        }
        
    curl_setopt($ch, CURLOPT_COOKIEJAR, COOKIE_FILE);   // Cookie management.
    curl_setopt($ch, CURLOPT_COOKIEFILE, COOKIE_FILE);
    curl_setopt($ch, CURLOPT_TIMEOUT, CURL_TIMEOUT);    // Timeout
    curl_setopt($ch, CURLOPT_USERAGENT, WEBBOT_NAME);   // Webbot name
    curl_setopt($ch, CURLOPT_URL, $target);             // Target site
    curl_setopt($ch, CURLOPT_REFERER, $ref);            // Referer value
    curl_setopt($ch, CURLOPT_VERBOSE, FALSE);           // Minimize logs
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, FALSE);    // No certificate
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, TRUE);     // Follow redirects
    curl_setopt($ch, CURLOPT_MAXREDIRS, 4);             // Limit redirections to four
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);     // Return in string
    
    # Create return array
    $return_array['FILE']   = curl_exec($ch); 
    $return_array['STATUS'] = curl_getinfo($ch);
    $return_array['ERROR']  = curl_error($ch);
    
    # Close PHP/CURL handle
      curl_close($ch);
    
    # Return results
      return $return_array;
    }


$website = http($target, $ref, $method="GET", $data_array="", INCL_HEAD);

echo "Website \n";
echo $target;

/*
echo "File Content \n";
var_dump($website['FILE']);
*/
var_dump($website['STATUS']);


?>







