<?php
/*
$insert_ical = array();
$insert_ical['link'] = $insert['link'];
$insert_ical['DTSTART'] = $strt;
$insert_ical['DTEND'] = $strt+86399;
$insert_ical['FREQ'] = "DAILY";
$insert_ical['BYDAY'] = "";
$insert_ical['WKST'] = "MO";
$insert_ical['COUNT'] = round(($nd-$strt)/86400);

$insert_event = array();
$insert_event['name'] = "";
$insert_event['link'] = "";

$insert_venue = array();
$insert_venue['name'] = "";
$insert_venue['postcode'] = "";
$insert_venue['lat'] = "";
$insert_venue['lng'] = "";
$insert_venue['picture'] = "";

*/
scraperwiki::attach("lichfield_cathedral_events", "cathedral");           
$cathedral = scraperwiki::select("* from cathedral.swdata");

foreach (scraperwiki::select("* from cathedral.swdata") as $record) {
    var_dump($record);
    die();
}

?>
