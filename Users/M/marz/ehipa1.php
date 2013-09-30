<?php
require 'scraperwiki/simple_html_dom.php';


function mycurl($url, $ckfile){

    $cc= file_get_contents($ckfile);
    var_dump($cc);
    var_dump($ckfile);
  
    /* STEP 3. visit cookiepage.php */

    
    $ch = curl_init ($url);
    curl_setopt ($ch, CURLOPT_COOKIEFILE, $ckfile); 
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);// allow redirects
    curl_setopt($ch, CURLOPT_RETURNTRANSFER,1); // return into a variable
    curl_setopt($ch, CURLOPT_TIMEOUT, 10); // times out after 4s
    curl_setopt($ch, CURLOPT_USERAGENT, "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0"); 
    $output = curl_exec ($ch);
    
    return $output;
}


/** 
* Open an url on https using curl and return content 
* 
* @author hatem <info@phptunisie.net> 
* @param string url            The url to open 
* @param string refer        Referer (optional) 
* @param mixed usecookie    If true, cookie.txt    will be used as default, or the usecookie value. 
* @return string 
*/ 
function open_https_url($url,$refer = "",$usecookie = false) { 

    if ($usecookie) { 
        
        if (file_exists($usecookie)) { 
        
            if (!is_writable($usecookie)) { 
                
                return "Can't write to $usecookie cookie file, change file permission to 777 or remove read only for windows."; 
            } 
        } else { 
            $usecookie = "cookie.txt"; 
            if (!is_writable($usecookie)) { 
                
                return "Can't write to $usecookie cookie file, change file permission to 777 or remove read only for windows."; 
            } 
        } 
    
    } 

    $ch = curl_init(); 
    
    curl_setopt($ch, CURLOPT_URL, $url); 
    
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, FALSE); 
    
    curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 2); 
    
    curl_setopt($ch, CURLOPT_HEADER, 1); 
    
    curl_setopt($ch, CURLOPT_USERAGENT, "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)"); 
    
    if ($usecookie) { 
        curl_setopt($ch, CURLOPT_COOKIEJAR, $usecookie); 
        
        curl_setopt($ch, CURLOPT_COOKIEFILE, $usecookie);    
    } 
    
    if ($refer != "") { 
    
        curl_setopt($ch, CURLOPT_REFERER, $refer ); 
        
    } 
    
    curl_setopt($ch, CURLOPT_RETURNTRANSFER,1); 
    
   $result =curl_exec ($ch); 
    
   curl_close ($ch); 
    
   return $result; 
} 

$page=1;
$url="https://webgate.ec.europa.eu/eipaha/initiative/index/index/page/".$page;

/* STEP 1. let’s create a cookie file */
$ckfile = tempnam ("/tmp", "CURLCOOKIE");
/* STEP 2. visit the homepage to set the cookie properly */
$ch = curl_init ($url);
curl_setopt ($ch, CURLOPT_COOKIEJAR, $ckfile); 
curl_setopt ($ch, CURLOPT_RETURNTRANSFER, true);
$output = curl_exec ($ch);

$html = mycurl($url, $ckfile);   

 
var_dump($html);

$html= open_https_url($url);
var_dump($html);


// get the last
$dom = new simple_html_dom();
$dom->load($html);
$AA=$dom->find(".DataTableEditable tbody tr td");
<?php
require 'scraperwiki/simple_html_dom.php';


function mycurl($url, $ckfile){

    $cc= file_get_contents($ckfile);
    var_dump($cc);
    var_dump($ckfile);
  
    /* STEP 3. visit cookiepage.php */

    
    $ch = curl_init ($url);
    curl_setopt ($ch, CURLOPT_COOKIEFILE, $ckfile); 
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);// allow redirects
    curl_setopt($ch, CURLOPT_RETURNTRANSFER,1); // return into a variable
    curl_setopt($ch, CURLOPT_TIMEOUT, 10); // times out after 4s
    curl_setopt($ch, CURLOPT_USERAGENT, "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0"); 
    $output = curl_exec ($ch);
    
    return $output;
}


/** 
* Open an url on https using curl and return content 
* 
* @author hatem <info@phptunisie.net> 
* @param string url            The url to open 
* @param string refer        Referer (optional) 
* @param mixed usecookie    If true, cookie.txt    will be used as default, or the usecookie value. 
* @return string 
*/ 
function open_https_url($url,$refer = "",$usecookie = false) { 

    if ($usecookie) { 
        
        if (file_exists($usecookie)) { 
        
            if (!is_writable($usecookie)) { 
                
                return "Can't write to $usecookie cookie file, change file permission to 777 or remove read only for windows."; 
            } 
        } else { 
            $usecookie = "cookie.txt"; 
            if (!is_writable($usecookie)) { 
                
                return "Can't write to $usecookie cookie file, change file permission to 777 or remove read only for windows."; 
            } 
        } 
    
    } 

    $ch = curl_init(); 
    
    curl_setopt($ch, CURLOPT_URL, $url); 
    
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, FALSE); 
    
    curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 2); 
    
    curl_setopt($ch, CURLOPT_HEADER, 1); 
    
    curl_setopt($ch, CURLOPT_USERAGENT, "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)"); 
    
    if ($usecookie) { 
        curl_setopt($ch, CURLOPT_COOKIEJAR, $usecookie); 
        
        curl_setopt($ch, CURLOPT_COOKIEFILE, $usecookie);    
    } 
    
    if ($refer != "") { 
    
        curl_setopt($ch, CURLOPT_REFERER, $refer ); 
        
    } 
    
    curl_setopt($ch, CURLOPT_RETURNTRANSFER,1); 
    
   $result =curl_exec ($ch); 
    
   curl_close ($ch); 
    
   return $result; 
} 

$page=1;
$url="https://webgate.ec.europa.eu/eipaha/initiative/index/index/page/".$page;

/* STEP 1. let’s create a cookie file */
$ckfile = tempnam ("/tmp", "CURLCOOKIE");
/* STEP 2. visit the homepage to set the cookie properly */
$ch = curl_init ($url);
curl_setopt ($ch, CURLOPT_COOKIEJAR, $ckfile); 
curl_setopt ($ch, CURLOPT_RETURNTRANSFER, true);
$output = curl_exec ($ch);

$html = mycurl($url, $ckfile);   

 
var_dump($html);

$html= open_https_url($url);
var_dump($html);


// get the last
$dom = new simple_html_dom();
$dom->load($html);
$AA=$dom->find(".DataTableEditable tbody tr td");
