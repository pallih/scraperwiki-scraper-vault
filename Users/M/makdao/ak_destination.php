<?php
// ScrapeWiki @ https://scraperwiki.com/profiles/makdao/
require('scraperwiki/simple_html_dom.php');

// AirAsia Flight Destination @ AK_Destination
$siteUrl = 'http://www.theairdb.com/airline/air-asia.html';
$html = str_get_html(scraperWiki::scrape($siteUrl));
//echo($html . "\n");
$savedTable = 'AK_Destination';

$dom = new simple_html_dom();
$dom->load($html);
foreach ($dom->find('//*[@id="AirportsForThisAirline"]/div/a[@title="Center it on the map!"]') as $data) {
  //echo($data . "\n");
  $airportName = $data->innertext;
  preg_match('/.+(\((.+)\))$/', $airportName, $match);
  $airportCode = $match[2];
  //echo($airportCode . ' => ' . $airportName . "\n");
  
  $destination = array('airportCode' => $airportCode,
                       'airportName' => $airportName);
  scraperwiki::save_sqlite(array('airportCode'), $destination, $savedTable);
}
?>
