<?php
######################################
# Basic PHP scraper
######################################

$html = scraperwiki::scrape("http://listz.co.uk/greater-london");
$html = oneline($html);
preg_match_all('|<div class="prts"><a href="(.*?)" title=".*?">.*?</a></div>|',$html,$area);


foreach ($area[1] as $key=>$val) {
$html = scraperwiki::scrape("http://listz.co.uk".$val."_photographers");
$html = oneline($html);
preg_match_all('|<a href="(/company/.*?)" title="|',$html,$link);


foreach ($link[1] as $key=>$val) {
$html = scraperwiki::scrape("http://listz.co.uk".$val);
$html = oneline($html);
#preg_match_all('|qualifications_overview.htm">([A-Z]+)<b>|',$html,$qual);

preg_match_all('|<b>City/Town:</b> (.*?)<br />|',$html,$county);
#preg_match_all('|</h2>(.*?)<br><br>|',$html,$details);
#preg_match_all('|</h2> +([A-Za-z\'\/ ]+) +.*? +<|',$html,$forename);
#preg_match_all('|</h2>[ ]+.*?[ ]+([A-Za-z\'\/]+)<|',$html,$surname);
preg_match_all('|<strong>(.*?)</strong>|',$html,$business);
#preg_match_all('|</h2>.*?([A-Za-z ]+)<br><br>|',$html,$country);
preg_match_all('|([A-Za-z]+[0-9A-Za-z]+ [0-9][A-Za-z]+)|',$html,$postcode);
#preg_match_all('|Postcode:([A-Za-z]+[0-9A-Za-z]+) [0-9][A-Za-z]+<br>|',$html,$postcodedistrict);
#preg_match_all('|Postcode:([A-Za-z]+)[0-9A-Za-z]+ [0-9][A-Za-z]+<br>|',$html,$postcodearea);
preg_match_all('|<b>Address:</b> (.*?)<br />|',$html,$address);
preg_match_all('|<b>Main phone:</b> (.*?)<br />|',$html,$tel);
#preg_match_all('|mobile:- ([0-9 ]+)<br>|',$html,$mob);
#preg_match_all('|mailto:(.*?)\?subject|',$html,$email);
#preg_match_all('|web address:-.*?redir=(.*?)"|',$html,$web);
#preg_match_all('|(http://www.facebook.com/.*?)"|',$html,$facebook);

if (!isset($county[1][0])) { $county[1][0] = '';}
#if (!isset($details[1][0])) { $details[1][0] = '';}
#if (!isset($forename[1][0])) { $forename[1][0] = '';}
#if (!isset($surname[1][0])) { $surname[1][0] = '';}
if (!isset($business[1][0])) { $business[1][0] = '';}
#if (!isset($qual[1][0])) { $qual[1][0] = '';}
#if (!isset($country[1][0])) { $country[1][0] = '';}
if (!isset($postcode[1][0])) { $postcode[1][0] = '';}
#if (!isset($postcode[1][0])) { $postcodedistrict[1][0] = '';}
#if (!isset($postcode[1][0])) { $postcodearea[1][0] = '';}
if (!isset($address[1][0])) { $address[1][0] = '';}
if (!isset($tel[1][0])) { $tel[1][0] = '';}
#if (!isset($mob[1][0])) { $mob[1][0] = '';}
#if (!isset($email[1][0])) { $email[1][0] = '';}
#if (!isset($web[1][0])) { $web[1][0] = '';}
#if (!isset($facebook[1][0])) { $facebook[1][0] = '';}

#$latlng = scraperwiki::gb_postcode_to_latlng($postcode[1][0]);
#$lat = $latlng[0];
#$lng = $latlng[1];

#if (!isset($lat[1][0])) { $lat[1][0] = '';}
#if (!isset($lng[1][0])) { $lng[1][0] = '';}


#$postcode = str_replace('LL18 3EB','',$postcode[1][0]);

scraperwiki::save(array('link'), array(
    'link' => "http://listz.co.uk".$val,
    #'county' => clean($county[1][0]),
    'country' => "UK",
    #'surname' => clean($surname[1][0]),
    #'forename' => clean($forename[1][0]),
    'business' => clean($business[1][0]),
    #'qual' => clean($qual[1][0]),
    #'details' => clean($details[1][0]),
    'postcode' => clean($postcode[1][0]),
    #'lat' => $lat,
    #'lng' => $lng,
    #'postcodedistrict' => clean($postcodedistrict[1][0]),
    #'postcodearea' => clean($postcodearea[1][0]),
    'address' => clean($address[1][0]),
    'tel' => clean($tel[1][0]),
    #'mob' => clean($mob[1][0]),
    #'email' => clean($email[1][0]),
    #'web' => clean($web[1][0]),
    #'facebook' => clean($facebook[1][0]),
    'index' => "Listz"
));

}
}

    function clean($val) {
        $val = str_replace('&nbsp;',' ',$val);
        $val = str_replace('&amp;','&',$val);
        $val = html_entity_decode($val);
        $val = strip_tags($val);
        $val = trim($val);
        $val = utf8_decode($val);
        return($val);
    }
    
    function oneline($code) {
        $code = str_replace("\n",'',$code);
        $code = str_replace("\r",'',$code);
        $code = str_replace("\t",'',$code);
        return $code;
    }
   
