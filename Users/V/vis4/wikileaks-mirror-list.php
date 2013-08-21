<?php

require "scraperwiki/simple_html_dom.php";

$html = file_get_html("http://wikileaks.ch/Mirrors.html");

$mirrors = array();

foreach ($html->find('table td a') as $link) {
    $hostname = $link->innertext;
    $ip = gethostbyname($link->innertext);
    $latlng = locate_ip($ip);
    $mirrors[] = $ip . "\t". $hostname . "\t" . $latlnt[0] . "\t" . $latlnt[1];
}

file_put_contents("mirrors.tsv", implode("\n", $mirrors));

/*
 * locates a given ip using the GeoLiteCity DB by maxmind.com
 * this will not run in scraperwiki since it needs the external db
 */
function locate_ip($ip_str) {
    $ip_arr = explode(".", $ip_str);
    $sql = "SELECT cbc.lat, cbc.lng FROM ip4 LEFT JOIN cityByCountry cbc ON (cbc.country = ip4.country AND cbc.city = ip4.city) "
          . "WHERE ip = INET_ATON('$ip_str') OR ip = INET_ATON('$ip_str') - ".intval($ip_arr[3])." "
          . "ORDER BY ip DESC LIMIT 1";
    $res = mysql_query($sql);
    if ($row = mysql_fetch_array($res, MYSQL_NUM)) {
        return $row;
    }
    // ip isn't found in list, let's try scraping some geo-location service on the web
    $data = file_get_contents( "http://www.websitegoodies.com/tools/geoip.php?ip=".$ip_str );
    if (!empty($data)) {
        $a = strpos($data, 'http://maps.google.com/maps?q=');
        if ($a > 0) {
            return explode("+", substr( $data, $a+30, strpos($data, '"', $a+30) - $a - 30));
        }
    }
    return array(0,0);
}

