import json
import urllib
import lxml.etree
import re
import scraperwiki
import math


incident_latlng = scraperwiki.geo.gb_postcode_to_latlng("B32 3NP")  # hardcoded
incident_latlng = scraperwiki.geo.gb_postcode_to_latlng("B15 2BJ")  # hardcoded

p = scraperwiki.geo.gb_postcode_to_latlng("B15 2BJ") # person
i = scraperwiki.geo.gb_postcode_to_latlng("B32 3NP") # incident

def WeightDist(m):
    i = incident_latlng
    v = m[0] - p[0], m[1] - p[1]
    d = i[0] - p[0], i[1] - p[1]
    vsq = v[0]*v[0] + v[1]*v[1] + 0.00001
    vlen = math.sqrt(vsq)
    a = abs((v[1]*d[0] - v[0]*d[1])/vlen + 0.000001)
    x1 = (d[0]*v[0] + d[1]*v[1])/vlen
    x2 = ((d[0]-v[0])*v[0] + (d[1]-v[1])*v[1])/vlen
    ix1 = math.log((x1 + math.sqrt(x1*x1 + a*a))/a)
    ix2 = math.log((x2 + math.sqrt(x2*x2 + a*a))/a)
    r = abs(ix2 - ix1)*0.1
    print r
    return r
    

def GetJData():
    musterstatus = { }
    scraperwiki.sqlite.attach('birmingham-leisure-centres')
    for data in scraperwiki.sqlite.select('* from `birmingham-leisure-centres`.swdata'):
        musterstatus[data.get('id')] = ["closed", 0, data]
    
    personlocs = { }
    donephones = set()
    
    scraperwiki.sqlite.attach('mustersms')
    alldata = list(scraperwiki.sqlite.select("* from mustersms.swdata"))
    for data in reversed(alldata):
        if data.get("musterid"):
            musterid = data.get("musterid")
            if musterid in musterstatus:
                musterstatus[musterid][0] = data.get("status", "closed")

    for data in alldata:
        phonenumber = data.get("phonenumber")
        if phonenumber:
            if phonenumber in donephones:
                continue
            else:
                donephones.add(phonenumber) 
        
        if data.get("mid"):
            #print data
            personmusterid = data.get("mid")
            if personmusterid in musterstatus:
                musterstatus[personmusterid][1] += 1
        if phonenumber:
            if data.get("latlng"):
                personlocs[phonenumber] = data.get("latlng")
            
    jdata = [ ]
    for status, count, data in musterstatus.values():
        latlng = data.get("latlng")
        if not latlng:
            continue
        #v = WeightDist(latlng)
        #b = max(0, min(15, int((v / 0.1)*15)))
        #col = "0123456789ABCDEF"[b] + "00"
        letter = "%d" % count
        col = (status == "open" and "0F0" or "F00")
            
        jdata.append((latlng[0], latlng[1], letter, col, "%s<br>[%s]" % (data.get("name"), data.get("id"))))

    for phone, latlng in personlocs.items():
        jdata.append((latlng[0], latlng[1], ":", '00F', "Phone: " + phone))

    jdata.append((incident_latlng[0], incident_latlng[1], "I", 'F0F', "Incident"))
    #jdata.append((p[0], p[1], "O", '00F', "stuff"))
    return jdata
                     
def Main():
    print part1
    print 'var jdata = %s;' % json.dumps(GetJData()) 
    print part2

