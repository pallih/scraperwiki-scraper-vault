###########################################################
# Google Maps Visualisation of Heritage Open Days Events  #
# Author: Will Abson                                      #
###########################################################

print """<!DOCTYPE html>
<html>
<head>
<title>Heritage Open Days Map View</title>
<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
<style type="text/css">
  html { height: 100% }
  body { height: 100%; margin: 0; padding: 0; font-size: 0.8em; font-family: arial, helvetica, sans-serif; }
  #map_canvas { }
  #rselect, #dselect { margin-right: 0.5em; }
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
  var DEFAULT_MAP_ZOOM = 8;
  var DEFAULT_MAP_CENTER = [52.66972, -1.658936];
  var DEFAULT_MAP_TYPE = google.maps.MapTypeId.ROADMAP;
  var DEFAULT_REGION = "South East";
  var DEFAULT_DAY = "Any";
  var map;
  var rdd; // region drop-down
  var regionCenters = {
     east_midlands: [52.9407695579855, 0.0609602966308076],
     eastern: [52.19455369009095, 0.7338728942870576],
     north_east: [55.20433862033806, -1.6611466369629424],
     north_west: [54.05011063713584, -2.6169571838379424],
     south_east: [51.27608488211616, -0.2548966369629424],
     south_west: [50.8133036998277, -2.9547867736816924],
     west_midlands: [52.56006621593447, -2.0401749572754424],
     yorkshire__the_humber: [54.01784899255871, -0.5597672424316924]
  }
  function getRegionCenter(rname)
  {
     return regionCenters[rname.replace(" ", "_", "g").replace("&", "", "g").toLowerCase()];
  }
  function initialize() {
     // Set up drop-down
     rdd = YAHOO.util.Dom.get("rselect");
     ddd = YAHOO.util.Dom.get("dselect");
     //var rbutton = new YAHOO.widget.Button("rbutton"); 
     YAHOO.util.Event.on("rbutton", "click", function(e) {
        window.location.href = (window.location.href.indexOf("?") > -1 ? window.location.href.substring(0, window.location.href.indexOf("?")) : window.location.href) + 
           "?region=" + encodeURIComponent(rdd.options[rdd.selectedIndex].value) + "&day=" + encodeURIComponent(ddd.options[ddd.selectedIndex].value);
     });
     var rname = getRegionName();
     for (var i=0; i<rdd.options.length; i++)
     {
        if (rname == rdd.options[i].value)
        {
           rdd.selectedIndex = i;
        }
     }
     var day = getDay();
     for (var i=0; i<ddd.options.length; i++)
     {
        if (day == ddd.options[i].value)
        {
           ddd.selectedIndex = i;
        }
     }

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
     });
     google.maps.event.addListener(map, "dragend", function() {
       saveMapCenter();
     });
     google.maps.event.addListener(map, "maptypeid_changed", function() {
       saveMapType();
     });

     loadMarkers();

     YAHOO.util.Cookie.set("region", getRegionName());
  }
  function getRegionName()
  {
     var search = window.location.search;
     var pos = search.indexOf("region=");
     if (search != "" && pos != -1)
     {
        amppos = search.indexOf("&", pos);
        return search.substring(pos + 7, amppos == -1 ? search.length : amppos).replace("%20", " ", "g").replace("%26", "&", "g");
     }
     return DEFAULT_REGION;
  }
  function getDay()
  {
     var search = window.location.search;
     var pos = search.indexOf("day=");
     if (search != "" && pos != -1)
     {
        amppos = search.indexOf("&", pos);
        return search.substring(pos + 4, amppos == -1 ? search.length : amppos).replace("%20", " ", "g").replace("%26", "&", "g");
     }
     return DEFAULT_DAY;
  }
  function getMapCenter()
  {
     var rname = getRegionName();
     var savedRegion = YAHOO.util.Cookie.get("region");
     if (savedRegion == rname)
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
     else 
     {
        // Use default zoom level when region changed
        return getRegionCenter(rname);
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
  function addMarker(event) {
     var marker = new google.maps.Marker({
        map: map,
        position: new google.maps.LatLng(event.lat, event.lng)
     });
     var ahtml = "<div class=\\"event-info\\">" + 
        "<div class=\\"event-name\\">" + event.name + "</div>" + 
        "<div class=\\"event-addr\\">" + event.address + "</div>" + 
        "<div class=\\"event-desc\\">" + event.description + "</div>" + 
        "<dl>" +
        "<dt>Opening Times</dt>" +
        "<dd>" + event.opening_times.replace(/(.)([A-Z][a-z]+day [0-9]+)/g, "$1<br />$2") + "</dd>" +
        "<dt>Pre-Booking Required?</dt>" +
        "<dd>" + event.prebooking_required.replace(".(JavaScript", "<" + "script type=\\"text/javascript\\">.(JavaScript").replace(/document\\.getElementById\\('([\\w]+)'\\)\\.innerHTML = output;\\r\\n\\/\\/]]>\\r\\n\\./, "document.getElementById('$1').innerHTML = output;\\r\\n//]]>\\r\\n.<" + "/script><div id=\\"$1\\"></div>") + "</dd>" +
        (event.directions != "" ? ("<dt>Directions</dt>" +
        "<dd>" + event.directions + "</dd>") : "") +
        "<dt>Access Information</dt>" +
        "<dd>" + (event.full_wheelchair_access == "Yes" ? "Full wheelchair access. " : (event.full_wheelchair_access == "Partial" ? "Partial wheelchair access. " : "")) + event.access_information + "</dd>" +
        (event.additional_information != "" ? "<dt>Additional Information</dt>" +
        "<dd>" + event.additional_information + "</dd>" : "") +
        "<dt>Normally Open?</dt>" +
        "<dd>" + (event.not_normally_open ? "No" : "Yes") + "</dd>" +
        "<dt>Normally Free?</dt>" +
        "<dd>" + (event.not_normally_free ? "No" : "Yes") + "</dd>" +
        "</dl>" +
        ((event.event_code != "") ? ("<p><a href=\\"http://www.heritageopendays.org.uk/directory/" + event.event_code + "/\\">More Details</a></p>") : "") +
        "</div>";
     var infowindow = new google.maps.InfoWindow({
            content: ahtml,
            size: new google.maps.Size(50,50)
         });
         google.maps.event.addListener(marker, 'click', function() {
            infowindow.open(map, marker);
            /*
            var windowContent = infowindow.getContent();
            var scriptRe = /<script type="text\\/javascript">\\.\\(JavaScript must be enabled to view this email address\\)([\w\W]*)\\.<\\/script>/gm;
            while ((m = scriptRe.exec(windowContent)) != null)
            {
               var src = m[1];
               var script = document.createElement("script");
               script.type = "text/javascript";
               document.getElementsByTagName("head")[0].appendChild(script);
               script.src = src;
            }
            */
         });
  }
  function loadMarkers()
  {
      // Initialize the temporary Panel to display while waiting for external content to load
      var wait = 
        new YAHOO.widget.Panel("wait",  
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

     // Define the callbacks for the asyncRequest
     var callbacks = {

        success : function (o) {
            //YAHOO.log("RAW JSON DATA: " + o.responseText);

            // Process the JSON data returned from the server
            var jsonText = o.responseText.replace(/<div.*>/, "", "g");
            //var jsonText = o.responseText;
            var events = [];
            try {
                events = YAHOO.lang.JSON.parse(jsonText);
            }
            catch (x) {
                wait.hide();
                alert("Invalid data was returned. Please try again in a moment.");
                return;
            }

            //YAHOO.log("PARSED DATA: " + YAHOO.lang.dump(events));

            // The returned data was parsed into an array of objects.
            for (var i = 0, len = events.length; i < len; ++i) {
                addMarker(events[i]);
            }
            wait.hide();
        },

        failure : function (o) {
            if (!YAHOO.util.Connect.isCallInProgress(o)) {
                wait.hide();
                alert("Failed to fetch data. Please try again in moment.");
            }
        },

        timeout : 30000
     }

     var search = window.location.search;
     if (search.indexOf("region=") == -1)
     {
        search += ((search.length > 1) ? "&" : "?") + "region=" + encodeURIComponent(getRegionName());
     }

     //var search = "?region=" + encodeURIComponent(getRegionName());

     // Make the call to the server for JSON data
     YAHOO.util.Connect.asyncRequest('GET', "https://views.scraperwiki.com/run/heritage_open_days_map_data/" + search, callbacks);
  }
</script>
<!-- Combo-handled YUI CSS files: --> 
<link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/combo?2.9.0/build/container/assets/skins/sam/container.css&2.9.0/build/button/assets/skins/sam/button.css"> 
<!-- Combo-handled YUI JS files: -->
<script type="text/javascript" src="http://yui.yahooapis.com/combo?2.9.0/build/yahoo-dom-event/yahoo-dom-event.js&2.9.0/build/connection/connection-min.js&2.9.0/build/cookie/cookie-min.js&2.9.0/build/json/json-min.js&2.9.0/build/animation/animation-min.js&2.9.0/build/dragdrop/dragdrop-min.js&2.9.0/build/container/container-min.js&2.9.0/build/element/element-min.js&2.9.0/build/button/button-min.js"></script>
</head>
<body class="yui-skin-sam">
<div id="info">
<div><a href="http://www.heritageopendays.org.uk/">Heritage Open Days 2011</a> runs from 8-11 September. Select a region from the drop-down to show the events taking place. Not all events are guaranteed to be shown, and information might be out-of-date. Check the <a href="http://www.heritageopendays.org.uk/directory/">official directory</a> for definitive details for an event.</div>
<div class="select">Select region: 
   <select id="rselect">
      <option>East Midlands</option>
      <option>Eastern</option>
      <option>North East</option>
      <option>North West</option>
      <option>South East</option>
      <option>South West</option>
      <option>West Midlands</option>
      <option>Yorkshire & the Humber</option>
   </select>
   <select id="dselect">
      <option>Any</option>
      <option>Thursday</option>
      <option>Friday</option>
      <option>Saturday</option>
      <option>Sunday</option>
   </select>
   <input id="rbutton" type="button" value="Display" />
</div>
</div>
<div id="map_canvas"></div>
<script type="text/javascript">
YAHOO.util.Event.onDOMReady(function init() {
    initialize();
});
</script>
</body>
</html>
"""

