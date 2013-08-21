<html dir="ltr" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>Galway City Planning Map</title>
    <style type="text/css" media="screen">
        body { color: #330; margin: 1em; font-family: Georgia; }
        h1 { font-size: 170%; font-weight: normal; margin: 0; padding: 0; }
        h2 { font-size: 130%; font-weight: normal; margin: 0; padding: 0; }
        p { margin: 0.7em 0; }
        h1 small { color: #885; font-size: 50%; }
        .minimap { float: right; }​
        #map { height: 600px; }
        #feedicon { float: right; }​
    </style>
    <link rel="alternate" type="application/atom+xml" href="http://lab.linkeddata.deri.ie/2010/planning-apps/feed" />
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
    <script type="text/javascript" charset="utf-8">
// ####################################################################
// Set the dynamic icon for your point.  For more see:
// http://code.google.com/apis/chart/docs/gallery/dynamic_icons.html
// ####################################################################
function mapicon(record)
{
    col = 'F00';
    if (record["Decision"] == "PENDING")
        col = '0F0';
    letter = '';
    if (record["Decision"] == "PENDING")
        letter = 'P';
     
    icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+letter+'|'+col+'|000';
    return icon
}

// ####################################################################
// Set the tooltip title value
// ####################################################################
function mapicontext(record)
{
    return "TOOLTIP " + record["appref"]
}

// ####################################################################
// Set the popup text for your pin, usually with the link
// ####################################################################
function mapicontent(record)
{
    return '<a href="'+record['url']+'" target="_blank">'+record["appref"]+'</a><br />Filed: '+record["date"]+'<br />'+record["address"];
}

var map;
var centreset = false;
function makemap()
{
    var mapOptions = { "zoom": 13,
                       "center": new google.maps.LatLng(53.27465, -9.05170),
                       "mapTypeId": google.maps.MapTypeId.HYBRID
                     };
    map = new google.maps.Map(document.getElementById("map"), mapOptions);
}

function recorddata(record)
{
    if (!('latlng' in record))
        return;
    pos = new google.maps.LatLng(record['latlng'][0], record['latlng'][1]);

    text = mapicontext(record);
    icon = mapicon(record);
    content = mapicontent(record);

    marker = new google.maps.Marker({position:pos,map:map,title:text, icon:icon});

    infowindow = new google.maps.InfoWindow({ content: content });
    (function(j) {
            google.maps.event.addListener(j.marker, "click", function(){
                                j.infowindow.open(map, j.marker); });
                 })({'marker':marker, 'infowindow':infowindow});
}

var olength = 500;
var olimit = 100;
var offset = 0; 1    
function gotback(r)
{
    for (i = 0; i < r.length; i++)
        recorddata(r[i]);

    offset += olength;
    if ((r.length == olength) && (offset < olimit))
        loaddata();
    else
        $("#message").html("Total records: " + (offset - olength + r.length));
}

function loaddata()
{
    $("#message").html("Loading ...");
    var s = document.createElement('script');
    url = "http://api.scraperwiki.com/api/1.0/datastore/getdata?&format=json&name=latest-galway-city-planning-applications&limit="+olength+"&callback=gotback&offset=" + offset;
    s.setAttribute('src', url);
    s.setAttribute('type', 'text/javascript');
    document.getElementsByTagName('head')[0].appendChild(s);
}

$(function() { makemap(); loaddata(); });

    </script>
</head>

<body>
    <div id="feedicon"><a href="http://lab.linkeddata.deri.ie/2010/planning-apps/feed"><img src="http://lab.linkeddata.deri.ie/2010/planning-apps/feed-icon-28x28.png" alt="RSS feed" title="Subscribe to RSS feed" /></a></div>
    <h1>Recent planning applications to Galway City Council <small id="message">...</small></h1>
        <p>Based on planning data from
            <a href="http://www.galwaycity.ie/AllServices/Planning/">Galway City Council</a>,
            extracted and visualised with
            <a href="http://scraperwiki.com/scrapers/latest-galway-city-planning-applications/">ScraperWiki</a>.</p>
    </div>
    <div id="map"></div>
<?php

$sourcescraper = 'latest-galway-city-planning-applications';
$applications = scraperwiki::getData($sourcescraper);

function e($s) {
  echo htmlspecialchars($s);
}

foreach ($applications as $app) { ?>
    <h2><a href="<?php e($app->url); ?>">#<?php e($app->appref); ?>: <?php e($app->address); ?></a></h2>
<?php if (isset($app->latlng)) { ?>
    <div class="minimap"><img src="<?php e('http://maps.google.com/maps/api/staticmap?size=200x200&zoom=16&markers=size:mid|color:blue|' . $app->latlng[0] . ',' . $app->latlng[1]. '&sensor=false'); ?>" /></div>
<?php } ?>
    <p>
        <strong>Applicant:</strong> <?php e($app->applicant); ?><br />
        <strong>Date received:</strong> <?php e($app->date); ?><br />
        <strong>File number:</strong> <?php e($app->appref); ?>​
    </p>​
    <p><?php e($app->details); ?></p>
<?php } ?>​
</body>
</html>