?><?php
######################################
# Basic PHP scraper
######################################

$html = scraperwiki::scrape("http://listz.co.uk/greater-london");
$html = oneline($html);
preg_match_all('|<div class="prts"><a href="(.*?)" title=".*?">.*?</a></div>|',$html,$area);


foreach ($area[1] as $key=>$val) {
$html = scraperwiki::scrape("http://listz.co.uk".$val."_photographers");
$html = oneline($html);
preg_match_all('|<a href="(/company/.*?)" title="|',$html,$link);


foreach ($link[1] as $key=>$val) {
$html = scraperwiki::scrape("http://listz.co.uk".$val);
$html = oneline($html);
#preg_match_all('|qualifications_overview.htm">([A-Z]+)<b>|',$html,$qual);

preg_match_all('|<b>City/Town:</b> (.*?)<br />|',$html,$county);
#preg_match_all('|</h2>(.*?)<br><br>|',$html,$details);
#preg_match_all('|</h2> +([A-Za-z\'\/ ]+) +.*? +<|',$html,$forename);
#preg_match_all('|</h2>[ ]+.*?[ ]+([A-Za-z\'\/]+)<|',$html,$surname);
preg_match_all('|<strong>(.*?)</strong>|',$html,$business);
#preg_match_all('|</h2>.*?([A-Za-z ]+)<br><br>|',$html,$country);
preg_match_all('|([A-Za-z]+[0-9A-Za-z]+ [0-9][A-Za-z]+)|',$html,$postcode);
#preg_match_all('|Postcode:([A-Za-z]+[0-9A-Za-z]+) [0-9][A-Za-z]+<br>|',$html,$postcodedistrict);
#preg_match_all('|Postcode:([A-Za-z]+)[0-9A-Za-z]+ [0-9][A-Za-z]+<br>|',$html,$postcodearea);
preg_match_all('|<b>Address:</b> (.*?)<br />|',$html,$address);
preg_match_all('|<b>Main phone:</b> (.*?)<br />|',$html,$tel);
#preg_match_all('|mobile:- ([0-9 ]+)<br>|',$html,$mob);
#preg_match_all('|mailto:(.*?)\?subject|',$html,$email);
#preg_match_all('|web address:-.*?redir=(.*?)"|',$html,$web);
#preg_match_all('|(http://www.facebook.com/.*?)"|',$html,$facebook);

if (!isset($county[1][0])) { $county[1][0] = '';}
#if (!isset($details[1][0])) { $details[1][0] = '';}
#if (!isset($forename[1][0])) { $forename[1][0] = '';}
#if (!isset($surname[1][0])) { $surname[1][0] = '';}
if (!isset($business[1][0])) { $business[1][0] = '';}
#if (!isset($qual[1][0])) { $qual[1][0] = '';}
#if (!isset($country[1][0])) { $country[1][0] = '';}
if (!isset($postcode[1][0])) { $postcode[1][0] = '';}
#if (!isset($postcode[1][0])) { $postcodedistrict[1][0] = '';}
#if (!isset($postcode[1][0])) { $postcodearea[1][0] = '';}
if (!isset($address[1][0])) { $address[1][0] = '';}
if (!isset($tel[1][0])) { $tel[1][0] = '';}
#if (!isset($mob[1][0])) { $mob[1][0] = '';}
#if (!isset($email[1][0])) { $email[1][0] = '';}
#if (!isset($web[1][0])) { $web[1][0] = '';}
#if (!isset($facebook[1][0])) { $facebook[1][0] = '';}

#$latlng = scraperwiki::gb_postcode_to_latlng($postcode[1][0]);
#$lat = $latlng[0];
#$lng = $latlng[1];

#if (!isset($lat[1][0])) { $lat[1][0] = '';}
#if (!isset($lng[1][0])) { $lng[1][0] = '';}


#$postcode = str_replace('LL18 3EB','',$postcode[1][0]);

scraperwiki::save(array('link'), array(
    'link' => "http://listz.co.uk".$val,
    #'county' => clean($county[1][0]),
    'country' => "UK",
    #'surname' => clean($surname[1][0]),
    #'forename' => clean($forename[1][0]),
    'business' => clean($business[1][0]),
    #'qual' => clean($qual[1][0]),
    #'details' => clean($details[1][0]),
    'postcode' => clean($postcode[1][0]),
    #'lat' => $lat,
    #'lng' => $lng,
    #'postcodedistrict' => clean($postcodedistrict[1][0]),
    #'postcodearea' => clean($postcodearea[1][0]),
    'address' => clean($address[1][0]),
    'tel' => clean($tel[1][0]),
    #'mob' => clean($mob[1][0]),
    #'email' => clean($email[1][0]),
    #'web' => clean($web[1][0]),
    #'facebook' => clean($facebook[1][0]),
    'index' => "Listz"
));

}
}

    function clean($val) {
        $val = str_replace('&nbsp;',' ',$val);
        $val = str_replace('&amp;','&',$val);
        $val = html_entity_decode($val);
        $val = strip_tags($val);
        $val = trim($val);
        $val = utf8_decode($val);
        return($val);
    }
    
    function oneline($code) {
        $code = str_replace("\n",'',$code);
        $code = str_replace("\r",'',$code);
        $code = str_replace("\t",'',$code);
        return $code;
    }
   
?>