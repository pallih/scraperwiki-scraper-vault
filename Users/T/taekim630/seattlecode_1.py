import scraperwiki
import urllib2
import lxml.html
import lxml.etree
import json


# http://data.seattle.gov/api/docs
# http://data.seattle.gov/api/docs/views    (search for /api/views/(view ID)/rows )
# http://lxml.de/cssselect.html
# https://scraperwiki.com/editor/raw/tutorial-lxml-html

NUMROWS = 10

codeviolated = scraperwiki.scrape("https://data.seattle.gov/api/views/dk8m-pdjf/rows.xml?max_rows="+str(NUMROWS))
#print codeviolated

root = lxml.html.fromstring(codeviolated)

cases = root.cssselect("row row")

for curr in cases:

    casenum = int(curr.cssselect("case_number")[0].text)
    descriptlist = curr.cssselect("description")
    if len(descriptlist)>0:
        descript = descriptlist[0].text
    else:
        descript = ""
    myloclist = curr.cssselect("location")
    if len(myloclist)>0:
        myloc = myloclist[0]
        print myloc.attrib["latitude"] + " " + myloc.attrib["longitude"]
        mylat = myloc.attrib["latitude"]
        mylong = myloc.attrib["longitude"]
    else:
        mylat = ""
        mylong = ""

    data = {
        'Number': casenum,
        'Lat': mylat,
        'Long': mylong,
        'Description': descript
    }

    scraperwiki.sqlite.save(unique_keys=['Number'],data=data)


#codeviolatedjson = scraperwiki.scrape("https://data.seattle.gov/api/views/dk8m-pdjf/rows.json?max_rows=10")
#print codeviolatedjson
#print json.loads(codeviolatedjson)

