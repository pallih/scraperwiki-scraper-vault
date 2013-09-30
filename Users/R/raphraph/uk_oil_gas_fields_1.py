import scraperwiki
import lxml.html
import urlparse
import sys
import re



def parseDetailPage(url):

    try:
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)
    
    except:
        print sys.exc_info()[0]
        print "Can't download " + url
        return

    fieldInfo = dict()
    
    fieldInfo['name'] = root.xpath("string(//td[@class='s6'])").strip()
    props = root.xpath("//tr[td[@class='s10']]")
    for entry in props:
        prop = entry.xpath("string(./td[@class='s10'])").strip()
        prop = prop.replace(' / ','_').lower().strip().replace(' ','_')
        value = entry.xpath("string(./td[@class='s11' or @class='s12' or @class='s14' or @class='s15'])").strip()
        if len(prop) > 0:
            fieldInfo[prop] = value

    fieldInfo['license'] = root.xpath("string(//td[@class='s19'])").strip()
    fieldInfo['depth_unit'] = root.xpath("string(//td[@class='s17'])").strip()
    #fieldInfo['owner'] = root.xpath("//td[@class='s25']/text()")[0]

    scraperwiki.sqlite.save(unique_keys=['name'], data=fieldInfo, table_name="field_info")

    ownerList = list()
    ownership = root.xpath("//tr[td[@class='s24']]")
    for entry in ownership:
        ownerInfo = dict()
        ownerInfo['name'] = fieldInfo['name']
        ownerInfo['owner'] = entry.xpath("string(./td[@class='s24'])").strip()
        ownerInfo['share'] = entry.xpath("string(./td[@class='s25'])").strip()
        ownerList.append(ownerInfo)

    scraperwiki.sqlite.save(unique_keys=['name','owner'], data=ownerList, table_name="field_owner")
    return



def parseProdPage(url, product):

    try:
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)
    
    except:
        print sys.exc_info()[0]
        print "Can't download " + url
        return

    name = root.xpath("string(//td[@class='s5'])").strip()

    i = 0
    prodList = list()
    prods = root.xpath("//td[@class='s11' or @class='s12']")
    for prod in prods:
        prodInfo = dict()
        prodInfo['name'] = name
        prodInfo['product'] = product
        prodInfo['date'] = prod.xpath("../td[@class='s10' or @class='s52']/text()")[0] + "/" + str((i % 12) + 1)
        #prodInfo['month'] = prod.xpath("../..//td[@class='s8']/text()")
        prodInfo['value'] = prod.text_content()
        prodList.append(prodInfo)
        i = i + 1

    scraperwiki.sqlite.save(unique_keys=['name','product','date'], data=prodList, table_name="field_production")
    return




def parseListPage(url, detail):

    try:
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)
    
    except:
        print sys.exc_info()[0]
        print "Can't download " + url
        return
    
    links = root.xpath("//a[not(contains(.,'full report'))]/@href")
    for link in links:
        if detail == "":
            parseDetailPage(urlparse.urljoin(url, link))
        else:
            parseProdPage(urlparse.urljoin(url, link), detail)

    return


#scraperwiki.sqlite.execute("drop table if exists field_info")
#scraperwiki.sqlite.execute("drop table if exists field_owner")
#scraperwiki.sqlite.execute("drop table if exists field_production")
#scraperwiki.sqlite.execute("create table if not exists field_info (name text)")
#scraperwiki.sqlite.execute("create table if not exists field_owner (name text)")
#scraperwiki.sqlite.execute("create table if not exists field_production (name text)")

parseListPage("https://www.og.decc.gov.uk/fields/fields_index/ukcs+field+information+listed+by+field+name/seclinks.htm", "")
parseListPage("https://www.og.decc.gov.uk/pprs/full_production/oil+production+sorted+by+field/seclinks.htm", "OIL")
parseListPage("https://www.og.decc.gov.uk/pprs/full_production/associated+gas+production+sorted+by+field/seclinks.htm", "Associated GAS")
parseListPage("https://www.og.decc.gov.uk/pprs/full_production/dry+gas+production+by+field/seclinks.htm", "Dry GAS")

