<html dir="ltr" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>General Map Thing</title>
    <style type="text/css" media="screen">p{padding:1px;}</style>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <script type="text/javascript" src="http://google-maps-utility-library-v3.googlecode.com/svn/tags/markerclusterer/1.0/src/markerclusterer.js"></script>
</head>

<body>

<h2>General Map Thing of <span id="scrapername">...</span> <em id="message">...</em></h2>
<div id="map" style="width:100%;height:400px"></div>

<script type="text/javascript" charset="utf-8">
//################################    
// Very quick implementation from the following example.  Needs improvement (with all the settings)
// and moving into the general template example
//    http://google-maps-utility-library-v3.googlecode.com/svn/tags/markerclusterer/1.0/examples/advanced_example.html
//################################        
    
// ####################################################################
// Start of javascript code.  You should edit the functions below
// so that your map expresses the particular contents of the data
// ####################################################################
    
var sourcescraper = 'national-river-flow-archive-stations';
$('#scrapername').html('<b>'+sourcescraper+'</b>');
    
// ####################################################################
// Set the dynamic icon for your point.  For more see:
// http://code.google.com/apis/chart/docs/gallery/dynamic_icons.html
// ####################################################################
function mapicon(record)
{
    col = '0F0';
    if (record["discontinued"] == "*")
        col = 'F00';
    letter = 'O';
    icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+letter+'|'+col+'|000';
    proportion = 60;     
    icon = "http://chart.apis.google.com/chart?cht=bvo&chco=0028AB,C6D9FD,4D89F9&chd=t:50|"+proportion+"|100&3E&chm=H,FF0000,0,0,1&chs=50";
    return icon
}

// ####################################################################
// Set the tooltip title value
// ####################################################################
function mapicontext(record)
{
    return record["River"] + ' at ' + record["Location"];
}

// ####################################################################
// Set the popup text for your pin, usually with the link
// ####################################################################
function mapicontent(record)
{
    return '<a href="'+record['url']+'" target="_blank">'+record["River"] + ' at ' + record["Location"]+'</a>';
}

var map;
var centreset = false;
function makemap()
{
    var mapOptions = { "zoom": 4, "center": new google.maps.LatLng(55.500515, -4.128317),
                    "mapTypeId": google.maps.MapTypeId.SATELLITE };
    map = new google.maps.Map(document.getElementById("map"), mapOptions);
}
 
var markers = [];
function recorddata(record)
{
    if (!('latlng' in record))
        return;
    pos = new google.maps.LatLng(record['latlng'][0], record['latlng'][1]);

    text = mapicontext(record);
    icon = mapicon(record);
    content = mapicontent(record);

    marker = new google.maps.Marker({position:pos, title:text, icon:icon});

    infowindow = new google.maps.InfoWindow({ content: content });
    (function(j) {
            google.maps.event.addListener(j.marker, "click", function(){
                                j.infowindow.open(map, j.marker); });
                 })({'marker':marker, 'infowindow':infowindow});
    markers.push(marker);     
}

function refreshMap()
{
    markerClusterer = new MarkerClusterer(map, markers, {gridSize:10});
}

            
var olength = 50;
var olimit = 1000;
var offset = 0; 1    
function gotback(r)
{
    for (i = 0; i < r.length; i++)
        recorddata(r[i]);
    refreshMap();
           
    offset += olength;
    if ((r.length == olength) && (offset < olimit))
        loaddata();
    else
        $("#message").html("Total records=" + (offset - olength + r.length));
}

function loaddata()
{
    $("#message").html("Loading ...");
    var s = document.createElement('script');
    url = "http://api.scraperwiki.com/api/1.0/datastore/getdata?&format=json&name="+sourcescraper+"&limit="+olength+"&callback=gotback&offset=" + offset;
    s.setAttribute('src', url);
    s.setAttribute('type', 'text/javascript');
    document.getElementsByTagName('head')[0].appendChild(s);
}

$(function() { makemap(); loaddata(); });

