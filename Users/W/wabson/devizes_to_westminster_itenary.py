import scraperwiki

scraperwiki.sqlite.attach('kennet_avon_canal_itenary')

# Blank Python
sourcescraper = 'kennet_avon_canal_itenary'

#data = scraperwiki.sqlite.select( '''* from kennet_avon_canal_itenary.swdata''' )
print "<html>"
print "<head>"
print "<title>Devices to Westminster Race Itenary</title>"
print """
<style type="text/css">
body {
   font-family: Arial, Helvetica, sans-serif;
   font-size: 0.75em;
   margin: 0 auto;
   padding: 0 0 0 0;
   overflow: hidden;
}
body table {
   font-size: 0.9em;
}
.itenary {
   width: 280px;
   float: left;
   overflow-y: hidden;
   overflow-x: hidden;
   height: 100%;
   position: relative;
   padding: 0;
   margin: 0;
}
.itenary > div {
   height: 100%;
   overflow-x: hidden;
   overflow-y: scroll;
   margin-right: 6px;
}
.itenary table {
   border-width: 0px;
   border-style: none;
   border-spacing: 0px;
   padding: 0px;
   margin: 1em 0px 1em 1em;
   overflow: hidden;
   min-width: 400px;
}
.itenary td {
   border-width: 0px;
   border-style: none;
   padding: 0px;
   margin: 0px;
}
.itenary td.dist {
   width: 3em;
   text-align: right;
}
.itenary div.waypoint {
   background-image: url('http://wabson.org/wwroutes/straight-20.png');
   background-repeat: no-repeat;
   background-position: top left;
   padding-top: 5px;
   padding-left: 30px;
   margin-left: 8px;
   height: 15px;
}
.itenary div.highway_motorway {
   background-image: url('http://wabson.org/wwroutes/motorway-bridge-20.png');
}
.itenary div.highway_trunk {
   background-image: url('http://wabson.org/wwroutes/route-primary-bridge-20.png');
}
.itenary div.highway_primary {
   background-image: url('http://wabson.org/wwroutes/route-primary-bridge-20.png');
}
.itenary div.highway_secondary {
   background-image: url('http://wabson.org/wwroutes/route-primary-bridge-20.png');
}
.itenary div.highway_tertiary, .itenary div.highway_unclassified {
   background-image: url('http://wabson.org/wwroutes/route-unclassified-bridge-20.png');
}
.itenary div.highway_service, .itenary div.highway_residential, .itenary div.highway_bridleway, .itenary div.highway_cycleway, .itenary div.highway_path, .itenary div.highway_footway {
   background-image: url('http://wabson.org/wwroutes/route-path-footway-20.png');
}
.itenary div.railway_rail {
   background-image: url('http://wabson.org/wwroutes/railway-rail-bridge-20.png');
}
.itenary div.tunnel_yes {
   background-image: url('http://wabson.org/wwroutes/tunnel-start-20.png');
}
.itenary div.tunnel_no {
   background-image: url('http://wabson.org/wwroutes/tunnel-end-20.png');
}
.itenary div.lock_yes, .itenary div.waterway_lock {
   background-image: url('http://wabson.org/wwroutes/lock-20.png');
}
.itenary .yui3-resize-handle {
   background-color: #f0f0f0;
}
.map {
   height: 500px;
   width: auto;
   height: 100%;
   float: right;
}
h1 {
   margin: 0 0 0 0;
   padding: 5px 5px 10px 5px;
}
#bd {
   border-top: 1px solid #cccccc;
}
</style>
 <link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.5/leaflet.css" />
 <!--[if lte IE 8]>
     <link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.5/leaflet.ie.css" />
 <![endif]-->
"""
dist = 0.0
lastname = ""
units = "mi"
print "</head>"
print "<body>"
print '<div id="hd">'
print "<h1>Devices to Westminster Race Itenary</h1>"
print '</div>'
print '<div id="bd">'
print '<div id="itenary" class="itenary"><div>'
print '<table>'
for d in []:
    if d["distance"] < dist + 10 and ((d["distance"] - dist) > 0.04 or lastname != d["name"]):
        print "<tr>"
        print '<td class="dist">'
        if (d["distance"] - dist) > 0.04:
            print "%.1f" % (d["distance"] if units == "km" else d["distance"] * 0.621371192)
        print "</td>"
        print '<td><div class="waypoint %s"><a id="wp_%s_%s" href="http://www.openstreetmap.org/index.html?mlat=%s&mlon=%s&zoom=15&layers=B000FTF">%s</a></div></td>' % (d["otag"].replace('=', '_'), d["way_id"], d["node_id"], d["lat"], d["lon"], d["name"])
        print "</tr>"
        dist = d["distance"]
        lastname = d["name"]
