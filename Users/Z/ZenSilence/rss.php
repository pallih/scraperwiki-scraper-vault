<?php
    scraperwiki::httpresponseheader('Content-Type', 'text/rss+xml');
    $sourcescraper = 'canadian_crown_assets_-_whats_for_sale_-_computer_'; 
    $keys = scraperwiki::getKeys($sourcescraper); 

    $s = scraperwiki::getData($sourcescraper, $limit=250); 

    print ('<?xml version="1.0" encoding="UTF-8" ?>
            <rss version="2.0">
            <channel>
                <title>Crown Assets - Computer Equipment, Parts and Accessories</title>
                <description>Feed of New Posts</description>
                <link>http://crownassets.pwgsc.gc.ca/mn-eng.cfm?&snc=wfsav&sc=ach-shop&str=1&rpp=25&sr=1&sf=aff-post&so=DESC&vndsld=0&lci=&srchtype=&hpcs=7000&hpsr=</link>
           ');


    foreach ($s as $c => $row) {
        foreach ($row as $k => $value) {
            print ('<item>
                    <title>'.$k = $value.'</title>
                <description>Here is some text containing an interesting description.</description>
                <link>http://www.wikipedia.org/</link>
                <guid>unique string per item</guid>
                <pubDate>Mon, 06 Sep 2009 16:45:00 +0000 </pubDate>');

        }
        echo "</item>";
    }
    
    print ('</channel>
            </rss>');
?>
  
    

<?php
    scraperwiki::httpresponseheader('Content-Type', 'text/rss+xml');
    $sourcescraper = 'canadian_crown_assets_-_whats_for_sale_-_computer_'; 
    $keys = scraperwiki::getKeys($sourcescraper); 

    $s = scraperwiki::getData($sourcescraper, $limit=250); 

    print ('<?xml version="1.0" encoding="UTF-8" ?>
            <rss version="2.0">
            <channel>
                <title>Crown Assets - Computer Equipment, Parts and Accessories</title>
                <description>Feed of New Posts</description>
                <link>http://crownassets.pwgsc.gc.ca/mn-eng.cfm?&snc=wfsav&sc=ach-shop&str=1&rpp=25&sr=1&sf=aff-post&so=DESC&vndsld=0&lci=&srchtype=&hpcs=7000&hpsr=</link>
           ');


    foreach ($s as $c => $row) {
        foreach ($row as $k => $value) {
            print ('<item>
                    <title>'.$k = $value.'</title>
                <description>Here is some text containing an interesting description.</description>
                <link>http://www.wikipedia.org/</link>
                <guid>unique string per item</guid>
                <pubDate>Mon, 06 Sep 2009 16:45:00 +0000 </pubDate>');

        }
        echo "</item>";
    }
    
    print ('</channel>
            </rss>');
?>
  
    

