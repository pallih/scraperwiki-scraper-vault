# scrapper to retrieve data from the Gene Expression Omnibus at the NCBI

import scraperwiki
import lxml.html
import sys


def GetAndSaveSampleList(study):
    url = "http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=%s" % study
    html = scraperwiki.scrape(url)
    #print html
    root = lxml.html.fromstring(html)
    tds = root.cssselect("td")
    lSamples = []
    lInds = []
    for td in tds:
        txt = lxml.html.tostring(td)
        #print txt
        if "GSM" in txt:
            sample = "GSM%s" % txt.split(">GSM")[1].split("<")[0]
            if sample not in lSamples:
                lSamples.append( sample )
        elif "_individual_" in txt:
            ind = txt.split(">")[1].split("<")[0]
            if ind not in lInds:
                lInds.append( ind )
    print "nb of samples: %i" % len(lSamples)
    print "nb of individuals: %i" % len(lInds)
    if len(lSamples) != len(lInds):
        print "error: different lengths"
        print lInds
        sys.exit()
    for i in range(0,len(lSamples)):
        record = { "sample" : lSamples[i],
                    "ind": lInds[i] }
        #scraperwiki.datastore.save(["sample"], record)
        scraperwiki.sqlite.save(unique_keys=['sample'], data=record)


def GetProbeIntensitiesUrl( data, verbose=0 ):
    sample = data["sample"]
    url = "http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=%s" % sample
    if verbose > 0:
        print "url:", url
    html = scraperwiki.scrape(url)
    if verbose > 0:
        print "html:", html[:-1]
    root = lxml.html.fromstring(html)
    if verbose > 0:
        print "root:", root
    inputs = root.cssselect("input")
    if verbose > 0:
        print "nb <input>: %i" % len(inputs)
    for i in inputs:
        txt = lxml.html.tostring(i)
        if "fulltable" in txt:
            j = txt.split("acc.cgi?")[1].split("', '")[0]
            record = { "sample": sample,
                        "ind": data["ind"],
                        "url_info": "http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?%s" % j }
            if verbose > 0:
                print record
            if record["url_info"] == "":
                print "missing url_info"
                sys.exit(1)
            scraperwiki.sqlite.save(unique_keys=['sample'], data=record)


def GetProbeIntensitiesData( url ):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    pres = root.cssselect("pre")
    print len(pres)


if scraperwiki.sqlite.show_tables() == {}:
    GetAndSaveSampleList("GSE17080")

lRecords = scraperwiki.sqlite.select('''* from swdata order by sample''')
print "nb of records: %i" % len(lRecords)
for i in range(0,len(lRecords)):
    record = lRecords[i]
    print "sample #%i/%i: %s" % (i+1, len(lRecords), record["sample"])
    GetProbeIntensitiesUrl( record, verbose=1 )

# scrapper to retrieve data from the Gene Expression Omnibus at the NCBI

import scraperwiki
import lxml.html
import sys


def GetAndSaveSampleList(study):
    url = "http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=%s" % study
    html = scraperwiki.scrape(url)
    #print html
    root = lxml.html.fromstring(html)
    tds = root.cssselect("td")
    lSamples = []
    lInds = []
    for td in tds:
        txt = lxml.html.tostring(td)
        #print txt
        if "GSM" in txt:
            sample = "GSM%s" % txt.split(">GSM")[1].split("<")[0]
            if sample not in lSamples:
                lSamples.append( sample )
        elif "_individual_" in txt:
            ind = txt.split(">")[1].split("<")[0]
            if ind not in lInds:
                lInds.append( ind )
    print "nb of samples: %i" % len(lSamples)
    print "nb of individuals: %i" % len(lInds)
    if len(lSamples) != len(lInds):
        print "error: different lengths"
        print lInds
        sys.exit()
    for i in range(0,len(lSamples)):
        record = { "sample" : lSamples[i],
                    "ind": lInds[i] }
        #scraperwiki.datastore.save(["sample"], record)
        scraperwiki.sqlite.save(unique_keys=['sample'], data=record)


def GetProbeIntensitiesUrl( data, verbose=0 ):
    sample = data["sample"]
    url = "http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=%s" % sample
    if verbose > 0:
        print "url:", url
    html = scraperwiki.scrape(url)
    if verbose > 0:
        print "html:", html[:-1]
    root = lxml.html.fromstring(html)
    if verbose > 0:
        print "root:", root
    inputs = root.cssselect("input")
    if verbose > 0:
        print "nb <input>: %i" % len(inputs)
    for i in inputs:
        txt = lxml.html.tostring(i)
        if "fulltable" in txt:
            j = txt.split("acc.cgi?")[1].split("', '")[0]
            record = { "sample": sample,
                        "ind": data["ind"],
                        "url_info": "http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?%s" % j }
            if verbose > 0:
                print record
            if record["url_info"] == "":
                print "missing url_info"
                sys.exit(1)
            scraperwiki.sqlite.save(unique_keys=['sample'], data=record)


def GetProbeIntensitiesData( url ):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    pres = root.cssselect("pre")
    print len(pres)


if scraperwiki.sqlite.show_tables() == {}:
    GetAndSaveSampleList("GSE17080")

lRecords = scraperwiki.sqlite.select('''* from swdata order by sample''')
print "nb of records: %i" % len(lRecords)
for i in range(0,len(lRecords)):
    record = lRecords[i]
    print "sample #%i/%i: %s" % (i+1, len(lRecords), record["sample"])
    GetProbeIntensitiesUrl( record, verbose=1 )