print "</table>"
print '</div></div>'
print '<div class="map" id="map"></div>'
print '</div>'
print """<script src="http://yui.yahooapis.com/3.4.1/build/yui/yui-min.js" type="text/javascript"></script>
<script src="http://cdn.leafletjs.com/leaflet-0.5/leaflet.js"></script>
<script type="text/javascript">
var map = null;
function resizeMap(Y) {
    var mapEl = Y.one('#map'), itEl = Y.one('#itenary'), bdEl = Y.one('#bd'), hdEl = Y.one('#hd');
    mapEl.setStyle("width", bdEl.get('region').width - itEl.get('region').width);
    bdEl.setStyle("height", bdEl.get('winHeight') - hdEl.get('region').height);
    itEl.setStyle("height", bdEl.get('winHeight') - hdEl.get('region').height);
    if (map != null) {
        map.invalidateSize();
    }
}
// Create a YUI sandbox on your page.
YUI().use('node', 'event', 'querystring-parse', 'datasource', 'history', function (Y) {
    // The Node and Event modules are loaded and ready to use.
    // Your code goes here!

    var markers = {};
    var leafletTileUrl= "http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", mapInitialZoom = 15, attribution = "Map data copyright OpenStreetMap contributors";
    var waypoints;

    var iconBlue = L.icon({
        iconUrl: 'http://wabson.org/wwroutes/markers/marker-blue.png',
        shadowUrl: 'http://cdn.leafletjs.com/leaflet-0.3.1/images/marker-shadow.png',
        iconSize: new L.Point(27, 41),
        shadowSize: new L.Point(41, 41),
        iconAnchor: new L.Point(14, 41),
        popupAnchor: new L.Point(0, -33)
    });

    var iconBlack = L.icon({
        iconUrl: 'http://wabson.org/wwroutes/markers/marker-black.png',
        shadowUrl: 'http://cdn.leafletjs.com/leaflet-0.3.1/images/marker-shadow.png',
        iconSize: new L.Point(27, 41),
        shadowSize: new L.Point(41, 41),
        iconAnchor: new L.Point(14, 41),
        popupAnchor: new L.Point(0, -33)
    });

    function loadMap(data) {
        var results = data.response.results, bubblehtml, latlng, marker, tag, name, notes, access;
        resizeMap(Y);
        map = new L.Map('map');
        // create the tile layer with correct attribution
        var osm = new L.TileLayer(leafletTileUrl, {attribution: attribution});
        //var first = Y.one('.waypoint a'), href = first.get('href').split("?")[1], args = Y.QueryString.parse(href);
        var slatlng = new L.LatLng(results[0]['gsx$lat']['$t'], results[0]['gsx$lon']['$t']);
    
        // start the map centred on the icon
        map.setView(slatlng, mapInitialZoom);
        map.addLayer(osm);

        var portageIcon = iconBlue, otherIcon = iconBlack;

        for (var i=0; i<results.length; i++) {
            latlng = new L.LatLng(results[i]['gsx$lat']['$t'], results[i]['gsx$lon']['$t']);
            // create a marker in the given location and add it to the map
            name = results[i]['gsx$name']['$t'];
            notes = results[i]['gsx$notes'] ? results[i]['gsx$notes']['$t'] : "";
            access = results[i]['gsx$access'] ? results[i]['gsx$access']['$t'] : "";
            tag = results[i]['gsx$otag']['$t'];
            marker = new L.Marker(latlng, {icon: tag == "waterway=lock" || tag == "lock=yes" ? portageIcon : otherIcon});
            map.addLayer(marker);
    
            // attach a given HTML content to the marker and immediately open it
            bubblehtml = "<p><strong>" + name + "</strong></p>" + (notes != "" ? ("<p>" + notes + "</p>") : "") + (access != "" ? ("<p>" + access + "</p>") : "");
            marker.bindPopup(bubblehtml, {});
            markers[getWPID(results[i])] = marker;
        }

        Y.on("windowresize", function(e) {
            resizeMap(Y);
        });
    };

    function onHistoryChange(e) {
        var changed = e.changed, removed = e.removed;
        if (changed.wp) {
            var wp = getWaypoint(changed.wp.newVal), latlng = new L.LatLng(wp['gsx$lat']['$t'], wp['gsx$lon']['$t']);
            map.panTo(latlng);
            markers[changed.wp.newVal].openPopup();
        }
    };

    function getWPID(wp) {
        return wp['gsx$nodeid']['$t'];
    };

    function getWaypoint(id) {
        for (var i=0; i<waypoints.length; i++) {
            if (getWPID(waypoints[i]) == id) {
                return waypoints[i];
            }
        }
        return null;
    }

    function populateTable(data) {
        var results = data.response.results, tEl = Y.one('#itenary table'), totalDist = 0, dist = 0, name = "", lastName = "";
        for (var i=0; i<results.length; i++) {
            name = results[i]['gsx$name']['$t'];
            dist = parseFloat(results[i]['gsx$distance']['$t']); // convert to miles
            var displayDist = ((dist - totalDist) > 0.04) ? new Number(dist * 0.621371192).toFixed(1) : '';
            if (dist < totalDist + 10 && ((dist - totalDist) > 0.04 || lastName != name)) {
                var html = '<tr><td class="dist">' + displayDist + '</td><td><div class="waypoint ' + results[i]['gsx$otag']['$t'].replace('=', '_') + '"><a id="wp_' + getWPID(results[i]) + '" href="#">' + name + '</a></div></td></tr>';
                tEl.append(html);
                totalDist = dist;
                lastName = name;
            }
        }
    };

    function ssLoadSuccess(e) {
        populateTable(e);
        loadMap(e);
        waypoints = e.response.results;

        var firstPoint = waypoints[0];
        var history = new Y.HistoryHash({
          initialState: {
            wp: getWPID(firstPoint)
          }
        });

        var links = Y.all('.waypoint a');
        links.on('click', function (e) {
            // Stop the event's default behavior
            e.preventDefault();
        
            // Stop the event from bubbling up the DOM tree
            e.stopPropagation();

            var wpid = e.target.get("id").replace('wp_', '');
            history.addValue('wp', wpid);

        });
        links.each(function (el) {
            var wpid = el.get("id").replace('wp_', '');
            markers[wpid].on('click', function(e) {
                history.addValue('wp', wpid);
            });
        });
    };

    var ssId = "0AsA0SXNo_BkZdEpya2FNTTEtWUhNSGJLVkxUNVYxQkE", sheetId = "od6";

    var myDataSource = new Y.DataSource.Get({
        source: "http://spreadsheets.google.com/feeds/list/" + ssId + "/" + sheetId + "/public/values?alt=json-in-script"
    });
    // Normalize the data sent to myCallback
    myDataSource.plug({fn: Y.Plugin.DataSourceJSONSchema, cfg: {
        schema: {
            resultListLocator: "feed.entry",
            resultFields: ["gsx$name", "gsx$distance", "gsx$lat", "gsx$lon", "gsx$otype", "gsx$nodeid", "gsx$wayid", "gsx$otag", "gsx$notes", "gsx$access"]
        }
    }});
    myDataSource.sendRequest({
        request: "",
        callback: {
            success: function(e){
                ssLoadSuccess(e);
            },
            failure: function(e){
                alert(e.error.message);
            }
        }
    });

    Y.on('history:change', onHistoryChange);
});

YUI().use('overlay', 'resize-plugin', function(Y) {
    var resize = new Y.Resize({
        node: '#itenary',
        preserveRatio: false,
        wrap: false,
        maxWidth: 600,
        handles: 'r'
    });
    resize.on('resize:resize', function(event) {
       //this function will be called on resize.
       resizeMap(Y);
    });
/*
    var overlay = new Y.Overlay({
       width: "280px",
       height: "100%",
       srcNode: "#itenary",
       visible: "true"
    });
    //Plug in the resizability plugin
    overlay.plug(Y.Plugin.Resize);
    overlay.render();
    overlay.resize.on('resize:resize', function(event) {
       //this function will be called on resize. 
       resizeMap(Y);
    });
*/
});
</script>
</body>"""
print "</html>"import scraperwiki

