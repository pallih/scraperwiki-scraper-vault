import scraperwiki
import urllib
import random

sourcescraper = "schulen-berlin-de_2"

query_args = scraperwiki.utils.GET()

if 'kml' in query_args:
    scraperwiki.sqlite.attach(sourcescraper)
    
    sql_query = "* FROM schule WHERE lat IS NOT NULL AND lon IS NOT NULL" + ("" if not 'where' in query_args else " AND " + urllib.unquote(query_args['where']))
    SCHULEN = [scraperwiki.sqlite.select(sql_query)[0]]
    print SCHULEN

    scraperwiki.utils.httpresponseheader("Content-Type", "application/vnd.google-earth.kml+xml")
    kml = '''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
    <Document>'''
    for item in SCHULEN:
        kml += '''
        <Placemark>
            <name>''' + item['SchulName'] + '''</name>
            <description></description>
            <Point>
                <coordinates>''' + str(item['lon']) + ',' + str(item['lat']) + ''',0</coordinates>
            </Point>
        </Placemark>'''
    kml += '''
    </Document>
</kml>'''
    print kml

elif 'georss' in query_args:
    print

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
        </style>
        <script type="text/javascript">
            function initialize() {
                var myOptions = {
                    zoom: 12,
                    center: new google.maps.LatLng(52.5, 13.4),
                    mapTypeId: google.maps.MapTypeId.ROADMAP
                };
                var map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
    
                var ctaLayer = new google.maps.KmlLayer("https://views.scraperwiki.com/run/schulen-berlin-de-view-map/?'''+("" if not 'where' in query_args else "where="+urllib.quote(query_args['where'])+"&")+str(random.randint(100, 999))+'''&kml=1");
                ctaLayer.setMap(map);
            }

            function loadScript() {
              var script = document.createElement("script");
              script.type = "text/javascript";
              script.src = "https://maps.googleapis.com/maps/api/js?v=3&sensor=false&callback=initialize";
              document.body.appendChild(script);
            }
              
            window.onload = loadScript;
        </script>
    </head>
    <body>
        <div id="map_canvas" style="width:100%; height:100%"></div>
    </body>
</html>'''