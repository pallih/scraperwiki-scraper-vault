# David Jones, Climate Code Foundation
# 2011-09
# An SVG map in polar orthographic projection.
# By default shows Canada weather station locations (not all of
# which are in Canada).
# But can, by using the 'target' query parameter, select another
# database to display.
# The 'query' parameter can be used to select subsets.

import scraperwiki

import cgi
import json
import math
import os
import urllib
# http://docs.python.org/release/2.4.4/lib/module-xml.sax.saxutils.html
from xml.sax.saxutils import escape as xmlescape

scraperwiki.utils.httpresponseheader('Content-Type', 'image/svg+xml')

qs = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))

# The ScraperWiki database containing the data.
target = qs.get('target', 'canada-temperature-data')

about, = json.load(urllib.urlopen("https://api.scraperwiki.com/api/1.0/scraper/getinfo?" +
    urllib.urlencode(dict(format='jsondict', name=target, version=-1,
        quietfields='datasummary|userroles|runevents|code|history'))))
scrapertitle = about['title']

# Title used in the plot.
title = qs.get('title', scrapertitle)

scale = 300

def xform(lat, lon):
    """Transform Latitude and Longitude into an SVG coordinate system,
    with (0,0) being at the top left (of a notional SVG viewing area),
    and positive x and y being to the right and down.
    
    Polar projection.
    *lat* and *lon* given in degrees.
    """

    x,y,z = xyz(lat,lon)
    # Flip y
    y *= -1
    # Move 0,0 to top left
    x += 1
    y += 1
    # scale
    x,y = [scale*v for v in (x,y)]
    # Offset by half a pixel so that thin lines centred on the pole
    # are one pixel wide.
    x += 0.5
    y += 0.5
    return x,y

def xyz(lat, lon):
    """Transform into (right handed) cartesian coordinates with:
    X axis running through (0,0);
    Y axis running through (0,90);
    Z axis running through (90,0).
    *lat* and *lon* given in degrees.
    """

    z = math.sin(math.radians(lat))
    s = math.cos(math.radians(lat))
    x = math.cos(math.radians(lon))
    y = math.sin(math.radians(lon))
    x,y = [s*v for v in (x,y)]
    return x,y,z

print """
<svg width='999px' height='999px'
      xmlns="http://www.w3.org/2000/svg"
      xmlns:xlink="http://www.w3.org/1999/xlink"
      version="1.1">
"""
print """<defs>
  <style type="text/css">
    .debug { display: none }
    .hidden { display: none }
    g.axes *{ stroke: blue; stroke-width: 1.0; fill: none }
    g.axes *.minor { stroke: blue; stroke-width: 0.35; fill: none }
    g.axes text { stroke: none; fill: black; font-family: Verdana }
    g.data * { stroke: none; fill: black }
    path { stroke: red; stroke-width: 1.4; fill: none }
    text { fill: black; font-family: Verdana }
  </style>
</defs>
"""
def plotaxes(title=None):
    """Plot crosshair and circles at 30N and 60N.  Outputs an
    SVG fragment.
    """
    if title:
        print "<g class='title'>"
        print "<text x='%.1f' y='16' text-anchor='middle'>%s</text>" % (scale*0.5, xmlescape(title))
        print "</g>"
    print "<g class='axes'>"
    # Crosshair at N pole.
    print "<path d='M%.1f %.1fL%.1f %.1f' />" % (xform(0,180) + xform(0,0))
    print "<path d='M%.1f %.1fL%.1f %.1f' />" % (xform(0,-90) + xform(0,+90))
    # Circles at 30N and 60N
    circles = {
        30: 'major',
        40: 'minor',
        50: 'minor',
        60: 'major',
        70: 'minor',
        80: 'minor',
    }
    # Compute radii by using distance between North pole and (somethingN, 0).
    nx,ny = xform(90,0)
    for lat,rank in circles.iteritems():
        radius = math.hypot(*[v-c for v,c in zip(xform(lat,0),(nx,ny))])
        print "<circle class='%s' cx='%.1f' cy='%.1f' r='%.1f' />" % (rank, nx,ny,radius)
    # Labels
    for lat in [k for k,v in circles.items() if v == 'major'] + [90]:
        print "<text x='%.1f' y='%.1f'>%sN</text>" % (xform(lat,90) + (lat,))
    print "</g>"

plotaxes(title=title)
query = qs.get('query', "select * from meta where 0 + Latitude > 0")
print "<g class='hidden query'>%s</g>" % xmlescape(query)
url = "https://api.scraperwiki.com/api/1.0/datastore/sqlite?" + urllib.urlencode(
    dict(format='jsondict',name=target, query=query))
print "<g class='data'>"
for station in json.load(urllib.urlopen(url)):
    lat,lon = [float(station[k]) for k in ('Latitude', 'Longitude')] 
    print "<circle cx='%.1f' cy='%.1f' r='1' />" % xform(lat,lon)