</script>
</body>
</html><html dir="ltr" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>General Map Thing</title>
    <style type="text/css" media="screen">p{padding:1px;}</style>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <script type="text/javascript" src="http://google-maps-utility-library-v3.googlecode.com/svn/tags/markerclusterer/1.0/src/markerclusterer.js"></script>
</head>

<body>

<h2>General Map Thing of <span id="scrapername">...</span> <em id="message">...</em></h2>
<div id="map" style="width:100%;height:400px"></div>

<script type="text/javascript" charset="utf-8">
//################################    
// Very quick implementation from the following example.  Needs improvement (with all the settings)
// and moving into the general template example
//    http://google-maps-utility-library-v3.googlecode.com/svn/tags/markerclusterer/1.0/examples/advanced_example.html
//################################        
    
// ####################################################################
// Start of javascript code.  You should edit the functions below
// so that your map expresses the particular contents of the data
// ####################################################################
    
var sourcescraper = 'national-river-flow-archive-stations';
$('#scrapername').html('<b>'+sourcescraper+'</b>');
    
// ####################################################################
// Set the dynamic icon for your point.  For more see:
// http://code.google.com/apis/chart/docs/gallery/dynamic_icons.html
// ####################################################################
function mapicon(record)
{
    col = '0F0';
    if (record["discontinued"] == "*")
        col = 'F00';
    letter = 'O';
    icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+letter+'|'+col+'|000';
    proportion = 60;     
    icon = "http://chart.apis.google.com/chart?cht=bvo&chco=0028AB,C6D9FD,4D89F9&chd=t:50|"+proportion+"|100&3E&chm=H,FF0000,0,0,1&chs=50";
    return icon
}

// ####################################################################
// Set the tooltip title value
// ####################################################################
function mapicontext(record)
{
    return record["River"] + ' at ' + record["Location"];
}

// ####################################################################
// Set the popup text for your pin, usually with the link
// ####################################################################
function mapicontent(record)
{
    return '<a href="'+record['url']+'" target="_blank">'+record["River"] + ' at ' + record["Location"]+'</a>';
}

var map;
var centreset = false;
function makemap()
{
    var mapOptions = { "zoom": 4, "center": new google.maps.LatLng(55.500515, -4.128317),
                    "mapTypeId": google.maps.MapTypeId.SATELLITE };
    map = new google.maps.Map(document.getElementById("map"), mapOptions);
}
 
var markers = [];
function recorddata(record)
{
    if (!('latlng' in record))
        return;
    pos = new google.maps.LatLng(record['latlng'][0], record['latlng'][1]);

    text = mapicontext(record);
    icon = mapicon(record);
    content = mapicontent(record);

    marker = new google.maps.Marker({position:pos, title:text, icon:icon});

    infowindow = new google.maps.InfoWindow({ content: content });
    (function(j) {
            google.maps.event.addListener(j.marker, "click", function(){
                                j.infowindow.open(map, j.marker); });
                 })({'marker':marker, 'infowindow':infowindow});
    markers.push(marker);     
}

function refreshMap()
{
    markerClusterer = new MarkerClusterer(map, markers, {gridSize:10});
}

            
var olength = 50;
var olimit = 1000;
var offset = 0; 1    
function gotback(r)
{
    for (i = 0; i < r.length; i++)
        recorddata(r[i]);
    refreshMap();
           
    offset += olength;
    if ((r.length == olength) && (offset < olimit))
        loaddata();
    else
        $("#message").html("Total records=" + (offset - olength + r.length));
}

function loaddata()
{
    $("#message").html("Loading ...");
    var s = document.createElement('script');
    url = "http://api.scraperwiki.com/api/1.0/datastore/getdata?&format=json&name="+sourcescraper+"&limit="+olength+"&callback=gotback&offset=" + offset;
    s.setAttribute('src', url);
    s.setAttribute('type', 'text/javascript');
    document.getElementsByTagName('head')[0].appendChild(s);
}

$(function() { makemap(); loaddata(); });

