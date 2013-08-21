<?php

scraperwiki::httpresponseheader("Content-Type", "text/plain");

scraperwiki::attach('days_of_the_year');
$vevents = scraperwiki::select("* from days_of_the_year.eventdays");
$icalevents = array();
foreach ($vevents as $vevent)
{
    $timestamp= strtotime($vevent['date']);
    $formattedStart = date('Ymd\T180000\Z',$timestamp);
    $formattedEnd = date('Ymd\T190000\Z',$timestamp);
    $description = $vevent['Description'].(strlen($vevent['Description'])>0?"\r":"")
    .$vevent['Founded'].(strlen($vevent['Founded'])>0?"\r":"")
    .$vevent['Resources'].(strlen($vevent['Resources'])>0?"\r":"")
    .$vevent['link'];
    $icalevent = "BEGIN:VEVENT"
                ."\rDTSTART:".$formattedStart
                ."\rDTEND:".$formattedEnd
                ."\rDTSTAMP:".$formattedStart
                ."\rUID:".date('Ymd123456',$timestamp)
                ."\rCLASS:PUBLIC"
                ."\rCREATED:20130101T000000Z"
                ."\rDESCRIPTION:".$description."\r"
                ."\rSUMMARY:".$vevent['name']
                ."\rSEQUENCE:0"
                ."\rSTATUS:CONFIRMED"
                ."\rTRANSP:OPAQUE"
                ."\rX-TITLE:".$vevent["name"]
                ."\rEND:VEVENT\r";
    /*#print_r($icalevent);*/
    $icalevents[] = $icalevent;
}

print "BEGIN:VCALENDAR\r
METHOD:PUBLISH\r
VERSION:2.0\r
X-WR-CALNAME:Days of the Year\r
PRODID:-//Apple Inc.//iCal 4.0.4//EN\r
X-WR-TIMEZONE:Europe/London\r
CALSCALE:GREGORIAN\r
".implode("", $icalevents)."END:VCALENDAR";

?>