<html dir="ltr" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>General Map Thing</title>
    <style type="text/css" media="screen">p{padding:1px;}</style>
    <script type="text/javascript" src="//maps.google.com/maps/api/js?sensor=false"></script>
    <script type="text/javascript" src="//ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
</head>

<body>

    <h2>Map of Dublin Bus lines from <span id="scrapername">...</span> <em id="message">...</em> <span id="processed"></span></h2>
<div id="map" style="width:100%;height:400px"></div>

<script type="text/javascript" charset="utf-8">
// ####################################################################
// Start of javascript code.  You should edit the functions below 
// so that your map expresses the particular contents of the data
// ####################################################################
    
var sourcescraper = 'dublinbusschedule';
$('#scrapername').html('<b>'+sourcescraper+'</b>'); 

var map; 
var centreset = false; 

function makemap()
{
    var mapOptions = { "zoom": 12, "center": new google.maps.LatLng(53.346452, -6.188049), 
                       "mapTypeId": google.maps.MapTypeId.ROADMAP };
    map = new google.maps.Map(document.getElementById("map"), mapOptions);
}

var colors = [ '#F0F8FF', '#00FFFF', '#7FFFD4', '#F0FFFF', '#FFEBCD', '#0000FF', '#8A2BE2', '#A52A2A', '#DEB887', '#5F9EA0', '#7FFF00', '#D2691E', '#FF7F50', '#6495ED', '#FFF8DC', '#DC143C', '#00FFFF','#00008B', '#008B8B', '#B8860B', '#A9A9A9', '#006400', '#BDB76B', '#8B008B', '#556B2F', '#FF8C00', '#9932CC', '#8B0000', '#E9967A', '#8FBC8F', '#483D8B', '#2F4F4F', '#00CED1', '#9400D3', '#FF1493', '#00BFFF', '#696969', '#1E90FF', '#B22222', '#FFFAF0', '#228B22', '#FF00FF', '#DCDCDC', '#FFD700', '#DAA520', '#808080', '#008000', '#ADFF2F', '#F0FFF0', '#FF69B4', '#CD5C5C', '#4B0082', '#FFFFF0', '#F0E68C', '#E6E6FA', '#FFF0F5', '#7CFC00', '#FFFACD', '#ADD8E6', '#F08080', '#E0FFFF', '#FAFAD2', '#90EE90', '#D3D3D3', '#FFB6C1', '#FFA07A', '#20B2AA', '#87CEFA', '#778899', '#B0C4DE', '#FFFFE0', '#00FF00', '#32CD32', '#FAF0E6', '#FF00FF', '#800000', '#66CDAA', '#0000CD', '#BA55D3', '#9370DB', '#3CB371', '#7B68EE', '#00FA9A', '#48D1CC', '#C71585', '#191970', '#F5FFFA', '#FFE4E1', '#FFE4B5', '#FFDEAD', '#000080', '#FDF5E6', '#808000', '#6B8E23', '#FFA500', '#FF4500', '#DA70D6', '#EEE8AA', '#98FB98', '#AFEEEE', '#DB7093', '#FFEFD5', '#FFDAB9', '#CD853F', '#FFC0CB', '#DDA0DD', '#B0E0E6', '#800080', '#FF0000', '#BC8F8F', '#4169E1', '#8B4513', '#FA8072', '#F4A460', '#2E8B57', '#FFF5EE', '#A0522D', '#C0C0C0', '#87CEEB', '#6A5ACD', '#708090', '#FFFAFA', '#00FF7F', '#4682B4', '#D2B48C', '#008080', '#D8BFD8', '#FF6347', '#40E0D0', '#EE82EE', '#F5DEB3', '#F5F5F5', '#FFFF00', '#9ACD32' ];

var markerSize = new google.maps.Size(32, 32, 'px', 'px');
var markerUrl = '//chart.apis.google.com/chart?chst=d_map_spin&chld=0.5|0|';

function recorddata(record, i)
{
    //$('#processed').append(record['busNumber'] + ' ');
    num = 0;

    if (!('stops' in record))
        return;
    
    var stops = record['stops'].split(',');
    var linePoints = [];
    
    for (j in stops) {
        var stopPos = stops[j].split('|');
        var pos = new google.maps.LatLng(parseFloat(stopPos[0]), parseFloat(stopPos[1]));
        linePoints.push(pos);
        if (num++ % 15 == 0) {
            var marker = new google.maps.Marker({ position: pos,
                                                  map:map,
                                                  title:record['busNumber'] + ' from ' + record['from'] + ' to ' + record['to'],
                                                  flat: true});
            marker.setIcon(new google.maps.MarkerImage(markerUrl + colors[i % colors.length].substring(1) + '|10|_|' + record['busNumber']));
        }
        /*var infowindow = new google.maps.InfoWindow({ content: record['busNumber'] });
          google.maps.event.addListener(marker, "click", function() { infowindow.open(map, marker); });*/
    }
    
    busLine = new google.maps.Polyline({
        path: linePoints,
        strokeColor: colors[i % colors.length],
        strokeOpacity: 1.0,
        strokeWeight: 3
    });
    busLine.setMap(map);
}

var olength = 60; 
var olimit = 20; 
var offset = 150;

function gotback(r) 
{
    for (i = 0; i < r.length; i++)
        recorddata(r[i], i); 

    $("#message").html("Total records=" + r.length); 
}

function loaddata() 
{
    $("#message").html("Loading ...");
    $.ajax({
      url:  'https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=' + sourcescraper + '&query=select%20*%20from%20swdata',
      dataType: 'json',
      success: function(data){ gotback(data); }
    }); 
}

$(function() { makemap(); loaddata(); });

</script> 
</body>
</html>