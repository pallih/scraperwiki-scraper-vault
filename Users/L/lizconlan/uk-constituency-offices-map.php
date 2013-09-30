<html dir="ltr" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>UK Constituency Offices Map</title>
    <style type="text/css" media="screen">p{padding:1px;}</style>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
</head>

<body>

<h2>General Map Thing of <span id="scrapername">...</span> <em id="message">...</em></h2>
<div id="map" style="width:100%;height:400px"></div>

<script type="text/javascript" charset="utf-8">
// ####################################################################
// Start of javascript code.  You should edit the functions below 
// so that your map expresses the particular contents of the data
// ####################################################################
    
var sourcescraper = 'mp-contact-details-from-parliamentuk';
$('#scrapername').html('<b>'+sourcescraper+'</b>'); 
    
// ####################################################################
// Set the dynamic icon for your point.  For more see: 
// http://code.google.com/apis/chart/docs/gallery/dynamic_icons.html
// ####################################################################
function mapicon(record)
{
    col = 'F00';
    letter = 'O';
     
    icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+letter+'|'+col+'|000';
    return icon
}

// ####################################################################
// Set the tooltip title value
// ####################################################################
function mapicontext(record)
{
    return record["constituency"];
}

// ####################################################################
// Set the popup text for your pin, usually with the link
// ####################################################################
function mapicontent(record)
{
    return '<h3>'+ record["constituency"] + '</h3><p>' + record["constituency_address"].replace(/,\ /g,",<br />") + '</p>';
}

var map; 
var centreset = false; 
function makemap()
{
    var mapOptions = { "zoom": 7, "center": new google.maps.LatLng(55.500515, -4.128317), 
                    "mapTypeId": google.maps.MapTypeId.ROADMAP };
    map = new google.maps.Map(document.getElementById("map"), mapOptions);
}
 
function recorddata(record)
{
    if (!('constituency_latlong' in record))
        return;
    if (record['constituency_latlong'] == "")
        return;
    if (!record['constituency_latlong'])
        return;

    str_latlng = record['constituency_latlong'].replace("[",'').replace("]",'').replace(" ",'');

    latlng = str_latlng.split(',');
    pos = new google.maps.LatLng(latlng[0], latlng[1]);

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
    <title>UK Constituency Offices Map</title>
    <style type="text/css" media="screen">p{padding:1px;}</style>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
</head>

<body>

<h2>General Map Thing of <span id="scrapername">...</span> <em id="message">...</em></h2>
<div id="map" style="width:100%;height:400px"></div>

<script type="text/javascript" charset="utf-8">
// ####################################################################
// Start of javascript code.  You should edit the functions below 
// so that your map expresses the particular contents of the data
// ####################################################################
    
var sourcescraper = 'mp-contact-details-from-parliamentuk';
$('#scrapername').html('<b>'+sourcescraper+'</b>'); 
    
// ####################################################################
// Set the dynamic icon for your point.  For more see: 
// http://code.google.com/apis/chart/docs/gallery/dynamic_icons.html
// ####################################################################
function mapicon(record)
{
    col = 'F00';
    letter = 'O';
     
    icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+letter+'|'+col+'|000';
    return icon
}

// ####################################################################
// Set the tooltip title value
// ####################################################################
function mapicontext(record)
{
    return record["constituency"];
}

// ####################################################################
// Set the popup text for your pin, usually with the link
// ####################################################################
function mapicontent(record)
{
    return '<h3>'+ record["constituency"] + '</h3><p>' + record["constituency_address"].replace(/,\ /g,",<br />") + '</p>';
}

var map; 
var centreset = false; 
function makemap()
{
    var mapOptions = { "zoom": 7, "center": new google.maps.LatLng(55.500515, -4.128317), 
                    "mapTypeId": google.maps.MapTypeId.ROADMAP };
    map = new google.maps.Map(document.getElementById("map"), mapOptions);
}
 
function recorddata(record)
{
    if (!('constituency_latlong' in record))
        return;
    if (record['constituency_latlong'] == "")
        return;
    if (!record['constituency_latlong'])
        return;

    str_latlng = record['constituency_latlong'].replace("[",'').replace("]",'').replace(" ",'');

    latlng = str_latlng.split(',');
    pos = new google.maps.LatLng(latlng[0], latlng[1]);

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