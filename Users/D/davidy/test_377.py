import scraperwiki
import string
# Blank Python
import scraperwiki
import lxml.html           


# function for parsing html ang save data
def parseHTML (html):
    root = lxml.html.fromstring(html)
    for el in root.cssselect("div.addr"):
        title = el.getchildren()[0].getchildren()[1].text
        tel = el.getchildren()[1].text
        addr = el.getchildren()[2].getchildren()[0].text_content() + el.getchildren()[2].getchildren()[1].text_content()
        niceAddr = " ".join(addr.split())
        data = {
            'title' : title,
            'tel' : tel,
            'addr' : niceAddr
        }
        scraperwiki.sqlite.save(unique_keys=['title'], data=data)
# run 50 pages recursively under same character
def runFiftyPages (baseHTML):
    for i in range(0, 50):
        #print i
        #baseHTML + str(i*10 + 1)
        htmlvar = baseHTML + str(i*10 + 1)
        html = scraperwiki.scrape(htmlvar)
        try:
            parseHTML(html)
        except:
            break
def searchHairdresser ():
    #baseHTML = "http://uk.local.yahoo.com/Greater_London/London/hairdresser/search-44418.html?fr=sfp&cs=title&cb="
    for i in range (9, 26):
        letter = string.uppercase[i]
        baseHTML = "http://uk.local.yahoo.com/Greater_London/London/hairdresser/search-44418.html?fr=sfp&cs=title&fw=" + letter +"&cb="
        #print letter
        runFiftyPages (baseHTML)

def searchSalons():
    #baseHTML = "http://uk.local.yahoo.com/Greater_London/London/beauty_salons/search-44418.html?fr=sfp&cs=title&cb="
    #runFiftyPages(baseHTML)
    for i in range (15, 26):
        letter = string.uppercase[i]
        baseHTML = "http://uk.local.yahoo.com/Greater_London/London/beauty_salons/search-44418.html?fr=sfp&cs=title&fw=" + letter +"&cb="
        runFiftyPages (baseHTML)

searchSalons()

#root = lxml.html.fromstring(html)
#for el in root.cssselect("div.addr  h2"):
    #print el.text_content()
    # 2 children ["span", "a"]
#    print el.getchildren()[1].text
    #print lxml.html.tostring(el)
#for el in root.cssselect("div.addr  h3"):
#    print el.text
#for el in root.cssselect("div.adr"):
#    print el.getchildren()[0].text_content() + el.getchildren()[1].text_content()
#for tr in root.cssselect("div[align='left'] tr"):
#    tds = tr.cssselect("td")
#    if len(tds)==12:
#        data = {
#            'country' : tds[0].text_content(),
#            'years_in_school' : int(tds[4].text_content())
#        }
#        print data
#        scraperwiki.sqlite.save(unique_keys=['country'], data=data)
import scraperwiki
import string
# Blank Python
import scraperwiki
import lxml.html           


# function for parsing html ang save data
def parseHTML (html):
    root = lxml.html.fromstring(html)
    for el in root.cssselect("div.addr"):
        title = el.getchildren()[0].getchildren()[1].text
        tel = el.getchildren()[1].text
        addr = el.getchildren()[2].getchildren()[0].text_content() + el.getchildren()[2].getchildren()[1].text_content()
        niceAddr = " ".join(addr.split())
        data = {
            'title' : title,
            'tel' : tel,
            'addr' : niceAddr
        }
        scraperwiki.sqlite.save(unique_keys=['title'], data=data)
# run 50 pages recursively under same character
def runFiftyPages (baseHTML):
    for i in range(0, 50):
        #print i
        #baseHTML + str(i*10 + 1)
        htmlvar = baseHTML + str(i*10 + 1)
        html = scraperwiki.scrape(htmlvar)
        try:
            parseHTML(html)
        except:
            break
def searchHairdresser ():
    #baseHTML = "http://uk.local.yahoo.com/Greater_London/London/hairdresser/search-44418.html?fr=sfp&cs=title&cb="
    for i in range (9, 26):
        letter = string.uppercase[i]
        baseHTML = "http://uk.local.yahoo.com/Greater_London/London/hairdresser/search-44418.html?fr=sfp&cs=title&fw=" + letter +"&cb="
        #print letter
        runFiftyPages (baseHTML)

def searchSalons():
    #baseHTML = "http://uk.local.yahoo.com/Greater_London/London/beauty_salons/search-44418.html?fr=sfp&cs=title&cb="
    #runFiftyPages(baseHTML)
    for i in range (15, 26):
        letter = string.uppercase[i]
        baseHTML = "http://uk.local.yahoo.com/Greater_London/London/beauty_salons/search-44418.html?fr=sfp&cs=title&fw=" + letter +"&cb="
        runFiftyPages (baseHTML)

searchSalons()

#root = lxml.html.fromstring(html)
#for el in root.cssselect("div.addr  h2"):
    #print el.text_content()
    # 2 children ["span", "a"]
#    print el.getchildren()[1].text
    #print lxml.html.tostring(el)
#for el in root.cssselect("div.addr  h3"):
#    print el.text
#for el in root.cssselect("div.adr"):
#    print el.getchildren()[0].text_content() + el.getchildren()[1].text_content()
#for tr in root.cssselect("div[align='left'] tr"):
#    tds = tr.cssselect("td")
#    if len(tds)==12:
#        data = {
#            'country' : tds[0].text_content(),
#            'years_in_school' : int(tds[4].text_content())
#        }
#        print data
#        scraperwiki.sqlite.save(unique_keys=['country'], data=data)
