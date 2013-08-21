<?php
require  'scraperwiki/simple_html_dom.php';


// v6 - all users just location
$chel=0;
$place=0;
$chelmin = 5691;
//$names= ();
//$locations = ();

for($page = 1; $page < 4000; $page++)
{
if($page*15 < $chelmin) {$chel+=15; $place+=15; continue;};
    print "*** Scraping all-stars page " . $page . "\n\n";

    $html = scraperwiki::scrape('http://dribbble.com/members/all-stars?page=' . $page);
    $dom = new simple_html_dom();
    $dom->load($html);

    $names = $dom->find('<a[rel=contact]');
    $locations = $dom->find('em[class=locality]');
    for ($i=0; $i<15; $i++)
    {

$chel++;
$place++;
if($chel < $chelmin) {continue;};
$loc = $locations[$i];
$data = $names[$i];


$locstr = $loc->plaintext;
//print $loc->plaintext;
$pattern = '/(\t)/i';
$replacement = '';
$locstr = preg_replace($pattern, $replacement, $locstr);

$pattern = '/(\s)(.*)(\s)/i';
$replacement = '$2';
$locstr = preg_replace($pattern, $replacement, $locstr);
//print "'" . $locstr . "'";
//http://where.yahooapis.com/geocode?q=NYC
//$xmlstr = scraperwiki::scrape('http://maps.googleapis.com/maps/api/geocode/xml?sensor=false&address=' . urlencode($locstr));
$xmlstr = scraperwiki::scrape('http://where.yahooapis.com/geocode?q=' . urlencode($locstr));
//print $xmlstr;

$xml = new SimpleXMLElement($xmlstr);

//print "Lat/Lng: " . $xml->result->geometry->location->lat . "/" . $xml->result->geometry->location->lng . "\n";
//print "Lat/Lng: " . $xml->Result->latitude . "/" . $xml->Result->longitude . "\n";

//if($xml->result->geometry->location->lat && $xml->result->geometry->location->lng){
if($xml->Result->latitude && $xml->Result->longitude){
//    $xmlstr = scraperwiki::scrape('http://www.earthtools.org/timezone/' . $xml->result->geometry->location->lat . '/' . $xml->result->geometry->location->lng);
    $xmlstr = scraperwiki::scrape('http://www.earthtools.org/timezone/' . $xml->Result->latitude . '/' . $xml->Result->longitude);
    $xml = new SimpleXMLElement($xmlstr);
}
//print "Offset: " . $xml->offset;

            print $place . ";" . $data->plaintext . '; ' . 'http://dribbble.com' . $data->href . '; ' . $loc->plaintext . ";" . $xml->offset . "\n";

            scraperwiki::save(array('http'), array('place' => $place, 'http' => 'http://dribbble.com' . $data->href, 'name' => $data->plaintext, 'location' => $loc->plaintext, 'offset' => "" . $xml->offset));
    }

    unset($html);

    $dom->clear();
    unset($dom);
}

?>