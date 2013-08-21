import scraperwiki
import re
import time
import urlparse
import chardet
from scraperwiki.sqlite import save

baselink = "http://brevets-patents.ic.gc.ca/opic-cipo/cpd/eng/search/results.html?query=%28APD%3E="
datelinker = "%29%20%3CAND%3E%20%28APD%3C="
baselinkender = "%29&start=1&num=500&type=boolean_search"
startyear = 2011
startmonth = 1
startday = 1
endyear = 2011
endmonth = 1
endday = 15

def patentscraper(patentlink):
    trycount = 0
    while trycount < 3:
        try: 
            pagesource = scraperwiki.scrape(patentlink)
            patnum = re.search('headers="patentNum"(.+?)</strong>', pagesource, re.DOTALL|re.S)
            patnum = re.search('<strong>(.+?)<', patnum.group(0))
            patnum = re.sub('<strong>', '', patnum.group(0))
            patnum = re.sub('<', '', patnum)
            patname = re.search('headers="EnglishTitle"(.+?)</td>', pagesource, re.DOTALL|re.S)
            patname = re.search('>(.+?)<', patname.group(0), re.DOTALL|re.S)
            patname = re.sub('>', '', patname.group(0), re.DOTALL|re.S)
            patname = re.sub('<', '', patname, re.DOTALL|re.S)
            drawingbase = "http://brevets-patents.ic.gc.ca"
            drawing = re.search('>Representative Drawing<(.+?)alt', pagesource, re.DOTALL|re.S)
            drawing = re.search('src="(.+?)"', drawing.group(0))
            drawing = drawingbase + drawing.group(1)
            owner = re.search('headers="owners"(.+?)</strong>', pagesource, re.DOTALL|re.S)
            owner = re.search('<strong>(.+?)<', owner.group(0))
            owner = owner.group(1)
            country = re.search('headers="owners"(.+?)</li>', pagesource, re.DOTALL|re.S)
            country = re.search('</strong>(.+?)<', country.group(0))
            country = re.search('\((.+?)\)', country.group(1))
            country = country.group(1)
            filed = re.search('headers="filingDate">(.+?)</td>', pagesource, re.DOTALL|re.S)
            filed = re.search('>(.+?)<', filed.group(1), re.DOTALL|re.S)
            filed = filed.group(1) 
            record = {}
            record['Patent Number'] = patnum
            try:
                record['Patent Link'] = patentlink
            except:
                record['Patent Link'] = "None available"
            try:
                record['Title'] = patname
            except:
                record['Title'] = "Invalid Characters"
            try:
                record['Drawing Link'] = drawing
            except:
                record['Drawing Link'] = "Invalid link"
            try:
                record['Owner'] = owner
            except:
                record['Owner'] = "Invalid Characters"
            try:
                record['Owner Country'] = country
            except:
                record['Owner Country'] = "Invalid Characters"
            try:
                record['Filed Date'] = filed
            except:
                record['Filed Date'] = "Invalid Characters"
            try: 
                save([], record)
                trycount = 3
            except: 
                record['Patent Link'] = patentlink
                record['Title'] = "None available"
                record['Drawing Link'] = drawing
                record['Owner'] = "None available"
                record['Owner Country'] = "Not Listed"
                record['Filed Date'] = filed
                save([], record)
                trycount = 3
        except: 
            trycount = trycount + 1

def patentlinkscraper(patentlistpagesource):
    basepatentlink = "http://brevets-patents.ic.gc.ca/opic-cipo/cpd/eng/patent/"
    for every_link in re.finditer('href="/opic-cipo/cpd/eng/patent/(.+?)"', patentlistpagesource):
        patentlink = basepatentlink + every_link.group(1)
        patentscraper(patentlink)
        time.sleep(1)

counter = 1

while counter < 12:
    if startmonth < 2:
        startmonth = 1
        endyear = 2011
        endmonth = 1
        startday = 1
        endday = 15
        pagelink = baselink + str(startyear) + "-" + str(startmonth) + "-" + str(startday) + datelinker + str(endyear) + "-" + str(endmonth) + "-" + str(endday) + baselinkender
        patentlistpagesource = scraperwiki.scrape(pagelink)
        patentlinkscraper(patentlistpagesource)
        startday = 16
        endday = 1
        endyear = 2011
        endmonth = 2
        pagelink = baselink + str(startyear) + "-" + str(startmonth) + "-" + str(startday) + datelinker + str(endyear) + "-" + str(endmonth) + "-" + str(endday) + baselinkender
        patentlistpagesource = scraperwiki.scrape(pagelink)
        patentlinkscraper(patentlistpagesource)
        startmonth = startmonth + 1
    startday = 2
    endday = 15   
    pagelink = baselink + str(startyear) + "-" + str(startmonth) + "-" + str(startday) + datelinker + str(endyear) + "-" + str(endmonth) + "-" + str(endday) + baselinkender
    patentlistpagesource = scraperwiki.scrape(pagelink)
    patentlinkscraper(patentlistpagesource)
    startday = 16
    endday = 1
    endmonth = endmonth + 1
    pagelink = baselink + str(startyear) + "-" + str(startmonth) + "-" + str(startday) + datelinker + str(endyear) + "-" + str(endmonth) + "-" + str(endday) + baselinkender
    patentlistpagesource = scraperwiki.scrape(pagelink)
    patentlinkscraper(patentlistpagesource)
    counter = counter + 1
    startmonth = startmonth + 1
    if startmonth > 11:
        startmonth = 12
        endyear = 2011
        endmonth = 12
        startday = 1
        endday = 15
        pagelink = baselink + str(startyear) + "-" + str(startmonth) + "-" + str(startday) + datelinker + str(endyear) + "-" + str(endmonth) + "-" + str(endday) + baselinkender
        patentlistpagesource = scraperwiki.scrape(pagelink)
        patentlinkscraper(patentlistpagesource)
        startday = 16
        endday = 31
        endyear = 2011
        endmonth = 12
        pagelink = baselink + str(startyear) + "-" + str(startmonth) + "-" + str(startday) + datelinker + str(endyear) + "-" + str(endmonth) + "-" + str(endday) + baselinkender
        patentlistpagesource = scraperwiki.scrape(pagelink)
        patentlinkscraper(patentlistpagesource)


