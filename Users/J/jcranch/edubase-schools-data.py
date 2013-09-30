"""
Obtains the edubase schools database

http://www.edubase.gov.uk
"""

from scraperwiki import datastore, scrape
from html5lib import HTMLParser, treebuilders
from lxml import etree
import mechanize
import re

def main():
    print "Phase I: getting list of URNs:"
    urns = shallow_scrape()
    print "... acquired %d URNs"%(len(urns))
    print "Phase II: acquiring school data:"
    for urn in urns:
        deep_scrape(urn)

pre = ''

def shallow_scrape():
    urns = set([])

    br = mechanize.Browser()
    resultspage = br.open("http://www.education.gov.uk/edubase/quickSearchResult.xhtml")

    moreWorkToDo = True
    c = 1

    while moreWorkToDo and (c<3):
        print "Handling page %d..."%c
    
        ### extract data from page
        parser = HTMLParser(tree=treebuilders.getTreeBuilder("lxml"))
        page = parser.parse(resultspage)

        for u in page.getroot().findall(path(["body","div","div","div","div","table","tbody","tr","td","table","tbody","tr","td","a"],"")):
            #href = u.attrib.get("href","")
            href = u.get("href")
            print "href: %s"%href
            urn = re.search("urn=([0-9]{6})",href).group(1)
            urns.add(urn)
            print "%s, "%urn
        print

        ### get new page
        try:
            resultspage = br.follow_link(text="Next")
            c += 1
        except mechanize.LinkNotFoundError:
            moreWorkToDo = False

    return urns

def path(l,s):
    return "/".join([s+x for x in l])

def deep_scrape(urn):
    print "URN: %s"%urn
    keyvaluepairs = {}

    def merge_in(d):
        "update keyvaluepairs with d; complain if anything is overwritten"
        for (k,v) in d.iteritems():
            if k in keyvaluepairs:
                assert keyvaluepairs[k] == v
            else:
                keyvaluepairs[k] = v

    merge_in(summary_scrape(urn))
    merge_in(page_scrape('general', urn))
    merge_in(page_scrape('school-characterisics', urn))
    merge_in(page_scrape('links', urn))
    merge_in(page_scrape('sen', urn))
    merge_in(page_scrape('pru', urn))
    merge_in(page_scrape('quality-indicators', urn))
    merge_in(page_scrape('communications', urn))
    merge_in(page_scrape('census-data', urn))
    merge_in(page_scrape('regional-indicators', urn))
    
    datastore.save(unique_keys=["URN"],data=keyvaluepairs)
    print

postcode = re.compile("^([A-Z][A-Z]?[0-9][0-9]?[A-Z]?)\s*([0-9][ABDEFGHJLNPQRSTUWXYZ][ABDEFGHJLNPQRSTUWXYZ])$")

def summary_scrape(urn):    
    print " - summary"
    url = "http://www.education.gov.uk/edubase/establishment/summary.xhtml?urn=" + urn
    parser = HTMLParser(tree=treebuilders.getTreeBuilder("lxml"))
    page = parser.parse(scrape(url))

    keyvaluepairs = table_extract(page)

    raw_address = [x.strip() for x in keyvaluepairs.pop("").split(" / ")]
    if postcode.match(raw_address[-1]):
        keyvaluepairs["Postcode"] = raw_address[-1]
        raw_address = raw_address[:-1]
    keyvaluepairs["Address"] = " / ".join(raw_address)

    for t in page.findall(path(["body","div","div","div","div","table","tbody","tr","td","h1"],pre)):
        x = t.text.split(": ")
        keyvaluepairs[x[0]] = x[1]

    for t in page.findall(path(["body","div","div","div","div","table","tbody","tr","td","div","p","b"],pre)):
        keyvaluepairs[t.text.strip().strip(":")] = (t.tail or "").strip()

    return keyvaluepairs


def page_scrape(name, urn):
    print name
    url = "http://www.education.gov.uk/edubase/establishment/"+name+".xhtml"+"?urn="+urn
    parser = HTMLParser(tree=treebuilders.getTreeBuilder("lxml"))
    page = parser.parse(scrape(url))
    return table_extract(page)

def table_extract(page):
    keyvaluepairs = {}
    for tr in page.findall(path(["body","div","div","div","div","table","tbody","tr","td","div","table","tbody","tr","td","table","tbody","tr"],pre)):
        th = tr.find(path(["th"],pre))
        if th != None:
            k = (th.text or "")
        else:
            k = ""
        td = tr.find(path(["td"],pre))
        if td != None:
            v = (td.text or "")
        else:
            v = ""
        if k in keyvaluepairs:
            keyvaluepairs[k] = keyvaluepairs[k] + " / " + v
        else:
            keyvaluepairs[k] = v
    return keyvaluepairs