</script>
</body>
</html><html dir="ltr" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>General Map Thing</title>
    <style type="text/css" media="screen">p{padding:1px;}</style>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <script type="text/javascript" src="http://google-maps-utility-library-v3.googlecode.com/svn/tags/markerclusterer/1.0/src/markerclusterer.js"></script>
</head>

<body>

<h2>General Map Thing of <span id="scrapername">...</span> <em id="message">...</em></h2>
<div id="map" style="width:100%;height:400px"></div>

<script type="text/javascript" charset="utf-8">
//################################    
// Very quick implementation from the following example.  Needs improvement (with all the settings)
// and moving into the general template example
//    http://google-maps-utility-library-v3.googlecode.com/svn/tags/markerclusterer/1.0/examples/advanced_example.html
//################################        
    
// ####################################################################
// Start of javascript code.  You should edit the functions below
// so that your map expresses the particular contents of the data
// ####################################################################
    
var sourcescraper = 'national-river-flow-archive-stations';
$('#scrapername').html('<b>'+sourcescraper+'</b>');
    
// ####################################################################
// Set the dynamic icon for your point.  For more see:
// http://code.google.com/apis/chart/docs/gallery/dynamic_icons.html
// ####################################################################
function mapicon(record)
{
    col = '0F0';
    if (record["discontinued"] == "*")
        col = 'F00';
    letter = 'O';
    icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+letter+'|'+col+'|000';
    proportion = 60;     
    icon = "http://chart.apis.google.com/chart?cht=bvo&chco=0028AB,C6D9FD,4D89F9&chd=t:50|"+proportion+"|100&3E&chm=H,FF0000,0,0,1&chs=50";
    return icon
}

// ####################################################################
// Set the tooltip title value
// ####################################################################
function mapicontext(record)
{
    return record["River"] + ' at ' + record["Location"];
}

// ####################################################################
// Set the popup text for your pin, usually with the link
// ####################################################################
function mapicontent(record)
{
    return '<a href="'+record['url']+'" target="_blank">'+record["River"] + ' at ' + record["Location"]+'</a>';
}

var map;
var centreset = false;
function makemap()
{
    var mapOptions = { "zoom": 4, "center": new google.maps.LatLng(55.500515, -4.128317),
                    "mapTypeId": google.maps.MapTypeId.SATELLITE };
    map = new google.maps.Map(document.getElementById("map"), mapOptions);
}
 
var markers = [];
function recorddata(record)
{
    if (!('latlng' in record))
        return;
    pos = new google.maps.LatLng(record['latlng'][0], record['latlng'][1]);

    text = mapicontext(record);
    icon = mapicon(record);
    content = mapicontent(record);

    marker = new google.maps.Marker({position:pos, title:text, icon:icon});

    infowindow = new google.maps.InfoWindow({ content: content });
    (function(j) {
            google.maps.event.addListener(j.marker, "click", function(){
                                j.infowindow.open(map, j.marker); });
                 })({'marker':marker, 'infowindow':infowindow});
    markers.push(marker);     
}

function refreshMap()
{
    markerClusterer = new MarkerClusterer(map, markers, {gridSize:10});
}

            
var olength = 50;
var olimit = 1000;
var offset = 0; 1    
function gotback(r)
{
    for (i = 0; i < r.length; i++)
        recorddata(r[i]);
    refreshMap();
           
    offset += olength;
    if ((r.length == olength) && (offset < olimit))
        loaddata();
    else
        $("#message").html("Total records=" + (offset - olength + r.length));
}

function loaddata()
{
    $("#message").html("Loading ...");
    var s = document.createElement('script');
    url = "http://api.scraperwiki.com/api/1.0/datastore/getdata?&format=json&name="+sourcescraper+"&limit="+olength+"&callback=gotback&offset=" + offset;
    s.setAttribute('src', url);
    s.setAttribute('type', 'text/javascript');
    document.getElementsByTagName('head')[0].appendChild(s);
}

$(function() { makemap(); loaddata(); });