scraperwiki.sqlite.attach('kennet_avon_canal_itenary')

# Blank Python
sourcescraper = 'kennet_avon_canal_itenary'

#data = scraperwiki.sqlite.select( '''* from kennet_avon_canal_itenary.swdata''' )
print "<html>"
print "<head>"
print "<title>Devices to Westminster Race Itenary</title>"
print """
<style type="text/css">
body {
   font-family: Arial, Helvetica, sans-serif;
   font-size: 0.75em;
   margin: 0 auto;
   padding: 0 0 0 0;
   overflow: hidden;
}
body table {
   font-size: 0.9em;
}
.itenary {
   width: 280px;
   float: left;
   overflow-y: hidden;
   overflow-x: hidden;
   height: 100%;
   position: relative;
   padding: 0;
   margin: 0;
}
.itenary > div {
   height: 100%;
   overflow-x: hidden;
   overflow-y: scroll;
   margin-right: 6px;
}
.itenary table {
   border-width: 0px;
   border-style: none;
   border-spacing: 0px;
   padding: 0px;
   margin: 1em 0px 1em 1em;
   overflow: hidden;
   min-width: 400px;
}
.itenary td {
   border-width: 0px;
   border-style: none;
   padding: 0px;
   margin: 0px;
}
.itenary td.dist {
   width: 3em;
   text-align: right;
}
.itenary div.waypoint {
   background-image: url('http://wabson.org/wwroutes/straight-20.png');
   background-repeat: no-repeat;
   background-position: top left;
   padding-top: 5px;
   padding-left: 30px;
   margin-left: 8px;
   height: 15px;
}
.itenary div.highway_motorway {
   background-image: url('http://wabson.org/wwroutes/motorway-bridge-20.png');
}
.itenary div.highway_trunk {
   background-image: url('http://wabson.org/wwroutes/route-primary-bridge-20.png');
}
.itenary div.highway_primary {
   background-image: url('http://wabson.org/wwroutes/route-primary-bridge-20.png');
}
.itenary div.highway_secondary {
   background-image: url('http://wabson.org/wwroutes/route-primary-bridge-20.png');
}
.itenary div.highway_tertiary, .itenary div.highway_unclassified {
   background-image: url('http://wabson.org/wwroutes/route-unclassified-bridge-20.png');
}
.itenary div.highway_service, .itenary div.highway_residential, .itenary div.highway_bridleway, .itenary div.highway_cycleway, .itenary div.highway_path, .itenary div.highway_footway {
   background-image: url('http://wabson.org/wwroutes/route-path-footway-20.png');
}
.itenary div.railway_rail {
   background-image: url('http://wabson.org/wwroutes/railway-rail-bridge-20.png');
}
.itenary div.tunnel_yes {
   background-image: url('http://wabson.org/wwroutes/tunnel-start-20.png');
}
.itenary div.tunnel_no {
   background-image: url('http://wabson.org/wwroutes/tunnel-end-20.png');
}
.itenary div.lock_yes, .itenary div.waterway_lock {
   background-image: url('http://wabson.org/wwroutes/lock-20.png');
}
.itenary .yui3-resize-handle {
   background-color: #f0f0f0;
}
.map {
   height: 500px;
   width: auto;
   height: 100%;
   float: right;
}
h1 {
   margin: 0 0 0 0;
   padding: 5px 5px 10px 5px;
}
#bd {
   border-top: 1px solid #cccccc;
}
</style>
 <link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.5/leaflet.css" />
 <!--[if lte IE 8]>
     <link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.5/leaflet.ie.css" />
 <![endif]-->
"""
dist = 0.0
lastname = ""
units = "mi"
print "</head>"
print "<body>"
print '<div id="hd">'
print "<h1>Devices to Westminster Race Itenary</h1>"
print '</div>'
print '<div id="bd">'
print '<div id="itenary" class="itenary"><div>'
print '<table>'
for d in []:
    if d["distance"] < dist + 10 and ((d["distance"] - dist) > 0.04 or lastname != d["name"]):
        print "<tr>"
        print '<td class="dist">'
        if (d["distance"] - dist) > 0.04:
            print "%.1f" % (d["distance"] if units == "km" else d["distance"] * 0.621371192)
        print "</td>"
        print '<td><div class="waypoint %s"><a id="wp_%s_%s" href="http://www.openstreetmap.org/index.html?mlat=%s&mlon=%s&zoom=15&layers=B000FTF">%s</a></div></td>' % (d["otag"].replace('=', '_'), d["way_id"], d["node_id"], d["lat"], d["lon"], d["name"])
        print "</tr>"
        dist = d["distance"]
        lastname = d["name"]
