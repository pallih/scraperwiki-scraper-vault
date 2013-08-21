import scraperwiki
import re, urllib, csv
import json
from scraperwiki import log


# trying to populate the YNMP readings with further info from party webpages 
# and then also consider BBC and Guardian sites
# Constituency names should be regularized at the start

def Main():
    for i in range(1, 14):
        text = scraperwiki.scrape("http://www.yournextmp.com/seats/all/%d" % i)
        seats = re.findall('<a href="http://www.yournextmp.com/seats/([^/]*?)"', text)
        print "Doing page", i, "Seats:", seats
        for j, seat in enumerate(seats):
            print j, seat
            for candidateurl in ParseSeatForCandidates(seat):
                scraperwiki.datastore.save(["url"], {"url":candidateurl})
    
def GetConstList():
    constituencylisturl = "http://www.theyworkforyou.com/boundaries/new-constituencies.tsv"
    constituencylist = scraperwiki.scrape(constituencylisturl)
    return [con  for con, r in re.findall("(.*?)\t(.*?)\n", constituencylist)]


def ParseSeatForCandidates(seat):
    jsontext = scraperwiki.scrape("http://www.yournextmp.com/seats/%s?output=json" % seat)
    contents = json.loads(jsontext)["result"]

    # get wikipedia link not in the json dump
    text = scraperwiki.scrape("http://www.yournextmp.com/seats/%s" % seat)
    constituencyurl = re.search('<a href="(http://en.wikipedia.org/wiki/[^"]*?\(UK_Parliament_constituency\))"', text).group(1)

    constituency = contents["name"]
    result = [ ]
    for candidate in contents["candidates"]:
        url = "http://www.yournextmp.com/candidates/%s" % candidate["code"]
        
        data = {"name":candidate["name"], "url":url, "party":candidate["party"]["name"], 
                 "constituency":constituency, "constituencyurl":constituencyurl}

        # get wikipedia link not in the json dump
        ptext = scraperwiki.scrape(url)
        wpurls = re.findall('<a href="(http://en.wikipedia.org/wiki/.*?)"', ptext)
        if wpurls:
            data["wpurl"] = re.sub(" ", "_", wpurls[0])
        #result.append(data)

        #print ptext
        for w in re.findall('<h3>\s*<a href="(.*?)"', ptext):
            if not re.match("http://www.labour.org.uk|http://www.conservatives.com|http://www.libdems.org.uk|http://en.wikipedia.org/", w):
                result.append(w)
        
    return result

Main()

import scraperwiki
import re, urllib, csv
import json
from scraperwiki import log


# trying to populate the YNMP readings with further info from party webpages 
# and then also consider BBC and Guardian sites
# Constituency names should be regularized at the start

def Main():
    for i in range(1, 14):
        text = scraperwiki.scrape("http://www.yournextmp.com/seats/all/%d" % i)
        seats = re.findall('<a href="http://www.yournextmp.com/seats/([^/]*?)"', text)
        print "Doing page", i, "Seats:", seats
        for j, seat in enumerate(seats):
            print j, seat
            for candidateurl in ParseSeatForCandidates(seat):
                scraperwiki.datastore.save(["url"], {"url":candidateurl})
    
def GetConstList():
    constituencylisturl = "http://www.theyworkforyou.com/boundaries/new-constituencies.tsv"
    constituencylist = scraperwiki.scrape(constituencylisturl)
    return [con  for con, r in re.findall("(.*?)\t(.*?)\n", constituencylist)]


def ParseSeatForCandidates(seat):
    jsontext = scraperwiki.scrape("http://www.yournextmp.com/seats/%s?output=json" % seat)
    contents = json.loads(jsontext)["result"]

    # get wikipedia link not in the json dump
    text = scraperwiki.scrape("http://www.yournextmp.com/seats/%s" % seat)
    constituencyurl = re.search('<a href="(http://en.wikipedia.org/wiki/[^"]*?\(UK_Parliament_constituency\))"', text).group(1)

    constituency = contents["name"]
    result = [ ]
    for candidate in contents["candidates"]:
        url = "http://www.yournextmp.com/candidates/%s" % candidate["code"]
        
        data = {"name":candidate["name"], "url":url, "party":candidate["party"]["name"], 
                 "constituency":constituency, "constituencyurl":constituencyurl}

        # get wikipedia link not in the json dump
        ptext = scraperwiki.scrape(url)
        wpurls = re.findall('<a href="(http://en.wikipedia.org/wiki/.*?)"', ptext)
        if wpurls:
            data["wpurl"] = re.sub(" ", "_", wpurls[0])
        #result.append(data)

        #print ptext
        for w in re.findall('<h3>\s*<a href="(.*?)"', ptext):
            if not re.match("http://www.labour.org.uk|http://www.conservatives.com|http://www.libdems.org.uk|http://en.wikipedia.org/", w):
                result.append(w)
        
    return result

