<?php
######################################
# Basic PHP scraper
######################################

$profbody = "SISLP";

#$html = scraperwiki::scrape("http://".$profbody.".com/members/");
#$html = oneline($html);
#preg_match_all('|<td width=""><a href="(.*?).htm">.*?</a>|',$html,$nation);

#foreach ($nation[1] as $key=>$val) {
#$val = urlencode($val);
$html = scraperwiki::scrape("http://".$profbody.".com/members");
$html = oneline($html);
preg_match_all('|<br><a href="([a-zA-Z0-9 ]+.htm)">|',$html,$link);


foreach ($link[1] as $key=>$val) {
$val = urlencode($val);
$html = scraperwiki::scrape("http://".$profbody.".com/members/".$val);
$html = oneline($html);
preg_match_all('|qualifications_overview.htm">([A-Z]+)<b>|',$html,$qual);
$html = preg_replace('|  <a class="tooltip" href="../qualifications_overview.htm">.*?<b><em></em>This shows the.*?and associated societies.</b></a>|','',$html);

preg_match_all('|<h2>(.*?)</h2>|',$html,$county);
preg_match_all('|</h2>(.*?)<br><br>|',$html,$details);
preg_match_all('|</h2> +([A-Za-z\'\/ ]+) +.*? +<|',$html,$forename);
preg_match_all('|</h2>[ ]+.*?[ ]+([A-Za-z\'\/]+)<|',$html,$surname);
preg_match_all('|</h2>.*?<br>(.*?)<br>|',$html,$business);
preg_match_all('|</h2>.*?([A-Za-z ]+)<br><br>|',$html,$country);
preg_match_all('|([A-Za-z]+[0-9A-Za-z]+ [0-9][A-Za-z]+)|',$html,$postcode);
preg_match_all('|([A-Za-z]+[0-9A-Za-z]+) [0-9][A-Za-z]+|',$html,$postcodedistrict);
preg_match_all('|([A-Za-z]+)[0-9A-Za-z]+ [0-9][A-Za-z]+|',$html,$postcodearea);
preg_match_all('|</h2>.*?<br>.*?<br>(.*?)[A-Za-z ]+<br><br>|',$html,$address);
preg_match_all('|tel:- ([0-9 ]+)<br>|',$html,$tel);
preg_match_all('|mobile:- ([0-9 ]+)<br>|',$html,$mob);
preg_match_all('|mailto:(.*?)\?subject|',$html,$email);
preg_match_all('|web address:-.*?redir=(.*?)"|',$html,$web);
preg_match_all('|(http://www.facebook.com/.*?)"|',$html,$facebook);

if (!isset($county[1][0])) { $county[1][0] = '';}
if (!isset($details[1][0])) { $details[1][0] = '';}
if (!isset($forename[1][0])) { $forename[1][0] = '';}
if (!isset($surname[1][0])) { $surname[1][0] = '';}
if (!isset($business[1][0])) { $business[1][0] = '';}
if (!isset($qual[1][0])) { $qual[1][0] = '';}
if (!isset($country[1][0])) { $country[1][0] = '';}
if (!isset($postcode[1][0])) { $postcode[1][0] = '';}
if (!isset($postcodedistrict[1][0])) { $postcodedistrict[1][0] = '';}
if (!isset($postcodearea[1][0])) { $postcodearea[1][0] = '';}
if (!isset($address[1][0])) { $address[1][0] = '';}
if (!isset($tel[1][0])) { $tel[1][0] = '';}
if (!isset($mob[1][0])) { $mob[1][0] = '';}
if (!isset($email[1][0])) { $email[1][0] = '';}
if (!isset($web[1][0])) { $web[1][0] = '';}
if (!isset($facebook[1][0])) { $facebook[1][0] = '';}

$latlng = scraperwiki::gb_postcode_to_latlng($postcode[1][0]);
$lat = $latlng[0];
$lng = $latlng[1];

#if (!isset($lat[1][0])) { $lat[1][0] = '';}
#if (!isset($lng[1][0])) { $lng[1][0] = '';}


$postcode = str_replace('LL18 3EB','',$postcode[1][0]);

scraperwiki::save(array('business'), array(
    'link' => "http://".$profbody.".co.uk/members/".$val,
    'county' => clean($county[1][0]),
    'country' => clean($country[1][0]),
    'surname' => clean($surname[1][0]),
    'forename' => clean($forename[1][0]),
    'business' => clean($business[1][0]),
    'qual' => clean($qual[1][0]),
    'details' => clean($details[1][0]),
    'postcode' => clean($postcode),
    'lat' => $lat,
    'lng' => $lng,
    'postcodedistrict' => clean($postcodedistrict[1][0]),
    'postcodearea' => clean($postcodearea[1][0]),
    'address' => clean($address[1][0]),
    'tel' => clean($tel[1][0]),
    'mob' => clean($mob[1][0]),
    'email' => clean($email[1][0]),
    'web' => clean($web[1][0]),
    'facebook' => clean($facebook[1][0]),
    'probody' => $profbody
));

}
#}

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
        return $code;
    }
   
?>