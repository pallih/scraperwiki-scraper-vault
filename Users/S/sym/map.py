# template for setting 

# set the name of the scraper with the geodata in the datastore here
sourcescraper = 'adnams-pubs'

# (This is a large body of javascript in quotes)

    
# map icon function where you can control what type of image is in the pin to visualize your information
#   for more details, see http://code.google.com/apis/chart/docs/gallery/dynamic_icons.html
mapiconfunction = """
function mapicon(record)
{
    col = 'F00'; 
    if (record["Decision"] == "PENDING")
        col = '0F0'; 

    letter = 'O'; 
    if (record["Decision"] == "PENDING")
        letter = 'P'; 
     
    icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+letter+'|'+col+'|000'; 
    return icon
}

function mapicontext(record)
{
    return record["Reference_number"] 
}
 """

# the following uses the google map interface v3
#   see http://code.google.com/apis/chart/docs/gallery/dynamic_icons.html
header = """
<!DOCTYPE html> 
<html dir="ltr" lang="en"> 
    <head> 
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/> 
        <title>General Map Thing</title> 
       <style type="text/css" media="screen"> 
        * {margin:0;padding:0;}
        p{padding:1px;}
       </style> 
        <meta name="robots" content="index, follow" /> 
        <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script> 
        <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
    </head> 
    <body> 
        <h2 id="message">General Map Thing</h2> 
        <div id="map" style="width:700px;height:400px"></div> 
        <script type="text/javascript" charset="utf-8"> 
"""

mapsetup = """
var map; 
var centreset = false; 
function makemap()
{
 var mapOptions = {
                    "zoom": 5, "center": new google.maps.LatLng(55.500515, -4.128317), 
                    "mapTypeId": google.maps.MapTypeId.SATELLITE
                  };
    map = new google.maps.Map(document.getElementById("map"), mapOptions);
}
"""
 
 
loaddata = """
function recorddata(record)
{
        if (!record['latlng_lat'])
             return; 
        pos = new google.maps.LatLng(record['latlng_lat'], record['latlng_lng']); 
        text = mapicontext(record)
        icon = mapicon(record);
        marker = new google.maps.Marker({position:pos,map:map,title:text, icon:icon});

        content = '<a href="'+record['url']+'" target="_blank">'+text+'</a>'; 
        infowindow = new google.maps.InfoWindow({ content: content });
        (function(j) {
             google.maps.event.addListener(j.marker, "click", function(){
                                  j.infowindow.open(map, j.marker);
                              });
        })({'marker':marker, 'infowindow':infowindow});
        if (!centreset)
            {  map.setCenter(pos); centreset = true }
}

var olength = 500; 
var olimit = 100; 
var offset = 0; 
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
    url = "http://api.scraperwiki.com/api/1.0/datastore/getdata?&format=json&name="+scrapername+"&limit="+olength+"&callback=gotback&offset=" + offset;
 s.setAttribute('src', url);
    s.setAttribute('type', 'text/javascript');
    document.getElementsByTagName('head')[0].appendChild(s);
}"""


footer = """
$(function() { makemap(); loaddata(); });

</script> 
    </body> 
</html>"""

 
# use link: 
# http://scraperwiki.com/scrapers/rpcexecute/general-map-proof?function=html&year=1972
 
def html():
    print header
    print mapsetup
    print "var scrapername = '%s';" % sourcescraper 
    print mapiconfunction
    print loaddata
    print footer
 
html()# template for setting 

# set the name of the scraper with the geodata in the datastore here
sourcescraper = 'adnams-pubs'

# (This is a large body of javascript in quotes)

    
# map icon function where you can control what type of image is in the pin to visualize your information
#   for more details, see http://code.google.com/apis/chart/docs/gallery/dynamic_icons.html
mapiconfunction = """
function mapicon(record)
{
    col = 'F00'; 
    if (record["Decision"] == "PENDING")
        col = '0F0'; 

    letter = 'O'; 
    if (record["Decision"] == "PENDING")
        letter = 'P'; 
     
    icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+letter+'|'+col+'|000'; 
    return icon
}

function mapicontext(record)
{
    return record["Reference_number"] 
}
 """

# the following uses the google map interface v3
#   see http://code.google.com/apis/chart/docs/gallery/dynamic_icons.html
header = """
<!DOCTYPE html> 
<html dir="ltr" lang="en"> 
    <head> 
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/> 
        <title>General Map Thing</title> 
       <style type="text/css" media="screen"> 
        * {margin:0;padding:0;}
        p{padding:1px;}
       </style> 
        <meta name="robots" content="index, follow" /> 
        <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script> 
        <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
    </head> 
    <body> 
        <h2 id="message">General Map Thing</h2> 
        <div id="map" style="width:700px;height:400px"></div> 
        <script type="text/javascript" charset="utf-8"> 
"""

mapsetup = """
var map; 
var centreset = false; 
function makemap()
{
 var mapOptions = {
                    "zoom": 5, "center": new google.maps.LatLng(55.500515, -4.128317), 
                    "mapTypeId": google.maps.MapTypeId.SATELLITE
                  };
    map = new google.maps.Map(document.getElementById("map"), mapOptions);
}
"""
 
 
loaddata = """
function recorddata(record)
{
        if (!record['latlng_lat'])
             return; 
        pos = new google.maps.LatLng(record['latlng_lat'], record['latlng_lng']); 
        text = mapicontext(record)
        icon = mapicon(record);
        marker = new google.maps.Marker({position:pos,map:map,title:text, icon:icon});

        content = '<a href="'+record['url']+'" target="_blank">'+text+'</a>'; 
        infowindow = new google.maps.InfoWindow({ content: content });
        (function(j) {
             google.maps.event.addListener(j.marker, "click", function(){
                                  j.infowindow.open(map, j.marker);
                              });
        })({'marker':marker, 'infowindow':infowindow});
        if (!centreset)
            {  map.setCenter(pos); centreset = true }
}

var olength = 500; 
var olimit = 100; 
var offset = 0; 
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
    url = "http://api.scraperwiki.com/api/1.0/datastore/getdata?&format=json&name="+scrapername+"&limit="+olength+"&callback=gotback&offset=" + offset;
 s.setAttribute('src', url);
    s.setAttribute('type', 'text/javascript');
    document.getElementsByTagName('head')[0].appendChild(s);
}"""


footer = """
$(function() { makemap(); loaddata(); });

</script> 
    </body> 
</html>"""

 
# use link: 
# http://scraperwiki.com/scrapers/rpcexecute/general-map-proof?function=html&year=1972
 
def html():
    print header
    print mapsetup
    print "var scrapername = '%s';" % sourcescraper 
    print mapiconfunction
    print loaddata
    print footer
 
html()