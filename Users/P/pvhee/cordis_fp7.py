import scraperwiki
import lxml.html
import lxml.etree
import urlparse
import gdata.docs.service
import csv 

nrlatlng = 0;

def Main():
    #list = [289880, 287252]
    list = ParseProjectList2()
    print "Start parsing " + str(len(list)) + " projects"
    for el in list:
        pnum = el['pnum'];
        url = 'http://cordis.europa.eu/newsearch/download.cfm?action=query&collection=CALLS,EN_ACRO,EN_CONT,EN_CRWR,EN_DOCS,EN_PUBLS,EN_EVENTS,EN_FUNDING,EN_NEWS,EN_OFFR,newpart,partreq,EN_PROG,EN_PROJ,EN_RSLT,FTP,STATIC,ICTRESULTS&text=(' +str(pnum) + ')+AND+(("CORDIS":SOURCE)+OR+("EUROPA":SOURCE))&sort=all&querySummary=quick&ENGINE_ID=CORDIS_ENGINE_ID&SEARCH_TYPE_ID=CORDIS_SEARCH_ID&typeResp=xml';
        ParsePage(url, el)

    print "nr latlng = " + str(nrlatlng)
    
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

    latlng = root.xpath('/response/channel/item/LatLng')
    if (len(latlng)):
        global nrlatlng
        nrlatlng = nrlatlng + 1
        #print "has latlng = " + str(latlng)
        latlngtext = latlng[0].text

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

nrlatlng = 0;

def Main():
    #list = [289880, 287252]
    list = ParseProjectList2()
    print "Start parsing " + str(len(list)) + " projects"
    for el in list:
        pnum = el['pnum'];
        url = 'http://cordis.europa.eu/newsearch/download.cfm?action=query&collection=CALLS,EN_ACRO,EN_CONT,EN_CRWR,EN_DOCS,EN_PUBLS,EN_EVENTS,EN_FUNDING,EN_NEWS,EN_OFFR,newpart,partreq,EN_PROG,EN_PROJ,EN_RSLT,FTP,STATIC,ICTRESULTS&text=(' +str(pnum) + ')+AND+(("CORDIS":SOURCE)+OR+("EUROPA":SOURCE))&sort=all&querySummary=quick&ENGINE_ID=CORDIS_ENGINE_ID&SEARCH_TYPE_ID=CORDIS_SEARCH_ID&typeResp=xml';
        ParsePage(url, el)

    print "nr latlng = " + str(nrlatlng)
    
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

    latlng = root.xpath('/response/channel/item/LatLng')
    if (len(latlng)):
        global nrlatlng
        nrlatlng = nrlatlng + 1
        #print "has latlng = " + str(latlng)
        latlngtext = latlng[0].text

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