</script>
</body>
</html><html dir="ltr" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>General Map Thing</title>
    <style type="text/css" media="screen">p{padding:1px;}</style>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <script type="text/javascript" src="http://google-maps-utility-library-v3.googlecode.com/svn/tags/markerclusterer/1.0/src/markerclusterer.js"></script>
</head>

<body>

<h2>General Map Thing of <span id="scrapername">...</span> <em id="message">...</em></h2>
<div id="map" style="width:100%;height:400px"></div>

<script type="text/javascript" charset="utf-8">
//################################    
// Very quick implementation from the following example.  Needs improvement (with all the settings)
// and moving into the general template example
//    http://google-maps-utility-library-v3.googlecode.com/svn/tags/markerclusterer/1.0/examples/advanced_example.html
//################################        
    
// ####################################################################
// Start of javascript code.  You should edit the functions below
// so that your map expresses the particular contents of the data
// ####################################################################
    
var sourcescraper = 'national-river-flow-archive-stations';
$('#scrapername').html('<b>'+sourcescraper+'</b>');
    
// ####################################################################
// Set the dynamic icon for your point.  For more see:
// http://code.google.com/apis/chart/docs/gallery/dynamic_icons.html
// ####################################################################
function mapicon(record)
{
    col = '0F0';
    if (record["discontinued"] == "*")
        col = 'F00';
    letter = 'O';
    icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+letter+'|'+col+'|000';
    proportion = 60;     
    icon = "http://chart.apis.google.com/chart?cht=bvo&chco=0028AB,C6D9FD,4D89F9&chd=t:50|"+proportion+"|100&3E&chm=H,FF0000,0,0,1&chs=50";
    return icon
}

// ####################################################################
// Set the tooltip title value
// ####################################################################
function mapicontext(record)
{
    return record["River"] + ' at ' + record["Location"];
}

// ####################################################################
// Set the popup text for your pin, usually with the link
// ####################################################################
function mapicontent(record)
{
    return '<a href="'+record['url']+'" target="_blank">'+record["River"] + ' at ' + record["Location"]+'</a>';
}

var map;
var centreset = false;
function makemap()
{
    var mapOptions = { "zoom": 4, "center": new google.maps.LatLng(55.500515, -4.128317),
                    "mapTypeId": google.maps.MapTypeId.SATELLITE };
    map = new google.maps.Map(document.getElementById("map"), mapOptions);
}
 
var markers = [];
function recorddata(record)
{
    if (!('latlng' in record))
        return;
    pos = new google.maps.LatLng(record['latlng'][0], record['latlng'][1]);

    text = mapicontext(record);
    icon = mapicon(record);
    content = mapicontent(record);

    marker = new google.maps.Marker({position:pos, title:text, icon:icon});

    infowindow = new google.maps.InfoWindow({ content: content });
    (function(j) {
            google.maps.event.addListener(j.marker, "click", function(){
                                j.infowindow.open(map, j.marker); });
                 })({'marker':marker, 'infowindow':infowindow});
    markers.push(marker);     
}

function refreshMap()
{
    markerClusterer = new MarkerClusterer(map, markers, {gridSize:10});
}

            
var olength = 50;
var olimit = 1000;
var offset = 0; 1    
function gotback(r)
{
    for (i = 0; i < r.length; i++)
        recorddata(r[i]);
    refreshMap();
           
    offset += olength;
    if ((r.length == olength) && (offset < olimit))
        loaddata();
    else
        $("#message").html("Total records=" + (offset - olength + r.length));
}

function loaddata()
{
    $("#message").html("Loading ...");
    var s = document.createElement('script');
    url = "http://api.scraperwiki.com/api/1.0/datastore/getdata?&format=json&name="+sourcescraper+"&limit="+olength+"&callback=gotback&offset=" + offset;
    s.setAttribute('src', url);
    s.setAttribute('type', 'text/javascript');
    document.getElementsByTagName('head')[0].appendChild(s);
}

$(function() { makemap(); loaddata(); });

