import scraperwiki
import sys
import urllib
import lxml.etree
import re
import datetime

wikipedia_utils = scraperwiki.swimport("wikipedia_utils")

nowtime = datetime.datetime.now()

#modifications
#first iteration create table
#second iteration comment out create table
#further iterations comment out updatecategory()

#scraperwiki.sqlite.execute("create table cavepages (lastrevid string, pageid string, title string, counter string, #length int, link string, touched string, ns string, updatedate string)")


def UpdateCategory():
    ldata = wikipedia_utils.GetWikipediaCategoryRecurse("Caves_of_the_United_Kingdom")
    for data in ldata:
        data["updatedate"] = nowtime
    scraperwiki.sqlite.save(["title"], ldata, "cavepages")
    scraperwiki.sqlite.execute("delete from cavepages where updatedate<>?", nowtime.isoformat())

def ExtractInfo():
    rdata = scraperwiki.sqlite.select("title, link from cavepages")
    ldata = [ ]
    for pdata in rdata:
        try:
            val = wikipedia_utils.GetWikipediaPage(pdata["title"])
        except IOError:
            print "Skipping", pdata["title"]
            continue
        res = wikipedia_utils.ParseTemplates(val["text"])
        #print dict(res["templates"]).keys()
        data = dict(res["templates"]).get("Infobox ukcave")
        if not data:
            continue
        data["title"] = pdata["title"]
        data["link"] = pdata["link"]
        for k, v in data.items():
            if type(k) == int or not v or not re.match("[\w\s_\d]+$", k):
                del data[k]
        for k in ["length_metres", "depth_metres", "altitude_metres", "location_lat", "location_lon"]:
            if k in data:
                data[k] = float(data[k])
        print data
        ldata.append(data)
    scraperwiki.sqlite.save(["title"], ldata, "caveinfo")
    


#UpdateCategory()
ExtractInfo()

