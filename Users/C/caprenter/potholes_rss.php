<?php
//Set correct mime-type for RSS
scraperwiki::httpresponseheader('Content-Type', 'application/rss+xml');
//Set correct timezone for date functions later on
date_default_timezone_set("Europe/London");
//Attach and grab the data we want to use
scraperwiki::attach("fill_that_hole_1");   
$data = scraperwiki::select("* from fill_that_hole_1.swdata order by dateadded desc limit 10" );
//print_r($data); 

//Create the RSS xml output
print('<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
    <channel>
        <atom:link href="http://scraperwikiviews.com/run/potholes_rss/" rel="self" type="application/rss+xml" />
        <title>Potholes reported on Fill That Hole - Bradford</title>
        <link>http://www.fillthathole.org.uk/node/51/hazards</link>
        <description>RSS feed of latest pothole reports via Fill That Hole in Bradford</description>
        <language>en-gb</language>');
foreach ($data as $item){
    print ('
            <item>
                <title>' . $item["road"] . '</title>
                <description>' . $item["description"] .'</description>
                <link>http://www.fillthathole.org.uk/hazard/' . $item["id"] . '</link>
                <pubDate>' . date("D, d M Y",strtotime($item["dateadded"])) .' 00:00:00 GMT</pubDate>
            </item>
            ');
    }

print ('</channel>
     </rss>
<!-- ScraperWiki insists on inserting this block, but its not valid XML, so we put it into a comment
Thanks http://scraperwiki.com/views/galway-city-planning-feed
<div id="scraperwikipane"/>
-->');
?>
<?php
//Set correct mime-type for RSS
scraperwiki::httpresponseheader('Content-Type', 'application/rss+xml');
//Set correct timezone for date functions later on
date_default_timezone_set("Europe/London");
//Attach and grab the data we want to use
scraperwiki::attach("fill_that_hole_1");   
$data = scraperwiki::select("* from fill_that_hole_1.swdata order by dateadded desc limit 10" );
//print_r($data); 

//Create the RSS xml output
print('<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
    <channel>
        <atom:link href="http://scraperwikiviews.com/run/potholes_rss/" rel="self" type="application/rss+xml" />
        <title>Potholes reported on Fill That Hole - Bradford</title>
        <link>http://www.fillthathole.org.uk/node/51/hazards</link>
        <description>RSS feed of latest pothole reports via Fill That Hole in Bradford</description>
        <language>en-gb</language>');
foreach ($data as $item){
    print ('
            <item>
                <title>' . $item["road"] . '</title>
                <description>' . $item["description"] .'</description>
                <link>http://www.fillthathole.org.uk/hazard/' . $item["id"] . '</link>
                <pubDate>' . date("D, d M Y",strtotime($item["dateadded"])) .' 00:00:00 GMT</pubDate>
            </item>
            ');
    }

print ('</channel>
     </rss>
<!-- ScraperWiki insists on inserting this block, but its not valid XML, so we put it into a comment
Thanks http://scraperwiki.com/views/galway-city-planning-feed
<div id="scraperwikipane"/>
-->');
?>