print"</g>"
print "</svg>"
# David Jones, Climate Code Foundation
# 2011-09
# An SVG map in polar orthographic projection.
# By default shows Canada weather station locations (not all of
# which are in Canada).
# But can, by using the 'target' query parameter, select another
# database to display.
# The 'query' parameter can be used to select subsets.

import scraperwiki

import cgi
import json
import math
import os
import urllib
# http://docs.python.org/release/2.4.4/lib/module-xml.sax.saxutils.html
from xml.sax.saxutils import escape as xmlescape

scraperwiki.utils.httpresponseheader('Content-Type', 'image/svg+xml')

qs = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))

# The ScraperWiki database containing the data.
target = qs.get('target', 'canada-temperature-data')

about, = json.load(urllib.urlopen("https://api.scraperwiki.com/api/1.0/scraper/getinfo?" +
    urllib.urlencode(dict(format='jsondict', name=target, version=-1,
        quietfields='datasummary|userroles|runevents|code|history'))))
scrapertitle = about['title']

# Title used in the plot.
title = qs.get('title', scrapertitle)

scale = 300

def xform(lat, lon):
    """Transform Latitude and Longitude into an SVG coordinate system,
    with (0,0) being at the top left (of a notional SVG viewing area),
    and positive x and y being to the right and down.
    
    Polar projection.
    *lat* and *lon* given in degrees.
    """

    x,y,z = xyz(lat,lon)
    # Flip y
    y *= -1
    # Move 0,0 to top left
    x += 1
    y += 1
    # scale
    x,y = [scale*v for v in (x,y)]
    # Offset by half a pixel so that thin lines centred on the pole
    # are one pixel wide.
    x += 0.5
    y += 0.5
    return x,y

def xyz(lat, lon):
    """Transform into (right handed) cartesian coordinates with:
    X axis running through (0,0);
    Y axis running through (0,90);
    Z axis running through (90,0).
    *lat* and *lon* given in degrees.
    """

    z = math.sin(math.radians(lat))
    s = math.cos(math.radians(lat))
    x = math.cos(math.radians(lon))
    y = math.sin(math.radians(lon))
    x,y = [s*v for v in (x,y)]
    return x,y,z

print """
<svg width='999px' height='999px'
      xmlns="http://www.w3.org/2000/svg"
      xmlns:xlink="http://www.w3.org/1999/xlink"
      version="1.1">
"""
print """<defs>
  <style type="text/css">
    .debug { display: none }
    .hidden { display: none }
    g.axes *{ stroke: blue; stroke-width: 1.0; fill: none }
    g.axes *.minor { stroke: blue; stroke-width: 0.35; fill: none }
    g.axes text { stroke: none; fill: black; font-family: Verdana }
    g.data * { stroke: none; fill: black }
    path { stroke: red; stroke-width: 1.4; fill: none }
    text { fill: black; font-family: Verdana }
  </style>
</defs>
"""
def plotaxes(title=None):
    """Plot crosshair and circles at 30N and 60N.  Outputs an
    SVG fragment.
    """
    if title:
        print "<g class='title'>"
        print "<text x='%.1f' y='16' text-anchor='middle'>%s</text>" % (scale*0.5, xmlescape(title))
        print "</g>"
    print "<g class='axes'>"
    # Crosshair at N pole.
    print "<path d='M%.1f %.1fL%.1f %.1f' />" % (xform(0,180) + xform(0,0))
    print "<path d='M%.1f %.1fL%.1f %.1f' />" % (xform(0,-90) + xform(0,+90))
    # Circles at 30N and 60N
    circles = {
        30: 'major',
        40: 'minor',
        50: 'minor',
        60: 'major',
        70: 'minor',
        80: 'minor',
    }
    # Compute radii by using distance between North pole and (somethingN, 0).
    nx,ny = xform(90,0)
    for lat,rank in circles.iteritems():
        radius = math.hypot(*[v-c for v,c in zip(xform(lat,0),(nx,ny))])
        print "<circle class='%s' cx='%.1f' cy='%.1f' r='%.1f' />" % (rank, nx,ny,radius)
    # Labels
    for lat in [k for k,v in circles.items() if v == 'major'] + [90]:
        print "<text x='%.1f' y='%.1f'>%sN</text>" % (xform(lat,90) + (lat,))
    print "</g>"

plotaxes(title=title)
query = qs.get('query', "select * from meta where 0 + Latitude > 0")
print "<g class='hidden query'>%s</g>" % xmlescape(query)
url = "https://api.scraperwiki.com/api/1.0/datastore/sqlite?" + urllib.urlencode(
    dict(format='jsondict',name=target, query=query))
print "<g class='data'>"
for station in json.load(urllib.urlopen(url)):
    lat,lon = [float(station[k]) for k in ('Latitude', 'Longitude')] 
    print "<circle cx='%.1f' cy='%.1f' r='1' />" % xform(lat,lon)
print"</g>"
print "</svg>"