part1 = """
<html dir="ltr" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <style type="text/css" media="screen">p{padding:1px;}</style>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
</head>
<body>

<h2>Muster directions</h2>
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
 
function recorddata(lat, lng, letter, col, address)
{
    icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+letter+'|'+col+'|000'
    pos = new google.maps.LatLng(lat, lng); 
    text = '';
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
         recorddata(jdata[i][0], jdata[i][1], jdata[i][2], jdata[i][3], jdata[i][4]); 
}

$(function() { makemap(); loaddata(); });

</script> 
 
<p><img src="http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=I|F0F|000" style="vertical-align: middle; padding: 0.5em;">The location of the incident.
<br>
<img src="http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=0|F00|000" style="vertical-align: middle; padding: 0.5em;">Red location of closed muster station.<br>
<img src="http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=0|0F0|000" style="vertical-align: middle; padding: 0.5em;">Green location of open muster station, with number of people directed to there.<br>
<img src="http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=:|00F|000" style="vertical-align: middle; padding: 0.5em;">Last known location of person.</p>
</p>
 
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
import math


incident_latlng = scraperwiki.geo.gb_postcode_to_latlng("B32 3NP")  # hardcoded
incident_latlng = scraperwiki.geo.gb_postcode_to_latlng("B15 2BJ")  # hardcoded

p = scraperwiki.geo.gb_postcode_to_latlng("B15 2BJ") # person
i = scraperwiki.geo.gb_postcode_to_latlng("B32 3NP") # incident

def WeightDist(m):
    i = incident_latlng
    v = m[0] - p[0], m[1] - p[1]
    d = i[0] - p[0], i[1] - p[1]
    vsq = v[0]*v[0] + v[1]*v[1] + 0.00001
    vlen = math.sqrt(vsq)
    a = abs((v[1]*d[0] - v[0]*d[1])/vlen + 0.000001)
    x1 = (d[0]*v[0] + d[1]*v[1])/vlen
    x2 = ((d[0]-v[0])*v[0] + (d[1]-v[1])*v[1])/vlen
    ix1 = math.log((x1 + math.sqrt(x1*x1 + a*a))/a)
    ix2 = math.log((x2 + math.sqrt(x2*x2 + a*a))/a)
    r = abs(ix2 - ix1)*0.1
    print r
    return r
    

def GetJData():
    musterstatus = { }
    scraperwiki.sqlite.attach('birmingham-leisure-centres')
    for data in scraperwiki.sqlite.select('* from `birmingham-leisure-centres`.swdata'):
        musterstatus[data.get('id')] = ["closed", 0, data]
    
    personlocs = { }
    donephones = set()
    
    scraperwiki.sqlite.attach('mustersms')
    alldata = list(scraperwiki.sqlite.select("* from mustersms.swdata"))
    for data in reversed(alldata):
        if data.get("musterid"):
            musterid = data.get("musterid")
            if musterid in musterstatus:
                musterstatus[musterid][0] = data.get("status", "closed")

    for data in alldata:
        phonenumber = data.get("phonenumber")
        if phonenumber:
            if phonenumber in donephones:
                continue
            else:
                donephones.add(phonenumber) 
        
        if data.get("mid"):
            #print data
            personmusterid = data.get("mid")
            if personmusterid in musterstatus:
                musterstatus[personmusterid][1] += 1
        if phonenumber:
            if data.get("latlng"):
                personlocs[phonenumber] = data.get("latlng")
            
    jdata = [ ]
    for status, count, data in musterstatus.values():
        latlng = data.get("latlng")
        if not latlng:
            continue
        #v = WeightDist(latlng)
        #b = max(0, min(15, int((v / 0.1)*15)))
        #col = "0123456789ABCDEF"[b] + "00"
        letter = "%d" % count
        col = (status == "open" and "0F0" or "F00")
            
        jdata.append((latlng[0], latlng[1], letter, col, "%s<br>[%s]" % (data.get("name"), data.get("id"))))

    for phone, latlng in personlocs.items():
        jdata.append((latlng[0], latlng[1], ":", '00F', "Phone: " + phone))

    jdata.append((incident_latlng[0], incident_latlng[1], "I", 'F0F', "Incident"))
    #jdata.append((p[0], p[1], "O", '00F', "stuff"))
    return jdata
                     
def Main():
    print part1
    print 'var jdata = %s;' % json.dumps(GetJData()) 
    print part2

part1 = """
<html dir="ltr" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <style type="text/css" media="screen">p{padding:1px;}</style>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
</head>
<body>

<h2>Muster directions</h2>
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
 
function recorddata(lat, lng, letter, col, address)
{
    icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+letter+'|'+col+'|000'
    pos = new google.maps.LatLng(lat, lng); 
    text = '';
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
         recorddata(jdata[i][0], jdata[i][1], jdata[i][2], jdata[i][3], jdata[i][4]); 
}

$(function() { makemap(); loaddata(); });

</script> 
 
<p><img src="http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=I|F0F|000" style="vertical-align: middle; padding: 0.5em;">The location of the incident.
<br>
<img src="http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=0|F00|000" style="vertical-align: middle; padding: 0.5em;">Red location of closed muster station.<br>
<img src="http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=0|0F0|000" style="vertical-align: middle; padding: 0.5em;">Green location of open muster station, with number of people directed to there.<br>
<img src="http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=:|00F|000" style="vertical-align: middle; padding: 0.5em;">Last known location of person.</p>
</p>
 
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
import math