main()
"""
Obtains the edubase schools database

http://www.edubase.gov.uk
"""

from scraperwiki import datastore, scrape
from html5lib import HTMLParser, treebuilders
from lxml import etree
import mechanize
import re

def main():
    print "Phase I: getting list of URNs:"
    urns = shallow_scrape()
    print "... acquired %d URNs"%(len(urns))
    print "Phase II: acquiring school data:"
    for urn in urns:
        deep_scrape(urn)

pre = ''

def shallow_scrape():
    urns = set([])

    br = mechanize.Browser()
    resultspage = br.open("http://www.education.gov.uk/edubase/quickSearchResult.xhtml")

    moreWorkToDo = True
    c = 1

    while moreWorkToDo and (c<3):
        print "Handling page %d..."%c
    
        ### extract data from page
        parser = HTMLParser(tree=treebuilders.getTreeBuilder("lxml"))
        page = parser.parse(resultspage)

        for u in page.getroot().findall(path(["body","div","div","div","div","table","tbody","tr","td","table","tbody","tr","td","a"],"")):
            #href = u.attrib.get("href","")
            href = u.get("href")
            print "href: %s"%href
            urn = re.search("urn=([0-9]{6})",href).group(1)
            urns.add(urn)
            print "%s, "%urn
        print

        ### get new page
        try:
            resultspage = br.follow_link(text="Next")
            c += 1
        except mechanize.LinkNotFoundError:
            moreWorkToDo = False

    return urns

def path(l,s):
    return "/".join([s+x for x in l])

def deep_scrape(urn):
    print "URN: %s"%urn
    keyvaluepairs = {}

    def merge_in(d):
        "update keyvaluepairs with d; complain if anything is overwritten"
        for (k,v) in d.iteritems():
            if k in keyvaluepairs:
                assert keyvaluepairs[k] == v
            else:
                keyvaluepairs[k] = v

    merge_in(summary_scrape(urn))
    merge_in(page_scrape('general', urn))
    merge_in(page_scrape('school-characterisics', urn))
    merge_in(page_scrape('links', urn))
    merge_in(page_scrape('sen', urn))
    merge_in(page_scrape('pru', urn))
    merge_in(page_scrape('quality-indicators', urn))
    merge_in(page_scrape('communications', urn))
    merge_in(page_scrape('census-data', urn))
    merge_in(page_scrape('regional-indicators', urn))
    
    datastore.save(unique_keys=["URN"],data=keyvaluepairs)
    print

postcode = re.compile("^([A-Z][A-Z]?[0-9][0-9]?[A-Z]?)\s*([0-9][ABDEFGHJLNPQRSTUWXYZ][ABDEFGHJLNPQRSTUWXYZ])$")

def summary_scrape(urn):    
    print " - summary"
    url = "http://www.education.gov.uk/edubase/establishment/summary.xhtml?urn=" + urn
    parser = HTMLParser(tree=treebuilders.getTreeBuilder("lxml"))
    page = parser.parse(scrape(url))

    keyvaluepairs = table_extract(page)

    raw_address = [x.strip() for x in keyvaluepairs.pop("").split(" / ")]
    if postcode.match(raw_address[-1]):
        keyvaluepairs["Postcode"] = raw_address[-1]
        raw_address = raw_address[:-1]
    keyvaluepairs["Address"] = " / ".join(raw_address)

    for t in page.findall(path(["body","div","div","div","div","table","tbody","tr","td","h1"],pre)):
        x = t.text.split(": ")
        keyvaluepairs[x[0]] = x[1]

    for t in page.findall(path(["body","div","div","div","div","table","tbody","tr","td","div","p","b"],pre)):
        keyvaluepairs[t.text.strip().strip(":")] = (t.tail or "").strip()

    return keyvaluepairs


def page_scrape(name, urn):
    print name
    url = "http://www.education.gov.uk/edubase/establishment/"+name+".xhtml"+"?urn="+urn
    parser = HTMLParser(tree=treebuilders.getTreeBuilder("lxml"))
    page = parser.parse(scrape(url))
    return table_extract(page)

def table_extract(page):
    keyvaluepairs = {}
    for tr in page.findall(path(["body","div","div","div","div","table","tbody","tr","td","div","table","tbody","tr","td","table","tbody","tr"],pre)):
        th = tr.find(path(["th"],pre))
        if th != None:
            k = (th.text or "")
        else:
            k = ""
        td = tr.find(path(["td"],pre))
        if td != None:
            v = (td.text or "")
        else:
            v = ""
        if k in keyvaluepairs:
            keyvaluepairs[k] = keyvaluepairs[k] + " / " + v
        else:
            keyvaluepairs[k] = v
    return keyvaluepairs

main()
