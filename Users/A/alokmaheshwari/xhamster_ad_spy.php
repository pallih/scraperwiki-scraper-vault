<?php

 function get_url( $url,  $javascript_loop = 0, $timeout = 5 )
 {
     $url = str_replace( "&amp;", "&", urldecode(trim($url)) );
 
     $cookie = tempnam ("/tmp", "CURLCOOKIE");
     $ch = curl_init();
     curl_setopt( $ch, CURLOPT_USERAGENT, "Mozilla/5.0 (Windows; U; Windows NT 5.1; rv:1.7.3) Gecko/20041001 Firefox/0.10.1" );
     curl_setopt( $ch, CURLOPT_URL, $url );
     curl_setopt( $ch, CURLOPT_COOKIEJAR, $cookie );
     curl_setopt( $ch, CURLOPT_FOLLOWLOCATION, true );
     curl_setopt( $ch, CURLOPT_ENCODING, "" );
     curl_setopt( $ch, CURLOPT_RETURNTRANSFER, true );
     curl_setopt( $ch, CURLOPT_AUTOREFERER, true );
     curl_setopt( $ch, CURLOPT_SSL_VERIFYPEER, false );    # required for https urls
     curl_setopt( $ch, CURLOPT_CONNECTTIMEOUT, $timeout );
     curl_setopt( $ch, CURLOPT_TIMEOUT, $timeout );
     curl_setopt( $ch, CURLOPT_MAXREDIRS, 10 );
     $content = curl_exec( $ch );
     $response = curl_getinfo( $ch );
     curl_close ( $ch );
 
     if ($response['http_code'] == 301 || $response['http_code'] == 302)
     {
         ini_set("user_agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; rv:1.7.3) Gecko/20041001 Firefox/0.10.1");
 
         if ( $headers = get_headers($response['url']) )
         {
             foreach( $headers as $value )
             {
                 if ( substr( strtolower($value), 0, 9 ) == "location:" )
                     return get_url( trim( substr( $value, 9, strlen($value) ) ) );
             }
         }
     }
 
     if (    ( preg_match("/>[[:space:]]+window\.location\.replace\('(.*)'\)/i", $content, $value) || preg_match("/>[[:space:]]+window\.location\=\"(.*)\"/i", $content, $value) ) &&
             $javascript_loop < 5
     )
     {
         return get_url( $value[1], $javascript_loop+1 );
     }
     else
     {
         return array( $content, $response );
     }
 } 

function get_web_page( $url ) {
    $res = array();
    $options = array( 
        CURLOPT_RETURNTRANSFER => true,     // return web page 
        CURLOPT_HEADER         => false,    // do not return headers 
        CURLOPT_FOLLOWLOCATION => true,     // follow redirects 
        CURLOPT_USERAGENT      => "spider", // who am i 
        CURLOPT_AUTOREFERER    => true,     // set referer on redirect 
        CURLOPT_CONNECTTIMEOUT => 120,      // timeout on connect 
        CURLOPT_TIMEOUT        => 120,      // timeout on response 
        CURLOPT_MAXREDIRS      => 10,       // stop after 10 redirects 
    ); 
    $ch      = curl_init( $url ); 
    curl_setopt_array( $ch, $options ); 
    $content = curl_exec( $ch ); 
    $err     = curl_errno( $ch ); 
    $errmsg  = curl_error( $ch ); 
    $header  = curl_getinfo( $ch ); 
    curl_close( $ch ); 

    $res['content'] = $content;     
    $res['url'] = $header['url'];
    return $res; 
}  




require 'scraperwiki/simple_html_dom.php';           
$html_content = scraperwiki::scrape("http://syndication.exoclick.com/ads-iframe-display.php?type=300x250&login=xhamster&cat=2&search=&ad_title_color=0000cc&bgcolor=FFFFFF&border=0&border_color=000000&font=&block_keywords=&ad_text_color=000000&ad_durl_color=008000&adult=0&sub=0&text_only=0&show_thumb=0&idzone=100633&idsite=34954&rand=1");
$html = str_get_html($html_content);
$imgtag=$html->find("img");
$atag=$html->find("a");

