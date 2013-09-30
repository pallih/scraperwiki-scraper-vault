<?php
// Derive an ical string of 10 eventss 
$querylist = explode("&", getenv("QUERY_STRING")); 
$limit = 100; 
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

//scraperwiki::httpresponseheader("Content-Type", 'text/calendar', 'charset=utf-8');
scraperwiki::httpresponseheader("Content-Type", 'text/calendar', 'charset=utf-8');
scraperwiki::httpresponseheader("Content-Disposition", "inline; filename=pres.ics");

scraperwiki::attach('irish_president_engagementstest'); 
# select * from swdata where birth_date < '2000-01-01' just most recentdate('now');
#$vevents = scraperwiki::select("* from irish_president_engagements.swdata limit $limit offset $offset");
$vevents = scraperwiki::select("* from irish_president_engagementstest.swdata where date > date('now','-7 day');");
  
$icalevents = array(); 
foreach ($vevents as $vevents)
{

//date info place time
//= ":".date("Ymd")."T".date("His")."Z";
$vdate = $vevents["date"];
$vtime = $vevents["time"];
$vtime = str_replace(":", "",$vtime);
$CustomDATE = ":".date("Ymd",strtotime($vdate))."T".$vtime."00Z";
$vinfo = $vevents["info"];
$vinfo = preg_replace( '`&([a-z]+)(acute|uml|circ|grave|ring|cedil|slash|tilde|caron|lig);`i',"\\1", $vinfo);

$vplace = $vevents["place"];
$vplace = preg_replace( '`&([a-z]+)(acute|uml|circ|grave|ring|cedil|slash|tilde|caron|lig);`i',"\\1", $vplace);

$vinfo = str_replace(',', '\,', $vinfo);
$vplace = str_replace(',', '\,', $vplace);

$vurl = $vevents["url"];
$vurl = utf8_encode($vurl);
addslashes($vinfo);
addslashes($vplace);
//addcslashes("hello\tworld\n", "\x00..\x1fz..\xff");

//$datetime = $date("Ymd")."T".$time("His")."Z";
$CustomDATETIMESTAMP = ":".date("Ymd")."T".date("His")."Z";
// "BEGIN:VEVENT\nDTSTAMP".$vevent["DTSTAMP"]."\nDTSTART".$vevent["DTSTART"]."\nX-TITLE:"
    $icalevent = "BEGIN:VEVENT\r\nDTSTAMP".$CustomDATETIMESTAMP."\r\nDTSTART".$CustomDATE."\r\nX-TITLE:".$vinfo."\r\nSUMMARY:".$vinfo."\r\nDESCRIPTION: ".$vinfo." ".$vurl." ".$vplace." ".$vevents["date"]." ".$vevents["time"]."\r\nEND:VEVENT\r\n"; 
//  $icalevent = "BEGIN:VEVENT\r\nDTSTAMP".$CustomDATETIMESTAMP."\r\nDTSTART".$CustomDATE."\r\nX-TITLE:".$vevents["info"]."\r\nSUMMARY:".$vevents["info"]."\r\nDESCRIPTION: ".$vevents["info"].$vevents["place"]." ".$vevents["date"]." ".$vevents["time"]."\r\nEND:VEVENT\r\n"; #orig
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
$limit = 100; 
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

//scraperwiki::httpresponseheader("Content-Type", 'text/calendar', 'charset=utf-8');
scraperwiki::httpresponseheader("Content-Type", 'text/calendar', 'charset=utf-8');
scraperwiki::httpresponseheader("Content-Disposition", "inline; filename=pres.ics");

scraperwiki::attach('irish_president_engagementstest'); 
# select * from swdata where birth_date < '2000-01-01' just most recentdate('now');
#$vevents = scraperwiki::select("* from irish_president_engagements.swdata limit $limit offset $offset");
$vevents = scraperwiki::select("* from irish_president_engagementstest.swdata where date > date('now','-7 day');");
  
$icalevents = array(); 
foreach ($vevents as $vevents)
{

//date info place time
//= ":".date("Ymd")."T".date("His")."Z";
$vdate = $vevents["date"];
$vtime = $vevents["time"];
$vtime = str_replace(":", "",$vtime);
$CustomDATE = ":".date("Ymd",strtotime($vdate))."T".$vtime."00Z";
$vinfo = $vevents["info"];
$vinfo = preg_replace( '`&([a-z]+)(acute|uml|circ|grave|ring|cedil|slash|tilde|caron|lig);`i',"\\1", $vinfo);

$vplace = $vevents["place"];
$vplace = preg_replace( '`&([a-z]+)(acute|uml|circ|grave|ring|cedil|slash|tilde|caron|lig);`i',"\\1", $vplace);

$vinfo = str_replace(',', '\,', $vinfo);
$vplace = str_replace(',', '\,', $vplace);

$vurl = $vevents["url"];
$vurl = utf8_encode($vurl);
addslashes($vinfo);
addslashes($vplace);
//addcslashes("hello\tworld\n", "\x00..\x1fz..\xff");

//$datetime = $date("Ymd")."T".$time("His")."Z";
$CustomDATETIMESTAMP = ":".date("Ymd")."T".date("His")."Z";
// "BEGIN:VEVENT\nDTSTAMP".$vevent["DTSTAMP"]."\nDTSTART".$vevent["DTSTART"]."\nX-TITLE:"
    $icalevent = "BEGIN:VEVENT\r\nDTSTAMP".$CustomDATETIMESTAMP."\r\nDTSTART".$CustomDATE."\r\nX-TITLE:".$vinfo."\r\nSUMMARY:".$vinfo."\r\nDESCRIPTION: ".$vinfo." ".$vurl." ".$vplace." ".$vevents["date"]." ".$vevents["time"]."\r\nEND:VEVENT\r\n"; 
//  $icalevent = "BEGIN:VEVENT\r\nDTSTAMP".$CustomDATETIMESTAMP."\r\nDTSTART".$CustomDATE."\r\nX-TITLE:".$vevents["info"]."\r\nSUMMARY:".$vevents["info"]."\r\nDESCRIPTION: ".$vevents["info"].$vevents["place"]." ".$vevents["date"]." ".$vevents["time"]."\r\nEND:VEVENT\r\n"; #orig
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
$limit = 100; 
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

//scraperwiki::httpresponseheader("Content-Type", 'text/calendar', 'charset=utf-8');
scraperwiki::httpresponseheader("Content-Type", 'text/calendar', 'charset=utf-8');
scraperwiki::httpresponseheader("Content-Disposition", "inline; filename=pres.ics");

scraperwiki::attach('irish_president_engagementstest'); 
# select * from swdata where birth_date < '2000-01-01' just most recentdate('now');
#$vevents = scraperwiki::select("* from irish_president_engagements.swdata limit $limit offset $offset");
$vevents = scraperwiki::select("* from irish_president_engagementstest.swdata where date > date('now','-7 day');");
  
$icalevents = array(); 
foreach ($vevents as $vevents)
{

//date info place time
//= ":".date("Ymd")."T".date("His")."Z";
$vdate = $vevents["date"];
$vtime = $vevents["time"];
$vtime = str_replace(":", "",$vtime);
$CustomDATE = ":".date("Ymd",strtotime($vdate))."T".$vtime."00Z";
$vinfo = $vevents["info"];
$vinfo = preg_replace( '`&([a-z]+)(acute|uml|circ|grave|ring|cedil|slash|tilde|caron|lig);`i',"\\1", $vinfo);

$vplace = $vevents["place"];
$vplace = preg_replace( '`&([a-z]+)(acute|uml|circ|grave|ring|cedil|slash|tilde|caron|lig);`i',"\\1", $vplace);

$vinfo = str_replace(',', '\,', $vinfo);
$vplace = str_replace(',', '\,', $vplace);

$vurl = $vevents["url"];
$vurl = utf8_encode($vurl);
addslashes($vinfo);
addslashes($vplace);
//addcslashes("hello\tworld\n", "\x00..\x1fz..\xff");

//$datetime = $date("Ymd")."T".$time("His")."Z";
$CustomDATETIMESTAMP = ":".date("Ymd")."T".date("His")."Z";
// "BEGIN:VEVENT\nDTSTAMP".$vevent["DTSTAMP"]."\nDTSTART".$vevent["DTSTART"]."\nX-TITLE:"
    $icalevent = "BEGIN:VEVENT\r\nDTSTAMP".$CustomDATETIMESTAMP."\r\nDTSTART".$CustomDATE."\r\nX-TITLE:".$vinfo."\r\nSUMMARY:".$vinfo."\r\nDESCRIPTION: ".$vinfo." ".$vurl." ".$vplace." ".$vevents["date"]." ".$vevents["time"]."\r\nEND:VEVENT\r\n"; 
//  $icalevent = "BEGIN:VEVENT\r\nDTSTAMP".$CustomDATETIMESTAMP."\r\nDTSTART".$CustomDATE."\r\nX-TITLE:".$vevents["info"]."\r\nSUMMARY:".$vevents["info"]."\r\nDESCRIPTION: ".$vevents["info"].$vevents["place"]." ".$vevents["date"]." ".$vevents["time"]."\r\nEND:VEVENT\r\n"; #orig
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
$limit = 100; 
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

//scraperwiki::httpresponseheader("Content-Type", 'text/calendar', 'charset=utf-8');
scraperwiki::httpresponseheader("Content-Type", 'text/calendar', 'charset=utf-8');
scraperwiki::httpresponseheader("Content-Disposition", "inline; filename=pres.ics");

scraperwiki::attach('irish_president_engagementstest'); 
# select * from swdata where birth_date < '2000-01-01' just most recentdate('now');
#$vevents = scraperwiki::select("* from irish_president_engagements.swdata limit $limit offset $offset");
$vevents = scraperwiki::select("* from irish_president_engagementstest.swdata where date > date('now','-7 day');");
  
$icalevents = array(); 
foreach ($vevents as $vevents)
{

//date info place time
//= ":".date("Ymd")."T".date("His")."Z";
$vdate = $vevents["date"];
$vtime = $vevents["time"];
$vtime = str_replace(":", "",$vtime);
$CustomDATE = ":".date("Ymd",strtotime($vdate))."T".$vtime."00Z";
$vinfo = $vevents["info"];
$vinfo = preg_replace( '`&([a-z]+)(acute|uml|circ|grave|ring|cedil|slash|tilde|caron|lig);`i',"\\1", $vinfo);

$vplace = $vevents["place"];
$vplace = preg_replace( '`&([a-z]+)(acute|uml|circ|grave|ring|cedil|slash|tilde|caron|lig);`i',"\\1", $vplace);

$vinfo = str_replace(',', '\,', $vinfo);
$vplace = str_replace(',', '\,', $vplace);

$vurl = $vevents["url"];
$vurl = utf8_encode($vurl);
addslashes($vinfo);
addslashes($vplace);
//addcslashes("hello\tworld\n", "\x00..\x1fz..\xff");

//$datetime = $date("Ymd")."T".$time("His")."Z";
$CustomDATETIMESTAMP = ":".date("Ymd")."T".date("His")."Z";
// "BEGIN:VEVENT\nDTSTAMP".$vevent["DTSTAMP"]."\nDTSTART".$vevent["DTSTART"]."\nX-TITLE:"
    $icalevent = "BEGIN:VEVENT\r\nDTSTAMP".$CustomDATETIMESTAMP."\r\nDTSTART".$CustomDATE."\r\nX-TITLE:".$vinfo."\r\nSUMMARY:".$vinfo."\r\nDESCRIPTION: ".$vinfo." ".$vurl." ".$vplace." ".$vevents["date"]." ".$vevents["time"]."\r\nEND:VEVENT\r\n"; 
//  $icalevent = "BEGIN:VEVENT\r\nDTSTAMP".$CustomDATETIMESTAMP."\r\nDTSTART".$CustomDATE."\r\nX-TITLE:".$vevents["info"]."\r\nSUMMARY:".$vevents["info"]."\r\nDESCRIPTION: ".$vevents["info"].$vevents["place"]." ".$vevents["date"]." ".$vevents["time"]."\r\nEND:VEVENT\r\n"; #orig
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
