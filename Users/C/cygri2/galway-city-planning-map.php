<html dir="ltr" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>Galway City Planning Map</title>
    <style type="text/css" media="screen">
        body { color: #330; }
        h1 { font-family: Georgia; font-size: 160%; font-weight: normal; margin: 0; padding: 0; }
        #header { position: absolute; top: 1em; left: 1em; right: 1em; height: 5.8em; }
        #header p { margin: 0.7em 0; }
        #map { position: absolute; top: 5.8em; left: 1em; right: 1em; bottom: 1em; }
        h1 small { color: #885; font-size: 50%; }
    </style>
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
    var mapOptions = { "zoom": 12,
                       "center": new google.maps.LatLng(53.27465, -9.05170),
                       "mapTypeId": google.maps.MapTypeId.ROADMAP
                     };
    map = new google.maps.Map(document.getElementById("map"), mapOptions);
}
 
function recorddata(record)
{
    if (!(record['latlng_lat']))
        return; 
    pos = new google.maps.LatLng(record['latlng_lat'], record['latlng_lng']); 

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
    url = "http://api.scraperwiki.com/api/1.0/datastore/getdata?&format=json&name=galway-city-planning-apps&limit="+olength+"&callback=gotback&offset=" + offset;
    s.setAttribute('src', url);
    s.setAttribute('type', 'text/javascript');
    document.getElementsByTagName('head')[0].appendChild(s);
}

$(function() { makemap(); loaddata(); });

    </script>
</head>

<body>
    <div id="header">
        <h1>Planning applications to Galway City Council <small id="message">...</small></h1>
        <p>Based on planning data from
            <a href="http://www.galwaycity.ie/AllServices/Planning/">Galway City Council</a>,
            extracted and visualised with
            <a href="http://scraperwiki.com/scrapers/galway-city-planning-apps/">ScraperWiki</a>.</p>
    </div>
    <div id="map"></div>
</body>
</html><html dir="ltr" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>Galway City Planning Map</title>
    <style type="text/css" media="screen">
        body { color: #330; }
        h1 { font-family: Georgia; font-size: 160%; font-weight: normal; margin: 0; padding: 0; }
        #header { position: absolute; top: 1em; left: 1em; right: 1em; height: 5.8em; }
        #header p { margin: 0.7em 0; }
        #map { position: absolute; top: 5.8em; left: 1em; right: 1em; bottom: 1em; }
        h1 small { color: #885; font-size: 50%; }
    </style>
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
    var mapOptions = { "zoom": 12,
                       "center": new google.maps.LatLng(53.27465, -9.05170),
                       "mapTypeId": google.maps.MapTypeId.ROADMAP
                     };
    map = new google.maps.Map(document.getElementById("map"), mapOptions);
}
 
function recorddata(record)
{
    if (!(record['latlng_lat']))
        return; 
    pos = new google.maps.LatLng(record['latlng_lat'], record['latlng_lng']); 

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
    url = "http://api.scraperwiki.com/api/1.0/datastore/getdata?&format=json&name=galway-city-planning-apps&limit="+olength+"&callback=gotback&offset=" + offset;
    s.setAttribute('src', url);
    s.setAttribute('type', 'text/javascript');
    document.getElementsByTagName('head')[0].appendChild(s);
}

$(function() { makemap(); loaddata(); });

    </script>
</head>

<body>
    <div id="header">
        <h1>Planning applications to Galway City Council <small id="message">...</small></h1>
        <p>Based on planning data from
            <a href="http://www.galwaycity.ie/AllServices/Planning/">Galway City Council</a>,
            extracted and visualised with
            <a href="http://scraperwiki.com/scrapers/galway-city-planning-apps/">ScraperWiki</a>.</p>
    </div>
    <div id="map"></div>
</body>
</html>