<!--
--   The opens up in a new window, showing a map of EU's capitals, centred on ScraperWiki HQ in Rome
-->

<!--
We could always change the map’s central spot, zoom level, or style later using something like this:
var pos = new google.maps.LatLng(52.11249, -2.61793);
map.setCenter(pos);
map.setZoom(2);
map.setMapTypeId('TERRAIN');
-->

<!--
Adding a marker at a specific point is just as easy, all you need is a latitude and a longitude:
var pos = new google.maps.LatLng(52.11249, -2.61793);
var marker = new google.maps.Marker({position:pos, map:map, animation: google.maps.Animation.DROP, title:"OHAI!"});
-->

<!DOCTYPE html>
<html>
    <head>
        <title>UE capitals</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
        <meta charset="UTF-8">

        <!-- This CSS makes the map fill the whole window: -->
        <style type="text/css">
            html, body, #map_canvas {
                margin: 0;
                padding: 0;
                height: 100%;
            }
        </style>

        <!-- Following two <script> tags pull in the Google Maps Javascript library (required to make the map),
             and the jQuery javascript library (will come in useful later) -->
        <script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?sensor=false"></script>
        <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.7/jquery.min.js"></script>


        <script type="text/javascript">
/*
MAPPA VUOTA
Options include:
- the default zoom level
- the location coordinates
- the style of map we’d like to see (ROADMAP | SATELLITE | HYBRID | TERRAIN)

var map;
$(function(){
    var myOptions = {
        zoom: 7,
        center: new google.maps.LatLng(53.405092, -2.969876),
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    map = new google.maps.Map(document.getElementById('map_canvas'), myOptions);
});
*/


/*
// The drop_markers() function takes our data points, extracts the latitude and longitude information from each,
// and plots those points on the map. It then resizes the map to make sure all the points fit on at the same time.
function drop_markers(data){
    bounds = new google.maps.LatLngBounds();
    for(i = 0; i < data.length; i++){
        myLatLng = new google.maps.LatLng(data[i].latitude, data[i].longitude);
        markerOptions = {position: myLatLng, map: map, title: data[i].name};
        new google.maps.Marker(markerOptions);
        bounds.extend(myLatLng);
        map.fitBounds(bounds);
    }
}
*/

// Scandisce l'elenco dei record recuperati e per ognuno 
// invoca il metodo che posiziona sulla mappa un marker
function drop_markers(data){
    bounds = new google.maps.LatLngBounds();
    geocoder = new google.maps.Geocoder();
    for(i = 0; i < data.length; i++){
        codeAddress(data[i]);
    }
}

// Introduce un marker per la capitale corrente risolvendo l'indirizzo (nome della citta') in un oggetto location.
// Per ogni marker aggiunto corregge i limiti della mappa per includerlo dentro.
function codeAddress(record) {
    bounds = new google.maps.LatLngBounds();
    geocoder = new google.maps.Geocoder();
    geocoder.geocode( { 'address': record.capitale}, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
        var myOptions = {
            map: map,
            position: results[0].geometry.location,
            title: record.capitale+' ('+record.country+')'
        }
        var marker = new google.maps.Marker(myOptions);
        bounds.extend(results[0].geometry.location);
        map.fitBounds(bounds);
      }
    });
}

/*** Variabili globali  ***/
// La mappa
var map;
// Le opzioni della mappa
var myOptions = {
    zoom: 4,
    center: new google.maps.LatLng(41.920673, 12.48024),  // Centra la mappa su Roma
    mapTypeId: google.maps.MapTypeId.ROADMAP
    };

$(function(){
    // This little bit of code is all we need to get the locations of every UK university
    // and college out of our datastore, and ready to plot on the map.
    // Here we’re using the jQuery.ajax() function to call the ScraperWiki datastore
    // and return a list of data points. Once jQuery has received the data, it passes it through
    // a function we’re about to write called drop_markers().
    $.ajax({
        url: 'https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=informazionistatiue&query=select%20country,capitale%20from%20%60swdata%60',
        dataType: 'json',
        success: function(data){ drop_markers(data); }
    });

    // Istanzia la mappa
    map = new google.maps.Map(document.getElementById('map_canvas'), myOptions);
});
        </script>
    </head>

    <body>
        <div id="map_canvas"></div>
    </body>
<html>
