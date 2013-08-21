import scraperwiki

scraperwiki.sqlite.attach('kennet_avon_canal_itenary')

# Blank Python
sourcescraper = 'kennet_avon_canal_itenary'

data = scraperwiki.sqlite.select( '''* from kennet_avon_canal_itenary.swdata''' )
print "<html>"
print "<head>"
print "<title>Devices to Westminster Race Itenary</title>"
print """
<style type="text/css">
body {
   font-family: Arial, Helvetica, sans-serif;
   font-size: 0.75em;
}
body table {
   font-size: 1em;
}
.itenary {
   border-width: 0px;
   border-style: none;
   border-spacing: 0px;
   padding: 0px;
   margin: 0px 0px 0px 5em;
}
.itenary td {
   border-width: 0px;
   border-style: none;
   padding: 0px;
   margin: 0px;
}
.itenary div {
   background-image: url('http://wabson.org/wwroutes/straight.png');
   background-repeat: no-repeat;
   background-position: top left;
   padding-top: 5px;
   padding-left: 40px;
   margin-left: 8px;
   height: 27px;
}
.itenary div.highway_motorway {
   background-image: url('http://wabson.org/wwroutes/motorway-bridge.png');
}
.itenary div.highway_trunk {
   background-image: url('http://wabson.org/wwroutes/route-primary-bridge.png');
}
.itenary div.highway_primary {
   background-image: url('http://wabson.org/wwroutes/route-primary-bridge.png');
}
.itenary div.highway_secondary {
   background-image: url('http://wabson.org/wwroutes/route-primary-bridge.png');
}
.itenary div.highway_tertiary, .itenary div.highway_unclassified {
   background-image: url('http://wabson.org/wwroutes/route-unclassified-bridge.png');
}
.itenary div.highway_service, .itenary div.highway_residential, .itenary div.highway_bridleway, .itenary div.highway_cycleway, .itenary div.highway_path, .itenary div.highway_footway {
   background-image: url('http://wabson.org/wwroutes/route-path-footway.png');
}
.itenary div.railway_rail {
   background-image: url('http://wabson.org/wwroutes/railway-rail-bridge.png');
}
.itenary div.tunnel_yes {
   background-image: url('http://wabson.org/wwroutes/tunnel-start.png');
}
.itenary div.tunnel_no {
   background-image: url('http://wabson.org/wwroutes/tunnel-end.png');
}
.itenary div.lock_yes, .itenary div.waterway_lock {
   background-image: url('http://wabson.org/wwroutes/lock.png');
}
</style>
"""
dist = 0.0
lastname = ""
units = "mi"
print "</head>"
print "<body>"
print "<h1>Devices to Westminster Race Itenary</h1>"
print '<table class="itenary">'
for d in data:
    if d["distance"] < dist + 10 and ((d["distance"] - dist) > 0.04 or lastname != d["name"]):
        print "<tr>"
        print "<td>"
        if (d["distance"] - dist) > 0.04:
            print "%.1f" % (d["distance"] if units == "km" else d["distance"] * 0.621371192)
        print "</td>"
        print '<td><div class="%s"><a href="http://www.openstreetmap.org/index.html?mlat=%s&mlon=%s&zoom=15&layers=B000FTF">%s</a></div></td>' % (d["otag"].replace('=', '_'), d["lat"], d["lon"], d["name"])
        print "</tr>"
        dist = d["distance"]
        lastname = d["name"]
print "</table>"
print "</body>"
print "</html>"
