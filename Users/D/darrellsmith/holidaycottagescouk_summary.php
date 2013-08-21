<?php

function get_xml_data_from_url($url,$lang = "en") 
  {         
    $url_array = parse_url($url); 
    $fp = fsockopen($url_array['host'], 80, $errno, $errstr, 5);  
    $send = "GET " . $url_array[path] . "?" . $url_array[query] ." HTTP/1.0\r\n"; 
    $send .= "Host: " . $url_array[host] . " \r\n"; 
    $send .= "User-Agent: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)\r\n"; 
    $send .= "Accept-Language: " . $lang . "\r\n"; 
    $send .= "Connection: Close\r\n\r\n"; 
    fwrite($fp, $send); 
    while ($fp && !feof($fp)) 
    { 
      $headerbuffer = fgets($fp, 1024); 
      if (urlencode($headerbuffer) == "%0D%0A") 
      { 
        break; 
      } 
    } 
    $xml_data = ''; 
    while (!feof($fp)) 
    { 
      $xml_data .= fgets($fp, 1024); 
    } 
    fclose($fp); 
    return $xml_data; 
  }  

require_once 'scraperwiki/simple_html_dom.php';
scraperwiki::save_var('dummy', 0);

$dom = new simple_html_dom();

$placeholder = scraperwiki::get_var("page");
scraperwiki::save_var("page",$i);
$xml = get_xml_data_from_url("http://www.holidaycottages.co.uk/cottageURL.xml");
// Load HTML from a URL
$dom->load($xml);
// page
foreach($dom->find('loc') as $coturl){
  $record = array(
    'COTTAGE_URL'   => $coturl->plaintext,
  );      
  
  if(!strpos($coturl->plaintext,"/map")&&!strpos($coturl->plaintext,"/photos"))
  scraperwiki::save(array('COTTAGE_URL'), $record);
}
?>