###########################################################
# Google Maps Visualisation of Heritage Open Days Events  #
# Author: Will Abson                                      #
###########################################################

print """<!DOCTYPE html>
<html>
<head>
<title>Heritage Open Days Map View</title>
<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
<style type="text/css">
  html { height: 100% }
  body { height: 100%; margin: 0; padding: 0; font-size: 0.8em; font-family: arial, helvetica, sans-serif; }
  #map_canvas { }
  #rselect, #dselect { margin-right: 0.5em; }
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
  var DEFAULT_MAP_ZOOM = 8;
  var DEFAULT_MAP_CENTER = [52.66972, -1.658936];
  var DEFAULT_MAP_TYPE = google.maps.MapTypeId.ROADMAP;
  var DEFAULT_REGION = "South East";
  var DEFAULT_DAY = "Any";
  var map;
  var rdd; // region drop-down
  var regionCenters = {
     east_midlands: [52.9407695579855, 0.0609602966308076],
     eastern: [52.19455369009095, 0.7338728942870576],
     north_east: [55.20433862033806, -1.6611466369629424],
     north_west: [54.05011063713584, -2.6169571838379424],
     south_east: [51.27608488211616, -0.2548966369629424],
     south_west: [50.8133036998277, -2.9547867736816924],
     west_midlands: [52.56006621593447, -2.0401749572754424],
     yorkshire__the_humber: [54.01784899255871, -0.5597672424316924]
  }
  function getRegionCenter(rname)
  {
     return regionCenters[rname.replace(" ", "_", "g").replace("&", "", "g").toLowerCase()];
  }
  function initialize() {
     // Set up drop-down
     rdd = YAHOO.util.Dom.get("rselect");
     ddd = YAHOO.util.Dom.get("dselect");
     //var rbutton = new YAHOO.widget.Button("rbutton"); 
     YAHOO.util.Event.on("rbutton", "click", function(e) {
        window.location.href = (window.location.href.indexOf("?") > -1 ? window.location.href.substring(0, window.location.href.indexOf("?")) : window.location.href) + 
           "?region=" + encodeURIComponent(rdd.options[rdd.selectedIndex].value) + "&day=" + encodeURIComponent(ddd.options[ddd.selectedIndex].value);
     });
     var rname = getRegionName();
     for (var i=0; i<rdd.options.length; i++)
     {
        if (rname == rdd.options[i].value)
        {
           rdd.selectedIndex = i;
        }
     }
     var day = getDay();
     for (var i=0; i<ddd.options.length; i++)
     {
        if (day == ddd.options[i].value)
        {
           ddd.selectedIndex = i;
        }
     }

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
     });
     google.maps.event.addListener(map, "dragend", function() {
       saveMapCenter();
     });
     google.maps.event.addListener(map, "maptypeid_changed", function() {
       saveMapType();
     });

     loadMarkers();

     YAHOO.util.Cookie.set("region", getRegionName());
  }
  function getRegionName()
  {
     var search = window.location.search;
     var pos = search.indexOf("region=");
     if (search != "" && pos != -1)
     {
        amppos = search.indexOf("&", pos);
        return search.substring(pos + 7, amppos == -1 ? search.length : amppos).replace("%20", " ", "g").replace("%26", "&", "g");
     }
     return DEFAULT_REGION;
  }
  function getDay()
  {
     var search = window.location.search;
     var pos = search.indexOf("day=");
     if (search != "" && pos != -1)
     {
        amppos = search.indexOf("&", pos);
        return search.substring(pos + 4, amppos == -1 ? search.length : amppos).replace("%20", " ", "g").replace("%26", "&", "g");
     }
     return DEFAULT_DAY;
  }
  function getMapCenter()
  {
     var rname = getRegionName();
     var savedRegion = YAHOO.util.Cookie.get("region");
     if (savedRegion == rname)
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
     else 
     {
        // Use default zoom level when region changed
        return getRegionCenter(rname);
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
  function addMarker(event) {
     var marker = new google.maps.Marker({
        map: map,
        position: new google.maps.LatLng(event.lat, event.lng)
     });
     var ahtml = "<div class=\\"event-info\\">" + 
        "<div class=\\"event-name\\">" + event.name + "</div>" + 
        "<div class=\\"event-addr\\">" + event.address + "</div>" + 
        "<div class=\\"event-desc\\">" + event.description + "</div>" + 
        "<dl>" +
        "<dt>Opening Times</dt>" +
        "<dd>" + event.opening_times.replace(/(.)([A-Z][a-z]+day [0-9]+)/g, "$1<br />$2") + "</dd>" +
        "<dt>Pre-Booking Required?</dt>" +
        "<dd>" + event.prebooking_required.replace(".(JavaScript", "<" + "script type=\\"text/javascript\\">.(JavaScript").replace(/document\\.getElementById\\('([\\w]+)'\\)\\.innerHTML = output;\\r\\n\\/\\/]]>\\r\\n\\./, "document.getElementById('$1').innerHTML = output;\\r\\n//]]>\\r\\n.<" + "/script><div id=\\"$1\\"></div>") + "</dd>" +
        (event.directions != "" ? ("<dt>Directions</dt>" +
        "<dd>" + event.directions + "</dd>") : "") +
        "<dt>Access Information</dt>" +
        "<dd>" + (event.full_wheelchair_access == "Yes" ? "Full wheelchair access. " : (event.full_wheelchair_access == "Partial" ? "Partial wheelchair access. " : "")) + event.access_information + "</dd>" +
        (event.additional_information != "" ? "<dt>Additional Information</dt>" +
        "<dd>" + event.additional_information + "</dd>" : "") +
        "<dt>Normally Open?</dt>" +
        "<dd>" + (event.not_normally_open ? "No" : "Yes") + "</dd>" +
        "<dt>Normally Free?</dt>" +
        "<dd>" + (event.not_normally_free ? "No" : "Yes") + "</dd>" +
        "</dl>" +
        ((event.event_code != "") ? ("<p><a href=\\"http://www.heritageopendays.org.uk/directory/" + event.event_code + "/\\">More Details</a></p>") : "") +
        "</div>";
     var infowindow = new google.maps.InfoWindow({
            content: ahtml,
            size: new google.maps.Size(50,50)
         });
         google.maps.event.addListener(marker, 'click', function() {
            infowindow.open(map, marker);
            /*
            var windowContent = infowindow.getContent();
            var scriptRe = /<script type="text\\/javascript">\\.\\(JavaScript must be enabled to view this email address\\)([\w\W]*)\\.<\\/script>/gm;
            while ((m = scriptRe.exec(windowContent)) != null)
            {
               var src = m[1];
               var script = document.createElement("script");
               script.type = "text/javascript";
               document.getElementsByTagName("head")[0].appendChild(script);
               script.src = src;
            }
            */
         });
  }
  function loadMarkers()
  {
      // Initialize the temporary Panel to display while waiting for external content to load
      var wait = 
        new YAHOO.widget.Panel("wait",  
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

     // Define the callbacks for the asyncRequest
     var callbacks = {

        success : function (o) {
            //YAHOO.log("RAW JSON DATA: " + o.responseText);

            // Process the JSON data returned from the server
            var jsonText = o.responseText.replace(/<div.*>/, "", "g");
            //var jsonText = o.responseText;
            var events = [];
            try {
                events = YAHOO.lang.JSON.parse(jsonText);
            }
            catch (x) {
                wait.hide();
                alert("Invalid data was returned. Please try again in a moment.");
                return;
            }

            //YAHOO.log("PARSED DATA: " + YAHOO.lang.dump(events));

            // The returned data was parsed into an array of objects.
            for (var i = 0, len = events.length; i < len; ++i) {
                addMarker(events[i]);
            }
            wait.hide();
        },

        failure : function (o) {
            if (!YAHOO.util.Connect.isCallInProgress(o)) {
                wait.hide();
                alert("Failed to fetch data. Please try again in moment.");
            }
        },

        timeout : 30000
     }

     var search = window.location.search;
     if (search.indexOf("region=") == -1)
     {
        search += ((search.length > 1) ? "&" : "?") + "region=" + encodeURIComponent(getRegionName());
     }

     //var search = "?region=" + encodeURIComponent(getRegionName());

     // Make the call to the server for JSON data
     YAHOO.util.Connect.asyncRequest('GET', "https://views.scraperwiki.com/run/heritage_open_days_map_data/" + search, callbacks);
  }
</script>
<!-- Combo-handled YUI CSS files: --> 
<link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/combo?2.9.0/build/container/assets/skins/sam/container.css&2.9.0/build/button/assets/skins/sam/button.css"> 
<!-- Combo-handled YUI JS files: -->
<script type="text/javascript" src="http://yui.yahooapis.com/combo?2.9.0/build/yahoo-dom-event/yahoo-dom-event.js&2.9.0/build/connection/connection-min.js&2.9.0/build/cookie/cookie-min.js&2.9.0/build/json/json-min.js&2.9.0/build/animation/animation-min.js&2.9.0/build/dragdrop/dragdrop-min.js&2.9.0/build/container/container-min.js&2.9.0/build/element/element-min.js&2.9.0/build/button/button-min.js"></script>
</head>
<body class="yui-skin-sam">
<div id="info">
<div><a href="http://www.heritageopendays.org.uk/">Heritage Open Days 2011</a> runs from 8-11 September. Select a region from the drop-down to show the events taking place. Not all events are guaranteed to be shown, and information might be out-of-date. Check the <a href="http://www.heritageopendays.org.uk/directory/">official directory</a> for definitive details for an event.</div>
<div class="select">Select region: 
   <select id="rselect">
      <option>East Midlands</option>
      <option>Eastern</option>
      <option>North East</option>
      <option>North West</option>
      <option>South East</option>
      <option>South West</option>
      <option>West Midlands</option>
      <option>Yorkshire & the Humber</option>
   </select>
   <select id="dselect">
      <option>Any</option>
      <option>Thursday</option>
      <option>Friday</option>
      <option>Saturday</option>
      <option>Sunday</option>
   </select>
   <input id="rbutton" type="button" value="Display" />
</div>
</div>
<div id="map_canvas"></div>
<script type="text/javascript">
YAHOO.util.Event.onDOMReady(function init() {
    initialize();
});
</script>
</body>
</html>
"""

