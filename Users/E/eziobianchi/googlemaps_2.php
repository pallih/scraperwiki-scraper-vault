<?php
/*
    Author: Yash Gupta
    File: search.php
    Description:
        This script searches google for a given search term and outputs all the results' urls for upto 1000 results.
    Usage:
        Make a form in some other page and pass the following parameters with GET method, or modify the url as search.php?pages=50&q=get+google+results+php     
        q => Your search query. Default query is: 'no query'     
        pages => The number of pages you want to parse. (default is 10, maximum of 100)     
        start => The page to start from. Default is 1
*/
ini_set("max_execution_time", 0); set_time_limit(0);     // no time-outs!
if(isset($_GET['q']))
    $query=$_GET['q'];
else
    $query="restaurants central coast";
if(isset($_GET['pages']))
    $npages=$_GET['pages'];
else
    $npages=100;
if(isset($_GET['start']))
    $start=$_GET['start'];
else
    $start=0;
if($npages>=100)
    $npages=100;
$gg_url = 'http://www.google.com.au/search?&num=100&tbm=plcs&hl=en&q=love' . urlencode($query) . '&start=';
/*
 $gg_url = 'http://www.google.com.au/search?&num=100&tbm=plcs&hl=en&q=' . urlencode($query) . '&start=';
*/
$i=1;
$size=0;
$options = array(
        CURLOPT_RETURNTRANSFER => true,     // return web page
        CURLOPT_HEADER         => false,    // don't return headers
        CURLOPT_FOLLOWLOCATION => true,     // follow redirects
        CURLOPT_ENCODING       => "",       // handle all encodings
        CURLOPT_AUTOREFERER    => true,     // set referer on redirect
        CURLOPT_CONNECTTIMEOUT => 120,      // timeout on connect
        CURLOPT_TIMEOUT        => 120,      // timeout on response
        CURLOPT_MAXREDIRS      => 10,       // stop after 10 redirects
    CURLOPT_COOKIEFILE    =>    "cookie.txt",
        CURLOPT_COOKIEJAR    =>    "cookie.txt",
    CURLOPT_USERAGENT    =>    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3",
    CURLOPT_REFERER    =>        "http://www.google.com/",
    );

for ($page = $start; $page < $npages; $page++)
{
    $ch = curl_init($gg_url.$page.'0');
    curl_setopt_array($ch,$options);
    $scraped="";
    $scraped.=curl_exec($ch);
    curl_close( $ch );
    $results = array();
$save=array();
    $keys=array('name','address','suburb','phone','url');
    preg_match_all('@line-height:1.24" valign="top">([^"]+)<br>([^"]+)<br>.<nobr>([^"]+)</nobr></table>.*<h3\s*class="r">\s*<a[^<>]*href="([^<>]*)"[^<>]*>(.*)</a>\s*</h3>@siU',$scraped,$results);
    
    $address = $results[1];
    $suburb = $results[2];
    
    $phone = $results[3];
    $url = $results[4];
    $name = $results[5];    
    for ($zf=0;$zf<count($results[0]);$zf++){
        $save[] = array('name' =>  $name[$zf], 'address' => $address[$zf], 'suburb' => $suburb[$zf], 'phone' => $phone[$zf] ,'url' =>  $url[$zf]);
        scraperwiki::save($keys,$save); 
        //echo $address[$zf]." : ".$suburb[$zf]." : ".$phone[$zf]." : ".$url[$zf]." : ".$name[$zf]." \n";
    }
    $size+=strlen($scraped);
    $i++;

}
//fclose($fp);
echo "Number of results: $i Total KB read: ".($size/1024.0);
print "Done.";
?>
