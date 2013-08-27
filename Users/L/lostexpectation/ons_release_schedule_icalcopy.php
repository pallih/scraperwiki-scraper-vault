<?php
// Derive an ical string of 10 eventss 
$querylist = explode("&", getenv("QUERY_STRING")); 
$limit = 10000; 
$offset = 0; 
foreach ($querylist as $queryl)
{
    $ql = explode("=", $queryl); 
    if (($ql[0] == "limit") && (count($ql) == 2))
        $limit = intval($ql[1]); 
    if (($ql[0] == "offset") && (count($ql) == 2))
        $offset = intval($ql[1]); 
}

//scraperwiki::httpresponseheader("Content-Type", "text/plain"); 

scraperwiki::httpresponseheader("Content-Type", 'text/calendar'); //; charset=utf-8');
scraperwiki::httpresponseheader("Content-Disposition", "inline; filename=pres.ics");

scraperwiki::attach('irish_president_engagements'); 
$vevents = scraperwiki::select("* from irish_president_engagements.swdata limit $limit offset $offset"); 
$icalevents = array(); 
foreach ($vevents as $vevents)
{

//date info place time
//= ":".date("Ymd")."T".date("His")."Z";
$vdate = $vevents["date"];
$vtime = $vevents["time"];
$vtime = str_replace(":", "",$vtime);
$CustomDATE = ":".date("Ymd",strtotime($vdate))."T".$vtime."00Z";


//$datetime = $date("Ymd")."T".$time("His")."Z";
$CustomDATETIMESTAMP = ":".date("Ymd")."T".date("His")."Z";
// "BEGIN:VEVENT\nDTSTAMP".$vevent["DTSTAMP"]."\nDTSTART".$vevent["DTSTART"]."\nX-TITLE:"
    $icalevent = "BEGIN:VEVENT\r\nDTSTAMP".$CustomDATETIMESTAMP."\r\nDTSTART".$CustomDATE."\r\nX-TITLE:".$vevents["info"]."\r\nSUMMARY:".$vevents["info"]."\r\nDESCRIPTION: ".$vevents["info"]."\r\n".$vevents["place"]." ".$vevents["date"]." ".$vevents["time"]."\r\nEND:VEVENT\r\n"; 
    #print_r($icalevent); 
    $icalevents[] = $icalevent; 
}

print "BEGIN:VCALENDAR\r\n
METHOD:PUBLISH\r\n
VERSION:2.0\r\n
X-WR-CALNAME:irish_president_engagements\r\n
PRODID:-//Apple Inc.//iCal 4.0.4//EN\r\n
X-APPLE-CALENDAR-COLOR:#B027AE\r\n
X-WR-TIMEZONE:Europe/Dublin\r\n
CALSCALE:GREGORIAN\r\n
".implode("", $icalevents)."\r\n
END:VCALENDAR\r\n";

?>
<?php
// Derive an ical string of 10 eventss 
$querylist = explode("&", getenv("QUERY_STRING")); 
$limit = 10000; 
$offset = 0; 
foreach ($querylist as $queryl)
{
    $ql = explode("=", $queryl); 
    if (($ql[0] == "limit") && (count($ql) == 2))
        $limit = intval($ql[1]); 
    if (($ql[0] == "offset") && (count($ql) == 2))
        $offset = intval($ql[1]); 
}

//scraperwiki::httpresponseheader("Content-Type", "text/plain"); 

scraperwiki::httpresponseheader("Content-Type", 'text/calendar'); //; charset=utf-8');
scraperwiki::httpresponseheader("Content-Disposition", "inline; filename=pres.ics");

