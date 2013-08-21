import scraperwiki
import sys
import urllib
import lxml.etree
import re
import datetime

wikipedia_utils = scraperwiki.swimport("wikipedia_utils")

nowtime = datetime.datetime.now()

def UpdateCategory():
    ldata = wikipedia_utils.GetWikipediaCategoryRecurse("Lists_of_Prime_Ministers_of_the_United_Kingdom")
       
    #for data in ldata:
    #    data["updatedate"] = nowtime
    scraperwiki.sqlite.save(["title"], ldata, "cavepages")
    #scraperwiki.sqlite.execute("delete from cavepages where updatedate<>?", nowtime.isoformat())

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
        data = dict(res["templates"]).get("Infobox officeholder")
        if not data:
            continue
        data["title"] = pdata["title"]
        data["link"] = pdata["link"]
        for k, v in data.items():
            if type(k) == int or not v or not re.match("[\w\s_\d]-+$", k):
                del data[k]
        for k in ["length_metres", "depth_metres", "altitude_metres", "location_lat", "location_lon"]:
            if k in data:
                data[k] = float(data[k])
        print data
        ldata.append(data)
    scraperwiki.sqlite.save(["title"], ldata, "caveinfo")
    


UpdateCategory()
#ExtractInfo()

