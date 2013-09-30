<!-- Do not edit - this is just for showing a bug in CodeMirror -->

<html dir="ltr" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>General Map Thing of Earthquakes in Iceland 1706 - 1990 // size >4</title>
    <style type="text/css" media="screen">p{padding:1px;}</style>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
</head>

<body>

<h2>General Map Thing of <span id="scrapername">...</span> <em id="message">...</em></h2>
<div id="map" style="width:100%;height:400px"></div>

<p><img src="http://blogs.warwick.ac.uk/images/campbello/2008/02/27/richter-scale.gif?maxWidth=500" alt="Richter Scale"></p>

<script type="text/javascript" charset="utf-8">
// ####################################################################
// Start of javascript code.  You should edit the functions below 
// so that your map expresses the particular contents of the data
// ####################################################################
    
var sourcescraper = 'jarskjalftar-a-islandi-4-1706-1990';
$('#scrapername').html('<b>'+sourcescraper+'</b>'); 
    
// ####################################################################
// Set the dynamic icon for your point.  For more see: 
// http://code.google.com/apis/chart/docs/gallery/dynamic_icons.html
// ####################################################################
function mapicon(record)
{
    col = '660099';
    if (record["size"] >= 2.0)
        col = '0099ff';
    if (record["size"] >= 3.0)
        col = '00cb98';
    if (record["size"] >= 4.0)
        col = '99cc66';
    if (record["size"] >= 5.0)
        col = '96fb32';
    if (record["size"] >= 6.0)
        col = 'ffff33';
    if (record["size"] >= 7.0)
        col = 'ffcc66';
    if (record["size"] >= 8.0)
        col = 'ff9966';
    if (record["size"] >= 9.0)
        col = 'ff3300';

    letter = 'O';
    //if (record["Decision"] == "PENDING")
    //    letter = 'P';
     
    icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+letter+'|'+col+'|000';
    return icon
}

// ####################################################################
// Set the tooltip title value
// ####################################################################
function mapicontext(record)
{
    return "TOOLTIP " + record["size"] 
}

// ####################################################################
// Set the popup text for your pin, usually with the link
// ####################################################################
function mapicontent(record)
{
    return 'Size: ' + record["size"]+'</br>Date: ' +record["date"];
}

var map; 
var centreset = false; 
function makemap()
{
    var mapOptions = { "zoom": 4, "center": new google.maps.LatLng(64.9607663214987, -18.984375), 
                    "mapTypeId": google.maps.MapTypeId.SATELLITE };
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
    if (!centreset)
        {  map.setCenter(pos); centreset = true }
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
        $("#message").html("Total records = " + (offset - olength + r.length)); 
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
</html><!-- Do not edit - this is just for showing a bug in CodeMirror -->

<html dir="ltr" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>General Map Thing of Earthquakes in Iceland 1706 - 1990 // size >4</title>
    <style type="text/css" media="screen">p{padding:1px;}</style>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
</head>

<body>

<h2>General Map Thing of <span id="scrapername">...</span> <em id="message">...</em></h2>
<div id="map" style="width:100%;height:400px"></div>

<p><img src="http://blogs.warwick.ac.uk/images/campbello/2008/02/27/richter-scale.gif?maxWidth=500" alt="Richter Scale"></p>

<script type="text/javascript" charset="utf-8">
// ####################################################################
// Start of javascript code.  You should edit the functions below 
// so that your map expresses the particular contents of the data
// ####################################################################
    
var sourcescraper = 'jarskjalftar-a-islandi-4-1706-1990';
$('#scrapername').html('<b>'+sourcescraper+'</b>'); 
    
// ####################################################################
// Set the dynamic icon for your point.  For more see: 
// http://code.google.com/apis/chart/docs/gallery/dynamic_icons.html
// ####################################################################
function mapicon(record)
{
    col = '660099';
    if (record["size"] >= 2.0)
        col = '0099ff';
    if (record["size"] >= 3.0)
        col = '00cb98';
    if (record["size"] >= 4.0)
        col = '99cc66';
    if (record["size"] >= 5.0)
        col = '96fb32';
    if (record["size"] >= 6.0)
        col = 'ffff33';
    if (record["size"] >= 7.0)
        col = 'ffcc66';
    if (record["size"] >= 8.0)
        col = 'ff9966';
    if (record["size"] >= 9.0)
        col = 'ff3300';

    letter = 'O';
    //if (record["Decision"] == "PENDING")
    //    letter = 'P';
     
    icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+letter+'|'+col+'|000';
    return icon
}

// ####################################################################
// Set the tooltip title value
// ####################################################################
function mapicontext(record)
{
    return "TOOLTIP " + record["size"] 
}

// ####################################################################
// Set the popup text for your pin, usually with the link
// ####################################################################
function mapicontent(record)
{
    return 'Size: ' + record["size"]+'</br>Date: ' +record["date"];
}

var map; 
var centreset = false; 
function makemap()
{
    var mapOptions = { "zoom": 4, "center": new google.maps.LatLng(64.9607663214987, -18.984375), 
                    "mapTypeId": google.maps.MapTypeId.SATELLITE };
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
    if (!centreset)
        {  map.setCenter(pos); centreset = true }
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
        $("#message").html("Total records = " + (offset - olength + r.length)); 
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