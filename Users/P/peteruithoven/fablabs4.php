<html>
<head>
<title>Global Fablabs</title>

<link rel="stylesheet" href="http://media.scraperwiki.com/css/jquery-ui-1.8.12.css">
<script type="text/javascript" src="http://media.scraperwiki.com/js/jquery-1.5.2.min.js"></script>
<script type="text/javascript" src="http://media.scraperwiki.com/js/jquery-ui-1.8.12.custom.min.js"></script>

<script type="text/javascript" src="http://openlayers.org/api/OpenLayers.js"></script> 
<script type="text/javascript" src="http://www.openstreetmap.org/openlayers/OpenStreetMap.js"></script>

<script type="text/javascript"> 

var lat=50.1;
var lon=18.3;
var zoom=3;

var map;
var markers;
var epsg;
var proj;
var currentPopup;

OpenLayers.ImgPath = "http://fablabamersfoort.nl/openlayers/themes/default_dark/img/";
AutoSizeAnchored = OpenLayers.Class(OpenLayers.Popup.Anchored, {
    'autoSize': true
});

var selectedFeature, selectControl;

$(function() {
  console.log("ready");
  
    map = new OpenLayers.Map('map', {
    controls: [
        new OpenLayers.Control.Navigation(),
        new OpenLayers.Control.PanZoomBar(),
        new OpenLayers.Control.Attribution()],
    maxResolution: 'auto',
    });
    
    layer = new OpenLayers.Layer.OSM.Mapnik("Mapnik");
    map.addLayer(layer);
    epsg = new OpenLayers.Projection("EPSG:4326");
    proj = map.getProjectionObject();
    var lonLat = new OpenLayers.LonLat(lon, lat).transform(epsg,proj);
    map.setCenter(lonLat, zoom);

    markers = new OpenLayers.Layer.Markers( "Markers" );
    map.addLayer(markers);

    var scraperURL = "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=fablabs&query=select%20*%20from%20%60swdata%60%20limit%20200";
    var ll, popupClass, popupContentHTML;

    $.getJSON(scraperURL, function(data) 
    {
        /*console.log("data: ",data);*/
        $.each(data, function(key, val) 
        {
            var fablab = val;
            console.log("  ",fablab);
            var lat = fablab.lat;
            var lng = fablab.lng;
            if(lat != "")
            {
                /*var lonLat = new OpenLayers.LonLat(lat,lng).transform(epsg,proj);
                var marker = new OpenLayers.Marker(lonLat);
                marker.attributes.description = description;
                markers.addMarker(marker);*/

                ll = new OpenLayers.LonLat(lat,lng);
                popupClass = OpenLayers.Popup.Anchored;
                popupContentHTML = "<h2>"+fablab.name+"</h2>"+fablab.location+"<br><a href='"+fablab.website+"' target='_blank'>"+fablab.website+"</a>";
                addMarker(ll, popupClass, popupContentHTML, true);
            }
        });
    });
    
    selectControl = new OpenLayers.Control.SelectFeature(markers, {
        onSelect: onFeatureSelect, // will be called on feature select
        onUnselect: onFeatureUnselect // will be called on feature unselect
    });
    selectControl.activate();

    map.events.register("click", map , function(e)
    {
        if(currentPopup != null) currentPopup.hide();
    });
});

