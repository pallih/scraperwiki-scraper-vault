import scraperwiki
import sys
import urllib
import lxml.etree
import re
import datetime

import lxml.html

urlapi =  "http://en.wikipedia.org/w/api.php"


#wikipedia_utils = scraperwiki.swimport("wikipedia_utils")
#wikipedia_utils = scraperwiki.tagint.swimport("Wikipedia_Utils_myver")

nowtime = datetime.datetime.now()

#modifications
#first iteration create table
#second iteration comment out create table
#further iterations comment out updatecategory()

def DatabaseOps():
    scraperwiki.sqlite.execute("drop table if exists cavepagesgeo")
    #scraperwiki.sqlite.execute("create table cavepagesgeo (lastrevid string, pageid string, title string, counter         #string,length int, link string, touched string, ns string, updatedate string lat_d real long_d real)")
    #scraperwiki.sqlite.execute("create table cavepagesgeo (title string, link string, lat_d real, long_d real)")


def UpdateCategory():
    ldata = wikipedia_utils.GetWikipediaCategoryRecurse("Caves_of_the_United_Kingdom")
    for data in ldata:
        data["updatedate"] = nowtime
    scraperwiki.sqlite.save(["title"], ldata, "cavepagesgeo")
    scraperwiki.sqlite.execute("delete from cavepagesgeo where updatedate<>?", nowtime.isoformat())

def ExtractInfo():
    rdata = scraperwiki.sqlite.select("title, link from cavepagesgeo")
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
        #for k, v in data.items():
            #if type(k) == int or not v or not re.match("[\w\s_\d]+$", k):
            #    del data[k]
        for k in ["length_metres", "depth_metres", "altitude_metres", "location_lat", "location_lon"]:
            if k in data:
                data[k] = float(data[k])
        print data
        ldata.append(data)
    scraperwiki.sqlite.save(["title"], ldata, "caveinfo")


def GetWikipediaCategory(categoryname):
    "Downloads all/some names and metadata of pages in given category"
    params = {"action":"query", "format":"xml", "generator":"categorymembers", "prop":"info", "gcmlimit":100 } 
    #gets full content
    #params = {"action":"query", "format":"xml", "generator":"categorymembers", #"prop":"revisions", "rvprop":"content", "gcmlimit":100 } 
    #gets full content
    params = {"action":"render"}
    #params["gcmtitle"] = "Category:%s" % categoryname.encode("utf8")
    result = [ ]
    while True:
        url = "%s?%s" % (urlapi, urllib.urlencode(params))
        print url
        #root = lxml.html.parse(url).getroot()
        tree = lxml.etree.parse(urllib.urlopen(url))
        docstr = lxml.html.tostring(tree) 
        print docstr
        for page in tree.xpath('//page'):
            pdata = dict(page.attrib.items())
            if "redirect" in pdata:   # case of the redirect page having a category, eg Paviland_Cave
                continue
            pdata.pop("new", None)
            assert pdata.keys() == ['lastrevid', 'pageid', 'title', 'counter', 'length', 'touched','ns'], (pdata.keys(), pdata)
            pdata['length'] = int(pdata['length'])
            if pdata["title"][:5] == "File:":
                continue
            pdata["link"] = "http://en.wikipedia.org/wiki/%s" % urllib.quote(pdata["title"].replace(" ", "_"))
            result.append(pdata)
        cmcontinue = tree.xpath('//query-continue/categorymembers') # attrib.get("gcmcontinue") is fed back in as gmcontinue parameter                     
        if not cmcontinue: 
            break
        params["gcmcontinue"] = cmcontinue[0].get("gcmcontinue")
    return result

def GetWikipediaCategoryRecurse(categoryname):
    "Downloads everything in a given category and all the subcategories"
    prestack = [ categoryname ]
    usedcategories = set()
    result = [ ]
    while prestack:
        lcategoryname = prestack.pop()
        if lcategoryname in usedcategories:
            continue
        for d in GetWikipediaCategory(lcategoryname):
            if d["title"][:9] == "Category:":
                prestack.append(d["title"][9:])
            else:
                result.append(d)
        usedcategories.add(lcategoryname)  # avoids infinite loops
    return result