Main()

import scraperwiki
import re, urllib, csv
import json
from scraperwiki import log


# trying to populate the YNMP readings with further info from party webpages 
# and then also consider BBC and Guardian sites
# Constituency names should be regularized at the start

def Main():
    for i in range(1, 14):
        text = scraperwiki.scrape("http://www.yournextmp.com/seats/all/%d" % i)
        seats = re.findall('<a href="http://www.yournextmp.com/seats/([^/]*?)"', text)
        print "Doing page", i, "Seats:", seats
        for j, seat in enumerate(seats):
            print j, seat
            for candidateurl in ParseSeatForCandidates(seat):
                scraperwiki.datastore.save(["url"], {"url":candidateurl})
    
def GetConstList():
    constituencylisturl = "http://www.theyworkforyou.com/boundaries/new-constituencies.tsv"
    constituencylist = scraperwiki.scrape(constituencylisturl)
    return [con  for con, r in re.findall("(.*?)\t(.*?)\n", constituencylist)]


def ParseSeatForCandidates(seat):
    jsontext = scraperwiki.scrape("http://www.yournextmp.com/seats/%s?output=json" % seat)
    contents = json.loads(jsontext)["result"]

    # get wikipedia link not in the json dump
    text = scraperwiki.scrape("http://www.yournextmp.com/seats/%s" % seat)
    constituencyurl = re.search('<a href="(http://en.wikipedia.org/wiki/[^"]*?\(UK_Parliament_constituency\))"', text).group(1)

    constituency = contents["name"]
    result = [ ]
    for candidate in contents["candidates"]:
        url = "http://www.yournextmp.com/candidates/%s" % candidate["code"]
        
        data = {"name":candidate["name"], "url":url, "party":candidate["party"]["name"], 
                 "constituency":constituency, "constituencyurl":constituencyurl}

        # get wikipedia link not in the json dump
        ptext = scraperwiki.scrape(url)
        wpurls = re.findall('<a href="(http://en.wikipedia.org/wiki/.*?)"', ptext)
        if wpurls:
            data["wpurl"] = re.sub(" ", "_", wpurls[0])
        #result.append(data)

        #print ptext
        for w in re.findall('<h3>\s*<a href="(.*?)"', ptext):
            if not re.match("http://www.labour.org.uk|http://www.conservatives.com|http://www.libdems.org.uk|http://en.wikipedia.org/", w):
                result.append(w)
        
    return result

Main()

import scraperwiki
import re, urllib, csv
import json
from scraperwiki import log


# trying to populate the YNMP readings with further info from party webpages 
# and then also consider BBC and Guardian sites
# Constituency names should be regularized at the start

def Main():
    for i in range(1, 14):
        text = scraperwiki.scrape("http://www.yournextmp.com/seats/all/%d" % i)
        seats = re.findall('<a href="http://www.yournextmp.com/seats/([^/]*?)"', text)
        print "Doing page", i, "Seats:", seats
        for j, seat in enumerate(seats):
            print j, seat
            for candidateurl in ParseSeatForCandidates(seat):
                scraperwiki.datastore.save(["url"], {"url":candidateurl})
    
def GetConstList():
    constituencylisturl = "http://www.theyworkforyou.com/boundaries/new-constituencies.tsv"
    constituencylist = scraperwiki.scrape(constituencylisturl)
    return [con  for con, r in re.findall("(.*?)\t(.*?)\n", constituencylist)]


def ParseSeatForCandidates(seat):
    jsontext = scraperwiki.scrape("http://www.yournextmp.com/seats/%s?output=json" % seat)
    contents = json.loads(jsontext)["result"]

    # get wikipedia link not in the json dump
    text = scraperwiki.scrape("http://www.yournextmp.com/seats/%s" % seat)
    constituencyurl = re.search('<a href="(http://en.wikipedia.org/wiki/[^"]*?\(UK_Parliament_constituency\))"', text).group(1)

    constituency = contents["name"]
    result = [ ]
    for candidate in contents["candidates"]:
        url = "http://www.yournextmp.com/candidates/%s" % candidate["code"]
        
        data = {"name":candidate["name"], "url":url, "party":candidate["party"]["name"], 
                 "constituency":constituency, "constituencyurl":constituencyurl}

        # get wikipedia link not in the json dump
        ptext = scraperwiki.scrape(url)
        wpurls = re.findall('<a href="(http://en.wikipedia.org/wiki/.*?)"', ptext)
        if wpurls:
            data["wpurl"] = re.sub(" ", "_", wpurls[0])
        #result.append(data)

        #print ptext
        for w in re.findall('<h3>\s*<a href="(.*?)"', ptext):
            if not re.match("http://www.labour.org.uk|http://www.conservatives.com|http://www.libdems.org.uk|http://en.wikipedia.org/", w):
                result.append(w)
        
    return result

Main()

