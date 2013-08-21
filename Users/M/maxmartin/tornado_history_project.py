# Tornado History Project
# Source (tabular data):
#    http://www.tornadohistoryproject.com/


import scraperwiki
import urllib
import lxml.html
import string

html = scraperwiki.scrape("http://www.tornadohistoryproject.com/custom/2725451/source")
print html

root = lxml.html.fromstring(html)

for twister in root.cssselect("table.id='spclines' tr"):
#for hotspots in root.cssselect("th.class tr")
    tds = twister.cssselect("td")

    name = tds[1].text

    print name

#    namelink = tds[0].cssselect("a")[0].attrib['href']
#    location = tds[1].cssselect("a")[0].text
#    loclink = tds[1].cssselect("a")[0].attrib['href']
#    lat = tds[1].cssselect("a")[1].cssselect("span")[2].text
#    lng = tds[1].cssselect("a")[1].cssselect("span")[3].text

#       image =

#    print name
#    print namelink
#    print location
#    print loclink
#    print lat
#    print lng

#    data = {
#        'Hotspot': name,
#        'Details': namelink,
#        'Basin': location,
#        'Details': loclink,
#        'Latitude': lat,
#        'Longitude': lng,     
#    }
#    scraperwiki.sqlite.save(unique_keys=['name'],data=data)