def UpdateCategoryPart():
    #ldata = wikipedia_utils.GetWikipediaCategoryRecurse("Caves_of_the_United_Kingdom")
    ldata = GetWikipediaCategoryRecurse("Caves_of_the_United_Kingdom")
    print ldata
    
#for data in ldata:
    #    data["updatedate"] = nowtime
    #scraperwiki.sqlite.save(["title"], ldata, "cavepagesgeo")
    #scraperwiki.sqlite.execute("delete from cavepagesgeo where updatedate<>?", nowtime.isoformat())

    
def ExtractInfoPart():
    rdata = scraperwiki.sqlite.select("title, link from cavepagesgeo")
    print rdata
    ldata = [ ]
    #for pdata in rdata:
    #    try:
    #        val = wikipedia_utils.GetWikipediaPage(pdata["title"])
    #    except IOError:
    #        print "Skipping", pdata["title"]
    #        continue
    #    res = wikipedia_utils.ParseTemplates(val["text"])
    #    #print dict(res["templates"]).keys()
    #    data = dict(res["templates"]).get("Infobox ukcave")
    #    if not data:
    #        continue
    #    data["title"] = pdata["title"]
    #    data["link"] = pdata["link"]
    #    for k, v in data.items():
    #        if type(k) == int or not v or not re.match("[\w\s_\d]+$", k):
    #            del data[k]
    #    for k in ["length_metres", "depth_metres", "altitude_metres", "location_lat", "location_lon"]:
    #        if k in data:
    #            data[k] = float(data[k])
    #    print data
    #    ldata.append(data)
    #scraperwiki.sqlite.save(["title"], ldata, "caveinfo")


DatabaseOps()
UpdateCategoryPart()
#ExtractInfoPart()
#UpdateCategory()
#ExtractInfo()
import scraperwiki
import sys
import urllib
import lxml.etree
import re
import datetime

import lxml.html

urlapi =  "http://en.wikipedia.org/w/api.php"


#wikipedia_utils = scraperwiki.swimport("wikipedia_utils")
#wikipedia_utils = scraperwiki.tagint.swimport("Wikipedia_Utils_myver")

nowtime = datetime.datetime.now()

#modifications
#first iteration create table
#second iteration comment out create table
#further iterations comment out updatecategory()

def DatabaseOps():
    scraperwiki.sqlite.execute("drop table if exists cavepagesgeo")
    #scraperwiki.sqlite.execute("create table cavepagesgeo (lastrevid string, pageid string, title string, counter         #string,length int, link string, touched string, ns string, updatedate string lat_d real long_d real)")
    #scraperwiki.sqlite.execute("create table cavepagesgeo (title string, link string, lat_d real, long_d real)")


def UpdateCategory():
    ldata = wikipedia_utils.GetWikipediaCategoryRecurse("Caves_of_the_United_Kingdom")
    for data in ldata:
        data["updatedate"] = nowtime
    scraperwiki.sqlite.save(["title"], ldata, "cavepagesgeo")
    scraperwiki.sqlite.execute("delete from cavepagesgeo where updatedate<>?", nowtime.isoformat())

def ExtractInfo():
    rdata = scraperwiki.sqlite.select("title, link from cavepagesgeo")
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
        #for k, v in data.items():
            #if type(k) == int or not v or not re.match("[\w\s_\d]+$", k):
            #    del data[k]
        for k in ["length_metres", "depth_metres", "altitude_metres", "location_lat", "location_lon"]:
            if k in data:
                data[k] = float(data[k])
        print data
        ldata.append(data)
    scraperwiki.sqlite.save(["title"], ldata, "caveinfo")