scraperwiki::attach('irish_president_engagements'); 
$vevents = scraperwiki::select("* from irish_president_engagements.swdata limit $limit offset $offset"); 
$icalevents = array(); 
foreach ($vevents as $vevents)
{

//date info place time
//= ":".date("Ymd")."T".date("His")."Z";
$vdate = $vevents["date"];
$vtime = $vevents["time"];
$vtime = str_replace(":", "",$vtime);
$CustomDATE = ":".date("Ymd",strtotime($vdate))."T".$vtime."00Z";


//$datetime = $date("Ymd")."T".$time("His")."Z";
$CustomDATETIMESTAMP = ":".date("Ymd")."T".date("His")."Z";
// "BEGIN:VEVENT\nDTSTAMP".$vevent["DTSTAMP"]."\nDTSTART".$vevent["DTSTART"]."\nX-TITLE:"
    $icalevent = "BEGIN:VEVENT\r\nDTSTAMP".$CustomDATETIMESTAMP."\r\nDTSTART".$CustomDATE."\r\nX-TITLE:".$vevents["info"]."\r\nSUMMARY:".$vevents["info"]."\r\nDESCRIPTION: ".$vevents["info"]."\r\n".$vevents["place"]." ".$vevents["date"]." ".$vevents["time"]."\r\nEND:VEVENT\r\n"; 
    #print_r($icalevent); 
    $icalevents[] = $icalevent; 
}

print "BEGIN:VCALENDAR\r\n
METHOD:PUBLISH\r\n
VERSION:2.0\r\n
X-WR-CALNAME:irish_president_engagements\r\n
PRODID:-//Apple Inc.//iCal 4.0.4//EN\r\n
X-APPLE-CALENDAR-COLOR:#B027AE\r\n
X-WR-TIMEZONE:Europe/Dublin\r\n
CALSCALE:GREGORIAN\r\n
".implode("", $icalevents)."\r\n
END:VCALENDAR\r\n";

?>
<?php
// Derive an ical string of 10 eventss 
$querylist = explode("&", getenv("QUERY_STRING")); 
$limit = 10000; 
$offset = 0; 
foreach ($querylist as $queryl)
{
    $ql = explode("=", $queryl); 
    if (($ql[0] == "limit") && (count($ql) == 2))
        $limit = intval($ql[1]); 
    if (($ql[0] == "offset") && (count($ql) == 2))
        $offset = intval($ql[1]); 
}

//scraperwiki::httpresponseheader("Content-Type", "text/plain"); 

scraperwiki::httpresponseheader("Content-Type", 'text/calendar'); //; charset=utf-8');
scraperwiki::httpresponseheader("Content-Disposition", "inline; filename=pres.ics");

scraperwiki::attach('irish_president_engagements'); 
$vevents = scraperwiki::select("* from irish_president_engagements.swdata limit $limit offset $offset"); 
$icalevents = array(); 
foreach ($vevents as $vevents)
{

//date info place time
//= ":".date("Ymd")."T".date("His")."Z";
$vdate = $vevents["date"];
$vtime = $vevents["time"];
$vtime = str_replace(":", "",$vtime);
$CustomDATE = ":".date("Ymd",strtotime($vdate))."T".$vtime."00Z";


//$datetime = $date("Ymd")."T".$time("His")."Z";
$CustomDATETIMESTAMP = ":".date("Ymd")."T".date("His")."Z";
// "BEGIN:VEVENT\nDTSTAMP".$vevent["DTSTAMP"]."\nDTSTART".$vevent["DTSTART"]."\nX-TITLE:"
    $icalevent = "BEGIN:VEVENT\r\nDTSTAMP".$CustomDATETIMESTAMP."\r\nDTSTART".$CustomDATE."\r\nX-TITLE:".$vevents["info"]."\r\nSUMMARY:".$vevents["info"]."\r\nDESCRIPTION: ".$vevents["info"]."\r\n".$vevents["place"]." ".$vevents["date"]." ".$vevents["time"]."\r\nEND:VEVENT\r\n"; 
    #print_r($icalevent); 
    $icalevents[] = $icalevent; 
}

print "BEGIN:VCALENDAR\r\n
METHOD:PUBLISH\r\n
VERSION:2.0\r\n
X-WR-CALNAME:irish_president_engagements\r\n
PRODID:-//Apple Inc.//iCal 4.0.4//EN\r\n
X-APPLE-CALENDAR-COLOR:#B027AE\r\n
X-WR-TIMEZONE:Europe/Dublin\r\n
CALSCALE:GREGORIAN\r\n
".implode("", $icalevents)."\r\n
END:VCALENDAR\r\n";

?>
