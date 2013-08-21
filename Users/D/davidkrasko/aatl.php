<?php

 $url = "https://leginfo.legislature.ca.gov/faces/loginClient.xhtml?destPage=home.xhtml";

$ch = curl_init();    
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);

curl_setopt($ch, CURLOPT_URL, $url);
$cookie = 'cookies.txt';
$timeout = 30;

curl_setopt ($ch, CURLOPT_FOLLOWLOCATION, 1);
curl_setopt($ch, CURLOPT_TIMEOUT,         10);
curl_setopt($ch, CURLOPT_CONNECTTIMEOUT,  $timeout );
curl_setopt($ch, CURLOPT_COOKIEJAR,       $cookie);
curl_setopt($ch, CURLOPT_COOKIEFILE,      $cookie);

curl_setopt ($ch, CURLOPT_POST, 1);
curl_setopt ($ch,CURLOPT_POSTFIELDS,"loginformclientfrm:passwordField=dkrasko@waveware.com&loginformclientfrm:passwordField=lotus9283");     

$result = curl_exec($ch);
curl_close($ch);
echo $result;



$html = scraperWiki::scrape("http://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=201320140AB6&search_keywords=");
print $html . "\n";

?>
