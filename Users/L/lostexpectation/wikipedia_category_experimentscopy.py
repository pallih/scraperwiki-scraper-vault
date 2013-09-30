import scraperwiki
import sys
import urllib
import lxml.etree
import re

wikipedia_utils = scraperwiki.swimport("wikipedia_utils")
#name = 
def ExtractCategory(category):
    categorycave = wikipedia_utils.GetWikipediaCategoryRecurse(category)
    ldata = [ ]
    timestamps = [ ]
    for data in categorycave:
        data["link"] = "http://en.wikipedia.org/wiki/%s" % data["name"].replace(" ", "_")

        if data["name"][:5] != "File:":
           ldata.append(data)
           timestamps.append(data["timestamp"])
    scraperwiki.sqlite.execute("drop table if exists `%s`" % category)
    scraperwiki.sqlite.save(["name", "category"], ldata, category)
        # must be some way of noting the timestamps as they come through and know what's advanced 
        # (poss saving in spare table what needs to be done)

def ExtractCatInfobox(category, infobox):
    rdata = scraperwiki.sqlite.select("* from %s order by timestamp desc limit 5000" % category)
    print "Iterating through %d pages" % len(rdata)
    for d in rdata:
        try:
            val = wikipedia_utils.GetWikipediaPage(d["name"])
        except IOError:
            print "Failed on", d
            continue
        res = wikipedia_utils.ParseTemplates(val["text"])
        data = dict(res["templates"]).get(infobox.replace("_", " "))
        print d["name"], data
        if not data:
            continue

        for k, v in data.items():
            if type(k) == int or not v or not re.match("[\w\s_\d]+$", k):
                del data[k]

        data["oname"] = d["name"]
        data["category"] = d["category"]
        data["link"] = d["link"]
        for k in ["length_metres", "depth_metres", "altitude_metres", "location_lat", "location_lon"]:
            if k in data:
                data[k] = float(data[k])
        scraperwiki.sqlite.save(["oname", "category"], data, infobox)

import urllib
print urllib.quote("á é")

ExtractCategory("Caves_of_the_United_Kingdom")
ExtractCatInfobox("Caves_of_the_United_Kingdom", "Infobox_ukcave")
#name = 

val = wikipedia_utils.GetWikipediaPage("Ireby Fell Cavern")
#print val["text"]
#print wikipedia_utils.GetWikipediaCategory("Physics")
#print wikipedia_utils.GetWikipediaCategory("United_Kingdom_historical_constituency_stubs")
#print wikipedia_utils.GetWikipediaCategory("Constituencies_in_the_United_Kingdom")

sys.exit(0)
res = wikipedia_utils.ParseTemplates(val["text"])
print "Categories", res["categories"]
print "Images", res["images"]
print "Links", res["links"]
for templ in res["templates"]:
    print templ[0], templ
print res["flattext"]
import scraperwiki
import sys
import urllib
import lxml.etree
import re

wikipedia_utils = scraperwiki.swimport("wikipedia_utils")
#name = 
def ExtractCategory(category):
    categorycave = wikipedia_utils.GetWikipediaCategoryRecurse(category)
    ldata = [ ]
    timestamps = [ ]
    for data in categorycave:
        data["link"] = "http://en.wikipedia.org/wiki/%s" % data["name"].replace(" ", "_")

        if data["name"][:5] != "File:":
           ldata.append(data)
           timestamps.append(data["timestamp"])
    scraperwiki.sqlite.execute("drop table if exists `%s`" % category)
    scraperwiki.sqlite.save(["name", "category"], ldata, category)
        # must be some way of noting the timestamps as they come through and know what's advanced 
        # (poss saving in spare table what needs to be done)

def ExtractCatInfobox(category, infobox):
    rdata = scraperwiki.sqlite.select("* from %s order by timestamp desc limit 5000" % category)
    print "Iterating through %d pages" % len(rdata)
    for d in rdata:
        try:
            val = wikipedia_utils.GetWikipediaPage(d["name"])
        except IOError:
            print "Failed on", d
            continue
        res = wikipedia_utils.ParseTemplates(val["text"])
        data = dict(res["templates"]).get(infobox.replace("_", " "))
        print d["name"], data
        if not data:
            continue

        for k, v in data.items():
            if type(k) == int or not v or not re.match("[\w\s_\d]+$", k):
                del data[k]

        data["oname"] = d["name"]
        data["category"] = d["category"]
        data["link"] = d["link"]
        for k in ["length_metres", "depth_metres", "altitude_metres", "location_lat", "location_lon"]:
            if k in data:
                data[k] = float(data[k])
        scraperwiki.sqlite.save(["oname", "category"], data, infobox)

import urllib
print urllib.quote("á é")

ExtractCategory("Caves_of_the_United_Kingdom")
ExtractCatInfobox("Caves_of_the_United_Kingdom", "Infobox_ukcave")
#name = 

val = wikipedia_utils.GetWikipediaPage("Ireby Fell Cavern")
#print val["text"]
#print wikipedia_utils.GetWikipediaCategory("Physics")
#print wikipedia_utils.GetWikipediaCategory("United_Kingdom_historical_constituency_stubs")
#print wikipedia_utils.GetWikipediaCategory("Constituencies_in_the_United_Kingdom")

sys.exit(0)
res = wikipedia_utils.ParseTemplates(val["text"])
print "Categories", res["categories"]
print "Images", res["images"]
print "Links", res["links"]
for templ in res["templates"]:
    print templ[0], templ
