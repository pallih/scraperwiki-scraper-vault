import scraperwiki
import urllib

unquote = urllib.unquote
sourcescraper = "schulen-berlin-de-new"

query_args = scraperwiki.utils.GET()

kml_args = "?kml=1"
sql_query = " FROM schule WHERE lat IS NOT NULL AND lon IS NOT NULL"

if 'where' in query_args:
    kml_args += "&where=" + unquote(query_args['where'])
    sql_query += " AND " + unquote(query_args['where'])
if 'SchulNr' in query_args:
    kml_args += "&SchulNr=" + unquote(query_args['SchulNr'])
    sql_query += " AND SchulNr='" + unquote(query_args['SchulNr']) + "' group by SchulNr"
elif 'IDSchulzweig' in query_args:
    kml_args += "&IDSchulzweig=" + unquote(query_args['IDSchulzweig'])
    sql_query += " AND IDSchulzweig=" + unquote(query_args['IDSchulzweig'])

if 'kml' in query_args:
    scraperwiki.sqlite.attach(sourcescraper)

    SCHULEN = scraperwiki.sqlite.select("IDSchulzweig, SchulName, lon, lat" + sql_query)

    url = "http://www.berlin.de/sen/bildung/schulverzeichnis_und_portraets/anwendung/Schulportrait.aspx?IDSchulzweig="

    scraperwiki.utils.httpresponseheader("Content-Type", "application/vnd.google-earth.kml+xml")

    kml_start = '''<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2"><Document>\n'''
    kml_item = '''<Placemark><name>%s</name><description>%s</description><Point><coordinates>%f, %f, 0</coordinates></Point></Placemark>\n'''
    kml_end = '''</Document></kml>'''

    kml_result = [kml_start] + [kml_item % (x['SchulName'], url+str(x['IDSchulzweig']), x['lon'], x['lat']) for x in SCHULEN] + [kml_end]
    print "".join(kml_result)

else:
    print '''<!DOCTYPE html>
<html>
    <head>
        <title></title>
        <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
        <style type="text/css">
            html {
                height: 100%
            }
            body {
                height: 100%;
                margin: 0;
                padding: 0
            }
            #scraperwikipane {
                display: none !important
            }
        </style>
        <script src="https://maps.googleapis.com/maps/api/js?v=3&sensor=false"></script>
        <script src="http://openlayers.org/api/OpenLayers.js"></script>
        <script type="text/javascript">
            function init() {
                map = new OpenLayers.Map({
                    div: "map",
                    units: "m",
                });
    
                var osm = new OpenLayers.Layer.OSM();            
                var gmap = new OpenLayers.Layer.Google("Google Streets");
    
                var schools = new OpenLayers.Layer.Vector("Schulen", {
                    projection: map.displayProjection,
                    strategies: [new OpenLayers.Strategy.Fixed()],
                    protocol: new OpenLayers.Protocol.HTTP({
                        url: "https://views.scraperwiki.com/run/schulen-berlin-de-view-map_1/'''+kml_args+'''",
                        format: new OpenLayers.Format.KML({
                            extractStyles: true,
                            extractAttributes: true
                        }),
                    })
                });
    
                map.addLayers([gmap, osm, schools]);
                map.addControl(new OpenLayers.Control.LayerSwitcher());
                map.setCenter(
                    new OpenLayers.LonLat(13.398889, 52.500556).transform(
                        new OpenLayers.Projection("EPSG:4326"),
                        map.getProjectionObject()
                    ), 12
                );

                select = new OpenLayers.Control.SelectFeature(schools);
            
                schools.events.on({
                    "featureselected": onFeatureSelect,
                    "featureunselected": onFeatureUnselect,
                    "loadend": adjustZoom
                });
     
                map.addControl(select);
                select.activate();   
            }

            function adjustZoom(event) {
                map.zoomToExtent(event.object.getDataExtent());
            }

            function onPopupClose(evt) {
                select.unselectAll();
            }

            function onFeatureSelect(event) {
                var feature = event.feature;
                var content = "<h2>"+feature.attributes.name + "</h2>" +
                    "<a href="+feature.attributes.description+" target='_blank'>"+feature.attributes.description+"</a>";
                popup = new OpenLayers.Popup.FramedCloud("chicken", 
                                         feature.geometry.getBounds().getCenterLonLat(),
                                         new OpenLayers.Size(100,100),
                                         content,
                                         null, true, onPopupClose);
                feature.popup = popup;
                map.addPopup(popup);
            }

            function onFeatureUnselect(event) {
                var feature = event.feature;
                if(feature.popup) {
                    map.removePopup(feature.popup);
                    feature.popup.destroy();
                    delete feature.popup;
                }
            }

        </script>
    </head>
    <body onload="init()">
        <div style="width:100%; height:100%" id="map"></div>
    </body>
</html>'''
import scraperwiki
import urllib

