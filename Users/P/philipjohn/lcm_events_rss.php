<?php

/**
 * LCM Events feed
 * An RSS feed of all Lichfield-based events
 */

/**
 To do list
  - Scrape the LDC events feed and pull that in too
  - Re-engineer the saved data from Cathdral and LDAA scrapers
*/

// Grab the Cathedral Events
scraperwiki::attach("lichfield_cathedral_events", "cathedral");           
$cathedral = scraperwiki::select("* from cathedral.swdata");

// Grab the LDAA Events
scraperwiki::attach("hhhlich-lichfield-arts-events", "ldaa");           
$ldaa = scraperwiki::select("* from ldaa.swdata");

// Set the content-type
//scraperwiki::httpresponseheader("Content-Type", "text/xml");

// Merge the events together
$events = array_merge($cathedral, $ldaa);

// Order the events by date
function aasort (&$array, $key) {
    $sorter=array();
    $ret=array();
    reset($array);
    foreach ($array as $ii => $va) {
        $sorter[$ii]=$va[$key];
    }
    asort($sorter);
    foreach ($sorter as $ii => $va) {
        $ret[$ii]=$array[$ii];
    }
    $array=$ret;
    return $array;
}
$sevents = aasort($events, "pubDate");

print_r($sevents);

?>