$img_attr="";
$a_attr="";
preg_match_all('/(src)=("[^"]*")/i',$imgtag[0], $img_attr);
preg_match_all('/(href)=("[^"]*")/i',$atag[0], $a_attr); 

$image_attribute="";
$a_attribute="";

$image_attribute=str_replace('"','', $img_attr[2][0] );
$a_attribute=str_replace('"','', $a_attr[2][0] );

//$lp_content = file_get_contents("$a_attribute");
//$lp_html = str_get_html($lp_content); 
//echo $lp_content;
//echo $a_attribute;
//$exo_html=get_url("$a_attribute"."&js=1");  
 $exo_html=file_get_contents("$a_attribute"."&js=1");   
//$exoclick_url=$exo_html["url"];
echo "\n";
print_r($exo_html);

//$exo_html_1=get_url($exo_html[0]);
// $exo_html_1=get_url($exo_html[0]); 
//print_r($exo_html_1);

//$lp_html= get_web_page("$exoclick_url"); 
//$lp_url=$lp_html["url"];

//print_r($lp_url);
//print_r(file_get_contents("http://main.exoclick.com/click.php?data=eGhhbXN0ZXJ8MjQxMjQ3fDB8aHR0cCUzQSUyRiUyRnRyay5rbGlja3RyZWsuY29tJTJGYmFzZS5waHAlM0ZjJTNEODMlMjZrZXklM0Q4NzNkNTA5YWZiNTRjM2RiZjNiMjFiYTFjOGQyMzAxZiUyNnNvdXJjZSUzRHhoYW1zdGVyLmNvbXwzNDk1NHx8MHwxMDB8MTM1MDA2OTQ4Nnx4aGFtc3Rlci5jb218NDYuNDMuNTUuODd8MjQxMjQ3LTUyMDgxODR8NTIwODE4NHwxMDA2MzN8Mnw3fDQ1Y2FkYTg5NTE5YmQ1ODBjZmE5YzAyODhkZjAzMGFh"));


$unique_keys=array();

scraperwiki::save_sqlite($unique_keys,array("image"=>"$image_attribute","link"=>"$a_attribute", "xhtml"=>"$html")); 
scraperwiki::sqlitecommit();

?><?php

 function get_url( $url,  $javascript_loop = 0, $timeout = 5 )
 {
     $url = str_replace( "&amp;", "&", urldecode(trim($url)) );
 
     $cookie = tempnam ("/tmp", "CURLCOOKIE");
     $ch = curl_init();
     curl_setopt( $ch, CURLOPT_USERAGENT, "Mozilla/5.0 (Windows; U; Windows NT 5.1; rv:1.7.3) Gecko/20041001 Firefox/0.10.1" );
     curl_setopt( $ch, CURLOPT_URL, $url );
     curl_setopt( $ch, CURLOPT_COOKIEJAR, $cookie );
     curl_setopt( $ch, CURLOPT_FOLLOWLOCATION, true );
     curl_setopt( $ch, CURLOPT_ENCODING, "" );
     curl_setopt( $ch, CURLOPT_RETURNTRANSFER, true );
     curl_setopt( $ch, CURLOPT_AUTOREFERER, true );
     curl_setopt( $ch, CURLOPT_SSL_VERIFYPEER, false );    # required for https urls
     curl_setopt( $ch, CURLOPT_CONNECTTIMEOUT, $timeout );
     curl_setopt( $ch, CURLOPT_TIMEOUT, $timeout );
     curl_setopt( $ch, CURLOPT_MAXREDIRS, 10 );
     $content = curl_exec( $ch );
     $response = curl_getinfo( $ch );
     curl_close ( $ch );
 
     if ($response['http_code'] == 301 || $response['http_code'] == 302)
     {
         ini_set("user_agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; rv:1.7.3) Gecko/20041001 Firefox/0.10.1");
 
         if ( $headers = get_headers($response['url']) )
         {
             foreach( $headers as $value )
             {
                 if ( substr( strtolower($value), 0, 9 ) == "location:" )
                     return get_url( trim( substr( $value, 9, strlen($value) ) ) );
             }
         }
     }
 
     if (    ( preg_match("/>[[:space:]]+window\.location\.replace\('(.*)'\)/i", $content, $value) || preg_match("/>[[:space:]]+window\.location\=\"(.*)\"/i", $content, $value) ) &&
             $javascript_loop < 5
     )
     {
         return get_url( $value[1], $javascript_loop+1 );
     }
     else
     {
         return array( $content, $response );
     }
 } 