unquote = urllib.unquote
sourcescraper = "schulen-berlin-de-new"

query_args = scraperwiki.utils.GET()

kml_args = "?kml=1"
sql_query = " FROM schule WHERE lat IS NOT NULL AND lon IS NOT NULL"

if 'where' in query_args:
    kml_args += "&where=" + unquote(query_args['where'])
    sql_query += " AND " + unquote(query_args['where'])
if 'SchulNr' in query_args:
    kml_args += "&SchulNr=" + unquote(query_args['SchulNr'])
    sql_query += " AND SchulNr='" + unquote(query_args['SchulNr']) + "' group by SchulNr"
elif 'IDSchulzweig' in query_args:
    kml_args += "&IDSchulzweig=" + unquote(query_args['IDSchulzweig'])
    sql_query += " AND IDSchulzweig=" + unquote(query_args['IDSchulzweig'])

if 'kml' in query_args:
    scraperwiki.sqlite.attach(sourcescraper)

    SCHULEN = scraperwiki.sqlite.select("IDSchulzweig, SchulName, lon, lat" + sql_query)

    url = "http://www.berlin.de/sen/bildung/schulverzeichnis_und_portraets/anwendung/Schulportrait.aspx?IDSchulzweig="

    scraperwiki.utils.httpresponseheader("Content-Type", "application/vnd.google-earth.kml+xml")

    kml_start = '''<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2"><Document>\n'''
    kml_item = '''<Placemark><name>%s</name><description>%s</description><Point><coordinates>%f, %f, 0</coordinates></Point></Placemark>\n'''
    kml_end = '''</Document></kml>'''

    kml_result = [kml_start] + [kml_item % (x['SchulName'], url+str(x['IDSchulzweig']), x['lon'], x['lat']) for x in SCHULEN] + [kml_end]
    print "".join(kml_result)

else:
    print '''<!DOCTYPE html>
<html>
    <head>
        <title></title>
        <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
        <style type="text/css">
            html {
                height: 100%
            }
            body {
                height: 100%;
                margin: 0;
                padding: 0
            }
            #scraperwikipane {
                display: none !important
            }
        </style>
        <script src="https://maps.googleapis.com/maps/api/js?v=3&sensor=false"></script>
        <script src="http://openlayers.org/api/OpenLayers.js"></script>
        <script type="text/javascript">
            function init() {
                map = new OpenLayers.Map({
                    div: "map",
                    units: "m",
                });
    
                var osm = new OpenLayers.Layer.OSM();            
                var gmap = new OpenLayers.Layer.Google("Google Streets");
    
                var schools = new OpenLayers.Layer.Vector("Schulen", {
                    projection: map.displayProjection,
                    strategies: [new OpenLayers.Strategy.Fixed()],
                    protocol: new OpenLayers.Protocol.HTTP({
                        url: "https://views.scraperwiki.com/run/schulen-berlin-de-view-map_1/'''+kml_args+'''",
                        format: new OpenLayers.Format.KML({
                            extractStyles: true,
                            extractAttributes: true
                        }),
                    })
                });
    
                map.addLayers([gmap, osm, schools]);
                map.addControl(new OpenLayers.Control.LayerSwitcher());
                map.setCenter(
                    new OpenLayers.LonLat(13.398889, 52.500556).transform(
                        new OpenLayers.Projection("EPSG:4326"),
                        map.getProjectionObject()
                    ), 12
                );

                select = new OpenLayers.Control.SelectFeature(schools);
            
                schools.events.on({
                    "featureselected": onFeatureSelect,
                    "featureunselected": onFeatureUnselect,
                    "loadend": adjustZoom
                });
     
                map.addControl(select);
                select.activate();   
            }

            function adjustZoom(event) {
                map.zoomToExtent(event.object.getDataExtent());
            }

            function onPopupClose(evt) {
                select.unselectAll();
            }

            function onFeatureSelect(event) {
                var feature = event.feature;
                var content = "<h2>"+feature.attributes.name + "</h2>" +
                    "<a href="+feature.attributes.description+" target='_blank'>"+feature.attributes.description+"</a>";
                popup = new OpenLayers.Popup.FramedCloud("chicken", 
                                         feature.geometry.getBounds().getCenterLonLat(),
                                         new OpenLayers.Size(100,100),
                                         content,
                                         null, true, onPopupClose);
                feature.popup = popup;
                map.addPopup(popup);
            }

            function onFeatureUnselect(event) {
                var feature = event.feature;
                if(feature.popup) {
                    map.removePopup(feature.popup);
                    feature.popup.destroy();
                    delete feature.popup;
                }
            }

        </script>
    </head>
    <body onload="init()">
        <div style="width:100%; height:100%" id="map"></div>
    </body>
</html>'''
