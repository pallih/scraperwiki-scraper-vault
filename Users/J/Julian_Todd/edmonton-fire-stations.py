import json
import urllib
import lxml.etree
import re
import scraperwiki
scraperwiki.cache(True)

def GetData():
    root = lxml.etree.parse(urllib.urlopen("http://datafeed.edmonton.ca/v1/coe/FireStations")).getroot()
    for r in root.findall('.//{http://www.w3.org/2005/Atom}content/{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties'):
        data = { }
        for d in r:
            data[re.sub('\{.*?}', '', d.tag)] = d.text
        yield data

def GetJData():
    jdata = [ ]
    for data in GetData():
        letter = (data.get('is_ems_combined') == 'yes' and 'Y' or 'N')
        jdata.append((float(data['latitude']), float(data['longitude']), letter, data.get('address', '')))
    return jdata
                     
def Main():
    print part1
    print 'var jdata = %s;' % json.dumps(GetJData()) 
    #print 'var jdata = %s;' % json.dumps([ [55.500515, -4.128317, 'L'] ]) 
    print part2

part1 = """
<html dir="ltr" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>Edmonton Firestations</title>
    <style type="text/css" media="screen">p{padding:1px;}</style>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
</head>

<body>

<h2>Map of Edmonton fire stations</h2>
<div id="map" style="width:100%;height:400px"></div>

<script type="text/javascript" charset="utf-8">
// ####################################################################
// Start of javascript code.  You should edit the functions below 
// so that your map expresses the particular contents of the data
// ####################################################################
    
var sourcescraper = 'Edmonton fire stations';
$('#scrapername').html('<b>'+sourcescraper+'</b>'); 
    

var map; 
var centreset = false; 
function makemap()
{
    var mapOptions = { "zoom": 11, "center": new google.maps.LatLng(55.500515, -4.128317), 
                    "mapTypeId": google.maps.MapTypeId.SATELLITE };
    map = new google.maps.Map(document.getElementById("map"), mapOptions);
}
 
function recorddata(lat, lng, letter, address)
{
    col = 'F00'; 
    if (letter == 'Y')  col = '0F0'; 
    icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+letter+'|'+col+'|000'
    pos = new google.maps.LatLng(lat, lng); 
    text = 'text';
    content = address; 

    marker = new google.maps.Marker({position:pos,map:map,title:text, icon:icon});

    infowindow = new google.maps.InfoWindow({ content: content });
    (function(j) {
            google.maps.event.addListener(j.marker, "click", function(){
                                j.infowindow.open(map, j.marker); });
                 })({'marker':marker, 'infowindow':infowindow});
    if (!centreset)
        {  map.setCenter(pos); centreset = true }
}
"""


part2 = """
function loaddata() 
{
 
    for (i = 0; i < jdata.length; i++)
         recorddata(jdata[i][0], jdata[i][1], jdata[i][2], jdata[i][3]); 
}

$(function() { makemap(); loaddata(); });

</script> 
 
<p><img src="http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=Y|0F0|000" style="vertical-align: middle; padding: 0.5em;">Green pins have the s_ems_combined = yes.
<br>
<img src="http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=N|F00|000" style="vertical-align: middle; padding: 0.5em;">Red pins have s_ems_combined = no.</p>
 
<p>Source: <a href="http://data.edmonton.ca/DataBrowser/coe/FireStations#param=NOFILTER--DataView--Results">Edmonton Open Data Catalogue</a>
 
</body> 
</html>
 """
Main()
import json
import urllib
import lxml.etree
import re
import scraperwiki
scraperwiki.cache(True)

def GetData():
    root = lxml.etree.parse(urllib.urlopen("http://datafeed.edmonton.ca/v1/coe/FireStations")).getroot()
    for r in root.findall('.//{http://www.w3.org/2005/Atom}content/{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties'):
        data = { }
        for d in r:
            data[re.sub('\{.*?}', '', d.tag)] = d.text
        yield data

def GetJData():
    jdata = [ ]
    for data in GetData():
        letter = (data.get('is_ems_combined') == 'yes' and 'Y' or 'N')
        jdata.append((float(data['latitude']), float(data['longitude']), letter, data.get('address', '')))
    return jdata
                     
def Main():
    print part1
    print 'var jdata = %s;' % json.dumps(GetJData()) 
    #print 'var jdata = %s;' % json.dumps([ [55.500515, -4.128317, 'L'] ]) 
    print part2

