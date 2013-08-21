import scraperwiki
import lxml.html
import urllib2
import datetime
import re

urlp = "http://portal.gov.im/pvi/CompanyDetails.aspx?company="

#help(re)

def SearchEnd(number, code):
    

    url = "%s%06d%s" % (urlp, number, code)
    root = lxml.html.parse(url).getroot()
    content = root.cssselect("div#maincontent")
    assert len(content) == 1, url
    tables = content[0].cssselect("table")
    assert 1 <= len(tables) <= 4, (url)
    html = lxml.html.tostring(root)
    mviewstate = re.search('name="__VIEWSTATE"\s*value="([^"]*)"\s*/?>', html)
    assert mviewstate, (url, html)
    html = "%s %s" % (html[:mviewstate.start(1)], html[mviewstate.end(1):])
    moutofrange1 = re.search('<font color="Red">Index was out of range.', html)
    
    if moutofrange1:
#        print "EndPoint at", number

        return 0
    else:

        return 1

def Scrape(number, code):
    url = "%s%06d%s" % (urlp, number, code)
    root = lxml.html.parse(url).getroot()
    content = root.cssselect("div#maincontent")
    assert len(content) == 1, url
    tables = content[0].cssselect("table")
    assert 1 <= len(tables) <= 4, (url)
    html = lxml.html.tostring(root)
    mviewstate = re.search('name="__VIEWSTATE"\s*value="([^"]*)"\s*/?>', html)
    assert mviewstate, (url, html)
    html = "%s %s" % (html[:mviewstate.start(1)], html[mviewstate.end(1):])
    moutofrange = re.search('<font color="Red">Index was out of range.', html)
    if moutofrange:
        return None

    data = {"number":number, "code":code, "url":url}
    data["html"] = html

    scraperwiki.sqlite.save(unique_keys=["number", "code", "html"], data=data, table_name="otable")

def MainScrape():
#    for code in ["V", "L", "B", "F", "C"]:
# Current max F is 005599F
# Current max V is 006644V
# Current max L is 000948L
# Current max B is 022953B
# Current max C is 125761C
# TODO: Need to stick some logic in here to deal with the above in a sensible way based on data already gathered into dataset.
#
#
# Be nice, there's a lot of data there so please don't try and get all 160000 records in one bite
# Eat the Elephant a small portion at a time...
# Only managing to get approx 120 records at a time, don't know whether this is a limitation on the 
# target site, or a limitation on scraperwiki, but either way it's going to be slooooooooww
#
## PYTHONY THING: Note when changing the range, python includes the start number and the last number -1
#
# Count back from max so you get the most recent first
# Foreigns
#    for i in range(5351, 4599, -1):
#        Scrape(i, "F")
# NMVs complete as at 11/3/11
#    for i in range(1, 1, -1):
#        Scrape(i, "V")
# Business Names
#   for i in range(22953, 22890, -1):
#       Scrape(i, "B")
# LLCs - already got the first 948 as of 23/02/2011
#    for i in range(949, 1, -1):
#        Scrape(i, "L")
# Companies
#    for i in range(125761, 1, -1):
#        Scrape(i, "C")

#####################        SECTION V           ########################


    PriNoV1 = scraperwiki.sqlite.execute("select number from otable where code = 'V' order by number DESC limit 1")
    print PriNoV1
    PriNoV2 = str(PriNoV1)
    PriNoV3 = re.search("([0-9]{4,6})", PriNoV2)
    print PriNoV3
    PriNoV = int(PriNoV3.group(1))
    print PriNoV, " Code V"

#    for i in range(PriNoV + 2, PriNoV, -1):
#            Scrape(i, "V")
#    return

    i = PriNoV + 1

#    print i

    while SearchEnd (i, "V"):
        Scrape(i, "V")

        i += 1
    
    EndNumber = i
    
    print "Code V start at", PriNoV, "ends at ", EndNumber

#    for i in range(12555, 22953, +1):
#        Scrape(i, "B")

#####################        SECTION B           ########################


    PriNoB1 = scraperwiki.sqlite.execute("select number from otable where code = 'B' order by number DESC limit 1")
    print PriNoB1
    PriNoB2 = str(PriNoB1)
    PriNoB3 = re.search("([0-9]{4,6})", PriNoB2)
    print PriNoB3
    PriNoB = int(PriNoB3.group(1))
    print PriNoB, " Code B"

#    for i in range(PriNoB + 2, PriNoB, -1):
#            Scrape(i, "B")
#    return

    i = PriNoB + 1

#    print i

    while SearchEnd (i, "B"):
        Scrape(i, "B")

        i += 1
    
    EndNumber = i
    
    print "Code B start at", PriNoB, "ends at ", EndNumber

#    for i in range(12555, 22953, +1):
#        Scrape(i, "B")
        

#####################        SECTION L           ########################
#    for i in range(2, 1, -1):
#        Scrape(i, "L")

    PriNoL1 = scraperwiki.sqlite.execute("select number from otable where code ='L' order by number DESC limit 1")
#    print PriNoL1
    PriNoL2 = str(PriNoL1)
    PriNoL3 = re.search("(\d{3,6}?)", PriNoL2)
#    print PriNoL3
    PriNoL = int(PriNoL3.group(1))
#    print PriNoL, " Code L"

    i = PriNoL + 1

    print i

    while SearchEnd (i, "L"):
        Scrape(i, "L")
        i += 1
    
    EndNumber = i
    
    print "Code L start at", PriNoL, "ends at ", EndNumber

#    for i in range(EndNumber, PriNoL, -1):

#####################        SECTION C           ########################
#    for i in range(2, 1, -1):
#        Scrape(i, "L")

    PriNoC1 = scraperwiki.sqlite.execute("select number from otable where code ='C' order by number DESC limit 1")
#    print PriNoL1
    PriNoC2 = str(PriNoC1)
    PriNoC3 = re.search("([0-9]{2,6})", PriNoC2)
#    print PriNoL3
    PriNoC = int(PriNoC3.group(1))
#    print PriNoL, " Code L"

    i = PriNoC + 1

    print i

    while SearchEnd (i, "C"):
        Scrape(i, "C")
        i += 1
    
    EndNumber = i
    
    print "Code C start at", PriNoC, "ends at ", EndNumber

#    for i in range(EndNumber, PriNoL, -1):


MainScrape()


