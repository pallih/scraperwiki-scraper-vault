"""
Obtains Derbyshire school data

"I went out to the Derby on Wednesday and think it is the most interesting
 thing I ever saw over here."
 - Richard H. Davis
"""

from scraperwiki import datastore, scrape
from html5lib import HTMLParser, treebuilders
from lxml import etree
import re


def main():

    urls = ["http://www.derbyshire.gov.uk/education/schools_colleges/names_addresses/infant_schools/",
            "http://www.derbyshire.gov.uk/education/schools_colleges/names_addresses/junior_schools/",
            "http://www.derbyshire.gov.uk/education/schools_colleges/names_addresses/nursery_schools/",
            "http://www.derbyshire.gov.uk/education/schools_colleges/names_addresses/primary_schools/",
            "http://www.derbyshire.gov.uk/education/schools_colleges/names_addresses/secondary_schools/",
            "http://www.derbyshire.gov.uk/education/schools_colleges/names_addresses/special_schools/"]

    for url in urls:
        categoryscrape(url)


def path(l,s):
    return "/".join([s+x for x in l])


def specialscrape(url):
    # it is a weird failing of html5lib -> lxml.etree that "xml:lang" causes it to fall over
    return scrape(url).replace("xml:lang","xml_lang")


def categoryscrape(url):
    
    parser = HTMLParser(tree=treebuilders.getTreeBuilder("lxml"))
    page = parser.parse(specialscrape(url+"default.asp"))

    # pre = "{http://www.w3.org/1999/xhtml}"
    pre = ""
    
    schools = []

    for t in page.getroot().findall(path(["body","div","div","div","form","table","tbody","tr","td","table","tbody","tr","td","a"],pre)):
        schools.append((t.text.strip(),"http://www.derbyshire.gov.uk/education/schools_colleges/names_addresses/primary_schools/"+t.get("href")))

    for (name,schoolurl) in schools:
        schoolscrape(url,name,schoolurl)


def schoolscrape(categoryurl,name,url):

    print ""
    print name

    parser = HTMLParser(tree=treebuilders.getTreeBuilder("lxml"))
    page = parser.parse(specialscrape(url))
    
    # pre = "{http://www.w3.org/1999/xhtml}"
    pre = ""
    
    keyvaluepairs = {}

    def addkeyvaluepair(k,v):
        keyvaluepairs[k] = v
        print k + ": " + v

    data_rows = [t for t in page.findall(path(["body","div","div","div","div"],pre)) if t.attrib.get("class","") == "detailsRow"]

    for row in data_rows:
        key = [t for t in row.findall(path(["span"],pre)) if t.attrib.get("class","") == "leftColumn"][0].text.rstrip(": ")
        valuetag = [t for t in row.findall(path(["span"],pre)) if t.attrib.get("class","") == "rightColumn"][0]
        if valuetag.text:
            if key == "Address":
                raw_address = [valuetag.text] + [br.tail for br in valuetag.findall(path(["br"],pre))]
                addkeyvaluepair("Address"," / ".join(raw_address[:-1]))
                addkeyvaluepair("Postcode",raw_address[-1])
            else:
                addkeyvaluepair(key,valuetag.text)
        else:
            links = valuetag.findall(path(["a"],pre))
            if len(links) == 1:
                addkeyvaluepair(key,links[0].attrib["href"])
            else:
                for link in links:
                    href = link.attrib["href"]
                    if href[:7] != "http://":
                        href = categoryurl + "details/" + href
                    addkeyvaluepair(link.text,href)
                    
    datastore.save(unique_keys=["Name"], data=keyvaluepairs)


main()
