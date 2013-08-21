# Blank Python
import os, scraperwiki, cgi
from operator import itemgetter
from geopy import distance
sourcescraper = 'stratford_b-and-b'
scraperwiki.sqlite.attach(sourcescraper)
query = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))

# def numcoord(s):
#     return map(float,(s['coords'][1:-1].split(',')))

if not query:
    print "add ?postcode=SW1A+1AA to end of string"
    exit()
else:
    pos=scraperwiki.geo.gb_postcode_to_latlng(query['postcode'])
    data = scraperwiki.sqlite.select(           
    '''* from swdata'''
    )
    for line in data:
        line['dist']=distance.distance(pos,(line['xcoord'],line['ycoord'])).miles

    data.sort(key=itemgetter('dist')) 

    print """<!DOCTYPE html>
    <html>
    <head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
    <style type="text/css">
      html { height: 100% }
      body { height: 100%; margin: 0; padding: 0 }
      #map_canvas { height: 50}
    </style>
    <script type="text/javascript"
      src="http://maps.googleapis.com/maps/api/js?key=AIzaSyDUjfQ_C5v59iu4OjbZ70BRc9FTGQv2nzU&sensor=false">
    </script>
    <script type="text/javascript">
      function initialize() {
        
    var myOptions = {
        center: new google.maps.LatLng"""+str(pos)+""",
        zoom: 12,
        mapTypeId: google.maps.MapTypeId.ROADMAP
        };

    var map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
    var marker=0
    """

    # add markers

    for line in data:
        print """   marker = new google.maps.Marker({
        position: new google.maps.LatLng(%s,%s),
        map: map,
        title:"%s"
    });

    google.maps.event.addListener(marker, 'click', function() {
        new google.maps.InfoWindow({
        content: "<a href='http://www.discover-stratford.com/%s'>%s</a>"
        }).open(map,marker);
    });"""%(str(line['xcoord']),str(line['ycoord']),line['title'], line['url'],line['title'])



    print"""  }
    </script>
    </head>
    <body onload="initialize()">
    <h1>Closest B&B's to %s</h1>
    """ % query['postcode']

    print "<table>"

    # annotate with distances


    for line in data[:10]:
        print "<tr>"
        print "<td><a href='http://discover-stratford.com/%s'>%s</a></td><td>%s miles</td><td></td>" % (line['url'],line['title'],round(line['dist'],2))
    
        print "</tr>"
    print "<table>"

    print """<div id="map_canvas" style="width:50%; height:50%"></div>
             </body>
             </html>"""