incident_latlng = scraperwiki.geo.gb_postcode_to_latlng("B32 3NP")  # hardcoded
incident_latlng = scraperwiki.geo.gb_postcode_to_latlng("B15 2BJ")  # hardcoded

p = scraperwiki.geo.gb_postcode_to_latlng("B15 2BJ") # person
i = scraperwiki.geo.gb_postcode_to_latlng("B32 3NP") # incident

def WeightDist(m):
    i = incident_latlng
    v = m[0] - p[0], m[1] - p[1]
    d = i[0] - p[0], i[1] - p[1]
    vsq = v[0]*v[0] + v[1]*v[1] + 0.00001
    vlen = math.sqrt(vsq)
    a = abs((v[1]*d[0] - v[0]*d[1])/vlen + 0.000001)
    x1 = (d[0]*v[0] + d[1]*v[1])/vlen
    x2 = ((d[0]-v[0])*v[0] + (d[1]-v[1])*v[1])/vlen
    ix1 = math.log((x1 + math.sqrt(x1*x1 + a*a))/a)
    ix2 = math.log((x2 + math.sqrt(x2*x2 + a*a))/a)
    r = abs(ix2 - ix1)*0.1
    print r
    return r
    

def GetJData():
    musterstatus = { }
    scraperwiki.sqlite.attach('birmingham-leisure-centres')
    for data in scraperwiki.sqlite.select('* from `birmingham-leisure-centres`.swdata'):
        musterstatus[data.get('id')] = ["closed", 0, data]
    
    personlocs = { }
    donephones = set()
    
    scraperwiki.sqlite.attach('mustersms')
    alldata = list(scraperwiki.sqlite.select("* from mustersms.swdata"))
    for data in reversed(alldata):
        if data.get("musterid"):
            musterid = data.get("musterid")
            if musterid in musterstatus:
                musterstatus[musterid][0] = data.get("status", "closed")

    for data in alldata:
        phonenumber = data.get("phonenumber")
        if phonenumber:
            if phonenumber in donephones:
                continue
            else:
                donephones.add(phonenumber) 
        
        if data.get("mid"):
            #print data
            personmusterid = data.get("mid")
            if personmusterid in musterstatus:
                musterstatus[personmusterid][1] += 1
        if phonenumber:
            if data.get("latlng"):
                personlocs[phonenumber] = data.get("latlng")
            
    jdata = [ ]
    for status, count, data in musterstatus.values():
        latlng = data.get("latlng")
        if not latlng:
            continue
        #v = WeightDist(latlng)
        #b = max(0, min(15, int((v / 0.1)*15)))
        #col = "0123456789ABCDEF"[b] + "00"
        letter = "%d" % count
        col = (status == "open" and "0F0" or "F00")
            
        jdata.append((latlng[0], latlng[1], letter, col, "%s<br>[%s]" % (data.get("name"), data.get("id"))))

    for phone, latlng in personlocs.items():
        jdata.append((latlng[0], latlng[1], ":", '00F', "Phone: " + phone))

    jdata.append((incident_latlng[0], incident_latlng[1], "I", 'F0F', "Incident"))
    #jdata.append((p[0], p[1], "O", '00F', "stuff"))
    return jdata
                     
def Main():
    print part1
    print 'var jdata = %s;' % json.dumps(GetJData()) 
    print part2

