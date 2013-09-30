<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>Liverpool empty residential properties by council tax records<</title>
    <style type="text/css" media="screen">p{padding:1px;}</style>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>

    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
    <script type="text/javascript" src="http://google-maps-utility-library-v3.googlecode.com/svn/tags/markerclusterer/1.0/src/markerclusterer.js"></script>
</head>

<body>

<h2>Liverpool empty residential properties by council tax records</h2>
    
<p> <span id="message">...</span> Source: Council tax records, Liverpool City Council, <a href="http://www.whatdotheyknow.com/request/empty_property_list_37">response to FOI request</a>, 7th April 2010</p>
        
<div id="map" style="width:100%;height:400px"></div>

<script type="text/javascript" charset="utf-8">
// ####################################################################
// Start of javascript code.  You should edit the functions below 
// so that your map expresses the particular contents of the data
// ####################################################################
    
var sourcescraper = 'liverpool-empty-residential-properties';
$('#scrapername').html('<b>'+sourcescraper+'</b>'); 
    
// ####################################################################
// Set the dynamic icon for your point.  For more see: 
// http://code.google.com/apis/chart/docs/gallery/dynamic_icons.html
// ####################################################################
function mapicon(record)
{
    // XXX maybe could vary colour according to band too?
    col = '0F0';

    letter = record['band'];
    
    icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+letter+'|'+col+'|000';
    return icon
}

// ####################################################################
// Set the tooltip title value
// ####################################################################
function mapicontext(record)
{
    return "TOOLTIP " + record["address1"] + "," + record["address2"]
}

// ####################################################################
// Set the popup text for your pin, usually with the link
// ####################################################################
function mapicontent(record)
{
    // This can have HTML in it, e.g. links
        return record["address1"] + "<br>" + record["address2"] + "<br>" + record["postcode"] + "<br><br>Period start: " + record["date"].substring(0, 10) + "<br>Council tax ref: " + record["ctax_prop_ref"]  + " Band: " + record["band"];
}

var map; 
var centreset = false; 
function makemap()
{    
    var mapOptions = { "zoom": 12, "center": new google.maps.LatLng(55.500515, -4.128317), 
                    "mapTypeId": google.maps.MapTypeId.ROADMAP };
    map = new google.maps.Map(document.getElementById("map"), mapOptions);
}
 
var markers = [];
function recorddata(record)
{
    if (!('latlng' in record))
        return; 
    
    // Move randomly a bit, as the marker clustering code will otherwise never
    // disaggregate two properties at the same postcode.
    rand1 = (Math.floor(Math.random()*10001) - 6) / 100000000
    rand2 = (Math.floor(Math.random()*10001) - 6) / 100000000

    pos = new google.maps.LatLng(record['latlng'][0] + rand1, record['latlng'][1] + rand2); 

    text = mapicontext(record);
    icon = mapicon(record);
    content = mapicontent(record); 

    marker = new google.maps.Marker({position:pos,title:text, icon:icon});

    infowindow = new google.maps.InfoWindow({ content: content });
    (function(j) {
            google.maps.event.addListener(j.marker, "click", function(){
                                j.infowindow.open(map, j.marker); });
                 })({'marker':marker, 'infowindow':infowindow});
    if (!centreset)
        {  map.setCenter(pos); centreset = true }

    markers.push(marker);
}
    

function refreshMap()
{
    markerClusterer = new MarkerClusterer(map, markers, {gridSize:10}); 
}


var olength = 250; 
var olimit = 20000; 
var offset = 0;
           
function gotback(r) 
{
    for (i = 0; i < r.length; i++)
        recorddata(r[i]);
    refreshMap();

    offset += olength; 
    if ((r.length == olength) && (offset < olimit))
        loaddata(); 
    else
        $("#message").html("Total homes: " + (offset - olength + r.length) + "."); 
}

