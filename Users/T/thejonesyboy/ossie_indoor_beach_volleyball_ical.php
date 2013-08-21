<?php

    $sourcescraper = 'ossie_indoor_beach_volleyball_2';
    scraperwiki::httpresponseheader('Content-Type', 'text/calendar');
    scraperwiki::attach($sourcescraper);

    $date = scraperwiki::get_var("date");
    $timeWAVD = scraperwiki::get_var("timeWAVD");
    $timeDIGGY = scraperwiki::get_var("timeDIGGY");

    
    print
    (
"BEGIN:VCALENDAR
PRODID:-//Google Inc//Google Calendar 70.9054//EN
VERSION:2.0
CALSCALE:GREGORIAN
METHOD:PUBLISH
X-WR-CALNAME:TEST
X-WR-TIMEZONE:Australia/Perth
X-WR-CALDESC:
BEGIN:VEVENT
DTSTART:20121005T100000Z
DTEND:20121005T110000Z
DTSTAMP:20121004T023432Z
UID:fqdkig4qvg7mnh8kkome3i979o@google.com
CREATED:20121004T023324Z
DESCRIPTION:
LAST-MODIFIED:20121004T023400Z
LOCATION:
SEQUENCE:1
STATUS:CONFIRMED
SUMMARY:TEST ITEM
TRANSP:TRANSPARENT
END:VEVENT
END:VCALENDAR"
    );

/*


    print '<?xml version="1.0" encoding="UTF-8" ?>';
    print '<rss version="2.0">';
    print '<channel>';
    print '    <title>Ossie Indoor Beach Volleyball Game Times</title>';
    print '    <description>Feed of game times</description>';
    print '    <link>http://www.ossieindoor.com.au/tuesday</link>';
    print
    (
    '    <item>
            <title>'.$date.' - WAVDS</title>
            <description>'.$timeWAVD.'</description>
            <link>http://www.ossieindoor.com.au/tuesday</link>
            <guid>'.md5($date.$timeWAVD).'</guid>
        </item>
        <item>
            <title>'.$date.' - GETTIN DIGGY</title>
            <description>'.$timeDIGGY.'</description>
            <link>http://www.ossieindoor.com.au/tuesday</link>
            <guid>'.md5($date.$timeDIGGY).'</guid>
        </item>
    </channel>
    </rss>'
    );
*/

?>