</script>
</body>
</html><html dir="ltr" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>General Map Thing</title>
    <style type="text/css" media="screen">p{padding:1px;}</style>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <script type="text/javascript" src="http://google-maps-utility-library-v3.googlecode.com/svn/tags/markerclusterer/1.0/src/markerclusterer.js"></script>
</head>

<body>

<h2>General Map Thing of <span id="scrapername">...</span> <em id="message">...</em></h2>
<div id="map" style="width:100%;height:400px"></div>

<script type="text/javascript" charset="utf-8">
//################################    
// Very quick implementation from the following example.  Needs improvement (with all the settings)
// and moving into the general template example
//    http://google-maps-utility-library-v3.googlecode.com/svn/tags/markerclusterer/1.0/examples/advanced_example.html
//################################        
    
// ####################################################################
// Start of javascript code.  You should edit the functions below
// so that your map expresses the particular contents of the data
// ####################################################################
    
var sourcescraper = 'national-river-flow-archive-stations';
$('#scrapername').html('<b>'+sourcescraper+'</b>');
    
// ####################################################################
// Set the dynamic icon for your point.  For more see:
// http://code.google.com/apis/chart/docs/gallery/dynamic_icons.html
// ####################################################################
function mapicon(record)
{
    col = '0F0';
    if (record["discontinued"] == "*")
        col = 'F00';
    letter = 'O';
    icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+letter+'|'+col+'|000';
    proportion = 60;     
    icon = "http://chart.apis.google.com/chart?cht=bvo&chco=0028AB,C6D9FD,4D89F9&chd=t:50|"+proportion+"|100&3E&chm=H,FF0000,0,0,1&chs=50";
    return icon
}

// ####################################################################
// Set the tooltip title value
// ####################################################################
function mapicontext(record)
{
    return record["River"] + ' at ' + record["Location"];
}

// ####################################################################
// Set the popup text for your pin, usually with the link
// ####################################################################
function mapicontent(record)
{
    return '<a href="'+record['url']+'" target="_blank">'+record["River"] + ' at ' + record["Location"]+'</a>';
}

var map;
var centreset = false;
function makemap()
{
    var mapOptions = { "zoom": 4, "center": new google.maps.LatLng(55.500515, -4.128317),
                    "mapTypeId": google.maps.MapTypeId.SATELLITE };
    map = new google.maps.Map(document.getElementById("map"), mapOptions);
}
 
var markers = [];
function recorddata(record)
{
    if (!('latlng' in record))
        return;
    pos = new google.maps.LatLng(record['latlng'][0], record['latlng'][1]);

    text = mapicontext(record);
    icon = mapicon(record);
    content = mapicontent(record);

    marker = new google.maps.Marker({position:pos, title:text, icon:icon});

    infowindow = new google.maps.InfoWindow({ content: content });
    (function(j) {
            google.maps.event.addListener(j.marker, "click", function(){
                                j.infowindow.open(map, j.marker); });
                 })({'marker':marker, 'infowindow':infowindow});
    markers.push(marker);     
}

function refreshMap()
{
    markerClusterer = new MarkerClusterer(map, markers, {gridSize:10});
}

            
var olength = 50;
var olimit = 1000;
var offset = 0; 1    
function gotback(r)
{
    for (i = 0; i < r.length; i++)
        recorddata(r[i]);
    refreshMap();
           
    offset += olength;
    if ((r.length == olength) && (offset < olimit))
        loaddata();
    else
        $("#message").html("Total records=" + (offset - olength + r.length));
}

function loaddata()
{
    $("#message").html("Loading ...");
    var s = document.createElement('script');
    url = "http://api.scraperwiki.com/api/1.0/datastore/getdata?&format=json&name="+sourcescraper+"&limit="+olength+"&callback=gotback&offset=" + offset;
    s.setAttribute('src', url);
    s.setAttribute('type', 'text/javascript');
    document.getElementsByTagName('head')[0].appendChild(s);
}

$(function() { makemap(); loaddata(); });

