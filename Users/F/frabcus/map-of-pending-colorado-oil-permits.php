<html dir="ltr" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>General Map Thing</title>
    <style type="text/css" media="screen">p{padding:1px;}</style>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
</head>

<body>

<h2>General Map Thing of <span id="scrapername">...</span> <em id="message">...</em></h2>
<div id="map" style="width:100%;height:800px"></div>

<script type="text/javascript" charset="utf-8">
// ####################################################################
// Start of javascript code.  You should edit the functions below 
// so that your map expresses the particular contents of the data
// ####################################################################
    
var sourcescraper = 'cogcc_pending_permits';
$('#scrapername').html('<b>'+sourcescraper+'</b>'); 
    
// ####################################################################
// Set the dynamic icon for your point.  For more see: 
// http://code.google.com/apis/chart/docs/gallery/dynamic_icons.html
// ####################################################################
function mapicon(record)
{
    col = 'F00';
    letter = 'O';
    
    status = jQuery.trim(record["Status"]);
    // console.log(record["Status"])
    if (status == "WITHDRAWN") {
        letter = 'W';
        col = '0F0';
    } else if (status == "ON HOLD") {
        letter = 'H';
        col = 'FA0';
    } else if (status == "IN PROCESS") {
        letter = 'P';
        col = 'F00';
    } else if (status === undefined) {
        letter = '-';
        col = '0F0';
    } else {
        /*alert("Unknown type *" + status + "*");*/
    }
    /*
    if (record["Decision"] == "PENDING")
        letter = 'P';
    */  
  
    icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+letter+'|'+col+'|000';
    return icon
}

// ####################################################################
// Set the tooltip title value
// ####################################################################
function mapicontext(record)
{
    return record["Well_name"] 
}

// ####################################################################
// Set the popup text for your pin, usually with the link
// ####################################################################
function mapicontent(record)
{
    //return '<a href="'+record['link']+'" target="_blank">'+record["Well_name"]+'</a>';
    return "Well: " + record['Well_name'] + "<br>Operator name: " + record["Operator_name"] + "<br>Status date: "+record["Status_date"]+"<br><br>"+record['Status'];
}

var map; 
var centreset = false; 
function makemap()
{
    var mapOptions = { "zoom": 8, "center": new google.maps.LatLng(40.340213999999997, -104.70579699999999), 
                    "mapTypeId": google.maps.MapTypeId.HYBRID };
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
    $("#message").html("Loading map..."); 
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
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
</head>

<body>

<h2>General Map Thing of <span id="scrapername">...</span> <em id="message">...</em></h2>
<div id="map" style="width:100%;height:800px"></div>

<script type="text/javascript" charset="utf-8">
// ####################################################################
// Start of javascript code.  You should edit the functions below 
// so that your map expresses the particular contents of the data
// ####################################################################
    
var sourcescraper = 'cogcc_pending_permits';
$('#scrapername').html('<b>'+sourcescraper+'</b>'); 
    
// ####################################################################
// Set the dynamic icon for your point.  For more see: 
// http://code.google.com/apis/chart/docs/gallery/dynamic_icons.html
// ####################################################################
function mapicon(record)
{
    col = 'F00';
    letter = 'O';
    
    status = jQuery.trim(record["Status"]);
    // console.log(record["Status"])
    if (status == "WITHDRAWN") {
        letter = 'W';
        col = '0F0';
    } else if (status == "ON HOLD") {
        letter = 'H';
        col = 'FA0';
    } else if (status == "IN PROCESS") {
        letter = 'P';
        col = 'F00';
    } else if (status === undefined) {
        letter = '-';
        col = '0F0';
    } else {
        /*alert("Unknown type *" + status + "*");*/
    }
    /*
    if (record["Decision"] == "PENDING")
        letter = 'P';
    */  
  
    icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+letter+'|'+col+'|000';
    return icon
}

// ####################################################################
// Set the tooltip title value
// ####################################################################
function mapicontext(record)
{
    return record["Well_name"] 
}

// ####################################################################
// Set the popup text for your pin, usually with the link
// ####################################################################
function mapicontent(record)
{
    //return '<a href="'+record['link']+'" target="_blank">'+record["Well_name"]+'</a>';
    return "Well: " + record['Well_name'] + "<br>Operator name: " + record["Operator_name"] + "<br>Status date: "+record["Status_date"]+"<br><br>"+record['Status'];
}

var map; 
var centreset = false; 
function makemap()
{
    var mapOptions = { "zoom": 8, "center": new google.maps.LatLng(40.340213999999997, -104.70579699999999), 
                    "mapTypeId": google.maps.MapTypeId.HYBRID };
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
    $("#message").html("Loading map..."); 
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