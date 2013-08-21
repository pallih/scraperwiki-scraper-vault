<?php
ini_set('display_errors', 0);
# Blank PHP
//$sourcescraper = '';

scraperwiki::httpresponseheader("Content-Type", 'text/calendar');//; charset=utf-8');
scraperwiki::httpresponseheader("Content-Disposition", "inline; filename=sqq.ics");

echo <<<EOS
BEGIN:VCALENDAR
CALSCALE:GREGORIAN
METHOD:PUBLISH
PRODID:-//Google Inc//Google Calendar 70.9054//EN
VERSION:2.0
X-ORIGINAL-URL:http://scraperwikiviews.com/run/torontoca_events_calendar_ical/
X-WR-CALNAME:Toronto Events Calendar
X-WR-TIMEZONE:America/Toronto
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//hacksw/handcal//NONSGML v1.0//EN
BEGIN:VEVENT
DTSTART:20110923T170000Z
DTEND:20110923T175959Z
SUMMARY:Bastille Day Party
END:VEVENT
END:VCALENDAR
EOS;
