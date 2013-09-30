import scraperwiki
import lxml.html
import requests
import xlrd, re
import dateutil.parser
import urlparse
import json


html2text=scraperwiki.swimport('html2text')

def parse_publications(i,url,html, response_status):
    record = {}
    record['old_url'] = url
    record['i'] = i
    if response_status == 404: #don't bother with the 404's
        record['status'] = 404
        return record
    root = lxml.html.fromstring(html.encode('iso-8859-1'))
    record['summary'] = root.cssselect('meta[name="DC.description"]')[0].get('content') #summary from metatag
    record['URN'] = root.cssselect('meta[name="DC.identifier"][scheme="ISBN"]')[0].get('content') #ISBN from metatag
    record['ISBN'] = record['URN']
    record['command_paper_number'] = record['URN']
    contentdiv = root.cssselect("div#content")
    if not contentdiv:
        return False
    content = contentdiv[0]
    if not content:
        return False
    titles = list(content.cssselect("div.hgroup h1"))
    if titles:
        record['title'] = titles[0].text_content().strip()
    meta = content.cssselect("table.meta")[0]
    try:
        record['associated_policies'] = meta.xpath('//*[contains(text(), "Mode/topic:")]/following-sibling::*')[0].text_content() #associated policies
    except:
        pass
    try:
        record['associated_organisations'] = meta.xpath('//*[contains(text(), "Publisher:")]/following-sibling::*')[0].text_content() #associate organisations
    except:
        pass
    try:
        record['publication_date'] = meta.xpath('//*[contains(text(), "Published date:")]/following-sibling::*')[0].text_content() #delivered by
    except:
        pass
    try:    
        record['publication_date_iso'] = dateutil.parser.parse(record["publication_date"], dayfirst=True).date().isoformat() #iso date
    except:
        pass
    

    for node in content.cssselect("div.header"): #drop the header info - we are done with it and don't want it in the body text
        node.drop_tree()
    
    links = content.cssselect('a')
    if len(links) > 0: #put the page(s) with large number of attachments into a json field
        n = 1
        attachment_json = []
        for link in links:
            try:
                if 'assets.dft.gov.uk' in link.attrib['href'] or 'webarchive.nationalarchives.gov.uk' in link.attrib['href']:
                    attachment_json.append({'link': link.attrib['href'], 'title': link.text_content()})
                    n = n+1
            except:
                pass
            try:
                if 'tsoshop.co.uk' in link.attrib['href']:
                    record['order_url'] = link.attrib['href']
            except:
                pass
        record['manual'] = 1
        record['z'] = attachment_json
    else: #process the attachments
        n = 1
        for link in links:
            try:
                if 'assets.dft.gov.uk' in link.attrib['href'] or 'webarchive.nationalarchives.gov.uk' in link.attrib['href']:
                    record['attachment_'+str(n)] = link.attrib['href']
                    record['attachment_'+str(n)+'_title'] = link.text_content()
                    n = n+1
            except:
                pass
            try:
                if 'tsoshop.co.uk' in link.attrib['href']:
                    record['order_url'] = link.attrib['href']
            except:
                pass
    record['body'] = html2text.HTML2Text().handle(data=lxml.html.tostring(content)) #bodytext
    record['body'] = record['body'].replace(u"\xa0", u" ") #non breaking spaces
    record['body'] = record['body'].encode('utf-8')

    
    return record

def Publications():
    scraperwiki.sqlite.execute("create table if not exists publications (old_url text, i integer)")
    hurlbatch = scraperwiki.sqlite.execute("select xllinks.i, xllinks.url, html, old.htmlcache.status from xllinks left join old.htmlcache on old.htmlcache.url=xllinks.url left join publications on publications.i=xllinks.i where xllinks.sheetname='Publications' and publications.old_url is null and old.htmlcache.url is not null limit 20") 

    ldata = [ ]
    print "fetched batch", len(hurlbatch["data"])
    for i, url, html, response_status in hurlbatch["data"]:        
        data = parse_publications(i, url, html, response_status)
        if data:
            ldata.append(data)
        else:
            print "Failed to parse", url, html
    myldata=[{'i':x['i'], 'old_url':x['old_url'], 'data':json.dumps(x)} for x in ldata]
    scraperwiki.sqlite.save(["i"], myldata, "publications")
    return len(ldata)

scraperwiki.sqlite.execute("drop table if exists publications")
scraperwiki.sqlite.attach('dftgovuk','old')
while Publications():  pass
import scraperwiki
import lxml.html
import requests
import xlrd, re
import dateutil.parser
import urlparse
import json


