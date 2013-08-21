import scraperwiki
from lxml import html
import urllib2
import re
import string
import json
import pprint

pp = pprint.PrettyPrinter(indent=4)
URL = "http://map.usaid.gov/MapData?r=overview&l=&w="
COUNTRY_REGION_URL = "http://map.usaid.gov/MapData?r=projects&l=&w=&p=%s&c=%s"

def fixdata(data):
    newdata = data.lstrip('(')
    newdata = newdata.rstrip(');')
    return newdata

req = urllib2.Request(URL)
webfile = urllib2.urlopen(req)
data = webfile.read()

thedata = json.loads(fixdata(data))

for countryregion in thedata["details"]:
    acountryregion = {}
    acountryregion["total"] = countryregion["total"]
    acountryregion["province"] = countryregion["province"]
    acountryregion["id"] = countryregion["id"]
    acountryregion["country"] = countryregion["country"]
    try:
        req = urllib2.Request(COUNTRY_REGION_URL % (urllib2.quote(countryregion["province"].encode('utf-8').strip()), urllib2.quote(countryregion["country"].encode('utf-8').strip())))
        webfile = urllib2.urlopen(req)
        data = webfile.read()
        theproject_data = json.loads(fixdata(data))
        projects = []
        for project in theproject_data:
            projects.append((project["Id"]).encode('utf-8'))
        acountryregion["projects"] = str(projects)
    # there's one dodgy region name at the moment, just ignore it for now (should really be logged)
    except UnicodeEncodeError:
        pass
    
    pp.pprint(acountryregion)
    scraperwiki.sqlite.save(unique_keys=["id"],
            data=acountryregion)