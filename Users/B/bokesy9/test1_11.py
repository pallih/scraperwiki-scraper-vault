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

    Date1 = scraperwiki.sqlite.execute("SELECT DATETIME()")

    Date2 = str(Date1)  
    Date3 = re.search("(\d\d\d\d[0-9]?)\-(\d\d[0-9]?)\-(\d\d[0-9]?)\s(\d\d[0-9]?)\:(\d\d[0-9]?)\:(\d\d[0-9]?)", Date2)

    Date4 = str(Date3.group(0))
    print "Date4", Date4

    if moutofrange:
        return None

    data = {"number":number, "code":code, "url":url, "DateScrape":Date4}
    data["html"] = html

    scraperwiki.sqlite.save(unique_keys=["number", "code", "html"], data=data, table_name="otable")

    
def MainScrape():

#####################        SECTION B           ########################
##
#
#    PriNoB1 = scraperwiki.sqlite.execute("select number from otable where code = 'B' order by number DESC limit 1")
#    print "PriNoB1", PriNoB1
#    PriNoB2 = str(PriNoB1[u'data'])
#    print "PriNoB2", PriNoB2
#    PriNoB3 = re.search("([0-9]+)", PriNoB2)
#    print "PriNoB3", PriNoB3
#    PriNoB = int(PriNoB3.group(1))
#    print PriNoB, " Code B"

#    PriNoB = 0
#    for i in range(PriNoB + 1, 13000, 1):
#            Scrape(i, "B")
#    return
#
#    i = PriNoB + 1
#
#    print "i", i
#
#    while SearchEnd (i, "B"):
#        Scrape(i, "B")
#
#        i += 1
#   
#    EndNumber = i
#    
#    print "Code B starts at", PriNoB, "ends at ", EndNumber
#
#####################        SECTION L           ########################
##
#
#    PriNoL1 = scraperwiki.sqlite.execute("select number from otable where code = 'L' order by number DESC limit 1")
#    print "PriNoL1", PriNoL1
#    PriNoL2 = str(PriNoL1[u'data'])
#    print "PriNoL2", PriNoL2
#    PriNoL3 = re.search("([0-9]+)", PriNoL2)
#    print "PriNoL3", PriNoL3
#    PriNoL = int(PriNoL3.group(1))
#    print PriNoL, " Code L"
#
#    PriNoL = 0
#    for i in range(PriNoL + 1, 13000, 1):
#            Scrape(i, "L")
#    return
#
#    i = PriNoL + 1
#
#    print "i", i
#
#    while SearchEnd (i, "L"):
#        Scrape(i, "L")
#
#        i += 1
#    
#    EndNumber = i
#    
#    print "Code L starts at", PriNoL, "ends at ", EndNumber
#
#####################        SECTION V          ########################
##
#
#    PriNoV1 = scraperwiki.sqlite.execute("select number from otable where code = 'V' order by number DESC limit 1")
#    print "PriNoV1", PriNoV1
#    PriNoV2 = str(PriNoV1[u'data'])
#    print "PriNoV2", PriNoV2
#    PriNoV3 = re.search("([0-9]+)", PriNoV2)
#    print "PriNoV3", PriNoV3
#    PriNoV = int(PriNoV3.group(1))
#    print PriNoV, " Code V"
#
#    PriNoV = 0
#    for i in range(PriNoV + 1, 13000, 1):
#            Scrape(i, "V")
#    return
#
#    i = PriNoV + 1
#
#    print "i", i
#
#    while SearchEnd (i, "V"):
#        Scrape(i, "V")
#
#        i += 1
#    
#    EndNumber = i
#    
#    print "Code V starts at", PriNoV, "ends at ", EndNumber
#
#####################        SECTION N          ########################
##
#
#    PriNoN1 = scraperwiki.sqlite.execute("select number from otable where code = 'N' order by number DESC limit 1")
#    print "PriNoN1", PriNoN1
#    PriNoN2 = str(PriNoN1)[u'data'])
#    print "PriNoN2", PriNoN2
#    PriNoN3 = re.search("([0-9]+)", PriNoN2)
#    print "PriNoN3", PriNoN3
#    PriNoN = int(PriNoN3.group(1))
#    print PriNoN, " Code N"
#
#    PriNoN = 0
#    for i in range(PriNoN + 1, 13000, 1):
#            Scrape(i, "N")
#    return
#
#    i = PriNoN + 1
#
#    print "i", i
#
#    while SearchEnd (i, "N"):
#        Scrape(i, "N")
#
#        i += 1
#    
#    EndNumber = i
#    
#    print "Code N starts at", PriNoN, "ends at ", EndNumber
#
#####################        SECTION C          ########################
##
#
    PriNoC1 = scraperwiki.sqlite.execute("select number from otable where code = 'C' order by number DESC limit 1")
    print "PriNoC1", PriNoC1
    PriNoC2 = str(PriNoC1[u'data'])
    print "PriNoC2", PriNoC2
    PriNoC3 = re.search("([0-9]+)", PriNoC2)
    print "PriNoC3", PriNoC3
    PriNoC = int(PriNoC3.group(1))
    print PriNoC, " Code C"
#
#    PriNoC = 0
    for i in range(PriNoC + 1, 130000, 1):
            Scrape(i, "C")
    return

    i = PriNoC + 1

    print "i", i

    while SearchEnd (i, "C"):
        Scrape(i, "C")

        i += 1
    
    EndNumber = i
    
    print "Code C starts at", PriNoC, "ends at ", EndNumber











        

        


