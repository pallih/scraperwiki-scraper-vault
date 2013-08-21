<?php

    $sourcescraper = 'ossie_indoor_beach_volleyball_2';
    scraperwiki::httpresponseheader('Content-Type', 'text/rss+xml');
    scraperwiki::attach($sourcescraper);
    
    $date = scraperwiki::get_var("date");
    $timeWAVD = scraperwiki::get_var("timeWAVD");
    $timeDIGGY = scraperwiki::get_var("timeDIGGY");

    print
    (
    '<?xml version="1.0" encoding="UTF-8" ?>
    <rss version="2.0">
    <channel>
        <title>Ossie Indoor Beach Volleyball Game Times</title>
        <description>Feed of game times</description>
        <link>http://www.ossieindoor.com.au/tuesday</link>
        <item>
            <title>'.$date.' - WAVD</title>
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

?>