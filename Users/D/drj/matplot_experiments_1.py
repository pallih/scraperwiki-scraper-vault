# Forked by drj

import numpy
# see http://www.scipy.org/Cookbook/Matplotlib/Maps
# from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.cbook as cbook
import matplotlib.ticker as ticker

import scraperwiki

import math
import sys
import base64
import StringIO

import urllib
import tempfile
import cgi
import os

print scraperwiki.utils.GET()

def LoadRecordsUsingApi(name, sql):
    apiurl = "https://api.scraperwiki.com/api/1.0/datastore/sqlite"
    fin = urllib.urlopen("%s?%s"% (apiurl, urllib.urlencode({"format":"csv", "name":name, "query":sql})))
    csv = StringIO.StringIO()
    csv.write(fin.read())
    csv.seek(0)
    return mlab.csv2rec(csv)

def LoadRecordsUsingAttach(name, sql):
    scraperwiki.sqlite.attach(name, 'src')
    tdata = scraperwiki.sqlite.execute(sql)
        # if we had formats list we could use recarray which has its own type system
    return numpy.rec.fromrecords(tdata["data"], names=tdata["keys"])  


# get the attributes (with defaults)
qs = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))
name = qs.get("name", "drj's plot")
sql = qs.get("sql", "select substr(`Spud Date`, 0, 5) as x, count(*) as y from wellpages group by x order by x limit 90")
title = qs.get("title", name)
format = qs.get("format", "png")   # png or svg
dpi = int(qs.get("dpi", 70))

if 0: r = LoadRecordsUsingApi(name, sql)
#r = LoadRecordsUsingAttach(name, sql)


# generate the image
fig = plt.figure()
ax = fig.add_subplot(111)     # don't know what this does [drj: It's for multiple subplots in one image, see http://matplotlib.sourceforge.net/users/pyplot_tutorial.html#working-with-multiple-figures-and-axes]
ax.plot(range(10), [math.sin(x) for x in range(10)], 'o-')
ax.set_title(title)


#produce the binary image.  the decoding into binary is done out in django
cout = StringIO.StringIO()
plt.savefig(cout, format=format, dpi=dpi)
if format == "svg":
    scraperwiki.utils.httpresponseheader("Content-Type", "image/svg+xml")
    scraperwiki.dumpMessage({"content":cout.getvalue(), "message_type":"console"})
else:
    scraperwiki.utils.httpresponseheader("Content-Type", "image/%s" % format)
    scraperwiki.dumpMessage({"content":base64.encodestring(cout.getvalue()), "message_type":"console", "encoding":"base64"})


