<html dir="ltr" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>NORDKLIM Map</title>
    <style type="text/css" media="screen">p{padding:1px;}</style>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.6.2/jquery.min.js"></script>
</head>

<body>

<h2>Map of <span id="scrapername">...</span> <em id="message">...</em></h2>
<div id="map" style="width:100%;height:500px"></div>
<ul>
    <li><img src="http://chart.apis.google.com/chart?chst=d_map_xpin_letter&chld=pin|O|0F0|000|CC3" />40 years of mean temperatures or more;</li>
    <li><img src="http://chart.apis.google.com/chart?chst=d_map_xpin_letter&amp;chld=pin_star|O|0F0|000|CC3" />100 years of mean temperatures or more;</li>
    <li><img src="http://chart.apis.google.com/chart?chst=d_map_xpin_letter&chld=pin|O|555|000|CC3" />no mean temperatures;</li>
</ul>

<script type="text/javascript" charset="utf-8">
   
var sourcescraper = 'nordklim-weather-stations';
$('#scrapername').html('<b>'+sourcescraper+'</b>'); 
    
// ####################################################################
// Set the dynamic icon for your point.  For more see: 
// http://code.google.com/apis/chart/docs/gallery/dynamic_icons.html
// ####################################################################
function mapicon(record)
{
    var col = '555';
    var l;
    var pinstyle = 'pin';

    if(record.tmeanyearmin) {
        l = record.tmeanyearmax - record.tmeanyearmin + 1;
        if(l >= 40) {
            col = '0F0';
        } else if(l >= 20) {
            col = 'C50';
        } else {
            col = 'C00';
        }
        if(l >= 100) {
            pinstyle = 'pin_star'
        }
    }
    letter = 'O';
     
    icon = 'http://chart.apis.google.com/chart?chst=d_map_xpin_letter' +
      '&chld='+pinstyle+'|'+letter+'|'+col+'|000|CC3';
    return icon
}

// ####################################################################
// Set the tooltip title value
// ####################################################################
function mapicontext(record)
{
    return record['name'];
}

// ####################################################################
// Set the popup text for your pin, usually with the link
// ####################################################################
function mapicontent(record)
{
    var s;

    s = '<p>' + record.name + '</p><p>' + record.id + '</p>';
    if(record.tmeanyearmin) {
      s += '<p>' + record.tmeanyearmin + ' to ' +
        record.tmeanyearmax + '</p>'
    }
    return s
}

var map; 
var centreset = true; 
function makemap()
{
    var mapOptions = { "zoom": 3, "center": new google.maps.LatLng(70, 4), 
                    "mapTypeId": google.maps.MapTypeId.SATELLITE };
    map = new google.maps.Map(document.getElementById("map"), mapOptions);
}
 
function recorddata(record)
{
    if (record.latitude === undefined)
        return; 
    pos = new google.maps.LatLng(record.latitude, record.longitude); 

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
var olimit = 2000; 
var offset = 0;    
function gotback(r) 
{
    for (i = 0; i < r.length; i++)
        recorddata(r[i]); 

    if ((r.length == olength) && (offset < olimit)) {
        $("#message").html("records=" + (offset + r.length)); 
        offset += olength; 
        loaddata(); 
    } else {
        $("#message").html("Total records=" + (offset + r.length)); 
    }
}

function loaddata() 
{
    var s = document.createElement('script');
    var url = "http://api.scraperwiki.com/api/1.0/datastore/getdata?&format=json&name="+sourcescraper +
      "&limit="+olength+"&offset=" + offset;
    $.ajax({url:url, success:gotback, dataType:'jsonp'}).error(function(){alert("error");});
}

$(function() { makemap(); loaddata(); });

</script> 
</body> 
</html>