/**
 * Function: addMarker
 * Add a new marker to the markers layer given the following lonlat, 
 *     popupClass, and popup contents HTML. Also allow specifying 
 *     whether or not to give the popup a close box.
 * 
 * Parameters:
 * ll - {<OpenLayers.LonLat>} Where to place the marker
 * popupClass - {<OpenLayers.Class>} Which class of popup to bring up 
 *     when the marker is clicked.
 * popupContentHTML - {String} What to put in the popup
 * closeBox - {Boolean} Should popup have a close box?
 * overflow - {Boolean} Let the popup overflow scrollbars?
*/
function addMarker(ll, popupClass, popupContentHTML, closeBox, overflow) 
{
    ll = ll.transform(epsg,proj);
    var feature = new OpenLayers.Feature(markers, ll); 
    feature.closeBox = closeBox;
    feature.popupClass = popupClass;
    feature.data.popupContentHTML = popupContentHTML;
    feature.data.overflow = (overflow) ? "auto" : "hidden";
            
    var marker = feature.createMarker();
    
    /*var markerClick = function (evt) {
        if(currentPopup != null && currentPopup != this.popup) currentPopup.hide();
        if (this.popup == null) {
            
            this.popup = this.createPopup(this.closeBox);
            this.popup.backgroundColor = "#555";
            map.addPopup(this.popup);
            this.popup.show();
        } else {
            this.popup.toggle();
        }
        currentPopup = this.popup;
        OpenLayers.Event.stop(evt);
    };
    marker.events.register("mousedown", feature, markerClick);*/
    
    markers.addMarker(marker);
}
function onFeatureSelect(feature) {
        if(currentPopup != null && currentPopup != this.popup) currentPopup.hide();
        if (this.popup == null) {
            
            this.popup = this.createPopup(this.closeBox);
            this.popup.backgroundColor = "#555";
            map.addPopup(this.popup);
            this.popup.show();
        } else {
            this.popup.toggle();
        }
        currentPopup = this.popup;
}
function onFeatureUnselect(feature) {
   map.removePopup(feature.popup);
   feature.popup.destroy();
   feature.popup = null;
} 
function onPopupClose(evt) {
   selectControl.unselect(selectedFeature);
}
</script>
<style>
.olMap .olPopup
{
    color: #eee;
}
.olMap .olPopup .olPopupCloseBox
{
    background-image: url("http://fablabamersfoort.nl/openlayers/themes/default_dark/img/close-popup.png");
    height: 20px !important;
    right: 6px !important;
    top: 8px !important;
    width: 20px !important;
}
body
{
    font-family: tahoma;
}
.olControlAttribution
{
    font-family: tahoma;
    font-size: 8pt;
    right: 1px !important;
    bottom: 1px !important;
}
</style>

</head>
<body>
<div style="width: 800px; margin: auto">
<div id="map" style="width: 100%; height: 400px; border: 1px solid black;"></div>
</div>
</body>
</html><html>
<head>
<title>Global Fablabs</title>

<link rel="stylesheet" href="http://media.scraperwiki.com/css/jquery-ui-1.8.12.css">
<script type="text/javascript" src="http://media.scraperwiki.com/js/jquery-1.5.2.min.js"></script>
<script type="text/javascript" src="http://media.scraperwiki.com/js/jquery-ui-1.8.12.custom.min.js"></script>

<script type="text/javascript" src="http://openlayers.org/api/OpenLayers.js"></script> 
<script type="text/javascript" src="http://www.openstreetmap.org/openlayers/OpenStreetMap.js"></script>

<script type="text/javascript"> 

var lat=50.1;
var lon=18.3;
var zoom=3;

var map;
var markers;
var epsg;
var proj;
var currentPopup;

OpenLayers.ImgPath = "http://fablabamersfoort.nl/openlayers/themes/default_dark/img/";
AutoSizeAnchored = OpenLayers.Class(OpenLayers.Popup.Anchored, {
    'autoSize': true
});

var selectedFeature, selectControl;