part1 = """
<html dir="ltr" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <style type="text/css" media="screen">p{padding:1px;}</style>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
</head>
<body>

<h2>Muster directions</h2>
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
 
function recorddata(lat, lng, letter, col, address)
{
    icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+letter+'|'+col+'|000'
    pos = new google.maps.LatLng(lat, lng); 
    text = '';
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
         recorddata(jdata[i][0], jdata[i][1], jdata[i][2], jdata[i][3], jdata[i][4]); 
}

$(function() { makemap(); loaddata(); });

</script> 
 
<p><img src="http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=I|F0F|000" style="vertical-align: middle; padding: 0.5em;">The location of the incident.
<br>
<img src="http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=0|F00|000" style="vertical-align: middle; padding: 0.5em;">Red location of closed muster station.<br>
<img src="http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=0|0F0|000" style="vertical-align: middle; padding: 0.5em;">Green location of open muster station, with number of people directed to there.<br>
<img src="http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=:|00F|000" style="vertical-align: middle; padding: 0.5em;">Last known location of person.</p>
</p>
 
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
import math


incident_latlng = scraperwiki.geo.gb_postcode_to_latlng("B32 3NP")  # hardcoded
incident_latlng = scraperwiki.geo.gb_postcode_to_latlng("B15 2BJ")  # hardcoded

p = scraperwiki.geo.gb_postcode_to_latlng("B15 2BJ") # person
i = scraperwiki.geo.gb_postcode_to_latlng("B32 3NP") # incident

def WeightDist(m):
    i = incident_latlng
    v = m[0] - p[0], m[1] - p[1]
    d = i[0] - p[0], i[1] - p[1]
    vsq = v[0]*v[0] + v[1]*v[1] + 0.00001
    vlen = math.sqrt(vsq)
    a = abs((v[1]*d[0] - v[0]*d[1])/vlen + 0.000001)
    x1 = (d[0]*v[0] + d[1]*v[1])/vlen
    x2 = ((d[0]-v[0])*v[0] + (d[1]-v[1])*v[1])/vlen
    ix1 = math.log((x1 + math.sqrt(x1*x1 + a*a))/a)
    ix2 = math.log((x2 + math.sqrt(x2*x2 + a*a))/a)
    r = abs(ix2 - ix1)*0.1
    print r
    return r
    

def GetJData():
    musterstatus = { }
    scraperwiki.sqlite.attach('birmingham-leisure-centres')
    for data in scraperwiki.sqlite.select('* from `birmingham-leisure-centres`.swdata'):
        musterstatus[data.get('id')] = ["closed", 0, data]
    
    personlocs = { }
    donephones = set()
    
    scraperwiki.sqlite.attach('mustersms')
    alldata = list(scraperwiki.sqlite.select("* from mustersms.swdata"))
    for data in reversed(alldata):
        if data.get("musterid"):
            musterid = data.get("musterid")
            if musterid in musterstatus:
                musterstatus[musterid][0] = data.get("status", "closed")

    for data in alldata:
        phonenumber = data.get("phonenumber")
        if phonenumber:
            if phonenumber in donephones:
                continue
            else:
                donephones.add(phonenumber) 
        
        if data.get("mid"):
            #print data
            personmusterid = data.get("mid")
            if personmusterid in musterstatus:
                musterstatus[personmusterid][1] += 1
        if phonenumber:
            if data.get("latlng"):
                personlocs[phonenumber] = data.get("latlng")
            
    jdata = [ ]
    for status, count, data in musterstatus.values():
        latlng = data.get("latlng")
        if not latlng:
            continue
        #v = WeightDist(latlng)
        #b = max(0, min(15, int((v / 0.1)*15)))
        #col = "0123456789ABCDEF"[b] + "00"
        letter = "%d" % count
        col = (status == "open" and "0F0" or "F00")
            
        jdata.append((latlng[0], latlng[1], letter, col, "%s<br>[%s]" % (data.get("name"), data.get("id"))))

    for phone, latlng in personlocs.items():
        jdata.append((latlng[0], latlng[1], ":", '00F', "Phone: " + phone))

    jdata.append((incident_latlng[0], incident_latlng[1], "I", 'F0F', "Incident"))
    #jdata.append((p[0], p[1], "O", '00F', "stuff"))
    return jdata
                     
def Main():
    print part1
    print 'var jdata = %s;' % json.dumps(GetJData()) 
    print part2

part1 = """
<html dir="ltr" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <style type="text/css" media="screen">p{padding:1px;}</style>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
</head>
<body>

<h2>Muster directions</h2>
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
 
function recorddata(lat, lng, letter, col, address)
{
    icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+letter+'|'+col+'|000'
    pos = new google.maps.LatLng(lat, lng); 
    text = '';
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
         recorddata(jdata[i][0], jdata[i][1], jdata[i][2], jdata[i][3], jdata[i][4]); 
}

$(function() { makemap(); loaddata(); });

</script> 
 
<p><img src="http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=I|F0F|000" style="vertical-align: middle; padding: 0.5em;">The location of the incident.
<br>
<img src="http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=0|F00|000" style="vertical-align: middle; padding: 0.5em;">Red location of closed muster station.<br>
<img src="http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=0|0F0|000" style="vertical-align: middle; padding: 0.5em;">Green location of open muster station, with number of people directed to there.<br>
<img src="http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=:|00F|000" style="vertical-align: middle; padding: 0.5em;">Last known location of person.</p>
</p>
 
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
import math