part1 = """
<html dir="ltr" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>Edmonton Firestations</title>
    <style type="text/css" media="screen">p{padding:1px;}</style>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
</head>

<body>

<h2>Map of Edmonton fire stations</h2>
<div id="map" style="width:100%;height:400px"></div>

<script type="text/javascript" charset="utf-8">
// ####################################################################
// Start of javascript code.  You should edit the functions below 
// so that your map expresses the particular contents of the data
// ####################################################################
    
var sourcescraper = 'Edmonton fire stations';
$('#scrapername').html('<b>'+sourcescraper+'</b>'); 
    

var map; 
var centreset = false; 
function makemap()
{
    var mapOptions = { "zoom": 11, "center": new google.maps.LatLng(55.500515, -4.128317), 
                    "mapTypeId": google.maps.MapTypeId.SATELLITE };
    map = new google.maps.Map(document.getElementById("map"), mapOptions);
}
 
function recorddata(lat, lng, letter, address)
{
    col = 'F00'; 
    if (letter == 'Y')  col = '0F0'; 
    icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+letter+'|'+col+'|000'
    pos = new google.maps.LatLng(lat, lng); 
    text = 'text';
    content = address; 

    marker = new google.maps.Marker({position:pos,map:map,title:text, icon:icon});

    infowindow = new google.maps.InfoWindow({ content: content });
    (function(j) {
            google.maps.event.addListener(j.marker, "click", function(){
                                j.infowindow.open(map, j.marker); });
                 })({'marker':marker, 'infowindow':infowindow});
    if (!centreset)
        {  map.setCenter(pos); centreset = true }
}
"""


part2 = """
function loaddata() 
{
 
    for (i = 0; i < jdata.length; i++)
         recorddata(jdata[i][0], jdata[i][1], jdata[i][2], jdata[i][3]); 
}

$(function() { makemap(); loaddata(); });

</script> 
 
<p><img src="http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=Y|0F0|000" style="vertical-align: middle; padding: 0.5em;">Green pins have the s_ems_combined = yes.
<br>
<img src="http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=N|F00|000" style="vertical-align: middle; padding: 0.5em;">Red pins have s_ems_combined = no.</p>
 
<p>Source: <a href="http://data.edmonton.ca/DataBrowser/coe/FireStations#param=NOFILTER--DataView--Results">Edmonton Open Data Catalogue</a>
 
</body> 
</html>
 """
Main()
import json
import urllib
import lxml.etree
import re
import scraperwiki
scraperwiki.cache(True)

def GetData():
    root = lxml.etree.parse(urllib.urlopen("http://datafeed.edmonton.ca/v1/coe/FireStations")).getroot()
    for r in root.findall('.//{http://www.w3.org/2005/Atom}content/{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties'):
        data = { }
        for d in r:
            data[re.sub('\{.*?}', '', d.tag)] = d.text
        yield data

def GetJData():
    jdata = [ ]
    for data in GetData():
        letter = (data.get('is_ems_combined') == 'yes' and 'Y' or 'N')
        jdata.append((float(data['latitude']), float(data['longitude']), letter, data.get('address', '')))
    return jdata
                     
def Main():
    print part1
    print 'var jdata = %s;' % json.dumps(GetJData()) 
    #print 'var jdata = %s;' % json.dumps([ [55.500515, -4.128317, 'L'] ]) 
    print part2

part1 = """
<html dir="ltr" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>Edmonton Firestations</title>
    <style type="text/css" media="screen">p{padding:1px;}</style>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
</head>

<body>

<h2>Map of Edmonton fire stations</h2>
<div id="map" style="width:100%;height:400px"></div>

<script type="text/javascript" charset="utf-8">
// ####################################################################
// Start of javascript code.  You should edit the functions below 
// so that your map expresses the particular contents of the data
// ####################################################################
    
var sourcescraper = 'Edmonton fire stations';
$('#scrapername').html('<b>'+sourcescraper+'</b>'); 
    

var map; 
var centreset = false; 
function makemap()
{
    var mapOptions = { "zoom": 11, "center": new google.maps.LatLng(55.500515, -4.128317), 
                    "mapTypeId": google.maps.MapTypeId.SATELLITE };
    map = new google.maps.Map(document.getElementById("map"), mapOptions);
}
 
function recorddata(lat, lng, letter, address)
{
    col = 'F00'; 
    if (letter == 'Y')  col = '0F0'; 
    icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+letter+'|'+col+'|000'
    pos = new google.maps.LatLng(lat, lng); 
    text = 'text';
    content = address; 

    marker = new google.maps.Marker({position:pos,map:map,title:text, icon:icon});

    infowindow = new google.maps.InfoWindow({ content: content });
    (function(j) {
            google.maps.event.addListener(j.marker, "click", function(){
                                j.infowindow.open(map, j.marker); });
                 })({'marker':marker, 'infowindow':infowindow});
    if (!centreset)
        {  map.setCenter(pos); centreset = true }
}
"""