$(function() {
  console.log("ready");
  
    map = new OpenLayers.Map('map', {
    controls: [
        new OpenLayers.Control.Navigation(),
        new OpenLayers.Control.PanZoomBar(),
        new OpenLayers.Control.Attribution()],
    maxResolution: 'auto',
    });
    
    layer = new OpenLayers.Layer.OSM.Mapnik("Mapnik");
    map.addLayer(layer);
    epsg = new OpenLayers.Projection("EPSG:4326");
    proj = map.getProjectionObject();
    var lonLat = new OpenLayers.LonLat(lon, lat).transform(epsg,proj);
    map.setCenter(lonLat, zoom);

    markers = new OpenLayers.Layer.Markers( "Markers" );
    map.addLayer(markers);

    var scraperURL = "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=fablabs&query=select%20*%20from%20%60swdata%60%20limit%20200";
    var ll, popupClass, popupContentHTML;

    $.getJSON(scraperURL, function(data) 
    {
        /*console.log("data: ",data);*/
        $.each(data, function(key, val) 
        {
            var fablab = val;
            console.log("  ",fablab);
            var lat = fablab.lat;
            var lng = fablab.lng;
            if(lat != "")
            {
                /*var lonLat = new OpenLayers.LonLat(lat,lng).transform(epsg,proj);
                var marker = new OpenLayers.Marker(lonLat);
                marker.attributes.description = description;
                markers.addMarker(marker);*/

                ll = new OpenLayers.LonLat(lat,lng);
                popupClass = OpenLayers.Popup.Anchored;
                popupContentHTML = "<h2>"+fablab.name+"</h2>"+fablab.location+"<br><a href='"+fablab.website+"' target='_blank'>"+fablab.website+"</a>";
                addMarker(ll, popupClass, popupContentHTML, true);
            }
        });
    });
    
    selectControl = new OpenLayers.Control.SelectFeature(markers, {
        onSelect: onFeatureSelect, // will be called on feature select
        onUnselect: onFeatureUnselect // will be called on feature unselect
    });
    selectControl.activate();

    map.events.register("click", map , function(e)
    {
        if(currentPopup != null) currentPopup.hide();
    });
});

/**
 * Function: addMarker
 * Add a new marker to the markers layer given the following lonlat, 
 *     popupClass, and popup contents HTML. Also allow specifying 
 *     whether or not to give the popup a close box.
 * 
 * Parameters:
 * ll - {<OpenLayers.LonLat>} Where to place the marker
 * popupClass - {<OpenLayers.Class>} Which class of popup to bring up 
 *     when the marker is clicked.
 * popupContentHTML - {String} What to put in the popup
 * closeBox - {Boolean} Should popup have a close box?
 * overflow - {Boolean} Let the popup overflow scrollbars?
*/
function addMarker(ll, popupClass, popupContentHTML, closeBox, overflow) 
{
    ll = ll.transform(epsg,proj);
    var feature = new OpenLayers.Feature(markers, ll); 
    feature.closeBox = closeBox;
    feature.popupClass = popupClass;
    feature.data.popupContentHTML = popupContentHTML;
    feature.data.overflow = (overflow) ? "auto" : "hidden";
            
    var marker = feature.createMarker();
    
    /*var markerClick = function (evt) {
        if(currentPopup != null && currentPopup != this.popup) currentPopup.hide();
        if (this.popup == null) {
            
            this.popup = this.createPopup(this.closeBox);
            this.popup.backgroundColor = "#555";
            map.addPopup(this.popup);
            this.popup.show();
        } else {
            this.popup.toggle();
        }
        currentPopup = this.popup;
        OpenLayers.Event.stop(evt);
    };
    marker.events.register("mousedown", feature, markerClick);*/
    
    markers.addMarker(marker);
}
function onFeatureSelect(feature) {
        if(currentPopup != null && currentPopup != this.popup) currentPopup.hide();
        if (this.popup == null) {
            
            this.popup = this.createPopup(this.closeBox);
            this.popup.backgroundColor = "#555";
            map.addPopup(this.popup);
            this.popup.show();
        } else {
            this.popup.toggle();
        }
        currentPopup = this.popup;
}
function onFeatureUnselect(feature) {
   map.removePopup(feature.popup);
   feature.popup.destroy();
   feature.popup = null;
} 
function onPopupClose(evt) {
   selectControl.unselect(selectedFeature);
}
</script>
<style>
.olMap .olPopup
{
    color: #eee;
}
.olMap .olPopup .olPopupCloseBox
{
    background-image: url("http://fablabamersfoort.nl/openlayers/themes/default_dark/img/close-popup.png");
    height: 20px !important;
    right: 6px !important;
    top: 8px !important;
    width: 20px !important;
}
body
{
    font-family: tahoma;
}
.olControlAttribution
{
    font-family: tahoma;
    font-size: 8pt;
    right: 1px !important;
    bottom: 1px !important;
}
</style>

</head>
<body>
<div style="width: 800px; margin: auto">
<div id="map" style="width: 100%; height: 400px; border: 1px solid black;"></div>
</div>
</body>
</html>