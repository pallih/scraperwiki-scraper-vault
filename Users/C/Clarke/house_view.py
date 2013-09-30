import string
import json
sourcescraper = 'house_search'

import scraperwiki
scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select(
    '''lat, lng, address, price from house_search.house_data'''
)
for item in data:
    lat = item['lat']
    lng = item['lng']

kwargs = {
    'lat' : lat,
    'lng': lng,
    'points': json.dumps(data),
}
s =  string.Template('''
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
<style type="text/css">
  html { height: 100% }
  body { height: 100%; margin: 0; padding: 0 }
  #map_canvas { height: 100% }
</style>
<script type="text/javascript"
    src="http://maps.googleapis.com/maps/api/js?sensor=false">
</script>
<script type="text/javascript">
  function initialize() {
    var latlng = new google.maps.LatLng($lat, $lng); 
    var myOptions = {
      zoom: 11,
      center: latlng,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(document.getElementById("map_canvas"),
        myOptions);

    var marker = new google.maps.Marker({
      position: latlng,
      title:"Hello World!"
    });
    // To add the marker to the map, call setMap();
    marker.setMap(map);  

    var mypoints = $points;


    
    for (index in mypoints){
        var point = mypoints[index];
        latlng = new google.maps.LatLng(point['lat'], point['lng']);
        marker = new google.maps.Marker({
          position: latlng,
          title: point['price'] + point['address']
        });
        // To add the marker to the map, call setMap();
        marker.setMap(map);  
    }
    
  }

</script>
</head>
<body onload="initialize()">
  <div id="map_canvas" style="width:100%; height:100%"></div>
</body>
</html>
''')

print s.substitute(**kwargs)
import string
import json
sourcescraper = 'house_search'

import scraperwiki
scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select(
    '''lat, lng, address, price from house_search.house_data'''
)
for item in data:
    lat = item['lat']
    lng = item['lng']

kwargs = {
    'lat' : lat,
    'lng': lng,
    'points': json.dumps(data),
}
s =  string.Template('''
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
<style type="text/css">
  html { height: 100% }
  body { height: 100%; margin: 0; padding: 0 }
  #map_canvas { height: 100% }
</style>
<script type="text/javascript"
    src="http://maps.googleapis.com/maps/api/js?sensor=false">
</script>
<script type="text/javascript">
  function initialize() {
    var latlng = new google.maps.LatLng($lat, $lng); 
    var myOptions = {
      zoom: 11,
      center: latlng,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(document.getElementById("map_canvas"),
        myOptions);

    var marker = new google.maps.Marker({
      position: latlng,
      title:"Hello World!"
    });
    // To add the marker to the map, call setMap();
    marker.setMap(map);  

    var mypoints = $points;


    
    for (index in mypoints){
        var point = mypoints[index];
        latlng = new google.maps.LatLng(point['lat'], point['lng']);
        marker = new google.maps.Marker({
          position: latlng,
          title: point['price'] + point['address']
        });
        // To add the marker to the map, call setMap();
        marker.setMap(map);  
    }
    
  }

</script>
</head>
<body onload="initialize()">
  <div id="map_canvas" style="width:100%; height:100%"></div>
</body>
</html>
''')

print s.substitute(**kwargs)
