import numpy
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.cbook as cbook
import matplotlib.ticker as ticker

import scraperwiki
import sys
import base64
import StringIO

import urllib
import tempfile
import cgi
import os

def LoadRecordsUsingApi(name, sql, apikey):
    apiurl = "https://api.scraperwiki.com/api/1.0/datastore/sqlite"
    qdata = {"format":"csv", "name":name, "query":sql}
    if apikey:
        qdata["apikey"] = apikey
    fin = urllib.urlopen("%s?%s"% (apiurl, urllib.urlencode(qdata)))
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
name = qs.get("name", "lichfield_district_council_fixmystreet_reports")
sql = qs.get("sql", "select substr(`requested`, 0, 8) as x, count(*) as y from swdata group by x order by x limit 90")
title = qs.get("title", "FixMyStreet reports by month")
format = qs.get("format", "png")   # png or svg
dpi = int(qs.get("dpi", 70))

r = LoadRecordsUsingApi(name, sql, qs.get("apikey", ""))
#r = LoadRecordsUsingAttach(name, sql)

# generate the image
fig = plt.figure()
ax = fig.add_subplot(111)     # don't know what this does
ax.plot(r.x, r.y, 'o-')  # what is o-? [drj: o: circle marker; -: solid line]
labels = ax.get_xticklabels() 
for label in labels: 
    label.set_rotation(30) 
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


