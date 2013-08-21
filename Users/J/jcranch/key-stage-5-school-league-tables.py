"""
DCSF School league tables: Key stage 5 (Sixth form)

http://www.education.gov.uk/performancetables/16to18_09.shtml

The following document explains some of the codes:

http://www.education.gov.uk/performancetables/16to18_09/glossary.shtml
"""



from urllib2 import urlopen
from lxml import html
import re
from scraperwiki import datastore

report = False



def main():
    lea_list = get_lea_list()

    for lea_name in lea_list:
        lea_number = obtain_lea_number(lea_name)
        scrape_lea(lea_name, lea_number)




def get_lea_list():
    "Get a list of LEAs"

    url = "http://www.education.gov.uk/performancetables/16to18_09.shtml"
    page = urlopen(url)

    lea_list = []

    # flag stores whether we're in the good bit
    flag = False

    dataline = re.compile('.*<option value="(.*)">.*</option>.*')

    for l in page:
        if flag:
            m = dataline.match(l)
            if m:
                g = m.groups()[0]
                if len(g) > 0: # beware, there is a null table entry
                    lea_list.append(m.groups()[0]) # got one!
            else:
                break # they're a contiguous block, so we can stop now
        else:
            if l.find('id="lalist"') != -1: # start scraping now!
                flag = True

    return lea_list



def obtain_lea_number(lea_name):
    "Given an LEA name, obtain the page with its league tables"
    url = "http://www.education.gov.uk/cgi-bin/performancetables/search_09.pl?Fieldname=&Fieldpostcode=&FieldLEA=%s&Mode=Z&Phase=2&Year=09&Base=a&Begin=s"%"+".join(lea_name.split(" "))

    linkline = re.compile('<li><a href="/cgi-bin/performancetables/.*No=([0-9]*).*">(.*)</a></li>')

    page = urlopen(url)
    for l in page:
        m = linkline.match(l)
        if m and (m.groups()[1] == lea_name):
            return int(m.groups()[0])

    raise ReturnFailure


class ReturnFailure(Exception):
    pass
            

def scrape_lea(name, number):
    """
    Given the LEA name and LEA number, find links to information pages on schools and scrape them.
    """

    print "Scraping: %s (#%s)"%(name, number)

    url = "http://www.education.gov.uk/cgi-bin/performancetables/group_09.pl?Mode=Z&No=%d&Base=a&Type=LA&Begin=s&Phase=2&Year=09&F=1&L=10000"%number
    page = html.parse(url)

    rowpath = "/".join(["body","div","div","div","table","tbody","tr"])

    headings = ["School",
                "% of pupils achieving Level 2 (5+ A*-C) including English and maths GCSEs",
                "% of pupils achieving English and maths Skills at Level 2",
                "% of pupils achieving English and maths Skills at Level 1",
                "% of pupils achieving Level 2 (5+ A*-C)",
                "% of pupils achieving Level 1 (5+ A*-G)",
                "% of pupils achieving 2 grades A*-C in science",
                "% of pupils achieving A*-C in a modern foreign language",
                "% of pupils achieving at least an A*-G short course in a modern foreign language",
                "% of pupils achieving at least one qualification",
                "Average total point score per pupil"]

    for row in page.findall(rowpath):
        if not("class" in row.attrib):
            link = row.find("td/a")
            scrape_school(name, number, link.attrib["href"])



def scrape_school(lea_name, lea_number, urlfrag):
    data = {"LEA name":lea_name, "LEA number":lea_number}
    
    url = "http://www.education.gov.uk" + urlfrag
    page = html.parse(url)

    # school name
    headerpath = "/".join(["body","div","div","h1"])
    name = page.find(headerpath).text
    print " * %s"%name
    data["School name"]=name

    # contact data, etc
    attribpath = "/".join(["body","div","div","div","div","dl"])
    for attriblist in page.findall(attribpath):
        for (title,entries) in description(attriblist):
            titletext = title.text.rstrip(":")  
            if titletext[-24:] == " (click for explanation)":
                titletext = titletext[:-24]

            entrytexts = []
            for entry in entries:
                link = entry.find("a")
                if (link is not None) and (link.attrib.get("class","") == "acronym") and ("title" in link.attrib):
                    entrytexts.append(link.attrib["title"])
                else:
                    entrytexts.append(unmarkup(entry).strip(" \n").replace("\n","; "))
            entrytext = ", ".join(entrytexts)

            data[titletext] = entrytext
            if report:
                print "    - %s: %s"%(titletext,entrytext)
            
    # main data
    listpath = "/".join(["body","div","div","div","div","div","dl"])
    for datalist in page.findall(listpath):
        if "class" in datalist.attrib and datalist.attrib["class"] == "schoolsstatslist":
            for (title,entry) in zip(datalist.findall("dt"),datalist.findall("dd")):
                titletext = title.text.strip()

                entrytext = unmarkup(entry).strip()

                data[titletext] = entrytext
                if report:
                    print "    - %s: %s"%(titletext,entrytext)

    datastore.save(data=data, unique_keys=["LEA name","School name"])




def general_split(l,f):
    """
    Takes a list l, splits it into pieces around elements where f = True
    """

    if len(l) == 0:
        return []
    else:
        total = []
        current = []
        for x in l:
            if f(x):
                total.append(current)
                current = []
            else:
                current.append(x)
        total.append(current)
        return total
            



def description(dl):
    """
    Takes a description list tag; converts it to a list of the form:
    [(dt1,[dd11,dd12]), (dt2,[]), (dt3,[dd31]), ... ]
    """

    titles = dl.findall("dt")
    descriptions = general_split(dl.getchildren(), lambda t: t.tag=="dt")[0]

    return zip(titles,descriptions)    
    



def unmarkup(e):
    "Extract all text from an element"

    return (e.text or "") + "".join(unmarkup(c) for c in e.getchildren()) + (e.tail or "")



        
main()

