<html dir="ltr" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>Lleoliadiadau</title>
    <style type="text/css" media="screen">p{padding:1px;}</style>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
</head>

<body>

    <h2>Locations / Lleoliadau <span id="scrapername">...</span> <em id="message">...</em></h2>
<div id="map" style="width:100%;height:400px"></div>

<script type="text/javascript" charset="utf-8">
// ####################################################################
// Start of javascript code.  You should edit the functions below
// so that your map expresses the particular contents of the data
// ####################################################################
    
var sourcescraper = 'welsh-medium-playgroups-cylchoedd-mym';
$('#scrapername').html('<b>'+sourcescraper+'</b>');
    
// ####################################################################
// Set the dynamic icon for your point.  For more see:
// http://code.google.com/apis/chart/docs/gallery/dynamic_icons.html
// ####################################################################
function mapicon(record)
{
    col = 'CC0066'; 
    letter = 'A';
        
    if (record["Math_o_gylch"] == "MEITHRIN")
    {
        col = 'F000F0';
        letter = 'M'; 
    }   
    
    if (record["Math_o_gylch"] == "MEITHRIN/TIAFI")
    {
        col = '6698FF';
        letter = 'C';
    }    
    
    if (record["Math_o_gylch"] == "TI A FI")
    {
        col = '00FF00'; letter = 'T';
    }
                     
    icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+letter+'|'+col;
    return icon
}

// ####################################################################
// Set the tooltip title value
// ####################################################################
function mapicontext(record)
{
        return "Math o gylch Type " + record["Math_o_gylch"]
}

// ####################################################################
// Set the popup text for your pin, usually with the link
// ####################################################################
function mapicontent(record)
{
        return record["Enw"] + " " + record["Cyfeiriad_1"] + ", " + record["Cyfeiriad_2"] + ", " + record["Cyfeiriad_3"]  + ", " + record["Cyfeiriad_4"] + " Tel: " + record["Rhif_Ffon"];
}

var map;
var centreset = false;
function makemap()
{
    var mapOptions = { "zoom": 7, "center": new google.maps.LatLng(53.5, -3.3),
                    "mapTypeId": google.maps.MapTypeId.SATELLITE };
    map = new google.maps.Map(document.getElementById("map"), mapOptions);
}
 
function recorddata(record)
{
    if (!(record['latlong']))
        return;
    coords = eval(record['latlong'].replace("(", "[").replace(")", "]"))
    pos = new google.maps.LatLng(coords[0], coords[1]);

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
    <title>Lleoliadiadau</title>
    <style type="text/css" media="screen">p{padding:1px;}</style>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
</head>

<body>

    <h2>Locations / Lleoliadau <span id="scrapername">...</span> <em id="message">...</em></h2>
<div id="map" style="width:100%;height:400px"></div>

<script type="text/javascript" charset="utf-8">
// ####################################################################
// Start of javascript code.  You should edit the functions below
// so that your map expresses the particular contents of the data
// ####################################################################
    
var sourcescraper = 'welsh-medium-playgroups-cylchoedd-mym';
$('#scrapername').html('<b>'+sourcescraper+'</b>');
    
// ####################################################################
// Set the dynamic icon for your point.  For more see:
// http://code.google.com/apis/chart/docs/gallery/dynamic_icons.html
// ####################################################################
function mapicon(record)
{
    col = 'CC0066'; 
    letter = 'A';
        
    if (record["Math_o_gylch"] == "MEITHRIN")
    {
        col = 'F000F0';
        letter = 'M'; 
    }   
    
    if (record["Math_o_gylch"] == "MEITHRIN/TIAFI")
    {
        col = '6698FF';
        letter = 'C';
    }    
    
    if (record["Math_o_gylch"] == "TI A FI")
    {
        col = '00FF00'; letter = 'T';
    }
                     
    icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+letter+'|'+col;
    return icon
}

// ####################################################################
// Set the tooltip title value
// ####################################################################
function mapicontext(record)
{
        return "Math o gylch Type " + record["Math_o_gylch"]
}

// ####################################################################
// Set the popup text for your pin, usually with the link
// ####################################################################
function mapicontent(record)
{
        return record["Enw"] + " " + record["Cyfeiriad_1"] + ", " + record["Cyfeiriad_2"] + ", " + record["Cyfeiriad_3"]  + ", " + record["Cyfeiriad_4"] + " Tel: " + record["Rhif_Ffon"];
}

var map;
var centreset = false;
function makemap()
{
    var mapOptions = { "zoom": 7, "center": new google.maps.LatLng(53.5, -3.3),
                    "mapTypeId": google.maps.MapTypeId.SATELLITE };
    map = new google.maps.Map(document.getElementById("map"), mapOptions);
}
 
function recorddata(record)
{
    if (!(record['latlong']))
        return;
    coords = eval(record['latlong'].replace("(", "[").replace(")", "]"))
    pos = new google.maps.LatLng(coords[0], coords[1]);

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