print res["flattext"]
import scraperwiki
import sys
import urllib
import lxml.etree
import re

wikipedia_utils = scraperwiki.swimport("wikipedia_utils")
#name = 
def ExtractCategory(category):
    categorycave = wikipedia_utils.GetWikipediaCategoryRecurse(category)
    ldata = [ ]
    timestamps = [ ]
    for data in categorycave:
        data["link"] = "http://en.wikipedia.org/wiki/%s" % data["name"].replace(" ", "_")

        if data["name"][:5] != "File:":
           ldata.append(data)
           timestamps.append(data["timestamp"])
    scraperwiki.sqlite.execute("drop table if exists `%s`" % category)
    scraperwiki.sqlite.save(["name", "category"], ldata, category)
        # must be some way of noting the timestamps as they come through and know what's advanced 
        # (poss saving in spare table what needs to be done)

def ExtractCatInfobox(category, infobox):
    rdata = scraperwiki.sqlite.select("* from %s order by timestamp desc limit 5000" % category)
    print "Iterating through %d pages" % len(rdata)
    for d in rdata:
        try:
            val = wikipedia_utils.GetWikipediaPage(d["name"])
        except IOError:
            print "Failed on", d
            continue
        res = wikipedia_utils.ParseTemplates(val["text"])
        data = dict(res["templates"]).get(infobox.replace("_", " "))
        print d["name"], data
        if not data:
            continue

        for k, v in data.items():
            if type(k) == int or not v or not re.match("[\w\s_\d]+$", k):
                del data[k]

        data["oname"] = d["name"]
        data["category"] = d["category"]
        data["link"] = d["link"]
        for k in ["length_metres", "depth_metres", "altitude_metres", "location_lat", "location_lon"]:
            if k in data:
                data[k] = float(data[k])
        scraperwiki.sqlite.save(["oname", "category"], data, infobox)

import urllib
print urllib.quote("á é")

ExtractCategory("Caves_of_the_United_Kingdom")
ExtractCatInfobox("Caves_of_the_United_Kingdom", "Infobox_ukcave")
#name = 

val = wikipedia_utils.GetWikipediaPage("Ireby Fell Cavern")
#print val["text"]
#print wikipedia_utils.GetWikipediaCategory("Physics")
#print wikipedia_utils.GetWikipediaCategory("United_Kingdom_historical_constituency_stubs")
#print wikipedia_utils.GetWikipediaCategory("Constituencies_in_the_United_Kingdom")

sys.exit(0)
res = wikipedia_utils.ParseTemplates(val["text"])
print "Categories", res["categories"]
print "Images", res["images"]
print "Links", res["links"]
for templ in res["templates"]:
    print templ[0], templ
print res["flattext"]
import scraperwiki
import sys
import urllib
import lxml.etree
import re

wikipedia_utils = scraperwiki.swimport("wikipedia_utils")
#name = 
def ExtractCategory(category):
    categorycave = wikipedia_utils.GetWikipediaCategoryRecurse(category)
    ldata = [ ]
    timestamps = [ ]
    for data in categorycave:
        data["link"] = "http://en.wikipedia.org/wiki/%s" % data["name"].replace(" ", "_")

        if data["name"][:5] != "File:":
           ldata.append(data)
           timestamps.append(data["timestamp"])
    scraperwiki.sqlite.execute("drop table if exists `%s`" % category)
    scraperwiki.sqlite.save(["name", "category"], ldata, category)
        # must be some way of noting the timestamps as they come through and know what's advanced 
        # (poss saving in spare table what needs to be done)

def ExtractCatInfobox(category, infobox):
    rdata = scraperwiki.sqlite.select("* from %s order by timestamp desc limit 5000" % category)
    print "Iterating through %d pages" % len(rdata)
    for d in rdata:
        try:
            val = wikipedia_utils.GetWikipediaPage(d["name"])
        except IOError:
            print "Failed on", d
            continue
        res = wikipedia_utils.ParseTemplates(val["text"])
        data = dict(res["templates"]).get(infobox.replace("_", " "))
        print d["name"], data
        if not data:
            continue

        for k, v in data.items():
            if type(k) == int or not v or not re.match("[\w\s_\d]+$", k):
                del data[k]

        data["oname"] = d["name"]
        data["category"] = d["category"]
        data["link"] = d["link"]
        for k in ["length_metres", "depth_metres", "altitude_metres", "location_lat", "location_lon"]:
            if k in data:
                data[k] = float(data[k])
        scraperwiki.sqlite.save(["oname", "category"], data, infobox)

import urllib
print urllib.quote("á é")

ExtractCategory("Caves_of_the_United_Kingdom")
ExtractCatInfobox("Caves_of_the_United_Kingdom", "Infobox_ukcave")
#name = 

val = wikipedia_utils.GetWikipediaPage("Ireby Fell Cavern")
#print val["text"]
#print wikipedia_utils.GetWikipediaCategory("Physics")
#print wikipedia_utils.GetWikipediaCategory("United_Kingdom_historical_constituency_stubs")
#print wikipedia_utils.GetWikipediaCategory("Constituencies_in_the_United_Kingdom")

sys.exit(0)
res = wikipedia_utils.ParseTemplates(val["text"])
print "Categories", res["categories"]
print "Images", res["images"]
print "Links", res["links"]
for templ in res["templates"]:
    print templ[0], templ
print res["flattext"]
