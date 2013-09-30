<?php
$counter = 10;
function disguise_curl($url) { 
  $curl = curl_init(); 

  // Setup headers - I used the same headers from Firefox version 2.0.0.6 
  // below was split up because php.net said the line was too long. :/ 
  $header[0] = "Accept: text/xml,application/xml,application/xhtml+xml,"; 
  $header[0] .= "text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5"; 
  $header[] = "Cache-Control: max-age=0"; 
  $header[] = "Connection: keep-alive"; 
  $header[] = "Keep-Alive: 300"; 
  $header[] = "Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7"; 
  $header[] = "Accept-Language: en-us,en;q=0.5"; 
  $header[] = "Pragma: "; // browsers keep this blank. 

  curl_setopt($curl, CURLOPT_URL, $url); 
  curl_setopt($curl, CURLOPT_USERAGENT, 'Googlebot/2.1 (+http://www.google.com/bot.html)'); 
  curl_setopt($curl, CURLOPT_HTTPHEADER, $header); 
  curl_setopt($curl, CURLOPT_REFERER, 'http://www.google.com'); 
  curl_setopt($curl, CURLOPT_ENCODING, 'gzip,deflate'); 
  curl_setopt($curl, CURLOPT_AUTOREFERER, true); 
  curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
  curl_setopt($curl, CURLOPT_TIMEOUT, 10); 
  
  $html = curl_exec($curl) ; // execute the curl command 
  
  // Проверяем наличие ошибки
   if(curl_errno($curl))
   { 
    echo 'Error curl ( URL = {$url} ) : ' . curl_error($curl);
    mail('igor.savinkin@gmail.com', 'CloudGrammar Scraper Error', 'Scraper error: '. curl_error($curl));
    throw new Exception ("Error to get page content on url = {$url} : " .curl_error($curl) );   
   }
   else 
   {
   // $info = curl_getinfo($curl);
/*
    foreach ($info as $key => $value) 
    {  
    echo $key . " = " . $value . "<br />\n";
    }
*/    
    // echo '<br />Total time ' . $info['total_time'] . ' seconds during the request to ' . $info['url'];  
    // echo "<br />Size downloaded is " . $info["size_download"] . PHP_EOL . " Connect time equal " . $info["connect_time"]. '<br />';
   }

  curl_close($curl); // close the connection 
  return $html; // and finally, return $html 
} 

$url = 'http://cloudgrammar.com/';
echo "Time start: " . date('h:i:s') . "<br/>";

for ($a = 0; $a < 180; $a++ ) {
    $url_n = $url . '?a=' . $a ;
    //echo "{$url_n} <br/>";
    try {
        $page = disguise_curl($url_n);
        } 
        catch (Exception $e) 
        {
        header ("http/1.0 500 Internal server error");
        echo 'Caught exception: ' .  $e->getMessage(); 
        }
    echo date('h:i:s') . "<br/>";
    
    // sleep for x seconds
    sleep (3);
    }
    
echo "Time end: " . date('h:i:s') . "<br/>";
echo $page;
?>
<?php
$counter = 10;
function disguise_curl($url) { 
  $curl = curl_init(); 

  // Setup headers - I used the same headers from Firefox version 2.0.0.6 
  // below was split up because php.net said the line was too long. :/ 
  $header[0] = "Accept: text/xml,application/xml,application/xhtml+xml,"; 
  $header[0] .= "text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5"; 
  $header[] = "Cache-Control: max-age=0"; 
  $header[] = "Connection: keep-alive"; 
  $header[] = "Keep-Alive: 300"; 
  $header[] = "Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7"; 
  $header[] = "Accept-Language: en-us,en;q=0.5"; 
  $header[] = "Pragma: "; // browsers keep this blank. 

  curl_setopt($curl, CURLOPT_URL, $url); 
  curl_setopt($curl, CURLOPT_USERAGENT, 'Googlebot/2.1 (+http://www.google.com/bot.html)'); 
  curl_setopt($curl, CURLOPT_HTTPHEADER, $header); 
  curl_setopt($curl, CURLOPT_REFERER, 'http://www.google.com'); 
  curl_setopt($curl, CURLOPT_ENCODING, 'gzip,deflate'); 
  curl_setopt($curl, CURLOPT_AUTOREFERER, true); 
  curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
  curl_setopt($curl, CURLOPT_TIMEOUT, 10); 
  
  $html = curl_exec($curl) ; // execute the curl command 
  
  // Проверяем наличие ошибки
   if(curl_errno($curl))
   { 
    echo 'Error curl ( URL = {$url} ) : ' . curl_error($curl);
    mail('igor.savinkin@gmail.com', 'CloudGrammar Scraper Error', 'Scraper error: '. curl_error($curl));
    throw new Exception ("Error to get page content on url = {$url} : " .curl_error($curl) );   
   }
   else 
   {
   // $info = curl_getinfo($curl);
/*
    foreach ($info as $key => $value) 
    {  
    echo $key . " = " . $value . "<br />\n";
    }
*/    
    // echo '<br />Total time ' . $info['total_time'] . ' seconds during the request to ' . $info['url'];  
    // echo "<br />Size downloaded is " . $info["size_download"] . PHP_EOL . " Connect time equal " . $info["connect_time"]. '<br />';
   }

  curl_close($curl); // close the connection 
  return $html; // and finally, return $html 
} 

$url = 'http://cloudgrammar.com/';
echo "Time start: " . date('h:i:s') . "<br/>";

for ($a = 0; $a < 180; $a++ ) {
    $url_n = $url . '?a=' . $a ;
    //echo "{$url_n} <br/>";
    try {
        $page = disguise_curl($url_n);
        } 
        catch (Exception $e) 
        {
        header ("http/1.0 500 Internal server error");
        echo 'Caught exception: ' .  $e->getMessage(); 
        }
    echo date('h:i:s') . "<br/>";
    
    // sleep for x seconds
    sleep (3);
    }
    
echo "Time end: " . date('h:i:s') . "<br/>";
echo $page;
?>