html2text=scraperwiki.swimport('html2text')

def parse_publications(i,url,html, response_status):
    record = {}
    record['old_url'] = url
    record['i'] = i
    if response_status == 404: #don't bother with the 404's
        record['status'] = 404
        return record
    root = lxml.html.fromstring(html.encode('iso-8859-1'))
    record['summary'] = root.cssselect('meta[name="DC.description"]')[0].get('content') #summary from metatag
    record['URN'] = root.cssselect('meta[name="DC.identifier"][scheme="ISBN"]')[0].get('content') #ISBN from metatag
    record['ISBN'] = record['URN']
    record['command_paper_number'] = record['URN']
    contentdiv = root.cssselect("div#content")
    if not contentdiv:
        return False
    content = contentdiv[0]
    if not content:
        return False
    titles = list(content.cssselect("div.hgroup h1"))
    if titles:
        record['title'] = titles[0].text_content().strip()
    meta = content.cssselect("table.meta")[0]
    try:
        record['associated_policies'] = meta.xpath('//*[contains(text(), "Mode/topic:")]/following-sibling::*')[0].text_content() #associated policies
    except:
        pass
    try:
        record['associated_organisations'] = meta.xpath('//*[contains(text(), "Publisher:")]/following-sibling::*')[0].text_content() #associate organisations
    except:
        pass
    try:
        record['publication_date'] = meta.xpath('//*[contains(text(), "Published date:")]/following-sibling::*')[0].text_content() #delivered by
    except:
        pass
    try:    
        record['publication_date_iso'] = dateutil.parser.parse(record["publication_date"], dayfirst=True).date().isoformat() #iso date
    except:
        pass
    

    for node in content.cssselect("div.header"): #drop the header info - we are done with it and don't want it in the body text
        node.drop_tree()
    
    links = content.cssselect('a')
    if len(links) > 0: #put the page(s) with large number of attachments into a json field
        n = 1
        attachment_json = []
        for link in links:
            try:
                if 'assets.dft.gov.uk' in link.attrib['href'] or 'webarchive.nationalarchives.gov.uk' in link.attrib['href']:
                    attachment_json.append({'link': link.attrib['href'], 'title': link.text_content()})
                    n = n+1
            except:
                pass
            try:
                if 'tsoshop.co.uk' in link.attrib['href']:
                    record['order_url'] = link.attrib['href']
            except:
                pass
        record['manual'] = 1
        record['z'] = attachment_json
    else: #process the attachments
        n = 1
        for link in links:
            try:
                if 'assets.dft.gov.uk' in link.attrib['href'] or 'webarchive.nationalarchives.gov.uk' in link.attrib['href']:
                    record['attachment_'+str(n)] = link.attrib['href']
                    record['attachment_'+str(n)+'_title'] = link.text_content()
                    n = n+1
            except:
                pass
            try:
                if 'tsoshop.co.uk' in link.attrib['href']:
                    record['order_url'] = link.attrib['href']
            except:
                pass
    record['body'] = html2text.HTML2Text().handle(data=lxml.html.tostring(content)) #bodytext
    record['body'] = record['body'].replace(u"\xa0", u" ") #non breaking spaces
    record['body'] = record['body'].encode('utf-8')

    
    return record

def Publications():
    scraperwiki.sqlite.execute("create table if not exists publications (old_url text, i integer)")
    hurlbatch = scraperwiki.sqlite.execute("select xllinks.i, xllinks.url, html, old.htmlcache.status from xllinks left join old.htmlcache on old.htmlcache.url=xllinks.url left join publications on publications.i=xllinks.i where xllinks.sheetname='Publications' and publications.old_url is null and old.htmlcache.url is not null limit 20") 

    ldata = [ ]
    print "fetched batch", len(hurlbatch["data"])
    for i, url, html, response_status in hurlbatch["data"]:        
        data = parse_publications(i, url, html, response_status)
        if data:
            ldata.append(data)
        else:
            print "Failed to parse", url, html
    myldata=[{'i':x['i'], 'old_url':x['old_url'], 'data':json.dumps(x)} for x in ldata]
    scraperwiki.sqlite.save(["i"], myldata, "publications")
    return len(ldata)

scraperwiki.sqlite.execute("drop table if exists publications")
scraperwiki.sqlite.attach('dftgovuk','old')
while Publications():  pass