incident_latlng = scraperwiki.geo.gb_postcode_to_latlng("B32 3NP")  # hardcoded
incident_latlng = scraperwiki.geo.gb_postcode_to_latlng("B15 2BJ")  # hardcoded

p = scraperwiki.geo.gb_postcode_to_latlng("B15 2BJ") # person
i = scraperwiki.geo.gb_postcode_to_latlng("B32 3NP") # incident

def WeightDist(m):
    i = incident_latlng
    v = m[0] - p[0], m[1] - p[1]
    d = i[0] - p[0], i[1] - p[1]
    vsq = v[0]*v[0] + v[1]*v[1] + 0.00001
    vlen = math.sqrt(vsq)
    a = abs((v[1]*d[0] - v[0]*d[1])/vlen + 0.000001)
    x1 = (d[0]*v[0] + d[1]*v[1])/vlen
    x2 = ((d[0]-v[0])*v[0] + (d[1]-v[1])*v[1])/vlen
    ix1 = math.log((x1 + math.sqrt(x1*x1 + a*a))/a)
    ix2 = math.log((x2 + math.sqrt(x2*x2 + a*a))/a)
    r = abs(ix2 - ix1)*0.1
    print r
    return r
    

def GetJData():
    musterstatus = { }
    scraperwiki.sqlite.attach('birmingham-leisure-centres')
    for data in scraperwiki.sqlite.select('* from `birmingham-leisure-centres`.swdata'):
        musterstatus[data.get('id')] = ["closed", 0, data]
    
    personlocs = { }
    donephones = set()
    
    scraperwiki.sqlite.attach('mustersms')
    alldata = list(scraperwiki.sqlite.select("* from mustersms.swdata"))
    for data in reversed(alldata):
        if data.get("musterid"):
            musterid = data.get("musterid")
            if musterid in musterstatus:
                musterstatus[musterid][0] = data.get("status", "closed")

    for data in alldata:
        phonenumber = data.get("phonenumber")
        if phonenumber:
            if phonenumber in donephones:
                continue
            else:
                donephones.add(phonenumber) 
        
        if data.get("mid"):
            #print data
            personmusterid = data.get("mid")
            if personmusterid in musterstatus:
                musterstatus[personmusterid][1] += 1
        if phonenumber:
            if data.get("latlng"):
                personlocs[phonenumber] = data.get("latlng")
            
    jdata = [ ]
    for status, count, data in musterstatus.values():
        latlng = data.get("latlng")
        if not latlng:
            continue
        #v = WeightDist(latlng)
        #b = max(0, min(15, int((v / 0.1)*15)))
        #col = "0123456789ABCDEF"[b] + "00"
        letter = "%d" % count
        col = (status == "open" and "0F0" or "F00")
            
        jdata.append((latlng[0], latlng[1], letter, col, "%s<br>[%s]" % (data.get("name"), data.get("id"))))

    for phone, latlng in personlocs.items():
        jdata.append((latlng[0], latlng[1], ":", '00F', "Phone: " + phone))

    jdata.append((incident_latlng[0], incident_latlng[1], "I", 'F0F', "Incident"))
    #jdata.append((p[0], p[1], "O", '00F', "stuff"))
    return jdata
                     
def Main():
    print part1
    print 'var jdata = %s;' % json.dumps(GetJData()) 
    print part2

