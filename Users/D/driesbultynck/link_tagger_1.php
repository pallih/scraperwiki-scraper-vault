<?php
/* SETTINGS */
//Nog loopen door resultaten

$source="http://www.washingtontimes.com/news/2012/sep/18/pentagon-stops-training-partnering-afghan-troops-b/";
$host = parse_url($source,PHP_URL_HOST);
$ip = gethostbyname($host);
$info = get_ip_info($ip);

$result = array('host'=>$host, 'ip'=>$ip, 'info'=>$info);

print_r($result);
/*
Array
(
    [host] => www.washingtontimes.com
    [ip] => 38.118.71.70
    [info] => Array
        (
            [host] => theconservatives.com
            [country] => United States
            [country_code] => USA
            [continent] => North America
            [region] => Virginia
            [latitude] => 38.9687
            [longitude] => -77.3411
            [organization] => Cogent Communications
            [isp] => Cogent Communications
        )

)
*/
echo $result['info']['country']; //United States

function get_ip_info($ip = NULL){
    if(empty($ip)) $ip = $_SERVER['REMOTE_ADDR'];

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL,'http://www.ipaddresslocation.org/ip-address-locator.php');
    curl_setopt($ch, CURLOPT_RETURNTRANSFER,1);
    curl_setopt($ch, CURLOPT_POST,true);
    curl_setopt($ch, CURLOPT_POSTFIELDS,array('ip'=>$ip));
    $data = curl_exec($ch);
    curl_close($ch);
    preg_match_all('/<i>([a-z\s]+)\:<\/i>\s+<b>(.*)<\/b>/im',$data,$matches,PREG_SET_ORDER);
    if(count($matches)==0)return false;
    $return = array();
    $labels = array(
    'Hostname'          => 'host',
    'IP Country'        => 'country',
    'IP Country Code'   => 'country_code',
    'IP Continent'      => 'continent',
    'IP Region'         => 'region',
    'IP Latitude'       => 'latitude',
    'IP Longitude'      => 'longitude',
    'Organization'      => 'organization',
    'ISP Provider'      => 'isp');
    foreach($matches as $info){
        if(isset($info[2]) && !is_null($labels[$info[1]])){
            $return[$labels[$info[1]]]=$info[2];
        }
    }

    return (count($return))?$return:false;
}


/*
require 'scraperwiki/simple_html_dom.php'; 
$source="http://www.washingtontimes.com/news/2012/sep/18/pentagon-stops-training-partnering-afghan-troops-b/";
$utmSource="";
$utmMedium="";
$utmTerm="";
$utmContent="";
$utmCampaign="";

scrape($source);

function scrape($source){
    global $source, $utmSource, $utmMedium, $utmTerm, $utmContent, $utmCampaign;
            $link = scraperwiki::scrape($source);
            $html = str_get_html($link);   
        foreach ($html->find('a[href]') as $a) {
            $href = $a->href;
            $a->href = $href.'#utm_source='.$utmSource.'&utm_medium='.$utmMedium.'&utm_term='.$utmTerm.'&utm_content='.$utmContent.'&utm_campaign='.$utmCampaign;
        } 
print $html;            
}



*/
?>
