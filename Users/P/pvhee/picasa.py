import scraperwiki
import lxml.html
import lxml.etree
import urlparse
import gdata.docs.service
import csv 

def Main():
    #list = [289880, 287252]

    url = "https://picasaweb.google.com/data/feed/api/user/109750673638535496225/albumid/5716360188091683297?kind=photo"
    html = scraperwiki.scrape(url)
    root = lxml.etree.fromstring(html)
    items = root.xpath('/feed/entry');
    for item in items:
        print item


    
    # get list of project numbers and loop through them

def ParseProjectList():
    # Google Docs listing the FP7-PEOPLE-2011-ITN projects
    url = 'https://spreadsheets.google.com/feeds/list/0AmhcXGA9zL3pdFJpYlhfSzhPai0yajZXLXhHNnNuWnc/od6/public/basic?alt=rss'
    html = scraperwiki.scrape(url)
    root = lxml.etree.fromstring(html)
    items = root.xpath('/rss/channel/item/title')
    list = []
    for item in items:
        list.append(item.text)
    return list

def ParseProjectList2():
    url = 'https://docs.google.com/spreadsheet/pub?key=0AmhcXGA9zL3pdGkxMFJrUmFQZFBhM0xuQzRyOU1LNHc&single=true&gid=0&output=csv';
    data = scraperwiki.scrape(url)
    reader = csv.reader(data.splitlines())
    list = []    
    header = 1   
    for row in reader:
        if (header):
            header = 0
            continue
        el = {"pnum" : row[2], "acronym" : row[0], "site" : row[4], "url" : row[5], "contact": row[8], "contacted": row[9], "reply": row[11]}
        list.append(el)

    return list

def ParsePage(url, item):
    print item['pnum'] + ' - ' + url
    html = scraperwiki.scrape(url)
    root = lxml.etree.fromstring(html)
    ccode = root.xpath('/response/channel/item/countrycode')
    iurl = root.xpath('/response/channel/item/url')
    title = root.xpath('/response/channel/item/title')
    if (len(ccode)):
        data = {}
        data['acronym'] = item['acronym']
        data['pnum'] = item['pnum']
        data['site'] = item['site']
        data['site_url'] = item['url']
        data['title'] = title[0].text
        data['country'] = ccode[0].text
        data['url'] = iurl[0].text
        data['contact'] = item['contact']
        data['contacted'] = item['contacted']
        data['reply'] = item['reply']
         # extract the RCN from the query string
        # print data['url']

        parse_url = urlparse.urlparse(data['url']).query.split('&')
        if (len(parse_url) >= 4):
            data['rcn'] = parse_url[3].split('=')[1]
        else:
            print "Error with URL: " + data['url']
            return

        #data['rcn'] = urlparse.urlparse(data['url']).query.split('&')[3].split('=')[1]
        #data['pnum'] = pnum
        
        scraperwiki.sqlite.save(["rcn"], data)
    else:
        print "Error scraping " + url



#ParseProjectList2()
Main()

import scraperwiki
import lxml.html
import lxml.etree
import urlparse
import gdata.docs.service
import csv 

def Main():
    #list = [289880, 287252]

    url = "https://picasaweb.google.com/data/feed/api/user/109750673638535496225/albumid/5716360188091683297?kind=photo"
    html = scraperwiki.scrape(url)
    root = lxml.etree.fromstring(html)
    items = root.xpath('/feed/entry');
    for item in items:
        print item


    
    # get list of project numbers and loop through them

def ParseProjectList():
    # Google Docs listing the FP7-PEOPLE-2011-ITN projects
    url = 'https://spreadsheets.google.com/feeds/list/0AmhcXGA9zL3pdFJpYlhfSzhPai0yajZXLXhHNnNuWnc/od6/public/basic?alt=rss'
    html = scraperwiki.scrape(url)
    root = lxml.etree.fromstring(html)
    items = root.xpath('/rss/channel/item/title')
    list = []
    for item in items:
        list.append(item.text)
    return list

def ParseProjectList2():
    url = 'https://docs.google.com/spreadsheet/pub?key=0AmhcXGA9zL3pdGkxMFJrUmFQZFBhM0xuQzRyOU1LNHc&single=true&gid=0&output=csv';
    data = scraperwiki.scrape(url)
    reader = csv.reader(data.splitlines())
    list = []    
    header = 1   
    for row in reader:
        if (header):
            header = 0
            continue
        el = {"pnum" : row[2], "acronym" : row[0], "site" : row[4], "url" : row[5], "contact": row[8], "contacted": row[9], "reply": row[11]}
        list.append(el)

    return list

def ParsePage(url, item):
    print item['pnum'] + ' - ' + url
    html = scraperwiki.scrape(url)
    root = lxml.etree.fromstring(html)
    ccode = root.xpath('/response/channel/item/countrycode')
    iurl = root.xpath('/response/channel/item/url')
    title = root.xpath('/response/channel/item/title')
    if (len(ccode)):
        data = {}
        data['acronym'] = item['acronym']
        data['pnum'] = item['pnum']
        data['site'] = item['site']
        data['site_url'] = item['url']
        data['title'] = title[0].text
        data['country'] = ccode[0].text
        data['url'] = iurl[0].text
        data['contact'] = item['contact']
        data['contacted'] = item['contacted']
        data['reply'] = item['reply']
         # extract the RCN from the query string
        # print data['url']

        parse_url = urlparse.urlparse(data['url']).query.split('&')
        if (len(parse_url) >= 4):
            data['rcn'] = parse_url[3].split('=')[1]
        else:
            print "Error with URL: " + data['url']
            return

        #data['rcn'] = urlparse.urlparse(data['url']).query.split('&')[3].split('=')[1]
        #data['pnum'] = pnum
        
        scraperwiki.sqlite.save(["rcn"], data)
    else:
        print "Error scraping " + url



#ParseProjectList2()
Main()

