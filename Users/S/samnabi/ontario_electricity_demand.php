<?php

// Set URL to parse
$url = "http://www.ieso.ca/imoweb/market/mi5_includes/maag/maag_xml/maag.xml";

// Return source code as a string ($viewsource)
$handler = curl_init($url);
curl_setopt($handler, CURLOPT_RETURNTRANSFER, true);
$viewsource = curl_exec($handler);
curl_close($handler);

// Look for date/time
$dateindicator = "dat1";
$datepos = strpos($viewsource, $dateindicator); // haystack, needle
$date = substr($viewsource, $datepos, 46); // haystack, start, length 
$date = substr($date, 17); // cut off first x characters of the specified length
$year = substr($date, 0, 4); // cursor position, length
$month = substr($date, 5, 2);
//$month = date("M", mktime(0, 0, 0, $month)); // Convert month number to words
$day = substr($date, 8, 2);
$hour = substr($date, 11, 2);
$minute = substr($date, 14, 2);

$timestamp = strtotime("$year/$month/$day $hour:$minute");
$timestamp = ($timestamp-18000)*1000; // 18000 seconds is 5 hours (to offset from UTC). Multiply by 1000 to get javascript format
if(date(I,strtotime("$month/$day/$year $hour:$minute"))==1) {
    $timestamp = $timestamp+3600000; // Add an hour during daylight savings
}

// Look for Market Demand (MW)
$mktMWindicator = "<info_title>Market Demand</info_title>";
$mktMWpos = strpos($viewsource, $mktMWindicator);
$mktMW = substr($viewsource, $mktMWpos, 59); 
$mktMW = substr($mktMW, 52);

// Look for Ontario Demand (MW)
$ontMWindicator = "<info_title>Ontario Demand</info_title>";
$ontMWpos = strpos($viewsource, $ontMWindicator);
$ontMW = substr($viewsource, $ontMWpos, 60); 
$ontMW = substr($ontMW, 53);

// Display the current info
echo "<p>On $day $month $year at $hour:$minute EST, total market demand for electricity in Ontario was $mktMW megawatts. Demand within Ontario was $ontMW megawatts.</p>";

// Save results tot he ScraperWiki database
$record = array(
    'timestamp' => $timestamp, // Gives the time in UTC
    'date' => $month.'/'.$day.'/'.$year.' '.$hour.':'.$minute,
    'marketdemand' => $mktMW,
    'ontariodemand' => $ontMW
);
scraperwiki::save(array('timestamp'), $record);
scraperwiki::save(array('date'), $record);
scraperwiki::save(array('marketdemand'), $record);
scraperwiki::save(array('ontariodemand'), $record);

?>
<?php

// Set URL to parse
$url = "http://www.ieso.ca/imoweb/market/mi5_includes/maag/maag_xml/maag.xml";

// Return source code as a string ($viewsource)
$handler = curl_init($url);
curl_setopt($handler, CURLOPT_RETURNTRANSFER, true);
$viewsource = curl_exec($handler);
curl_close($handler);

// Look for date/time
$dateindicator = "dat1";
$datepos = strpos($viewsource, $dateindicator); // haystack, needle
$date = substr($viewsource, $datepos, 46); // haystack, start, length 
$date = substr($date, 17); // cut off first x characters of the specified length
$year = substr($date, 0, 4); // cursor position, length
$month = substr($date, 5, 2);
//$month = date("M", mktime(0, 0, 0, $month)); // Convert month number to words
$day = substr($date, 8, 2);
$hour = substr($date, 11, 2);
$minute = substr($date, 14, 2);

$timestamp = strtotime("$year/$month/$day $hour:$minute");
$timestamp = ($timestamp-18000)*1000; // 18000 seconds is 5 hours (to offset from UTC). Multiply by 1000 to get javascript format
if(date(I,strtotime("$month/$day/$year $hour:$minute"))==1) {
    $timestamp = $timestamp+3600000; // Add an hour during daylight savings
}

// Look for Market Demand (MW)
$mktMWindicator = "<info_title>Market Demand</info_title>";
$mktMWpos = strpos($viewsource, $mktMWindicator);
$mktMW = substr($viewsource, $mktMWpos, 59); 
$mktMW = substr($mktMW, 52);

// Look for Ontario Demand (MW)
$ontMWindicator = "<info_title>Ontario Demand</info_title>";
$ontMWpos = strpos($viewsource, $ontMWindicator);
$ontMW = substr($viewsource, $ontMWpos, 60); 
$ontMW = substr($ontMW, 53);

// Display the current info
echo "<p>On $day $month $year at $hour:$minute EST, total market demand for electricity in Ontario was $mktMW megawatts. Demand within Ontario was $ontMW megawatts.</p>";

// Save results tot he ScraperWiki database
$record = array(
    'timestamp' => $timestamp, // Gives the time in UTC
    'date' => $month.'/'.$day.'/'.$year.' '.$hour.':'.$minute,
    'marketdemand' => $mktMW,
    'ontariodemand' => $ontMW
);
scraperwiki::save(array('timestamp'), $record);
scraperwiki::save(array('date'), $record);
scraperwiki::save(array('marketdemand'), $record);
scraperwiki::save(array('ontariodemand'), $record);

?>