</script>
</body>
</html><html dir="ltr" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>General Map Thing</title>
    <style type="text/css" media="screen">p{padding:1px;}</style>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <script type="text/javascript" src="http://google-maps-utility-library-v3.googlecode.com/svn/tags/markerclusterer/1.0/src/markerclusterer.js"></script>
</head>

<body>

<h2>General Map Thing of <span id="scrapername">...</span> <em id="message">...</em></h2>
<div id="map" style="width:100%;height:400px"></div>

<script type="text/javascript" charset="utf-8">
//################################    
// Very quick implementation from the following example.  Needs improvement (with all the settings)
// and moving into the general template example
//    http://google-maps-utility-library-v3.googlecode.com/svn/tags/markerclusterer/1.0/examples/advanced_example.html
//################################        
    
// ####################################################################
// Start of javascript code.  You should edit the functions below
// so that your map expresses the particular contents of the data
// ####################################################################
    
var sourcescraper = 'national-river-flow-archive-stations';
$('#scrapername').html('<b>'+sourcescraper+'</b>');
    
// ####################################################################
// Set the dynamic icon for your point.  For more see:
// http://code.google.com/apis/chart/docs/gallery/dynamic_icons.html
// ####################################################################
function mapicon(record)
{
    col = '0F0';
    if (record["discontinued"] == "*")
        col = 'F00';
    letter = 'O';
    icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+letter+'|'+col+'|000';
    proportion = 60;     
    icon = "http://chart.apis.google.com/chart?cht=bvo&chco=0028AB,C6D9FD,4D89F9&chd=t:50|"+proportion+"|100&3E&chm=H,FF0000,0,0,1&chs=50";
    return icon
}

// ####################################################################
// Set the tooltip title value
// ####################################################################
function mapicontext(record)
{
    return record["River"] + ' at ' + record["Location"];
}

// ####################################################################
// Set the popup text for your pin, usually with the link
// ####################################################################
function mapicontent(record)
{
    return '<a href="'+record['url']+'" target="_blank">'+record["River"] + ' at ' + record["Location"]+'</a>';
}

var map;
var centreset = false;
function makemap()
{
    var mapOptions = { "zoom": 4, "center": new google.maps.LatLng(55.500515, -4.128317),
                    "mapTypeId": google.maps.MapTypeId.SATELLITE };
    map = new google.maps.Map(document.getElementById("map"), mapOptions);
}
 
var markers = [];
function recorddata(record)
{
    if (!('latlng' in record))
        return;
    pos = new google.maps.LatLng(record['latlng'][0], record['latlng'][1]);

    text = mapicontext(record);
    icon = mapicon(record);
    content = mapicontent(record);

    marker = new google.maps.Marker({position:pos, title:text, icon:icon});

    infowindow = new google.maps.InfoWindow({ content: content });
    (function(j) {
            google.maps.event.addListener(j.marker, "click", function(){
                                j.infowindow.open(map, j.marker); });
                 })({'marker':marker, 'infowindow':infowindow});
    markers.push(marker);     
}

function refreshMap()
{
    markerClusterer = new MarkerClusterer(map, markers, {gridSize:10});
}

            
var olength = 50;
var olimit = 1000;
var offset = 0; 1    
function gotback(r)
{
    for (i = 0; i < r.length; i++)
        recorddata(r[i]);
    refreshMap();
           
    offset += olength;
    if ((r.length == olength) && (offset < olimit))
        loaddata();
    else
        $("#message").html("Total records=" + (offset - olength + r.length));
}

function loaddata()
{
    $("#message").html("Loading ...");
    var s = document.createElement('script');
    url = "http://api.scraperwiki.com/api/1.0/datastore/getdata?&format=json&name="+sourcescraper+"&limit="+olength+"&callback=gotback&offset=" + offset;
    s.setAttribute('src', url);
    s.setAttribute('type', 'text/javascript');
    document.getElementsByTagName('head')[0].appendChild(s);
}

$(function() { makemap(); loaddata(); });

