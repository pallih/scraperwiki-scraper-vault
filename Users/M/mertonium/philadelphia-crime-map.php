<html dir="ltr" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>Philadelphia Crime Map</title>
    <style type="text/css" media="screen">
        p{padding:1px;}
        body { 
            font:12px/1.4em Verdana, sans-serif;
            color:#333;
            background-color:#efefef;
            padding:0;
        }
        ul.info-list { 
            list-style-type: none; 
            padding-left: 15px;
            margin-top: 5px;
        }
        h3 { margin: 5px 0; }
    </style>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
</head>

<body>

<h1>Map of the last <span id="totalcrimes"></span> crimes in Philadelphia</h1>
<em id="message">...</em>
<p>The data for this map was obtained from the <a href="http://citymaps.phila.gov/CrimeMap/StepByStep.aspx" traget="_blank">Philadelphia city maps site</a>.  That map is very good, but I wanted to open the data a bit and provide an API so other developers could build off of it.  The data points are hitting a level where they are crowding up the map so it would be cool for someone to add some filtering to this interface.
</p>
<div id="map" style="width:100%;height:600px"></div>

<script type="text/javascript" charset="utf-8">
// ####################################################################
// Start of javascript code.  You should edit the functions below 
// so that your map expresses the particular contents of the data
// ####################################################################
    
var sourcescraper = 'philadelphia-crime-data-1'; 

crimeCodes = {
  "10": { title: "Homicides", mapLetter: "H" },
  "11": { title: "Criminal Homicide", mapLetter: "H" },
  "12": { title: "Justifiable Homicide", mapLetter: "H" },
  "13": { title: "Manslaughter Gross Negligence", mapLetter: "H" },
  "20": { title: "Rapes", mapLetter: "R" },
  "30": { title: "Robberies", mapLetter: "R" },
  "31": { title: "Robberies w/ Gun", mapLetter: "R" },
  "32": { title: "Robberies no Gun", mapLetter: "R" },
  "40": { title: "Agg Assaults", mapLetter: "A" },
  "41": { title: "Agg Assault w/ Gun", mapLetter: "A" },
  "42": { title: "Agg Assault No Gun", mapLetter: "A" },
  "50": { title: "Burglaries", mapLetter: "B" },
  "51": { title: "Residential Burglaries", mapLetter: "B" },
  "52": { title: "Residentail Burglaries - Day", mapLetter: "B" },
  "53": { title: "Residential Burglaries - Night", mapLetter: "B" },
  "54": { title: "Commercial Burglaries", mapLetter: "B" },
  "60": { title: "Thefts", mapLetter: "T" },
  "61": { title: "Theft from Auto", mapLetter: "T" },
  "62": { title: "Theft Other", mapLetter: "T" },
  "63": { title: "Purse Snatchings", mapLetter: "T" },
  "64": { title: "Pick Pockets", mapLetter: "T" },
  "65": { title: "Bicycle Thefts", mapLetter: "T" },
  "66": { title: "Retail Theft", mapLetter: "T" },
  "67": { title: "Vehicle Stickers/Tags", mapLetter: "V" },
  "70": { title: "Stolen/Recovered Vehicles", mapLetter: "V" },
  "71": { title: "Stolen Vehicles", mapLetter: "V" },
  "72": { title: "Recovered Vehicles", mapLetter: "V" },
  "default": { title: "Dunno", mapLetter: "O"}
}
    
// ####################################################################
// Set the dynamic icon for your point.  For more see: 
// http://code.google.com/apis/chart/docs/gallery/dynamic_icons.html
// ####################################################################
function mapicon(record)
{
    col = 'F00';
    if (record["Decision"] == "PENDING")
        col = '0F0';

    letter = 'O';
    if (record["Decision"] == "PENDING")
        letter = 'P';
    
    letter = (crimeCodes[record["crimeclass"]] || crimeCodes["default"])["mapLetter"] 
 
    icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+letter+'|'+col+'|000';
    return icon
}

// ####################################################################
// Set the tooltip title value
// ####################################################################
function mapicontext(record)
{
    return record["Ucr_text"];
}

// ####################################################################
// Set the popup text for your pin, usually with the link
// ####################################################################
function mapicontent(record)
{
    return '<h3>'+record['Ucr_text']+'</h3><ul class="info-list"><li>'+record['Dispatch_date_time']+'</li><li><strong>Location:</strong> '+record['Location']+'</li><li><strong>DC Key:</strong> '+record['Dc_key']+'</li></ul>';
}

var map; 
var centreset = false; 
function makemap()
{
    var mapOptions = { "zoom": 12, "center": new google.maps.LatLng(39.95291166179976, -75.16021728515625), 
                    "mapTypeId": google.maps.MapTypeId.SATELLITE };
    map = new google.maps.Map(document.getElementById("map"), mapOptions);
}
 
