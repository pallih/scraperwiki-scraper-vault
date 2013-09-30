import scraperwiki
import re
import lxml.html
import datetime

html = scraperwiki.scrape("http://www.marinetraffic.com/ais/shipdetails.aspx?mmsi=311963000")
root = lxml.html.fromstring(html)

el = root.cssselect("div#detailtext a")[2]           
data = el.text
latitude = data.split()[0]
longitude = data.split()[2]

if latitude.startswith('-'):
    latitude = latitude.strip('-') + "S"
else:
    latitude = latitude + "N"

if longitude.startswith('-'):
    longitude = longitude.strip('-') + "W"
else:
    longitude = longitude + "E"

print latitude
print longitude

now = datetime.datetime.now()
localtime = now + datetime.timedelta(hours=1)

print str(localtime)

data = {
    'datestamp': str(localtime),
    'latitude': latitude,
    'longitude': longitude
}

scraperwiki.sqlite.save(unique_keys=['datestamp'], data=data)
import scraperwiki
import re
import lxml.html
import datetime

html = scraperwiki.scrape("http://www.marinetraffic.com/ais/shipdetails.aspx?mmsi=311963000")
root = lxml.html.fromstring(html)

el = root.cssselect("div#detailtext a")[2]           
data = el.text
latitude = data.split()[0]
longitude = data.split()[2]

if latitude.startswith('-'):
    latitude = latitude.strip('-') + "S"
else:
    latitude = latitude + "N"

if longitude.startswith('-'):
    longitude = longitude.strip('-') + "W"
else:
    longitude = longitude + "E"

print latitude
print longitude

now = datetime.datetime.now()
localtime = now + datetime.timedelta(hours=1)

print str(localtime)

data = {
    'datestamp': str(localtime),
    'latitude': latitude,
    'longitude': longitude
}

scraperwiki.sqlite.save(unique_keys=['datestamp'], data=data)