</script>
</body>
</html><html dir="ltr" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>General Map Thing</title>
    <style type="text/css" media="screen">p{padding:1px;}</style>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <script type="text/javascript" src="http://google-maps-utility-library-v3.googlecode.com/svn/tags/markerclusterer/1.0/src/markerclusterer.js"></script>
</head>

<body>

<h2>General Map Thing of <span id="scrapername">...</span> <em id="message">...</em></h2>
<div id="map" style="width:100%;height:400px"></div>

<script type="text/javascript" charset="utf-8">
//################################    
// Very quick implementation from the following example.  Needs improvement (with all the settings)
// and moving into the general template example
//    http://google-maps-utility-library-v3.googlecode.com/svn/tags/markerclusterer/1.0/examples/advanced_example.html
//################################        
    
// ####################################################################
// Start of javascript code.  You should edit the functions below
// so that your map expresses the particular contents of the data
// ####################################################################
    
var sourcescraper = 'national-river-flow-archive-stations';
$('#scrapername').html('<b>'+sourcescraper+'</b>');
    
// ####################################################################
// Set the dynamic icon for your point.  For more see:
// http://code.google.com/apis/chart/docs/gallery/dynamic_icons.html
// ####################################################################
function mapicon(record)
{
    col = '0F0';
    if (record["discontinued"] == "*")
        col = 'F00';
    letter = 'O';
    icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+letter+'|'+col+'|000';
    proportion = 60;     
    icon = "http://chart.apis.google.com/chart?cht=bvo&chco=0028AB,C6D9FD,4D89F9&chd=t:50|"+proportion+"|100&3E&chm=H,FF0000,0,0,1&chs=50";
    return icon
}

// ####################################################################
// Set the tooltip title value
// ####################################################################
function mapicontext(record)
{
    return record["River"] + ' at ' + record["Location"];
}

// ####################################################################
// Set the popup text for your pin, usually with the link
// ####################################################################
function mapicontent(record)
{
    return '<a href="'+record['url']+'" target="_blank">'+record["River"] + ' at ' + record["Location"]+'</a>';
}

var map;
var centreset = false;
function makemap()
{
    var mapOptions = { "zoom": 4, "center": new google.maps.LatLng(55.500515, -4.128317),
                    "mapTypeId": google.maps.MapTypeId.SATELLITE };
    map = new google.maps.Map(document.getElementById("map"), mapOptions);
}
 
var markers = [];
function recorddata(record)
{
    if (!('latlng' in record))
        return;
    pos = new google.maps.LatLng(record['latlng'][0], record['latlng'][1]);

    text = mapicontext(record);
    icon = mapicon(record);
    content = mapicontent(record);

    marker = new google.maps.Marker({position:pos, title:text, icon:icon});

    infowindow = new google.maps.InfoWindow({ content: content });
    (function(j) {
            google.maps.event.addListener(j.marker, "click", function(){
                                j.infowindow.open(map, j.marker); });
                 })({'marker':marker, 'infowindow':infowindow});
    markers.push(marker);     
}

function refreshMap()
{
    markerClusterer = new MarkerClusterer(map, markers, {gridSize:10});
}

            
var olength = 50;
var olimit = 1000;
var offset = 0; 1    
function gotback(r)
{
    for (i = 0; i < r.length; i++)
        recorddata(r[i]);
    refreshMap();
           
    offset += olength;
    if ((r.length == olength) && (offset < olimit))
        loaddata();
    else
        $("#message").html("Total records=" + (offset - olength + r.length));
}

function loaddata()
{
    $("#message").html("Loading ...");
    var s = document.createElement('script');
    url = "http://api.scraperwiki.com/api/1.0/datastore/getdata?&format=json&name="+sourcescraper+"&limit="+olength+"&callback=gotback&offset=" + offset;
    s.setAttribute('src', url);
    s.setAttribute('type', 'text/javascript');
    document.getElementsByTagName('head')[0].appendChild(s);
}

$(function() { makemap(); loaddata(); });