import scraperwiki
import lxml.html
import urlparse
import sys
import re



def parseDetailPage(url):

    try:
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)
    
    except:
        print sys.exc_info()[0]
        print "Can't download " + url
        return

    fieldInfo = dict()
    
    fieldInfo['name'] = root.xpath("string(//td[@class='s6'])").strip()
    props = root.xpath("//tr[td[@class='s10']]")
    for entry in props:
        prop = entry.xpath("string(./td[@class='s10'])").strip()
        prop = prop.replace(' / ','_').lower().strip().replace(' ','_')
        value = entry.xpath("string(./td[@class='s11' or @class='s12' or @class='s14' or @class='s15'])").strip()
        if len(prop) > 0:
            fieldInfo[prop] = value

    fieldInfo['license'] = root.xpath("string(//td[@class='s19'])").strip()
    fieldInfo['depth_unit'] = root.xpath("string(//td[@class='s17'])").strip()
    #fieldInfo['owner'] = root.xpath("//td[@class='s25']/text()")[0]

    scraperwiki.sqlite.save(unique_keys=['name'], data=fieldInfo, table_name="field_info")

    ownerList = list()
    ownership = root.xpath("//tr[td[@class='s24']]")
    for entry in ownership:
        ownerInfo = dict()
        ownerInfo['name'] = fieldInfo['name']
        ownerInfo['owner'] = entry.xpath("string(./td[@class='s24'])").strip()
        ownerInfo['share'] = entry.xpath("string(./td[@class='s25'])").strip()
        ownerList.append(ownerInfo)

    scraperwiki.sqlite.save(unique_keys=['name','owner'], data=ownerList, table_name="field_owner")
    return



def parseProdPage(url, product):

    try:
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)
    
    except:
        print sys.exc_info()[0]
        print "Can't download " + url
        return

    name = root.xpath("string(//td[@class='s5'])").strip()

    i = 0
    prodList = list()
    prods = root.xpath("//td[@class='s11' or @class='s12']")
    for prod in prods:
        prodInfo = dict()
        prodInfo['name'] = name
        prodInfo['product'] = product
        prodInfo['date'] = prod.xpath("../td[@class='s10' or @class='s52']/text()")[0] + "/" + str((i % 12) + 1)
        #prodInfo['month'] = prod.xpath("../..//td[@class='s8']/text()")
        prodInfo['value'] = prod.text_content()
        prodList.append(prodInfo)
        i = i + 1

    scraperwiki.sqlite.save(unique_keys=['name','product','date'], data=prodList, table_name="field_production")
    return




def parseListPage(url, detail):

    try:
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)
    
    except:
        print sys.exc_info()[0]
        print "Can't download " + url
        return
    
    links = root.xpath("//a[not(contains(.,'full report'))]/@href")
    for link in links:
        if detail == "":
            parseDetailPage(urlparse.urljoin(url, link))
        else:
            parseProdPage(urlparse.urljoin(url, link), detail)

    return


#scraperwiki.sqlite.execute("drop table if exists field_info")
#scraperwiki.sqlite.execute("drop table if exists field_owner")
#scraperwiki.sqlite.execute("drop table if exists field_production")
#scraperwiki.sqlite.execute("create table if not exists field_info (name text)")
#scraperwiki.sqlite.execute("create table if not exists field_owner (name text)")
#scraperwiki.sqlite.execute("create table if not exists field_production (name text)")

parseListPage("https://www.og.decc.gov.uk/fields/fields_index/ukcs+field+information+listed+by+field+name/seclinks.htm", "")
parseListPage("https://www.og.decc.gov.uk/pprs/full_production/oil+production+sorted+by+field/seclinks.htm", "OIL")
parseListPage("https://www.og.decc.gov.uk/pprs/full_production/associated+gas+production+sorted+by+field/seclinks.htm", "Associated GAS")
parseListPage("https://www.og.decc.gov.uk/pprs/full_production/dry+gas+production+by+field/seclinks.htm", "Dry GAS")