function get_web_page( $url ) {
    $res = array();
    $options = array( 
        CURLOPT_RETURNTRANSFER => true,     // return web page 
        CURLOPT_HEADER         => false,    // do not return headers 
        CURLOPT_FOLLOWLOCATION => true,     // follow redirects 
        CURLOPT_USERAGENT      => "spider", // who am i 
        CURLOPT_AUTOREFERER    => true,     // set referer on redirect 
        CURLOPT_CONNECTTIMEOUT => 120,      // timeout on connect 
        CURLOPT_TIMEOUT        => 120,      // timeout on response 
        CURLOPT_MAXREDIRS      => 10,       // stop after 10 redirects 
    ); 
    $ch      = curl_init( $url ); 
    curl_setopt_array( $ch, $options ); 
    $content = curl_exec( $ch ); 
    $err     = curl_errno( $ch ); 
    $errmsg  = curl_error( $ch ); 
    $header  = curl_getinfo( $ch ); 
    curl_close( $ch ); 

    $res['content'] = $content;     
    $res['url'] = $header['url'];
    return $res; 
}  




require 'scraperwiki/simple_html_dom.php';           
$html_content = scraperwiki::scrape("http://syndication.exoclick.com/ads-iframe-display.php?type=300x250&login=xhamster&cat=2&search=&ad_title_color=0000cc&bgcolor=FFFFFF&border=0&border_color=000000&font=&block_keywords=&ad_text_color=000000&ad_durl_color=008000&adult=0&sub=0&text_only=0&show_thumb=0&idzone=100633&idsite=34954&rand=1");
$html = str_get_html($html_content);
$imgtag=$html->find("img");
$atag=$html->find("a");

$img_attr="";
$a_attr="";
preg_match_all('/(src)=("[^"]*")/i',$imgtag[0], $img_attr);
preg_match_all('/(href)=("[^"]*")/i',$atag[0], $a_attr); 

$image_attribute="";
$a_attribute="";

$image_attribute=str_replace('"','', $img_attr[2][0] );
$a_attribute=str_replace('"','', $a_attr[2][0] );

//$lp_content = file_get_contents("$a_attribute");
//$lp_html = str_get_html($lp_content); 
//echo $lp_content;
//echo $a_attribute;
//$exo_html=get_url("$a_attribute"."&js=1");  
 $exo_html=file_get_contents("$a_attribute"."&js=1");   
//$exoclick_url=$exo_html["url"];
echo "\n";
print_r($exo_html);

//$exo_html_1=get_url($exo_html[0]);
// $exo_html_1=get_url($exo_html[0]); 
//print_r($exo_html_1);

//$lp_html= get_web_page("$exoclick_url"); 
//$lp_url=$lp_html["url"];

//print_r($lp_url);
//print_r(file_get_contents("http://main.exoclick.com/click.php?data=eGhhbXN0ZXJ8MjQxMjQ3fDB8aHR0cCUzQSUyRiUyRnRyay5rbGlja3RyZWsuY29tJTJGYmFzZS5waHAlM0ZjJTNEODMlMjZrZXklM0Q4NzNkNTA5YWZiNTRjM2RiZjNiMjFiYTFjOGQyMzAxZiUyNnNvdXJjZSUzRHhoYW1zdGVyLmNvbXwzNDk1NHx8MHwxMDB8MTM1MDA2OTQ4Nnx4aGFtc3Rlci5jb218NDYuNDMuNTUuODd8MjQxMjQ3LTUyMDgxODR8NTIwODE4NHwxMDA2MzN8Mnw3fDQ1Y2FkYTg5NTE5YmQ1ODBjZmE5YzAyODhkZjAzMGFh"));


$unique_keys=array();

scraperwiki::save_sqlite($unique_keys,array("image"=>"$image_attribute","link"=>"$a_attribute", "xhtml"=>"$html")); 
scraperwiki::sqlitecommit();

?>