function recorddata(record)
{
    if (!record['latlng_lat'])
        return; 
    pos = new google.maps.LatLng(record['latlng_lat'], record['latlng_lng']); 

    var d = new Date(record['Dispatch_date_time']);
    record['Dispatch_date_time'] = d.toLocaleDateString();

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
 
$('#totalcrimes').html(olength);
 
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
<p><strong>Add some other filtering here.</strong> Maybe a nice date slider, or time of day option, or a way to select which crimes appear, etc.</p>
</body> 
</html><html dir="ltr" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>Philadelphia Crime Map</title>
    <style type="text/css" media="screen">
        p{padding:1px;}
        body { 
            font:12px/1.4em Verdana, sans-serif;
            color:#333;
            background-color:#efefef;
            padding:0;
        }
        ul.info-list { 
            list-style-type: none; 
            padding-left: 15px;
            margin-top: 5px;
        }
        h3 { margin: 5px 0; }
    </style>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
</head>

<body>

<h1>Map of the last <span id="totalcrimes"></span> crimes in Philadelphia</h1>
<em id="message">...</em>
<p>The data for this map was obtained from the <a href="http://citymaps.phila.gov/CrimeMap/StepByStep.aspx" traget="_blank">Philadelphia city maps site</a>.  That map is very good, but I wanted to open the data a bit and provide an API so other developers could build off of it.  The data points are hitting a level where they are crowding up the map so it would be cool for someone to add some filtering to this interface.
</p>
<div id="map" style="width:100%;height:600px"></div>

<script type="text/javascript" charset="utf-8">
// ####################################################################
// Start of javascript code.  You should edit the functions below 
// so that your map expresses the particular contents of the data
// ####################################################################
    
var sourcescraper = 'philadelphia-crime-data-1'; 

crimeCodes = {
  "10": { title: "Homicides", mapLetter: "H" },
  "11": { title: "Criminal Homicide", mapLetter: "H" },
  "12": { title: "Justifiable Homicide", mapLetter: "H" },
  "13": { title: "Manslaughter Gross Negligence", mapLetter: "H" },
  "20": { title: "Rapes", mapLetter: "R" },
  "30": { title: "Robberies", mapLetter: "R" },
  "31": { title: "Robberies w/ Gun", mapLetter: "R" },
  "32": { title: "Robberies no Gun", mapLetter: "R" },
  "40": { title: "Agg Assaults", mapLetter: "A" },
  "41": { title: "Agg Assault w/ Gun", mapLetter: "A" },
  "42": { title: "Agg Assault No Gun", mapLetter: "A" },
  "50": { title: "Burglaries", mapLetter: "B" },
  "51": { title: "Residential Burglaries", mapLetter: "B" },
  "52": { title: "Residentail Burglaries - Day", mapLetter: "B" },
  "53": { title: "Residential Burglaries - Night", mapLetter: "B" },
  "54": { title: "Commercial Burglaries", mapLetter: "B" },
  "60": { title: "Thefts", mapLetter: "T" },
  "61": { title: "Theft from Auto", mapLetter: "T" },
  "62": { title: "Theft Other", mapLetter: "T" },
  "63": { title: "Purse Snatchings", mapLetter: "T" },
  "64": { title: "Pick Pockets", mapLetter: "T" },
  "65": { title: "Bicycle Thefts", mapLetter: "T" },
  "66": { title: "Retail Theft", mapLetter: "T" },
  "67": { title: "Vehicle Stickers/Tags", mapLetter: "V" },
  "70": { title: "Stolen/Recovered Vehicles", mapLetter: "V" },
  "71": { title: "Stolen Vehicles", mapLetter: "V" },
  "72": { title: "Recovered Vehicles", mapLetter: "V" },
  "default": { title: "Dunno", mapLetter: "O"}
}
    
// ####################################################################
// Set the dynamic icon for your point.  For more see: 
// http://code.google.com/apis/chart/docs/gallery/dynamic_icons.html
// ####################################################################
function mapicon(record)
{
    col = 'F00';
    if (record["Decision"] == "PENDING")
        col = '0F0';

    letter = 'O';
    if (record["Decision"] == "PENDING")
        letter = 'P';
    
    letter = (crimeCodes[record["crimeclass"]] || crimeCodes["default"])["mapLetter"] 
 
    icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+letter+'|'+col+'|000';
    return icon
}

// ####################################################################
// Set the tooltip title value
// ####################################################################
function mapicontext(record)
{
    return record["Ucr_text"];
}

// ####################################################################
// Set the popup text for your pin, usually with the link
// ####################################################################
function mapicontent(record)
{
    return '<h3>'+record['Ucr_text']+'</h3><ul class="info-list"><li>'+record['Dispatch_date_time']+'</li><li><strong>Location:</strong> '+record['Location']+'</li><li><strong>DC Key:</strong> '+record['Dc_key']+'</li></ul>';
}

var map; 
var centreset = false; 
function makemap()
{
    var mapOptions = { "zoom": 12, "center": new google.maps.LatLng(39.95291166179976, -75.16021728515625), 
                    "mapTypeId": google.maps.MapTypeId.SATELLITE };
    map = new google.maps.Map(document.getElementById("map"), mapOptions);
}
 
function recorddata(record)
{
    if (!record['latlng_lat'])
        return; 
    pos = new google.maps.LatLng(record['latlng_lat'], record['latlng_lng']); 

    var d = new Date(record['Dispatch_date_time']);
    record['Dispatch_date_time'] = d.toLocaleDateString();

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
 
$('#totalcrimes').html(olength);
 
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
<p><strong>Add some other filtering here.</strong> Maybe a nice date slider, or time of day option, or a way to select which crimes appear, etc.</p>
</body> 
</html>