part2 = """
function loaddata() 
{
 
    for (i = 0; i < jdata.length; i++)
         recorddata(jdata[i][0], jdata[i][1], jdata[i][2], jdata[i][3]); 
}

$(function() { makemap(); loaddata(); });

</script> 
 
<p><img src="http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=Y|0F0|000" style="vertical-align: middle; padding: 0.5em;">Green pins have the s_ems_combined = yes.
<br>
<img src="http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=N|F00|000" style="vertical-align: middle; padding: 0.5em;">Red pins have s_ems_combined = no.</p>
 
<p>Source: <a href="http://data.edmonton.ca/DataBrowser/coe/FireStations#param=NOFILTER--DataView--Results">Edmonton Open Data Catalogue</a>
 
</body> 
</html>
 """
Main()
import json
import urllib
import lxml.etree
import re
import scraperwiki
scraperwiki.cache(True)

def GetData():
    root = lxml.etree.parse(urllib.urlopen("http://datafeed.edmonton.ca/v1/coe/FireStations")).getroot()
    for r in root.findall('.//{http://www.w3.org/2005/Atom}content/{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties'):
        data = { }
        for d in r:
            data[re.sub('\{.*?}', '', d.tag)] = d.text
        yield data

def GetJData():
    jdata = [ ]
    for data in GetData():
        letter = (data.get('is_ems_combined') == 'yes' and 'Y' or 'N')
        jdata.append((float(data['latitude']), float(data['longitude']), letter, data.get('address', '')))
    return jdata
                     
def Main():
    print part1
    print 'var jdata = %s;' % json.dumps(GetJData()) 
    #print 'var jdata = %s;' % json.dumps([ [55.500515, -4.128317, 'L'] ]) 
    print part2

part1 = """
<html dir="ltr" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>Edmonton Firestations</title>
    <style type="text/css" media="screen">p{padding:1px;}</style>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
</head>

<body>

<h2>Map of Edmonton fire stations</h2>
<div id="map" style="width:100%;height:400px"></div>

<script type="text/javascript" charset="utf-8">
// ####################################################################
// Start of javascript code.  You should edit the functions below 
// so that your map expresses the particular contents of the data
// ####################################################################
    
var sourcescraper = 'Edmonton fire stations';
$('#scrapername').html('<b>'+sourcescraper+'</b>'); 
    

var map; 
var centreset = false; 
function makemap()
{
    var mapOptions = { "zoom": 11, "center": new google.maps.LatLng(55.500515, -4.128317), 
                    "mapTypeId": google.maps.MapTypeId.SATELLITE };
    map = new google.maps.Map(document.getElementById("map"), mapOptions);
}
 
function recorddata(lat, lng, letter, address)
{
    col = 'F00'; 
    if (letter == 'Y')  col = '0F0'; 
    icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+letter+'|'+col+'|000'
    pos = new google.maps.LatLng(lat, lng); 
    text = 'text';
    content = address; 

    marker = new google.maps.Marker({position:pos,map:map,title:text, icon:icon});

    infowindow = new google.maps.InfoWindow({ content: content });
    (function(j) {
            google.maps.event.addListener(j.marker, "click", function(){
                                j.infowindow.open(map, j.marker); });
                 })({'marker':marker, 'infowindow':infowindow});
    if (!centreset)
        {  map.setCenter(pos); centreset = true }
}
"""


part2 = """
function loaddata() 
{
 
    for (i = 0; i < jdata.length; i++)
         recorddata(jdata[i][0], jdata[i][1], jdata[i][2], jdata[i][3]); 
}

$(function() { makemap(); loaddata(); });

</script> 
 
<p><img src="http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=Y|0F0|000" style="vertical-align: middle; padding: 0.5em;">Green pins have the s_ems_combined = yes.
<br>
<img src="http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=N|F00|000" style="vertical-align: middle; padding: 0.5em;">Red pins have s_ems_combined = no.</p>
 
<p>Source: <a href="http://data.edmonton.ca/DataBrowser/coe/FireStations#param=NOFILTER--DataView--Results">Edmonton Open Data Catalogue</a>
 
</body> 
</html>
 """
Main()