part1 = """
<html dir="ltr" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <style type="text/css" media="screen">p{padding:1px;}</style>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
</head>
<body>

<h2>Muster directions</h2>
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
 
function recorddata(lat, lng, letter, col, address)
{
    icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+letter+'|'+col+'|000'
    pos = new google.maps.LatLng(lat, lng); 
    text = '';
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
         recorddata(jdata[i][0], jdata[i][1], jdata[i][2], jdata[i][3], jdata[i][4]); 
}

$(function() { makemap(); loaddata(); });

</script> 
 
<p><img src="http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=I|F0F|000" style="vertical-align: middle; padding: 0.5em;">The location of the incident.
<br>
<img src="http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=0|F00|000" style="vertical-align: middle; padding: 0.5em;">Red location of closed muster station.<br>
<img src="http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=0|0F0|000" style="vertical-align: middle; padding: 0.5em;">Green location of open muster station, with number of people directed to there.<br>
<img src="http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=:|00F|000" style="vertical-align: middle; padding: 0.5em;">Last known location of person.</p>
</p>
 
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
import math


incident_latlng = scraperwiki.geo.gb_postcode_to_latlng("B32 3NP")  # hardcoded
incident_latlng = scraperwiki.geo.gb_postcode_to_latlng("B15 2BJ")  # hardcoded

p = scraperwiki.geo.gb_postcode_to_latlng("B15 2BJ") # person
i = scraperwiki.geo.gb_postcode_to_latlng("B32 3NP") # incident

def WeightDist(m):
    i = incident_latlng
    v = m[0] - p[0], m[1] - p[1]
    d = i[0] - p[0], i[1] - p[1]
    vsq = v[0]*v[0] + v[1]*v[1] + 0.00001
    vlen = math.sqrt(vsq)
    a = abs((v[1]*d[0] - v[0]*d[1])/vlen + 0.000001)
    x1 = (d[0]*v[0] + d[1]*v[1])/vlen
    x2 = ((d[0]-v[0])*v[0] + (d[1]-v[1])*v[1])/vlen
    ix1 = math.log((x1 + math.sqrt(x1*x1 + a*a))/a)
    ix2 = math.log((x2 + math.sqrt(x2*x2 + a*a))/a)
    r = abs(ix2 - ix1)*0.1
    print r
    return r
    

def GetJData():
    musterstatus = { }
    scraperwiki.sqlite.attach('birmingham-leisure-centres')
    for data in scraperwiki.sqlite.select('* from `birmingham-leisure-centres`.swdata'):
        musterstatus[data.get('id')] = ["closed", 0, data]
    
    personlocs = { }
    donephones = set()
    
    scraperwiki.sqlite.attach('mustersms')
    alldata = list(scraperwiki.sqlite.select("* from mustersms.swdata"))
    for data in reversed(alldata):
        if data.get("musterid"):
            musterid = data.get("musterid")
            if musterid in musterstatus:
                musterstatus[musterid][0] = data.get("status", "closed")

    for data in alldata:
        phonenumber = data.get("phonenumber")
        if phonenumber:
            if phonenumber in donephones:
                continue
            else:
                donephones.add(phonenumber) 
        
        if data.get("mid"):
            #print data
            personmusterid = data.get("mid")
            if personmusterid in musterstatus:
                musterstatus[personmusterid][1] += 1
        if phonenumber:
            if data.get("latlng"):
                personlocs[phonenumber] = data.get("latlng")
            
    jdata = [ ]
    for status, count, data in musterstatus.values():
        latlng = data.get("latlng")
        if not latlng:
            continue
        #v = WeightDist(latlng)
        #b = max(0, min(15, int((v / 0.1)*15)))
        #col = "0123456789ABCDEF"[b] + "00"
        letter = "%d" % count
        col = (status == "open" and "0F0" or "F00")
            
        jdata.append((latlng[0], latlng[1], letter, col, "%s<br>[%s]" % (data.get("name"), data.get("id"))))

    for phone, latlng in personlocs.items():
        jdata.append((latlng[0], latlng[1], ":", '00F', "Phone: " + phone))

    jdata.append((incident_latlng[0], incident_latlng[1], "I", 'F0F', "Incident"))
    #jdata.append((p[0], p[1], "O", '00F', "stuff"))
    return jdata
                     
def Main():
    print part1
    print 'var jdata = %s;' % json.dumps(GetJData()) 
    print part2

part1 = """
<html dir="ltr" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <style type="text/css" media="screen">p{padding:1px;}</style>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
</head>
<body>

<h2>Muster directions</h2>
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
 
function recorddata(lat, lng, letter, col, address)
{
    icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+letter+'|'+col+'|000'
    pos = new google.maps.LatLng(lat, lng); 
    text = '';
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
         recorddata(jdata[i][0], jdata[i][1], jdata[i][2], jdata[i][3], jdata[i][4]); 
}

$(function() { makemap(); loaddata(); });

</script> 
 
<p><img src="http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=I|F0F|000" style="vertical-align: middle; padding: 0.5em;">The location of the incident.
<br>
<img src="http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=0|F00|000" style="vertical-align: middle; padding: 0.5em;">Red location of closed muster station.<br>
<img src="http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=0|0F0|000" style="vertical-align: middle; padding: 0.5em;">Green location of open muster station, with number of people directed to there.<br>
<img src="http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=:|00F|000" style="vertical-align: middle; padding: 0.5em;">Last known location of person.</p>
</p>
 
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
import math


incident_latlng = scraperwiki.geo.gb_postcode_to_latlng("B32 3NP")  # hardcoded
incident_latlng = scraperwiki.geo.gb_postcode_to_latlng("B15 2BJ")  # hardcoded

