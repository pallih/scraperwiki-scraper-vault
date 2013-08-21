<?php
// Derive an ical string of 10 eventss 
$querylist = explode("&", getenv("QUERY_STRING")); 
$limit = 10; 
$offset = 0; 
foreach ($querylist as $queryl)
{
    $ql = explode("=", $queryl); 
    if (($ql[0] == "limit") && (count($ql) == 2))
        $limit = intval($ql[1]); 
    if (($ql[0] == "offset") && (count($ql) == 2))
        $offset = intval($ql[1]); 
}

scraperwiki::httpresponseheader("Content-Type", "text/plain"); 

scraperwiki::attach('ons_release_schedule_ical'); 
$vevents = scraperwiki::select("* from ons_release_schedule_ical.vevents limit $limit offset $offset"); 
$icalevents = array(); 
foreach ($vevents as $vevent)
{
    $icalevent = "BEGIN:VEVENT\nDTSTAMP".$vevent["DTSTAMP"]."\nDTSTART".$vevent["DTSTART"]."\nX-TITLE:".$vevent["Title"]."\nSUMMARY:".$vevent["Summary"]."\nDESCRIPTION:Theme: ".$vevent["Theme"]."\n".$vevent["Summary"]."\\nEND:VEVENT\n"; 
    #print_r($icalevent); 
    $icalevents[] = $icalevent; 
}

print "BEGIN:VCALENDAR
METHOD:PUBLISH
VERSION:2.0
X-WR-CALNAME:ONS Release Calendar
PRODID:-//Apple Inc.//iCal 4.0.4//EN
X-APPLE-CALENDAR-COLOR:#B027AE
X-WR-TIMEZONE:Europe/London
CALSCALE:GREGORIAN
".implode("", $icalevents)."
END:VCALENDAR";

?>