MainScrape()
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

    Date1 = scraperwiki.sqlite.execute("SELECT DATETIME()")

    Date2 = str(Date1)  
    Date3 = re.search("(\d\d\d\d[0-9]?)\-(\d\d[0-9]?)\-(\d\d[0-9]?)\s(\d\d[0-9]?)\:(\d\d[0-9]?)\:(\d\d[0-9]?)", Date2)

    Date4 = str(Date3.group(0))
    print "Date4", Date4

    if moutofrange:
        return None

    data = {"number":number, "code":code, "url":url, "DateScrape":Date4}
    data["html"] = html

    scraperwiki.sqlite.save(unique_keys=["number", "code", "html"], data=data, table_name="otable")

    
def MainScrape():

#####################        SECTION B           ########################
##
#
#    PriNoB1 = scraperwiki.sqlite.execute("select number from otable where code = 'B' order by number DESC limit 1")
#    print "PriNoB1", PriNoB1
#    PriNoB2 = str(PriNoB1[u'data'])
#    print "PriNoB2", PriNoB2
#    PriNoB3 = re.search("([0-9]+)", PriNoB2)
#    print "PriNoB3", PriNoB3
#    PriNoB = int(PriNoB3.group(1))
#    print PriNoB, " Code B"

#    PriNoB = 0
#    for i in range(PriNoB + 1, 13000, 1):
#            Scrape(i, "B")
#    return
#
#    i = PriNoB + 1
#
#    print "i", i
#
#    while SearchEnd (i, "B"):
#        Scrape(i, "B")
#
#        i += 1
#   
#    EndNumber = i
#    
#    print "Code B starts at", PriNoB, "ends at ", EndNumber
#
#####################        SECTION L           ########################
##
#
#    PriNoL1 = scraperwiki.sqlite.execute("select number from otable where code = 'L' order by number DESC limit 1")
#    print "PriNoL1", PriNoL1
#    PriNoL2 = str(PriNoL1[u'data'])
#    print "PriNoL2", PriNoL2
#    PriNoL3 = re.search("([0-9]+)", PriNoL2)
#    print "PriNoL3", PriNoL3
#    PriNoL = int(PriNoL3.group(1))
#    print PriNoL, " Code L"
#
#    PriNoL = 0
#    for i in range(PriNoL + 1, 13000, 1):
#            Scrape(i, "L")
#    return
#
#    i = PriNoL + 1
#
#    print "i", i
#
#    while SearchEnd (i, "L"):
#        Scrape(i, "L")
#
#        i += 1
#    
#    EndNumber = i
#    
#    print "Code L starts at", PriNoL, "ends at ", EndNumber
#
#####################        SECTION V          ########################
##
#
#    PriNoV1 = scraperwiki.sqlite.execute("select number from otable where code = 'V' order by number DESC limit 1")
#    print "PriNoV1", PriNoV1
#    PriNoV2 = str(PriNoV1[u'data'])
#    print "PriNoV2", PriNoV2
#    PriNoV3 = re.search("([0-9]+)", PriNoV2)
#    print "PriNoV3", PriNoV3
#    PriNoV = int(PriNoV3.group(1))
#    print PriNoV, " Code V"
#
#    PriNoV = 0
#    for i in range(PriNoV + 1, 13000, 1):
#            Scrape(i, "V")
#    return
#
#    i = PriNoV + 1
#
#    print "i", i
#
#    while SearchEnd (i, "V"):
#        Scrape(i, "V")
#
#        i += 1
#    
#    EndNumber = i
#    
#    print "Code V starts at", PriNoV, "ends at ", EndNumber
#
#####################        SECTION N          ########################
##
#
#    PriNoN1 = scraperwiki.sqlite.execute("select number from otable where code = 'N' order by number DESC limit 1")
#    print "PriNoN1", PriNoN1
#    PriNoN2 = str(PriNoN1)[u'data'])
#    print "PriNoN2", PriNoN2
#    PriNoN3 = re.search("([0-9]+)", PriNoN2)
#    print "PriNoN3", PriNoN3
#    PriNoN = int(PriNoN3.group(1))
#    print PriNoN, " Code N"
#
#    PriNoN = 0
#    for i in range(PriNoN + 1, 13000, 1):
#            Scrape(i, "N")
#    return
#
#    i = PriNoN + 1
#
#    print "i", i
#
#    while SearchEnd (i, "N"):
#        Scrape(i, "N")
#
#        i += 1
#    
#    EndNumber = i
#    
#    print "Code N starts at", PriNoN, "ends at ", EndNumber
#
#####################        SECTION C          ########################
##
#
    PriNoC1 = scraperwiki.sqlite.execute("select number from otable where code = 'C' order by number DESC limit 1")
    print "PriNoC1", PriNoC1
    PriNoC2 = str(PriNoC1[u'data'])
    print "PriNoC2", PriNoC2
    PriNoC3 = re.search("([0-9]+)", PriNoC2)
    print "PriNoC3", PriNoC3
    PriNoC = int(PriNoC3.group(1))
    print PriNoC, " Code C"
#
#    PriNoC = 0
    for i in range(PriNoC + 1, 130000, 1):
            Scrape(i, "C")
    return

    i = PriNoC + 1

    print "i", i

    while SearchEnd (i, "C"):
        Scrape(i, "C")

        i += 1
    
    EndNumber = i
    
    print "Code C starts at", PriNoC, "ends at ", EndNumber











        

        


MainScrape()