p = scraperwiki.geo.gb_postcode_to_latlng("B15 2BJ") # person
i = scraperwiki.geo.gb_postcode_to_latlng("B32 3NP") # incident

def WeightDist(m):
    i = incident_latlng
    v = m[0] - p[0], m[1] - p[1]
    d = i[0] - p[0], i[1] - p[1]
    vsq = v[0]*v[0] + v[1]*v[1] + 0.00001
    vlen = math.sqrt(vsq)
    a = abs((v[1]*d[0] - v[0]*d[1])/vlen + 0.000001)
    x1 = (d[0]*v[0] + d[1]*v[1])/vlen
    x2 = ((d[0]-v[0])*v[0] + (d[1]-v[1])*v[1])/vlen
    ix1 = math.log((x1 + math.sqrt(x1*x1 + a*a))/a)
    ix2 = math.log((x2 + math.sqrt(x2*x2 + a*a))/a)
    r = abs(ix2 - ix1)*0.1
    print r
    return r
    

def GetJData():
    musterstatus = { }
    scraperwiki.sqlite.attach('birmingham-leisure-centres')
    for data in scraperwiki.sqlite.select('* from `birmingham-leisure-centres`.swdata'):
        musterstatus[data.get('id')] = ["closed", 0, data]
    
    personlocs = { }
    donephones = set()
    
    scraperwiki.sqlite.attach('mustersms')
    alldata = list(scraperwiki.sqlite.select("* from mustersms.swdata"))
    for data in reversed(alldata):
        if data.get("musterid"):
            musterid = data.get("musterid")
            if musterid in musterstatus:
                musterstatus[musterid][0] = data.get("status", "closed")

    for data in alldata:
        phonenumber = data.get("phonenumber")
        if phonenumber:
            if phonenumber in donephones:
                continue
            else:
                donephones.add(phonenumber) 
        
        if data.get("mid"):
            #print data
            personmusterid = data.get("mid")
            if personmusterid in musterstatus:
                musterstatus[personmusterid][1] += 1
        if phonenumber:
            if data.get("latlng"):
                personlocs[phonenumber] = data.get("latlng")
            
    jdata = [ ]
    for status, count, data in musterstatus.values():
        latlng = data.get("latlng")
        if not latlng:
            continue
        #v = WeightDist(latlng)
        #b = max(0, min(15, int((v / 0.1)*15)))
        #col = "0123456789ABCDEF"[b] + "00"
        letter = "%d" % count
        col = (status == "open" and "0F0" or "F00")
            
        jdata.append((latlng[0], latlng[1], letter, col, "%s<br>[%s]" % (data.get("name"), data.get("id"))))

    for phone, latlng in personlocs.items():
        jdata.append((latlng[0], latlng[1], ":", '00F', "Phone: " + phone))

    jdata.append((incident_latlng[0], incident_latlng[1], "I", 'F0F', "Incident"))
    #jdata.append((p[0], p[1], "O", '00F', "stuff"))
    return jdata
                     
def Main():
    print part1
    print 'var jdata = %s;' % json.dumps(GetJData()) 
    print part2