</script>
</body>
</html><html dir="ltr" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>General Map Thing</title>
    <style type="text/css" media="screen">p{padding:1px;}</style>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <script type="text/javascript" src="http://google-maps-utility-library-v3.googlecode.com/svn/tags/markerclusterer/1.0/src/markerclusterer.js"></script>
</head>

<body>

<h2>General Map Thing of <span id="scrapername">...</span> <em id="message">...</em></h2>
<div id="map" style="width:100%;height:400px"></div>

<script type="text/javascript" charset="utf-8">
//################################    
// Very quick implementation from the following example.  Needs improvement (with all the settings)
// and moving into the general template example
//    http://google-maps-utility-library-v3.googlecode.com/svn/tags/markerclusterer/1.0/examples/advanced_example.html
//################################        
    
// ####################################################################
// Start of javascript code.  You should edit the functions below
// so that your map expresses the particular contents of the data
// ####################################################################
    
var sourcescraper = 'national-river-flow-archive-stations';
$('#scrapername').html('<b>'+sourcescraper+'</b>');
    
// ####################################################################
// Set the dynamic icon for your point.  For more see:
// http://code.google.com/apis/chart/docs/gallery/dynamic_icons.html
// ####################################################################
function mapicon(record)
{
    col = '0F0';
    if (record["discontinued"] == "*")
        col = 'F00';
    letter = 'O';
    icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+letter+'|'+col+'|000';
    proportion = 60;     
    icon = "http://chart.apis.google.com/chart?cht=bvo&chco=0028AB,C6D9FD,4D89F9&chd=t:50|"+proportion+"|100&3E&chm=H,FF0000,0,0,1&chs=50";
    return icon
}

// ####################################################################
// Set the tooltip title value
// ####################################################################
function mapicontext(record)
{
    return record["River"] + ' at ' + record["Location"];
}

// ####################################################################
// Set the popup text for your pin, usually with the link
// ####################################################################
function mapicontent(record)
{
    return '<a href="'+record['url']+'" target="_blank">'+record["River"] + ' at ' + record["Location"]+'</a>';
}

var map;
var centreset = false;
function makemap()
{
    var mapOptions = { "zoom": 4, "center": new google.maps.LatLng(55.500515, -4.128317),
                    "mapTypeId": google.maps.MapTypeId.SATELLITE };
    map = new google.maps.Map(document.getElementById("map"), mapOptions);
}
 
var markers = [];
function recorddata(record)
{
    if (!('latlng' in record))
        return;
    pos = new google.maps.LatLng(record['latlng'][0], record['latlng'][1]);

    text = mapicontext(record);
    icon = mapicon(record);
    content = mapicontent(record);

    marker = new google.maps.Marker({position:pos, title:text, icon:icon});

    infowindow = new google.maps.InfoWindow({ content: content });
    (function(j) {
            google.maps.event.addListener(j.marker, "click", function(){
                                j.infowindow.open(map, j.marker); });
                 })({'marker':marker, 'infowindow':infowindow});
    markers.push(marker);     
}

function refreshMap()
{
    markerClusterer = new MarkerClusterer(map, markers, {gridSize:10});
}

            
var olength = 50;
var olimit = 1000;
var offset = 0; 1    
function gotback(r)
{
    for (i = 0; i < r.length; i++)
        recorddata(r[i]);
    refreshMap();
           
    offset += olength;
    if ((r.length == olength) && (offset < olimit))
        loaddata();
    else
        $("#message").html("Total records=" + (offset - olength + r.length));
}

function loaddata()
{
    $("#message").html("Loading ...");
    var s = document.createElement('script');
    url = "http://api.scraperwiki.com/api/1.0/datastore/getdata?&format=json&name="+sourcescraper+"&limit="+olength+"&callback=gotback&offset=" + offset;
    s.setAttribute('src', url);
    s.setAttribute('type', 'text/javascript');
    document.getElementsByTagName('head')[0].appendChild(s);
}

$(function() { makemap(); loaddata(); });

</script>
</body>
</html>