function loaddata() 
{
    $("#message").html("<span style='background-color: green; color: white; padding: 0.5em;'>Loading ... " + offset + " homes so far.</span>"); 
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
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>Liverpool empty residential properties by council tax records<</title>
    <style type="text/css" media="screen">p{padding:1px;}</style>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>

    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
    <script type="text/javascript" src="http://google-maps-utility-library-v3.googlecode.com/svn/tags/markerclusterer/1.0/src/markerclusterer.js"></script>
</head>

<body>

<h2>Liverpool empty residential properties by council tax records</h2>
    
<p> <span id="message">...</span> Source: Council tax records, Liverpool City Council, <a href="http://www.whatdotheyknow.com/request/empty_property_list_37">response to FOI request</a>, 7th April 2010</p>
        
<div id="map" style="width:100%;height:400px"></div>

<script type="text/javascript" charset="utf-8">
// ####################################################################
// Start of javascript code.  You should edit the functions below 
// so that your map expresses the particular contents of the data
// ####################################################################
    
var sourcescraper = 'liverpool-empty-residential-properties';
$('#scrapername').html('<b>'+sourcescraper+'</b>'); 
    
// ####################################################################
// Set the dynamic icon for your point.  For more see: 
// http://code.google.com/apis/chart/docs/gallery/dynamic_icons.html
// ####################################################################
function mapicon(record)
{
    // XXX maybe could vary colour according to band too?
    col = '0F0';

    letter = record['band'];
    
    icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+letter+'|'+col+'|000';
    return icon
}

// ####################################################################
// Set the tooltip title value
// ####################################################################
function mapicontext(record)
{
    return "TOOLTIP " + record["address1"] + "," + record["address2"]
}

// ####################################################################
// Set the popup text for your pin, usually with the link
// ####################################################################
function mapicontent(record)
{
    // This can have HTML in it, e.g. links
        return record["address1"] + "<br>" + record["address2"] + "<br>" + record["postcode"] + "<br><br>Period start: " + record["date"].substring(0, 10) + "<br>Council tax ref: " + record["ctax_prop_ref"]  + " Band: " + record["band"];
}

var map; 
var centreset = false; 
function makemap()
{    
    var mapOptions = { "zoom": 12, "center": new google.maps.LatLng(55.500515, -4.128317), 
                    "mapTypeId": google.maps.MapTypeId.ROADMAP };
    map = new google.maps.Map(document.getElementById("map"), mapOptions);
}
 
var markers = [];
function recorddata(record)
{
    if (!('latlng' in record))
        return; 
    
    // Move randomly a bit, as the marker clustering code will otherwise never
    // disaggregate two properties at the same postcode.
    rand1 = (Math.floor(Math.random()*10001) - 6) / 100000000
    rand2 = (Math.floor(Math.random()*10001) - 6) / 100000000

    pos = new google.maps.LatLng(record['latlng'][0] + rand1, record['latlng'][1] + rand2); 

    text = mapicontext(record);
    icon = mapicon(record);
    content = mapicontent(record); 

    marker = new google.maps.Marker({position:pos,title:text, icon:icon});

    infowindow = new google.maps.InfoWindow({ content: content });
    (function(j) {
            google.maps.event.addListener(j.marker, "click", function(){
                                j.infowindow.open(map, j.marker); });
                 })({'marker':marker, 'infowindow':infowindow});
    if (!centreset)
        {  map.setCenter(pos); centreset = true }

    markers.push(marker);
}
    

function refreshMap()
{
    markerClusterer = new MarkerClusterer(map, markers, {gridSize:10}); 
}


var olength = 250; 
var olimit = 20000; 
var offset = 0;
           
function gotback(r) 
{
    for (i = 0; i < r.length; i++)
        recorddata(r[i]);
    refreshMap();

    offset += olength; 
    if ((r.length == olength) && (offset < olimit))
        loaddata(); 
    else
        $("#message").html("Total homes: " + (offset - olength + r.length) + "."); 
}

function loaddata() 
{
    $("#message").html("<span style='background-color: green; color: white; padding: 0.5em;'>Loading ... " + offset + " homes so far.</span>"); 
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
