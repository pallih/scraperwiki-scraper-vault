<?php


scraperwiki::attach("cordis_fp7_1");
$data = scraperwiki::select("* from `swdata`");
//print_r($data);
#print_r($countries);


?>
<!DOCTYPE html>
<html>
    <head>
        <title>FP7 People ITN</title>
<link href="http://leaflet.cloudmade.com/dist/leaflet.css" rel="stylesheet"></link>

        <script type="text/javascript" src="http://leaflet.cloudmade.com/dist/leaflet.js"></script>


    </head>
    <body>
<div id="map" style="height: 500px;"></div>


<script>
  var map = new L.Map('map');
  // var url = 'http://{s}.tile.cloudmade.com/BC9A493B41014CAABB98F0471D759707/997/256/{z}/{x}/{y}.png';
  // var url = 'http://{s}.tile.stamen.com/watercolor/{z}/{x}/{y}.jpg';
  // var url = 'http://{s}.tiles.mapbox.com/v3/mapbox.mapbox-streets/{z}/{x}/{y}.png32';
  var url = 'http://{s}.tiles.mapbox.com/v3/mapbox.mapbox-chester/{z}/{x}/{y}.png32';
  // var url = 'http://{s}.tiles.mapbox.com/v3/mapbox.world-light/{z}/{x}/{y}.png32';
  var attribution = 'Map data &copy; 2011 OpenStreetMap contributors, Imagery &copy; 2011 CloudMade';
  var layer = new L.TileLayer(url, {maxZoom: 18, attribution: attribution});
  
  var OCIcon = L.Icon.extend({
    options: {
      iconUrl: '{{ site.IMG_PATH }}/oc_square_logo_128_reasonably_small.png',
      // shadowUrl: '{{ site.IMG_PATH }}/oc_square_logo_111.png',
      // shadowUrl: '../docs/images/leaf-shadow.png',
      iconSize: new L.Point(60, 60),
      // shadowSize: new L.Point(68, 95),
      iconAnchor: new L.Point(30, 30),
      popupAnchor: new L.Point(0, -30)
    }
  });
  var LeafIcon = L.Icon.extend({
    options: {
       iconUrl: '{{ site.IMG_PATH }}/leaf-green.png',
       shadowUrl: '{{ site.IMG_PATH }}/leaf-shadow.png',
       iconSize: new L.Point(38, 95),
       shadowSize: new L.Point(68, 95),
       iconAnchor: new L.Point(22, 94),
       popupAnchor: new L.Point(-3, -76)
    } 
  });
    
  var myIcon = new OCIcon();
  // var myIcon = new LeafIcon();
  
  map.setView(new L.LatLng(41.383931, 2.199927), 4).addLayer(layer);
  // marker = new L.Marker(new L.LatLng(41.383931, 2.199927), {icon: myIcon});
  marker = new L.Marker(new L.LatLng(41.383931, 2.199927));
  
  map.addLayer(marker);
  
  html = 'Calle Escullera de Poblenou 15<br/>08005 Barcelona, Spain<br/><br/>';
  html += "<a href='https://www.google.com/maps/ms?msa=0&amp;msid=216938678935670822755.0004c2306ab10c2258707&amp;ie=UTF8&amp;ll=41.386166,2.198068&amp;spn=0.00449,0.009589&amp;t=m&amp;source=embed' class='btn btn-small btn-info'><i class='icon-map-marker icon-white' target='_blank'> </i> <b>Open in Google Maps</b></a>";
  
  marker.bindPopup(html, {closeButton: false});
</script>


</body>
</html>
<?php


scraperwiki::attach("cordis_fp7_1");
$data = scraperwiki::select("* from `swdata`");
//print_r($data);
#print_r($countries);


?>
<!DOCTYPE html>
<html>
    <head>
        <title>FP7 People ITN</title>
<link href="http://leaflet.cloudmade.com/dist/leaflet.css" rel="stylesheet"></link>

        <script type="text/javascript" src="http://leaflet.cloudmade.com/dist/leaflet.js"></script>


    </head>
    <body>
<div id="map" style="height: 500px;"></div>


<script>
  var map = new L.Map('map');
  // var url = 'http://{s}.tile.cloudmade.com/BC9A493B41014CAABB98F0471D759707/997/256/{z}/{x}/{y}.png';
  // var url = 'http://{s}.tile.stamen.com/watercolor/{z}/{x}/{y}.jpg';
  // var url = 'http://{s}.tiles.mapbox.com/v3/mapbox.mapbox-streets/{z}/{x}/{y}.png32';
  var url = 'http://{s}.tiles.mapbox.com/v3/mapbox.mapbox-chester/{z}/{x}/{y}.png32';
  // var url = 'http://{s}.tiles.mapbox.com/v3/mapbox.world-light/{z}/{x}/{y}.png32';
  var attribution = 'Map data &copy; 2011 OpenStreetMap contributors, Imagery &copy; 2011 CloudMade';
  var layer = new L.TileLayer(url, {maxZoom: 18, attribution: attribution});
  
  var OCIcon = L.Icon.extend({
    options: {
      iconUrl: '{{ site.IMG_PATH }}/oc_square_logo_128_reasonably_small.png',
      // shadowUrl: '{{ site.IMG_PATH }}/oc_square_logo_111.png',
      // shadowUrl: '../docs/images/leaf-shadow.png',
      iconSize: new L.Point(60, 60),
      // shadowSize: new L.Point(68, 95),
      iconAnchor: new L.Point(30, 30),
      popupAnchor: new L.Point(0, -30)
    }
  });
  var LeafIcon = L.Icon.extend({
    options: {
       iconUrl: '{{ site.IMG_PATH }}/leaf-green.png',
       shadowUrl: '{{ site.IMG_PATH }}/leaf-shadow.png',
       iconSize: new L.Point(38, 95),
       shadowSize: new L.Point(68, 95),
       iconAnchor: new L.Point(22, 94),
       popupAnchor: new L.Point(-3, -76)
    } 
  });
    
  var myIcon = new OCIcon();
  // var myIcon = new LeafIcon();
  
  map.setView(new L.LatLng(41.383931, 2.199927), 4).addLayer(layer);
  // marker = new L.Marker(new L.LatLng(41.383931, 2.199927), {icon: myIcon});
  marker = new L.Marker(new L.LatLng(41.383931, 2.199927));
  
  map.addLayer(marker);
  
  html = 'Calle Escullera de Poblenou 15<br/>08005 Barcelona, Spain<br/><br/>';
  html += "<a href='https://www.google.com/maps/ms?msa=0&amp;msid=216938678935670822755.0004c2306ab10c2258707&amp;ie=UTF8&amp;ll=41.386166,2.198068&amp;spn=0.00449,0.009589&amp;t=m&amp;source=embed' class='btn btn-small btn-info'><i class='icon-map-marker icon-white' target='_blank'> </i> <b>Open in Google Maps</b></a>";
  
  marker.bindPopup(html, {closeButton: false});
</script>


</body>
</html>