part1 = """
<html dir="ltr" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <style type="text/css" media="screen">p{padding:1px;}</style>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
</head>
<body>

<h2>Muster directions</h2>
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
 
function recorddata(lat, lng, letter, col, address)
{
    icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+letter+'|'+col+'|000'
    pos = new google.maps.LatLng(lat, lng); 
    text = '';
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
         recorddata(jdata[i][0], jdata[i][1], jdata[i][2], jdata[i][3], jdata[i][4]); 
}

$(function() { makemap(); loaddata(); });

</script> 
 
<p><img src="http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=I|F0F|000" style="vertical-align: middle; padding: 0.5em;">The location of the incident.
<br>
<img src="http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=0|F00|000" style="vertical-align: middle; padding: 0.5em;">Red location of closed muster station.<br>
<img src="http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=0|0F0|000" style="vertical-align: middle; padding: 0.5em;">Green location of open muster station, with number of people directed to there.<br>
<img src="http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=:|00F|000" style="vertical-align: middle; padding: 0.5em;">Last known location of person.</p>
</p>
 
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
import math


incident_latlng = scraperwiki.geo.gb_postcode_to_latlng("B32 3NP")  # hardcoded
incident_latlng = scraperwiki.geo.gb_postcode_to_latlng("B15 2BJ")  # hardcoded

p = scraperwiki.geo.gb_postcode_to_latlng("B15 2BJ") # person
i = scraperwiki.geo.gb_postcode_to_latlng("B32 3NP") # incident

def WeightDist(m):
    i = incident_latlng
    v = m[0] - p[0], m[1] - p[1]
    d = i[0] - p[0], i[1] - p[1]
    vsq = v[0]*v[0] + v[1]*v[1] + 0.00001
    vlen = math.sqrt(vsq)
    a = abs((v[1]*d[0] - v[0]*d[1])/vlen + 0.000001)
    x1 = (d[0]*v[0] + d[1]*v[1])/vlen
    x2 = ((d[0]-v[0])*v[0] + (d[1]-v[1])*v[1])/vlen
    ix1 = math.log((x1 + math.sqrt(x1*x1 + a*a))/a)
    ix2 = math.log((x2 + math.sqrt(x2*x2 + a*a))/a)
    r = abs(ix2 - ix1)*0.1
    print r
    return r
    

def GetJData():
    musterstatus = { }
    scraperwiki.sqlite.attach('birmingham-leisure-centres')
    for data in scraperwiki.sqlite.select('* from `birmingham-leisure-centres`.swdata'):
        musterstatus[data.get('id')] = ["closed", 0, data]
    
    personlocs = { }
    donephones = set()
    
    scraperwiki.sqlite.attach('mustersms')
    alldata = list(scraperwiki.sqlite.select("* from mustersms.swdata"))
    for data in reversed(alldata):
        if data.get("musterid"):
            musterid = data.get("musterid")
            if musterid in musterstatus:
                musterstatus[musterid][0] = data.get("status", "closed")

    for data in alldata:
        phonenumber = data.get("phonenumber")
        if phonenumber:
            if phonenumber in donephones:
                continue
            else:
                donephones.add(phonenumber) 
        
        if data.get("mid"):
            #print data
            personmusterid = data.get("mid")
            if personmusterid in musterstatus:
                musterstatus[personmusterid][1] += 1
        if phonenumber:
            if data.get("latlng"):
                personlocs[phonenumber] = data.get("latlng")
            
    jdata = [ ]
    for status, count, data in musterstatus.values():
        latlng = data.get("latlng")
        if not latlng:
            continue
        #v = WeightDist(latlng)
        #b = max(0, min(15, int((v / 0.1)*15)))
        #col = "0123456789ABCDEF"[b] + "00"
        letter = "%d" % count
        col = (status == "open" and "0F0" or "F00")
            
        jdata.append((latlng[0], latlng[1], letter, col, "%s<br>[%s]" % (data.get("name"), data.get("id"))))

    for phone, latlng in personlocs.items():
        jdata.append((latlng[0], latlng[1], ":", '00F', "Phone: " + phone))

    jdata.append((incident_latlng[0], incident_latlng[1], "I", 'F0F', "Incident"))
    #jdata.append((p[0], p[1], "O", '00F', "stuff"))
    return jdata
                     
def Main():
    print part1
    print 'var jdata = %s;' % json.dumps(GetJData()) 
    print part2

part1 = """
<html dir="ltr" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <style type="text/css" media="screen">p{padding:1px;}</style>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
</head>
<body>

<h2>Muster directions</h2>
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
 
function recorddata(lat, lng, letter, col, address)
{
    icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+letter+'|'+col+'|000'
    pos = new google.maps.LatLng(lat, lng); 
    text = '';
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
         recorddata(jdata[i][0], jdata[i][1], jdata[i][2], jdata[i][3], jdata[i][4]); 
}

$(function() { makemap(); loaddata(); });

</script> 
 
<p><img src="http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=I|F0F|000" style="vertical-align: middle; padding: 0.5em;">The location of the incident.
<br>
<img src="http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=0|F00|000" style="vertical-align: middle; padding: 0.5em;">Red location of closed muster station.<br>
<img src="http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=0|0F0|000" style="vertical-align: middle; padding: 0.5em;">Green location of open muster station, with number of people directed to there.<br>
<img src="http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=:|00F|000" style="vertical-align: middle; padding: 0.5em;">Last known location of person.</p>
</p>
 
<p>Source: <a href="http://data.edmonton.ca/DataBrowser/coe/FireStations#param=NOFILTER--DataView--Results">Edmonton Open Data Catalogue</a>
 
</body> 
</html>
 """
Main()