print "</table>"
print '</div></div>'
print '<div class="map" id="map"></div>'
print '</div>'
print """<script src="http://yui.yahooapis.com/3.4.1/build/yui/yui-min.js" type="text/javascript"></script>
<script src="http://cdn.leafletjs.com/leaflet-0.5/leaflet.js"></script>
<script type="text/javascript">
var map = null;
function resizeMap(Y) {
    var mapEl = Y.one('#map'), itEl = Y.one('#itenary'), bdEl = Y.one('#bd'), hdEl = Y.one('#hd');
    mapEl.setStyle("width", bdEl.get('region').width - itEl.get('region').width);
    bdEl.setStyle("height", bdEl.get('winHeight') - hdEl.get('region').height);
    itEl.setStyle("height", bdEl.get('winHeight') - hdEl.get('region').height);
    if (map != null) {
        map.invalidateSize();
    }
}
// Create a YUI sandbox on your page.
YUI().use('node', 'event', 'querystring-parse', 'datasource', 'history', function (Y) {
    // The Node and Event modules are loaded and ready to use.
    // Your code goes here!

    var markers = {};
    var leafletTileUrl= "http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", mapInitialZoom = 15, attribution = "Map data copyright OpenStreetMap contributors";
    var waypoints;

    var iconBlue = L.icon({
        iconUrl: 'http://wabson.org/wwroutes/markers/marker-blue.png',
        shadowUrl: 'http://cdn.leafletjs.com/leaflet-0.3.1/images/marker-shadow.png',
        iconSize: new L.Point(27, 41),
        shadowSize: new L.Point(41, 41),
        iconAnchor: new L.Point(14, 41),
        popupAnchor: new L.Point(0, -33)
    });

    var iconBlack = L.icon({
        iconUrl: 'http://wabson.org/wwroutes/markers/marker-black.png',
        shadowUrl: 'http://cdn.leafletjs.com/leaflet-0.3.1/images/marker-shadow.png',
        iconSize: new L.Point(27, 41),
        shadowSize: new L.Point(41, 41),
        iconAnchor: new L.Point(14, 41),
        popupAnchor: new L.Point(0, -33)
    });

    function loadMap(data) {
        var results = data.response.results, bubblehtml, latlng, marker, tag, name, notes, access;
        resizeMap(Y);
        map = new L.Map('map');
        // create the tile layer with correct attribution
        var osm = new L.TileLayer(leafletTileUrl, {attribution: attribution});
        //var first = Y.one('.waypoint a'), href = first.get('href').split("?")[1], args = Y.QueryString.parse(href);
        var slatlng = new L.LatLng(results[0]['gsx$lat']['$t'], results[0]['gsx$lon']['$t']);
    
        // start the map centred on the icon
        map.setView(slatlng, mapInitialZoom);
        map.addLayer(osm);

        var portageIcon = iconBlue, otherIcon = iconBlack;

        for (var i=0; i<results.length; i++) {
            latlng = new L.LatLng(results[i]['gsx$lat']['$t'], results[i]['gsx$lon']['$t']);
            // create a marker in the given location and add it to the map
            name = results[i]['gsx$name']['$t'];
            notes = results[i]['gsx$notes'] ? results[i]['gsx$notes']['$t'] : "";
            access = results[i]['gsx$access'] ? results[i]['gsx$access']['$t'] : "";
            tag = results[i]['gsx$otag']['$t'];
            marker = new L.Marker(latlng, {icon: tag == "waterway=lock" || tag == "lock=yes" ? portageIcon : otherIcon});
            map.addLayer(marker);
    
            // attach a given HTML content to the marker and immediately open it
            bubblehtml = "<p><strong>" + name + "</strong></p>" + (notes != "" ? ("<p>" + notes + "</p>") : "") + (access != "" ? ("<p>" + access + "</p>") : "");
            marker.bindPopup(bubblehtml, {});
            markers[getWPID(results[i])] = marker;
        }

        Y.on("windowresize", function(e) {
            resizeMap(Y);
        });
    };

    function onHistoryChange(e) {
        var changed = e.changed, removed = e.removed;
        if (changed.wp) {
            var wp = getWaypoint(changed.wp.newVal), latlng = new L.LatLng(wp['gsx$lat']['$t'], wp['gsx$lon']['$t']);
            map.panTo(latlng);
            markers[changed.wp.newVal].openPopup();
        }
    };

    function getWPID(wp) {
        return wp['gsx$nodeid']['$t'];
    };

    function getWaypoint(id) {
        for (var i=0; i<waypoints.length; i++) {
            if (getWPID(waypoints[i]) == id) {
                return waypoints[i];
            }
        }
        return null;
    }

    function populateTable(data) {
        var results = data.response.results, tEl = Y.one('#itenary table'), totalDist = 0, dist = 0, name = "", lastName = "";
        for (var i=0; i<results.length; i++) {
            name = results[i]['gsx$name']['$t'];
            dist = parseFloat(results[i]['gsx$distance']['$t']); // convert to miles
            var displayDist = ((dist - totalDist) > 0.04) ? new Number(dist * 0.621371192).toFixed(1) : '';
            if (dist < totalDist + 10 && ((dist - totalDist) > 0.04 || lastName != name)) {
                var html = '<tr><td class="dist">' + displayDist + '</td><td><div class="waypoint ' + results[i]['gsx$otag']['$t'].replace('=', '_') + '"><a id="wp_' + getWPID(results[i]) + '" href="#">' + name + '</a></div></td></tr>';
                tEl.append(html);
                totalDist = dist;
                lastName = name;
            }
        }
    };

    function ssLoadSuccess(e) {
        populateTable(e);
        loadMap(e);
        waypoints = e.response.results;

        var firstPoint = waypoints[0];
        var history = new Y.HistoryHash({
          initialState: {
            wp: getWPID(firstPoint)
          }
        });

        var links = Y.all('.waypoint a');
        links.on('click', function (e) {
            // Stop the event's default behavior
            e.preventDefault();
        
            // Stop the event from bubbling up the DOM tree
            e.stopPropagation();

            var wpid = e.target.get("id").replace('wp_', '');
            history.addValue('wp', wpid);

        });
        links.each(function (el) {
            var wpid = el.get("id").replace('wp_', '');
            markers[wpid].on('click', function(e) {
                history.addValue('wp', wpid);
            });
        });
    };

    var ssId = "0AsA0SXNo_BkZdEpya2FNTTEtWUhNSGJLVkxUNVYxQkE", sheetId = "od6";

    var myDataSource = new Y.DataSource.Get({
        source: "http://spreadsheets.google.com/feeds/list/" + ssId + "/" + sheetId + "/public/values?alt=json-in-script"
    });
    // Normalize the data sent to myCallback
    myDataSource.plug({fn: Y.Plugin.DataSourceJSONSchema, cfg: {
        schema: {
            resultListLocator: "feed.entry",
            resultFields: ["gsx$name", "gsx$distance", "gsx$lat", "gsx$lon", "gsx$otype", "gsx$nodeid", "gsx$wayid", "gsx$otag", "gsx$notes", "gsx$access"]
        }
    }});
    myDataSource.sendRequest({
        request: "",
        callback: {
            success: function(e){
                ssLoadSuccess(e);
            },
            failure: function(e){
                alert(e.error.message);
            }
        }
    });

    Y.on('history:change', onHistoryChange);
});

YUI().use('overlay', 'resize-plugin', function(Y) {
    var resize = new Y.Resize({
        node: '#itenary',
        preserveRatio: false,
        wrap: false,
        maxWidth: 600,
        handles: 'r'
    });
    resize.on('resize:resize', function(event) {
       //this function will be called on resize.
       resizeMap(Y);
    });
/*
    var overlay = new Y.Overlay({
       width: "280px",
       height: "100%",
       srcNode: "#itenary",
       visible: "true"
    });
    //Plug in the resizability plugin
    overlay.plug(Y.Plugin.Resize);
    overlay.render();
    overlay.resize.on('resize:resize', function(event) {
       //this function will be called on resize. 
       resizeMap(Y);
    });
*/
});
</script>
</body>"""
print "</html>"