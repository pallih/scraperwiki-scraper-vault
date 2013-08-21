<!DOCTYPE html>
<html>
<head>
<title>Environment Agency HiFlows UK Stations</title>
<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
<style type="text/css">
  html { height: 100% }
  body { height: 100%; margin: 0; padding: 0; font-size: 0.8em; font-family: arial, helvetica, sans-serif; }
  #map_canvas { }
  #tselect { margin-right: 0.5em; }
  .event-name { font-size: 1.2em; font-weight: bold; margin-bottom: 0.3em; }
  .event-addr { color: #666666; margin-bottom: 0.3em; }
  .event-name { margin-bottom: 0.3em; }
  dt { font-weight: bold; }
  div#info { padding: 1em 189px 1em 1em; border-bottom: 2px solid #cccccc; }
  div.select { padding-top: 0.5em; }
</style>
<script type="text/javascript"
    src="http://maps.googleapis.com/maps/api/js?sensor=false">
</script>
<script type="text/javascript">
  var DEFAULT_MAP_ZOOM = 13;
  var DEFAULT_MAP_CENTER = [ 51.524418316423855, -0.3168015242920297 ];
  var DEFAULT_MAP_TYPE = google.maps.MapTypeId.TERRAIN;
  var map;
  var marker_ids = [];
  var wait = null;
  var showWaiting = false;
  function getMapCenter()
  {
     return DEFAULT_MAP_CENTER;
  }
  function initialize() {
     // Region height
     region = YAHOO.util.Dom.getRegion(YAHOO.util.Dom.get("info"));
     infoheight = region.height;
     YAHOO.util.Dom.setStyle("map_canvas", "height", "" + (YAHOO.util.Dom.getDocumentHeight() - infoheight) + "px");

     // Initialise the map
     var center = getMapCenter();
     var latlng = new google.maps.LatLng(center[0], center[1]);
     var myOptions = {
       zoom: getMapZoom(),
       center: latlng,
       mapTypeId: getMapType()
     };
     map = new google.maps.Map(document.getElementById("map_canvas"),
        myOptions);
     google.maps.event.addListener(map, "zoom_changed", function() {
       saveMapZoom();
       saveMapCenter();
       loadData();
     });
     google.maps.event.addListener(map, "dragend", function() {
       saveMapCenter();
       loadData();
     });
     google.maps.event.addListener(map, "maptypeid_changed", function() {
       saveMapType();
     });

     google.maps.event.addListenerOnce(map, 'idle', function(){
        // do something only the first time the map is loaded
        loadMarkers();
     });

  }
  function getMapCenter()
  {
     var center = YAHOO.util.Cookie.get("mapcenter");
     if (center != null)
     {
        var parts = center.split(",");
        return [parseFloat(parts[0]), parseFloat(parts[1])];
     }
     else
     {
        return DEFAULT_MAP_CENTER;
     }
  }
  function getMapZoom()
  {
     var zoom = YAHOO.util.Cookie.get("mapzoom");
     if (zoom != null)
     {
        return parseInt(zoom);
     }
     else
     {
        return DEFAULT_MAP_ZOOM;
     }
  }
  function getMapType()
  {
     var type = YAHOO.util.Cookie.get("maptype");
     if (type != null)
     {
        return type;
     }
     else
     {
        return DEFAULT_MAP_TYPE;
     }
  }
  function saveMapCenter()
  {
     var center = map.getCenter();
     YAHOO.util.Cookie.set("mapcenter", "" + center.lat() + "," + center.lng());
  }
  function saveMapZoom(zoom)
  {
     YAHOO.util.Cookie.set("mapzoom", map.getZoom());
  }
  function saveMapType(zoom)
  {
     YAHOO.util.Cookie.set("maptype", map.getgetMapTypeId());
  }
  function hasMarker(id) {
     for (var i = 0, len = marker_ids.length; i < len; ++i) {
        if (id == marker_ids[i]) {
           return true;
        }
     }
     return false;
  }
  function addMarker(event) {
     if (hasMarker(event.ceh_number)) {
        return;
     }
     var marker = new google.maps.Marker({
        map: map,
        position: new google.maps.LatLng(event.latlng_lat, event.latlng_lng)
     });
     var ahtml = "<div class=\"event-info\">" +
        "<div class=\"event-name\">" + event.location + " (" + parseInt(event.ceh_number) + ")</div>" +
        "<dl>" +
        "<dt>Watercourse</dt>" +
        "<dd>" + event.watercourse + "</dd>" +
        "<dt>Nominal Area (km2)</dt>" +
        "<dd>" + event.nominal_area + "</dd>" +
        "<dt>Gauging Authority or Region</dt>" +
        "<dd>" + event.gauging_authority_or_region + "</dd>" +
        "<dt>Status</dt>" +
        "<dd>" + event.status + "</dd>" +
        "</dl>" +
        ((event.pkid != "") ? ("<p><a href=\"http://www.environment-agency.gov.uk/hiflows/station.aspx?" + event.ceh_number + "\">More Details</a></p>") : "") +
        "</div>";
     var infowindow = new google.maps.InfoWindow({
        content: ahtml,
        size: new google.maps.Size(50,50)
     });
     google.maps.event.addListener(marker, 'click', function() {
        infowindow.open(map, marker);
     });
     marker_ids.push(event.ceh_number);
  }
  function loadMarkers()
  {
      // Initialize the temporary Panel to display while waiting for external content to load
      if (showWaiting) {
        wait = new YAHOO.widget.Panel("wait",  
           {
              width: "240px",
              fixedcenter: true,
              close: false,
              draggable: false,
              zIndex: 10,
              modal: true,
              visible: false,
           }
        );

        wait.setHeader("Loading locations");
        wait.setBody('<img src="http://l.yimg.com/a/i/us/per/gr/gp/rel_interstitial_loading.gif" />');
        wait.render(document.body);
        wait.show();
     }

     loadData();
   }
   function getDataUrl()
   {
      var sqlQuery = 'select * from `swdata`';
      var sw = map.getBounds().getSouthWest(), ne = map.getBounds().getNorthEast();
      if (map.getZoom() > 8) {
         sqlQuery += " where latlng_lat < " + ne.lat() + " and latlng_lat > " + sw.lat() + " and latlng_lng > " + sw.lng() + " and latlng_lng < " + ne.lng();
      }
      sqlQuery += " limit 500";
      return ('https:' == document.location.protocol ? 'https://' : 'http://') + "api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=hiflows_uk_stations&query=" + encodeURIComponent(sqlQuery) + '&callback=addItems';
   }
   function loadData()
   {
      // Make the call to the server for JSON data
      // Does not work due to XSS limitations. Cannot find any reference to a suitable server-side proxy?
      //YAHOO.util.Connect.asyncRequest('GET', "https://scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=ealing_tree_preservation_orders&query=select%20*%20from%20%60swdata%60%20limit%20100", callbacks);
      var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
      ga.src = getDataUrl();
      var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
   }
   function addItems(items)
   {
      for (var i = 0, len = items.length; i < len; ++i) {
         addMarker(items[i]);
      }
      if (wait != null)
      {
         wait.hide();
      }
   }
</script>
<!-- Combo-handled YUI CSS files: -->
<link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/combo?2.9.0/build/container/assets/skins/sam/container.css&2.9.0/build/button/assets/skins/sam/button.css">
<!-- Combo-handled YUI JS files: -->
<script type="text/javascript" src="http://yui.yahooapis.com/combo?2.9.0/build/yahoo-dom-event/yahoo-dom-event.js&2.9.0/build/connection/connection-min.js&2.9.0/build/cookie/cookie-min.js&2.9.0/build/json/json-min.js&2.9.0/build/animation/animation-min.js&2.9.0/build/dragdrop/dragdrop-min.js&2.9.0/build/container/container-min.js&2.9.0/build/element/element-min.js&2.9.0/build/button/button-min.js"></script>
</head>
<body class="yui-skin-sam">
<div id="info">
<div>This map shows the complete list of around 1000 <a href="http://www.environment-agency.gov.uk/hiflows/91727.aspx">HiFlows river flow gauging stations</a> throughout the UK, which are used by the Environment Agency. Click an item on the map to display more information and a link to the full page.</div>
</div>
<div id="map_canvas"></div>
<script type="text/javascript">
YAHOO.util.Event.onDOMReady(function init() {
    initialize();
});
</script>
</body>
</html>
