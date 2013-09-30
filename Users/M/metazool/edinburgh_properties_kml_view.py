# quicker this way?
# request for spatial indexing and inbuilt kml handling

import scraperwiki
scraperwiki.sqlite.attach("commercial_property_in_edinburgh")

ents = scraperwiki.sqlite.select("lat, lng, alt, name from ents")

scraperwiki.utils.httpresponseheader("Content-Type", "application/vnd.google-earth.kml+xml")

print """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">"""
print "<Document>"
for ent in ents:
    print """<Placemark>
    <name>%s</name>""" % ent["name"]
    print """<Point>
      <coordinates>%f,%f,%f</coordinates>
    </Point>
    </Placemark>""" % (ent["lng"], ent["lat"], ent["alt"])

print """</Document></kml>"""


## quicker this way?
# request for spatial indexing and inbuilt kml handling

import scraperwiki
scraperwiki.sqlite.attach("commercial_property_in_edinburgh")

ents = scraperwiki.sqlite.select("lat, lng, alt, name from ents")

scraperwiki.utils.httpresponseheader("Content-Type", "application/vnd.google-earth.kml+xml")

print """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">"""
print "<Document>"
for ent in ents:
    print """<Placemark>
    <name>%s</name>""" % ent["name"]
    print """<Point>
      <coordinates>%f,%f,%f</coordinates>
    </Point>
    </Placemark>""" % (ent["lng"], ent["lat"], ent["alt"])

print """</Document></kml>"""


#