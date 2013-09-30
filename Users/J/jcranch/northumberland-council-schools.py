"""
Obtains Northumberland Council school data

"We had better remain in union with England, even at the risk of becoming a
 subordinate species of Northumberland..."
 - Sir Walter Scott
"""

from scraperwiki import datastore, scrape, log
from BeautifulSoup import BeautifulSoup, NavigableString
import re


def main():
    urls = ["http://www.northumberland.gov.uk/default.aspx?page=4153",
            "http://www.northumberland.gov.uk/default.aspx?page=4154",
            "http://www.northumberland.gov.uk/default.aspx?page=4155",
            "http://www.northumberland.gov.uk/default.aspx?page=4156",
            "http://www.northumberland.gov.uk/default.aspx?page=4698"]

    for url in urls:
        log(url)
        categoryscrape(url)


def postcode_format(s):
    "if s is a postcode, return it in standard format"

    postcode = re.compile("^\s*([A-Z][A-Z]?[0-9][0-9]?[A-Z]?)\s*([0-9][ABDEFGHJLNPQRSTUWXYZ][ABDEFGHJLNPQRSTUWXYZ])\s*$")
    (t,i) = postcode.subn("\\1 \\2",s)
    if i == 1:
        return t
    else:
        return None


def tagcontents_to_string(t):
    if isinstance(t,NavigableString):
        return str(t).replace("&nbsp;"," ")
    else:
        while t.br:
            t.br.replaceWith(" / ")
        while t.a:
            t.a.replaceWith(t.a.get("href"))
        return "".join([str(x).replace("&nbsp;"," ") for x in t.contents]).rstrip(" \n\r")


def categoryscrape(url):     
    print "Ripping " + url
    print ""

    page = BeautifulSoup(scrape(url))
    for nametag in page.findAll("h3"):

        keyvalues = {}

        def addkeyvaluepair(k,v):
            print k + ": " + v
            keyvalues[k] = v    
        
        name = str(nametag.contents[0])
        addkeyvaluepair("Schoolname",name)
        school_details = nametag.nextSibling

        for table_row in school_details.findAll("tr"):
            table_cells = table_row.findAll("td")
            attrib = str(table_cells[0].contents[0]).rstrip(":")

            if attrib == "Address":
                lines = str(table_cells[1].contents[0]).split("\n")
                postcode = postcode_format(str(lines[-1]).replace("&nbsp;",""))
                addkeyvaluepair("Postcode",postcode)
                address = " / ".join([l.rstrip(", ") for l in lines[:-1]])
                addkeyvaluepair("Address",address)

            else:
                contents = tagcontents_to_string(table_cells[1])
                addkeyvaluepair(attrib,contents)

        datastore.save(unique_keys=["Schoolname"], data=keyvalues)
                
        print ""

    print ""

    
main()
"""
Obtains Northumberland Council school data

"We had better remain in union with England, even at the risk of becoming a
 subordinate species of Northumberland..."
 - Sir Walter Scott
"""

from scraperwiki import datastore, scrape, log
from BeautifulSoup import BeautifulSoup, NavigableString
import re


def main():
    urls = ["http://www.northumberland.gov.uk/default.aspx?page=4153",
            "http://www.northumberland.gov.uk/default.aspx?page=4154",
            "http://www.northumberland.gov.uk/default.aspx?page=4155",
            "http://www.northumberland.gov.uk/default.aspx?page=4156",
            "http://www.northumberland.gov.uk/default.aspx?page=4698"]

    for url in urls:
        log(url)
        categoryscrape(url)


def postcode_format(s):
    "if s is a postcode, return it in standard format"

    postcode = re.compile("^\s*([A-Z][A-Z]?[0-9][0-9]?[A-Z]?)\s*([0-9][ABDEFGHJLNPQRSTUWXYZ][ABDEFGHJLNPQRSTUWXYZ])\s*$")
    (t,i) = postcode.subn("\\1 \\2",s)
    if i == 1:
        return t
    else:
        return None


def tagcontents_to_string(t):
    if isinstance(t,NavigableString):
        return str(t).replace("&nbsp;"," ")
    else:
        while t.br:
            t.br.replaceWith(" / ")
        while t.a:
            t.a.replaceWith(t.a.get("href"))
        return "".join([str(x).replace("&nbsp;"," ") for x in t.contents]).rstrip(" \n\r")


def categoryscrape(url):     
    print "Ripping " + url
    print ""

    page = BeautifulSoup(scrape(url))
    for nametag in page.findAll("h3"):

        keyvalues = {}

        def addkeyvaluepair(k,v):
            print k + ": " + v
            keyvalues[k] = v    
        
        name = str(nametag.contents[0])
        addkeyvaluepair("Schoolname",name)
        school_details = nametag.nextSibling

        for table_row in school_details.findAll("tr"):
            table_cells = table_row.findAll("td")
            attrib = str(table_cells[0].contents[0]).rstrip(":")

            if attrib == "Address":
                lines = str(table_cells[1].contents[0]).split("\n")
                postcode = postcode_format(str(lines[-1]).replace("&nbsp;",""))
                addkeyvaluepair("Postcode",postcode)
                address = " / ".join([l.rstrip(", ") for l in lines[:-1]])
                addkeyvaluepair("Address",address)

            else:
                contents = tagcontents_to_string(table_cells[1])
                addkeyvaluepair(attrib,contents)

        datastore.save(unique_keys=["Schoolname"], data=keyvalues)
                
        print ""

    print ""

    
main()