def GetWikipediaCategory(categoryname):
    "Downloads all/some names and metadata of pages in given category"
    params = {"action":"query", "format":"xml", "generator":"categorymembers", "prop":"info", "gcmlimit":100 } 
    #gets full content
    #params = {"action":"query", "format":"xml", "generator":"categorymembers", #"prop":"revisions", "rvprop":"content", "gcmlimit":100 } 
    #gets full content
    params = {"action":"render"}
    #params["gcmtitle"] = "Category:%s" % categoryname.encode("utf8")
    result = [ ]
    while True:
        url = "%s?%s" % (urlapi, urllib.urlencode(params))
        print url
        #root = lxml.html.parse(url).getroot()
        tree = lxml.etree.parse(urllib.urlopen(url))
        docstr = lxml.html.tostring(tree) 
        print docstr
        for page in tree.xpath('//page'):
            pdata = dict(page.attrib.items())
            if "redirect" in pdata:   # case of the redirect page having a category, eg Paviland_Cave
                continue
            pdata.pop("new", None)
            assert pdata.keys() == ['lastrevid', 'pageid', 'title', 'counter', 'length', 'touched','ns'], (pdata.keys(), pdata)
            pdata['length'] = int(pdata['length'])
            if pdata["title"][:5] == "File:":
                continue
            pdata["link"] = "http://en.wikipedia.org/wiki/%s" % urllib.quote(pdata["title"].replace(" ", "_"))
            result.append(pdata)
        cmcontinue = tree.xpath('//query-continue/categorymembers') # attrib.get("gcmcontinue") is fed back in as gmcontinue parameter                     
        if not cmcontinue: 
            break
        params["gcmcontinue"] = cmcontinue[0].get("gcmcontinue")
    return result

def GetWikipediaCategoryRecurse(categoryname):
    "Downloads everything in a given category and all the subcategories"
    prestack = [ categoryname ]
    usedcategories = set()
    result = [ ]
    while prestack:
        lcategoryname = prestack.pop()
        if lcategoryname in usedcategories:
            continue
        for d in GetWikipediaCategory(lcategoryname):
            if d["title"][:9] == "Category:":
                prestack.append(d["title"][9:])
            else:
                result.append(d)
        usedcategories.add(lcategoryname)  # avoids infinite loops
    return result



def UpdateCategoryPart():
    #ldata = wikipedia_utils.GetWikipediaCategoryRecurse("Caves_of_the_United_Kingdom")
    ldata = GetWikipediaCategoryRecurse("Caves_of_the_United_Kingdom")
    print ldata
    
#for data in ldata:
    #    data["updatedate"] = nowtime
    #scraperwiki.sqlite.save(["title"], ldata, "cavepagesgeo")
    #scraperwiki.sqlite.execute("delete from cavepagesgeo where updatedate<>?", nowtime.isoformat())

    
def ExtractInfoPart():
    rdata = scraperwiki.sqlite.select("title, link from cavepagesgeo")
    print rdata
    ldata = [ ]
    #for pdata in rdata:
    #    try:
    #        val = wikipedia_utils.GetWikipediaPage(pdata["title"])
    #    except IOError:
    #        print "Skipping", pdata["title"]
    #        continue
    #    res = wikipedia_utils.ParseTemplates(val["text"])
    #    #print dict(res["templates"]).keys()
    #    data = dict(res["templates"]).get("Infobox ukcave")
    #    if not data:
    #        continue
    #    data["title"] = pdata["title"]
    #    data["link"] = pdata["link"]
    #    for k, v in data.items():
    #        if type(k) == int or not v or not re.match("[\w\s_\d]+$", k):
    #            del data[k]
    #    for k in ["length_metres", "depth_metres", "altitude_metres", "location_lat", "location_lon"]:
    #        if k in data:
    #            data[k] = float(data[k])
    #    print data
    #    ldata.append(data)
    #scraperwiki.sqlite.save(["title"], ldata, "caveinfo")


DatabaseOps()
UpdateCategoryPart()
#ExtractInfoPart()
#UpdateCategory()
#ExtractInfo()
