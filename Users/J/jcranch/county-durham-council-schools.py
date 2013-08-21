"""
Obtains County Durham Council school data

"We went out there and wrestled hard."
 - Nick Durham
"""


from scraperwiki import datastore, scrape
from BeautifulSoup import BeautifulSoup, NavigableString
import re


def main():
    masterurl = "http://www.durham.gov.uk/Pages/Service.aspx?ServiceId=17"
    masterpage = BeautifulSoup(scrape(masterurl))

    r = re.compile('http://nd.durham.gov.uk/durhamcc/directory.nsf/vsch[a-z]*\?openview&count=300')
    categories = list(set([str(link.get("href")) for link in masterpage.findAll("a",href=r)]))

    for categoryurl in categories:
        categoryscrape(categoryurl)


def categoryscrape(categoryurl):
    subpage = BeautifulSoup(scrape(categoryurl))
    title = str(subpage.find("h1").contents[0])
    print title
    print ""

    schools = []

    for table_row in subpage.findAll("tr"):
        for link in table_row.findAll("a",href=re.compile('/durhamcc/directory.nsf/[0-9a-f]*/[0-9a-f]*\\?OpenDocument')):
            schoolname = str(link.contents[0]).rstrip(" ")
            schoolurl = "http://nd.durham.gov.uk" + link.get("href")
            schools.append((schoolname,schoolurl))

    for (schoolname,schoolurl) in schools:
        schoolscrape(schoolname,schoolurl)

    print ""
    print ""


def tagcontents_to_string(t):
    if isinstance(t,NavigableString):
        return str(t).replace("&nbsp;"," ")
    else:
        while t.br:
            t.br.replaceWith(" / ")
        while t.a:
            t.a.replaceWith(t.a.get("href"))
        return "".join([str(x).replace("&nbsp;"," ") for x in t.contents]).rstrip(" \n\r")


def postcode_format(s):
    "if s is a postcode, return it in standard format"
    postcode = re.compile("^\s*([A-Z][A-Z]?[0-9][0-9]?[A-Z]?)\s*([0-9][ABDEFGHJLNPQRSTUWXYZ][ABDEFGHJLNPQRSTUWXYZA-Z])\s*$")
    
    (t,i) = postcode.subn("\\1 \\2",s)
    if i == 1:
        return t
    else:
        return None


def schoolscrape(schoolname,schoolurl):
    
    schoolpage = BeautifulSoup(scrape(schoolurl))

    keyvalues = {}

    def addkeyvaluepair(k,v):
        print k + ": " + v
        keyvalues[k] = v

    addkeyvaluepair("schoolname",schoolname)

    # there's some extra data in the HTML comments which currently goes missed
    for label in schoolpage.findAll("div",{"class":"ecol1"}):
        attrib = tagcontents_to_string(label).rstrip(":")
        if attrib == "Address":
            field = label.findNextSibling("div",{"class":"ecol2"})
            while field.br:
                field.br.extract()
            lines = [str(x) for x in field.contents]
            postcode = postcode_format(str(lines[-1]).replace("&nbsp;",""))
            addkeyvaluepair("Postcode",postcode)
            address = " / ".join([l.rstrip(", ") for l in lines[:-1]])
            addkeyvaluepair("Address",address)
        else:
            value = tagcontents_to_string(label.findNextSibling("div",{"class":"ecol2"}))
            addkeyvaluepair(attrib,value)

    print ""

    datastore.save(unique_keys=["schoolname"], data=keyvalues)


main()
