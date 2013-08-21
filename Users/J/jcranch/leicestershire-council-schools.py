"""
Obtains Leicestershire Council school data

"Leicestershire is being investigated."
 - googlism.com
"""


from scraperwiki import datastore, scrape
from BeautifulSoup import BeautifulSoup, NavigableString
import re


def main():
    main_page = BeautifulSoup(scrape("http://www.leics.gov.uk/index/education/information_about_schools/schools_searchform.htm"))
    school_list = [(x.get("value"),str(x.contents[0])) for x in main_page.findAll("option",value=re.compile("^[0-9][0-9][0-9][0-9]$"))]

    for (serial,name) in school_list:
        schoolscrape(serial,name)


def postcode_format(s):
    "if s is a postcode, return it in standard format"

    postcode = re.compile("^\s*([A-Z][A-Z]?[0-9][0-9]?[A-Z]?)\s*([0-9][ABDEFGHJLNPQRSTUWXYZ][ABDEFGHJLNPQRSTUWXYZA-Z])\s*$")
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


def schoolscrape(serial,name):
    url = "http://www.leics.gov.uk/index/education/going_to_school/information_about_schools/schools_resultdetail.htm?DFES=" + serial + "&submit=Search"
    subpage = BeautifulSoup(scrape(url))
    print name

    keyvalues = {}

    def addkeyvaluepair(k,v):
        print k + ": " + v
        keyvalues[k] = v    
    
    addkeyvaluepair("schoolname",name)

    for t in subpage.findAll("td",headers=re.compile("..*")):
        attrib = t.get("headers")
        if attrib[:7] == "school_":
            attrib = attrib[7:]
        if attrib == "address":
            pc = postcode_format(str(t.contents[-1]))
            addkeyvaluepair("postcode",pc)
            t.contents = t.contents [:-2]
        addkeyvaluepair(attrib,tagcontents_to_string(t))
    print ""

    datastore.save(unique_keys=["schoolname"], data=keyvalues)


main()
