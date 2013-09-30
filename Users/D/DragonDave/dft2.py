import scraperwiki
import lxml.html
import requests
import xlrd, re
import dateutil.parser
import urlparse
import json
import csv
import StringIO
import json


html2text=scraperwiki.swimport('html2text')

xlurl = 'https://dl.dropbox.com/s/ugyauhxhs3xuf1z/dft_scraping_instructions_new.xls?dl=1' #'dft scraping instructions new' doc emailed by dragon on sep 12.

csvorigin={'consult':'https://www.dropbox.com/s/qn1by61snu2mk2l/dft-consultations-second-migration - consultations_new_and_modified-.csv',
'news':'https://www.dropbox.com/s/i6amgww0oynww5d/dft-news-second-migration%20-%20story_new_and_modified.csv',
'pubs':'https://www.dropbox.com/s/ukbjd880wvvsnk6/dft-publications-second-migration%20-%20publications_new_and_modified.csv',
'speeches':'https://www.dropbox.com/s/8r0x43ugoh5yvp5/dft-speeches-second-migration%20-%20speeches_new_and_modified-from%20.csv',
'statsrel':'https://www.dropbox.com/s/a7pbrdwqc0an58c/dft-stats-release-second-migration%20-%20stats_releases_new_and_modified.csv',
'statstab':'https://www.dropbox.com/s/mrwhyy1xdtnzt78/dft-stats-tables-second-migration%20-%20dft%20statistics%20tables.csv'}


def getcsv(url, index, link=0, title=1, skip=[]):
    print url, index
    r=requests.get(url+"?dl=1", verify=False)
    raw=r.content
    r.raise_for_status()
    csvreader = csv.reader(StringIO.StringIO(raw))
    builder=[]
    for i,r in enumerate(csvreader):
        if i in skip:
            continue
        if len(r) <= link:
            continue
        if i%100 == 3: print i,r
        #data={'link':r[link].strip(), 'title':t, 'html':page_u, 'status':page_stat, 'meta':{}, 'type':index}
        data={'sheetname':index, 'i': i, 'url':r[link].strip()}
        builder.append(data)
    print builder[:4]
    scraperwiki.sqlite.save(table_name='xllinks',data=builder, unique_keys=['url'],verbose=0)
    return builder

def LoadCSVlinks():
    for i in csvorigin:
        getcsv(csvorigin[i],i)

# julians xls loader
def LoadXLlinks():
    book = xlrd.open_workbook(file_contents=requests.get(xlurl,verify=False).content)
    for i in [0,2,4,6,8,10,12]:
        sheet = book.sheet_by_index(i)
        print sheet.name, "rows:", sheet.nrows
        ldata = [ ] 
        for i in range(sheet.nrows): 
            sheetvalue = sheet.cell(i, 0).value.strip()
            if sheetvalue:
                ldata.append({"sheetname":sheet.name, "i":i, "url":sheetvalue})
        scraperwiki.sqlite.save(["sheetname", "i"], ldata, "xllinks")

# julians raw scraper
def ScrapeRaw():
    scraperwiki.sqlite.execute("create table if not exists htmlcache (url text)")
    urlbatch = scraperwiki.sqlite.execute("select xllinks.url from xllinks left join htmlcache on htmlcache.url = xllinks.url where htmlcache.url is null limit 30")
    urlbatch = [u[0]  for u in urlbatch["data"]]
    if not urlbatch:
        return False
    ldata = [ ]
    print urlbatch
    for url in urlbatch:
        if url == "Old URL" or url == 'public_url':
            continue
        page_req=requests.get(url)
        page_raw=page_req.content
        data = {'url':url, 'status':page_req.status_code}
        data['html']=unicode(page_raw, 'iso-8859-1')
        ldata.append(data)
    scraperwiki.sqlite.save(["url"], ldata, "htmlcache")
    return True

def parse_news(i,url,html, response_status):
    record = {}
    record['old_url'] = url
    record['i'] = i
    if response_status == 404: #don't bother with the 404's
        record['status'] = 404
        return record
    root = lxml.html.fromstring(html.encode('iso-8859-1'))
    record['summary'] = root.cssselect('meta[name="DC.description"]')[0].get('content') #summary from metatag
    contentdiv = root.cssselect("div#content")
    if not contentdiv:
        return False
    content = contentdiv[0]
    if not content:
        return False
    titles = list(content.cssselect("div.hgroup h1"))
    if titles:
        record['title'] = titles[0].text_content().strip() #stripped title
    meta = content.cssselect("table.meta")[0]
    try:
        record['associated_organisations'] = meta.xpath('//*[contains(text(), "Publisher:")]/following-sibling::*')[0].text_content() #associate organisations
    except:
        pass
    try:
        record['associated_policies'] = meta.xpath('//*[contains(text(), "Mode/topic:")]/following-sibling::*')[0].text_content() #associate policies
    except:
        pass
    try:
        record['first_published'] = meta.xpath('//*[contains(text(), "Published date:")]/following-sibling::*')[0].text_content().strip() # first published date
    except:
        pass
    try:
        record['type'] = meta.xpath('//*[contains(text(), "Type:")]/following-sibling::*')[0].text_content().strip() # type
    except:
        pass
    try:    
        record['date'] = dateutil.parser.parse(record["first_published"], dayfirst=True).date().isoformat() #iso date
    except:
        pass
    
    for node in content.cssselect("div.header"): #drop the header info - we are done with it and don't want it in the body text
        node.drop_tree()
    #record['body'] = html2text.HTML2Text().handle(data=lxml.html.tostring(content,encoding=unicode)) #bodytext
    
    #record['body'] = html2text.HTML2Text().handle(data=lxml.html.tostring(content,encoding="ascii")) #bodytext

    #encoding mess:
    record['body'] = html2text.HTML2Text().handle(data=lxml.html.tostring(content)) #bodytext
    record['body'] = record['body'].replace(u"\xa0", u" ") #non breaking spaces
    record['body'] = record['body'].encode('utf-8')
    #print lxml.html.tostring(content,encoding="ascii")
    #print repr(record['body'])
    
    return record

def News():
    #scraperwiki.sqlite.execute("drop table if exists news")
    scraperwiki.sqlite.execute("create table if not exists news (old_url text, i integer)")
    hurlbatch = scraperwiki.sqlite.execute("select xllinks.i, xllinks.url, html, htmlcache.status from xllinks left join htmlcache on htmlcache.url=xllinks.url left join news on news.i=xllinks.i where xllinks.sheetname='news' and news.old_url is null and htmlcache.url is not null limit 20")
    ldata = [ ]
    print "fetched batch", len(hurlbatch["data"])
    for i, url, html, response_status in hurlbatch["data"]:        
        data = parse_news(i, url, html, response_status)
        if data:
            ldata.append(data)
        else:
            print "Failed to parse", url, html
    scraperwiki.sqlite.save(["i"], ldata, "news")
    return len(ldata)

def parse_speeches(i,url,html, response_status):
    record = {}
    record['old_url'] = url
    record['i'] = i
    if response_status == 404: #don't bother with the 404's
        record['status'] = 404
        return record
    root = lxml.html.fromstring(html.encode('iso-8859-1'))
    record['summary'] = root.cssselect('meta[name="DC.description"]')[0].get('content') #summary from metatag
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
        record['associated_organisations'] = meta.xpath('//*[contains(text(), "Publisher:")]/following-sibling::*')[0].text_content() #associate organisations
    except:
        pass
    try:
        record['delivered_by'] = meta.xpath('//*[contains(text(), "Delivered by:")]/following-sibling::*')[0].text_content() #delivered by
    except:
        pass
    try:
        record['delivered_on_date'] = meta.xpath('//*[contains(text(), "Delivered date:")]/following-sibling::*')[0].text_content().strip() # delivered on date
    except:
        pass
    try:
        record['speech_type'] = meta.xpath('//*[contains(text(), "Type:")]/following-sibling::*')[0].text_content().strip() # speech type
    except:
        pass
    try:
        record['event'] = meta.xpath('//*[contains(text(), "Event:")]/following-sibling::*')[0].text_content().strip() # event
    except:
        pass
    try:
        record['location'] = meta.xpath('//*[contains(text(), "Location:")]/following-sibling::*')[0].text_content().strip() # location
    except:
        pass
    if 'event' in record and 'location' in record:
        record['event_and_location'] = record['event'] + ', ' + record['location'] # event + location 
    try:    
        record['date'] = dateutil.parser.parse(record["delivered_on_date"], dayfirst=True).date().isoformat() #iso date
    except:
        pass
    try:
        record['associated_policies'] = meta.xpath('//*[contains(text(), "Mode/topic:")]/following-sibling::*')[0].text_content() #associate policies
    except:
        pass    
    for node in content.cssselect("div.header"): #drop the header info - we are done with it and don't want it in the body text
        node.drop_tree()
    record['body'] = html2text.HTML2Text().handle(data=lxml.html.tostring(content)) #bodytext
    record['body'] = record['body'].replace(u"\xa0", u" ") #non breaking spaces
    record['body'] = record['body'].encode('utf-8')
    return record

def Speeches():
    #scraperwiki.sqlite.execute("drop table if exists speeches")
    scraperwiki.sqlite.execute("create table if not exists speeches (old_url text, i integer)")
    hurlbatch = scraperwiki.sqlite.execute("select xllinks.i, xllinks.url, html, htmlcache.status from xllinks left join htmlcache on htmlcache.url=xllinks.url left join speeches on speeches.i=xllinks.i where xllinks.sheetname='speeches' and speeches.old_url is null and htmlcache.url is not null limit 20")
    ldata = [ ]
    print "fetched batch", len(hurlbatch["data"])
    for i, url, html, response_status in hurlbatch["data"]:        
        data = parse_speeches(i, url, html, response_status)
        if data:
            ldata.append(data)
        else:
            print "Failed to parse", url, html
    scraperwiki.sqlite.save(["i"], ldata, "speeches")
    return len(ldata)

def parse_consultations(i,url,html, response_status):
    record = {}
    record['old_url'] = url
    record['i'] = i
    if response_status == 404: #don't bother with the 404's
        record['status'] = 404
        return record
    root = lxml.html.fromstring(html)
    record['summary'] = root.cssselect('meta[name="DC.description"]')[0].get('content') #summary from metatag
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
        record['type'] = meta.xpath('//*[contains(text(), "Type:")]/following-sibling::*')[0].text_content() #type
    except:
        pass
    try:
        record['opening_date'] = meta.xpath('//*[contains(text(), "Published date:")]/following-sibling::*')[0].text_content().strip() # opening date
    except:
        pass
    try:
        record['closing_date'] = meta.xpath('//*[contains(text(), "Closing date:")]/following-sibling::*')[0].text_content().strip() # closing date
    except:
        pass
    try:    
        record['opening_date_iso'] = dateutil.parser.parse(record["opening_date"], dayfirst=True).date().isoformat() #iso date
    except:
        pass
    try:    
        record['closing_date_iso'] = dateutil.parser.parse(record["closing_date"], dayfirst=True).date().isoformat() #iso date
    except:
        pass
    for node in content.cssselect("div.header"): #drop the header info - we are done with it and don't want it in the body text
        node.drop_tree()
    record['body'] = html2text.HTML2Text().handle(data=lxml.html.tostring(content)) #bodytext
    #response = content.xpath('//h2[text()="Consultation responses"]//following-sibling::ul')
    responses = content.xpath('//h2[text()="Consultation responses"]//following-sibling::ul[following::h2[text()="Consultation documents"]]')    
    try:
        n = 1
        for r in responses:
            record['response_'+str(n)+'_title'] = r[0][0].text
            record['response_'+str(n)]= r[0][0].attrib['href']
            n = n+1
    except:
        pass
    respond = content.xpath('//h2[@id="respond-to-the-consultation"]//following-sibling::p[following::h2[@id="related"]]')
    #respond = content.xpath('//h2[@id="respond-to-the-consultation"]')
    record['how_to_respond'] = "\n".join(html2text.HTML2Text().handle(data=lxml.html.tostring(p))  for p in respond)
    #respondtext=
    #for r in respond:
    #    print r.text_content()
    links = root.xpath('//div[@property="dc:abstract"]//li/a/.')
    n = 1
    for link in links:
      
       try:
           if 'assets.dft.gov.uk' in link.attrib['href'] or 'webarchive.nationalarchives.gov.uk' in link.attrib['href']:
               record['attachment_'+str(n)] = link.attrib['href']
               record['attachment_'+str(n)+'_title'] = link.text_content()
               n = n+1
       except:
           pass
    #print record
    return record

def Consultations():
    #scraperwiki.sqlite.execute("drop table if exists consultations")
    scraperwiki.sqlite.execute("create table if not exists consultations (old_url text, i integer)")
    hurlbatch = scraperwiki.sqlite.execute("select xllinks.i, xllinks.url, html, htmlcache.status from xllinks left join htmlcache on htmlcache.url=xllinks.url left join consultations on consultations.i=xllinks.i where xllinks.sheetname='consult' and consultations.old_url is null and htmlcache.url is not null limit 20")
    ldata = [ ]
    print "fetched batch", len(hurlbatch["data"])
    for i, url, html, response_status in hurlbatch["data"]:        
        data = parse_consultations(i, url, html.encode('latin-1'), response_status)
        if data:
            ldata.append(data)
            print data
        else:
            print "Failed to parse", url, html
    scraperwiki.sqlite.save(["i"], ldata, "consultations")
    return len(ldata)

def parse_publications(i,url,html, response_status):
    record = {}
    record['old_url'] = url
    print url
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
    
    links = content.xpath('//li/a/.')
    
    n = 1
    jsonattach=[]
    for link in links:
        #print link.attrib['href']
        try:
            if 'assets.dft.gov.uk' in link.attrib['href'] or 'webarchive.nationalarchives.gov.uk' in link.attrib['href']:
                #record['attachment_'+str(n)] = link.attrib['href']
                #record['attachment_'+str(n)+'_title'] = link.text_content()
                jsonattach.append({'link':link.attrib['href'], 'title':link.text_content()})
                n = n+1
            record['jsonattach']=json.dumps(jsonattach)
        except:
            pass

    record['body'] = html2text.HTML2Text().handle(data=lxml.html.tostring(content)) #bodytext
    record['body'] = record['body'].replace(u"\xa0", u" ") #non breaking spaces
    record['body'] = record['body'].encode('utf-8')

    
    return record

def Publications():
    #scraperwiki.sqlite.execute("drop table if exists publications")
    scraperwiki.sqlite.execute("create table if not exists publications (old_url text, i integer)")
    hurlbatch = scraperwiki.sqlite.execute("select xllinks.i, xllinks.url, html, htmlcache.status from xllinks left join htmlcache on htmlcache.url=xllinks.url left join publications on publications.i=xllinks.i where xllinks.sheetname='pubs' and publications.old_url is null and htmlcache.url is not null limit 20") 

    ldata = [ ]
    print "fetched batch", len(hurlbatch["data"])
    for i, url, html, response_status in hurlbatch["data"]:        
        data = parse_publications(i, url, html, response_status)
        if data:
            ldata.append(data)
        else:
            print "Failed to parse", url, html
    print repr(ldata)
    scraperwiki.sqlite.save(["i"], ldata, "publications")
    return len(ldata)

def parse_fois(i,url,html, response_status):
    record = {}
    record['old_url'] = url
    record['i'] = i
    if response_status == 404: #don't bother with the 404's
        record['status'] = 404
        return record
    root = lxml.html.fromstring(html.encode('iso-8859-1'))
    record['summary'] = root.cssselect('meta[name="DC.description"]')[0].get('content') #summary from metatag
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
    try:
        record['URN'] = meta.xpath('//*[contains(text(), "FOI Reference:")]/following-sibling::*')[0].text_content() #delivered by
    except:
        pass 

    for node in content.cssselect("div.header"): #drop the header info - we are done with it and don't want it in the body text
        node.drop_tree()
    
    links = content.cssselect('a')
    if len(links) > 50: #put the page(s) with large number of attachments into a json field
        n = 1
        attachment_json = {}
        for link in links:
            try:
                if 'href' in link.attrib and ('assets.dft.gov.uk' in link.attrib['href'] or 'webarchive.nationalarchives.gov.uk' in link.attrib['href']):
                    attachment_json['attachment_'+str(n)] = link.attrib['href']
                    attachment_json['attachment_'+str(n)+'_title'] = link.text_content()
                    n = n+1
            except:
                pass
        record['manual'] = 1
        record['attachment_json'] = json.dumps(attachment_json)
    else: #process the attachments
        n = 1
        for link in links:
            try:
                if 'href' in link.attrib and ('assets.dft.gov.uk' in link.attrib['href'] or 'webarchive.nationalarchives.gov.uk' in link.attrib['href']):
                    record['attachment_'+str(n)] = link.attrib['href']
                    record['attachment_'+str(n)+'_title'] = link.text_content()
                    n = n+1
            except:
                pass

    record['body'] = html2text.HTML2Text().handle(data=lxml.html.tostring(content)) #bodytext
    record['body'] = record['body'].replace(u"\xa0", u" ") #non breaking spaces
    record['body'] = record['body'].encode('utf-8')
    vcard = root.cssselect("div.vcard")
    vcard = vcard[0]
    record['contact_info'] = html2text.HTML2Text().handle(data=lxml.html.tostring(vcard))
    return record

def FOIs():
    #scraperwiki.sqlite.execute("drop table if exists fois")
    scraperwiki.sqlite.execute("create table if not exists fois (old_url text, i integer)")
    hurlbatch = scraperwiki.sqlite.execute("select xllinks.i, xllinks.url, html, htmlcache.status from xllinks left join htmlcache on htmlcache.url=xllinks.url left join fois on fois.i=xllinks.i where xllinks.sheetname='foi' and fois.old_url is null and htmlcache.url is not null limit 20")
    ldata = [ ]
    print "fetched batch", len(hurlbatch["data"])
    for i, url, html, response_status in hurlbatch["data"]:        
        data = parse_fois(i, url, html, response_status)
        if data:
            ldata.append(data)
        else:
            print "Failed to parse", url, html
    scraperwiki.sqlite.save(["i"], ldata, "fois")
    return len(ldata)

def parse_srs(i,url,html, response_status):
    record = {}
    record['old_url'] = url
    record['i'] = i
    if response_status == 404: #don't bother with the 404's
        record['status'] = 404
        return record
    root = lxml.html.fromstring(html.encode('iso-8859-1'))
    record['summary'] = root.cssselect('meta[name="DC.description"]')[0].get('content') #summary from metatag
    record['type'] = 'release'
    type_img = root.xpath('//img[@alt="National Statistics logo"]')
    if type_img:
        record['type'] = 'National Stats'
    chart = root.xpath('//div[@id="line_chart"]')
    if chart:
        record['chart'] = 'yes'
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
        record['associated_policies'] = meta.xpath('//*[contains(text(), "Statistics topic:")]/following-sibling::*')[0].text_content() #associated policies
    except:
        pass
    try:
        record['associated_organisations'] = meta.xpath('//*[contains(text(), "Publisher:")]/following-sibling::*')[0].text_content() #associate organisations
    except:
        pass
    try:
        record['publication_date'] = meta.xpath('//*[contains(text(), "Published date:")]/following-sibling::*')[0].text_content().replace(u'\xa0', u'')
    except:
        pass
    try:    
        record['publication_date_iso'] = dateutil.parser.parse(record["publication_date"], dayfirst=True).date().isoformat() #iso date
    except:
        pass
    try:
        record['publication_series'] = meta.xpath('//*[contains(text(), "Series:")]/following-sibling::*')[0].text_content() #delivered by
    except:
        pass 
    print record
    for node in content.cssselect("div.header"): #drop the header info - we are done with it and don't want it in the body text
        node.drop_tree()
    
    links = content.cssselect('a')
    if len(links) > 50: #put the page(s) with large number of attachments into a json field
        n = 1
        attachment_json = {}
        for link in links:
            try:
                if 'assets.dft.gov.uk' in link.attrib['href'] or 'webarchive.nationalarchives.gov.uk' in link.attrib['href']:
                    attachment_json['attachment_'+str(n)] = link.attrib['href']
                    attachment_json['attachment_'+str(n)+'_title'] = link.text_content()
                    n = n+1
            except:
                pass
        record['manual'] = 1
        record['attachment_json'] = json.dumps(attachment_json)
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

    record['body'] = html2text.HTML2Text().handle(data=lxml.html.tostring(content)) #bodytext
    record['body'] = record['body'].replace(u"\xa0", u" ") #non breaking spaces
    record['body'] = record['body'].encode('utf-8')
    print record['body']
    return record

def SRs():
    #scraperwiki.sqlite.execute("drop table if exists srs")
    scraperwiki.sqlite.execute("create table if not exists srs(old_url text, i integer)")
    hurlbatch = scraperwiki.sqlite.execute("select xllinks.i, xllinks.url, html, htmlcache.status from xllinks left join htmlcache on htmlcache.url=xllinks.url left join srs on srs.i=xllinks.i where xllinks.sheetname='statsrel' and srs.old_url is null and htmlcache.url is not null limit 20")
    ldata = [ ]
    print "fetched batch", len(hurlbatch["data"])
    for i, url, html, response_status in hurlbatch["data"]:        
        data = parse_srs(i, url, html, response_status)
        if data:
            ldata.append(data)
        else:
            print "Failed to parse", url, html
    scraperwiki.sqlite.save(["i"], ldata, "srs")
    return len(ldata)

def parse_sts(i,url,html, response_status):
    record = {}
    record['old_url'] = url
    record['i'] = i
    if response_status == 404: #don't bother with the 404's
        record['status'] = 404
        return record
    root = lxml.html.fromstring(html.encode('iso-8859-1'))
    record['summary'] = root.cssselect('meta[name="DC.description"]')[0].get('content') #summary from metatag
    
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
        record['geo_scope'] = meta.xpath('//*[contains(text(), "Geographical scope:")]/following-sibling::*')[0].text_content() 
    except:
        pass
    try:
        record['geo_breakdown'] = meta.xpath('//*[contains(text(), "Geographical breakdown:")]/following-sibling::*')[0].text_content() 
    except:
        pass
    try:
        record['urn'] = meta.xpath('//*[contains(text(), "Reference:")]/following-sibling::*')[0].text_content().replace(u'\xa0', u'') #delivered by
    except:
        pass
    try:
        record['associated_policies'] = meta.xpath('//*[contains(text(), "Statistics topic:")]/following-sibling::*')[0].text_content() #associated policies
    except:
        pass
    try:
        record['associated_organisations'] = meta.xpath('//*[contains(text(), "Publisher:")]/following-sibling::*')[0].text_content() #associate organisations
    except:
        pass
    try:
        record['publication_date'] = meta.xpath('//*[contains(text(), "Published date:")]/following-sibling::*')[0].text_content().replace(u'\xa0', u'')
    except:
        pass
    try:    
        record['publication_date_iso'] = dateutil.parser.parse(record["publication_date"], dayfirst=True).date().isoformat() #iso date
    except:
        pass
    try:
        record['publication_series'] = meta.xpath('//*[contains(text(), "Series:")]/following-sibling::*')[0].text_content() #delivered by
    except:
        pass
    try:
        record['type'] = meta.xpath('//*[contains(text(), "Type:")]/following-sibling::*')[0].text_content() #delivered by
    except:
        pass
    for node in content.cssselect("div.header"): #drop the header info - we are done with it and don't want it in the body text
        node.drop_tree()
    for node in content.xpath('div[@id="secondary"]'): #drop the secondary 
        node.drop_tree()
    
    #links = content.xpath('//li/a/.')
    #linksul = content.xpath('//h2[text()="Download table"]//following-sibling::*')
    #for link in linksul:
    #    print link.tag
    links = root.xpath('//div[@id="content"]//li/a/.')
   
    n = 1
    for link in links:
      
       try:
           if 'assets.dft.gov.uk' in link.attrib['href'] or 'webarchive.nationalarchives.gov.uk' in link.attrib['href']:
               record['attachment_'+str(n)] = link.attrib['href']
               record['attachment_'+str(n)+'_title'] = link.text_content()
               n = n+1
       except:
           pass

    record['body'] = html2text.HTML2Text().handle(data=lxml.html.tostring(content)) #bodytext
    record['body'] = record['body'].replace(u"\xa0", u" ") #non breaking spaces
    record['body'] = record['body'].encode('utf-8')
    print record
    return record

def STs():
    #scraperwiki.sqlite.execute("drop table if exists sts")
    scraperwiki.sqlite.execute("create table if not exists sts(old_url text, i integer)")
    hurlbatch = scraperwiki.sqlite.execute("select xllinks.i, xllinks.url, html, htmlcache.status from xllinks left join htmlcache on htmlcache.url=xllinks.url left join sts on sts.i=xllinks.i where xllinks.sheetname='statstab' and sts.old_url is null and htmlcache.url is not null limit 20")
    ldata = [ ]
    print "fetched batch", len(hurlbatch["data"])
    for i, url, html, response_status in hurlbatch["data"]:        
        data = parse_sts(i, url, html, response_status)
        if data:
            ldata.append(data)
        else:
            print "Failed to parse", url, html
    scraperwiki.sqlite.save(["i"], ldata, "sts")
    return len(ldata)

def fixfoi():
    print scraperwiki.sqlite.execute("UPDATE xllinks SET sheetname = 'foi' WHERE sheetname = 'pubs' AND url LIKE 'http://www.dft.gov.uk/foi/%'")
    scraperwiki.sqlite.commit()

scraperwiki.sqlite.execute('drop table publications')
scraperwiki.sqlite.commit()
#exit()
#LoadCSVlinks()
#print "parse CSV done"
#while ScrapeRaw(): pass
#print "RAW done"
#while News():  pass
#while Speeches():  pass
#while Consultations():  pass
#fixfoi()
while Publications():  pass
#while FOIs():  pass
#while SRs():  pass
#while STs():  pass
import scraperwiki
import lxml.html
import requests
import xlrd, re
import dateutil.parser
import urlparse
import json
import csv
import StringIO
import json


html2text=scraperwiki.swimport('html2text')

xlurl = 'https://dl.dropbox.com/s/ugyauhxhs3xuf1z/dft_scraping_instructions_new.xls?dl=1' #'dft scraping instructions new' doc emailed by dragon on sep 12.

csvorigin={'consult':'https://www.dropbox.com/s/qn1by61snu2mk2l/dft-consultations-second-migration - consultations_new_and_modified-.csv',
'news':'https://www.dropbox.com/s/i6amgww0oynww5d/dft-news-second-migration%20-%20story_new_and_modified.csv',
'pubs':'https://www.dropbox.com/s/ukbjd880wvvsnk6/dft-publications-second-migration%20-%20publications_new_and_modified.csv',
'speeches':'https://www.dropbox.com/s/8r0x43ugoh5yvp5/dft-speeches-second-migration%20-%20speeches_new_and_modified-from%20.csv',
'statsrel':'https://www.dropbox.com/s/a7pbrdwqc0an58c/dft-stats-release-second-migration%20-%20stats_releases_new_and_modified.csv',
'statstab':'https://www.dropbox.com/s/mrwhyy1xdtnzt78/dft-stats-tables-second-migration%20-%20dft%20statistics%20tables.csv'}


def getcsv(url, index, link=0, title=1, skip=[]):
    print url, index
    r=requests.get(url+"?dl=1", verify=False)
    raw=r.content
    r.raise_for_status()
    csvreader = csv.reader(StringIO.StringIO(raw))
    builder=[]
    for i,r in enumerate(csvreader):
        if i in skip:
            continue
        if len(r) <= link:
            continue
        if i%100 == 3: print i,r
        #data={'link':r[link].strip(), 'title':t, 'html':page_u, 'status':page_stat, 'meta':{}, 'type':index}
        data={'sheetname':index, 'i': i, 'url':r[link].strip()}
        builder.append(data)
    print builder[:4]
    scraperwiki.sqlite.save(table_name='xllinks',data=builder, unique_keys=['url'],verbose=0)
    return builder

def LoadCSVlinks():
    for i in csvorigin:
        getcsv(csvorigin[i],i)

# julians xls loader
def LoadXLlinks():
    book = xlrd.open_workbook(file_contents=requests.get(xlurl,verify=False).content)
    for i in [0,2,4,6,8,10,12]:
        sheet = book.sheet_by_index(i)
        print sheet.name, "rows:", sheet.nrows
        ldata = [ ] 
        for i in range(sheet.nrows): 
            sheetvalue = sheet.cell(i, 0).value.strip()
            if sheetvalue:
                ldata.append({"sheetname":sheet.name, "i":i, "url":sheetvalue})
        scraperwiki.sqlite.save(["sheetname", "i"], ldata, "xllinks")

# julians raw scraper
def ScrapeRaw():
    scraperwiki.sqlite.execute("create table if not exists htmlcache (url text)")
    urlbatch = scraperwiki.sqlite.execute("select xllinks.url from xllinks left join htmlcache on htmlcache.url = xllinks.url where htmlcache.url is null limit 30")
    urlbatch = [u[0]  for u in urlbatch["data"]]
    if not urlbatch:
        return False
    ldata = [ ]
    print urlbatch
    for url in urlbatch:
        if url == "Old URL" or url == 'public_url':
            continue
        page_req=requests.get(url)
        page_raw=page_req.content
        data = {'url':url, 'status':page_req.status_code}
        data['html']=unicode(page_raw, 'iso-8859-1')
        ldata.append(data)
    scraperwiki.sqlite.save(["url"], ldata, "htmlcache")
    return True

def parse_news(i,url,html, response_status):
    record = {}
    record['old_url'] = url
    record['i'] = i
    if response_status == 404: #don't bother with the 404's
        record['status'] = 404
        return record
    root = lxml.html.fromstring(html.encode('iso-8859-1'))
    record['summary'] = root.cssselect('meta[name="DC.description"]')[0].get('content') #summary from metatag
    contentdiv = root.cssselect("div#content")
    if not contentdiv:
        return False
    content = contentdiv[0]
    if not content:
        return False
    titles = list(content.cssselect("div.hgroup h1"))
    if titles:
        record['title'] = titles[0].text_content().strip() #stripped title
    meta = content.cssselect("table.meta")[0]
    try:
        record['associated_organisations'] = meta.xpath('//*[contains(text(), "Publisher:")]/following-sibling::*')[0].text_content() #associate organisations
    except:
        pass
    try:
        record['associated_policies'] = meta.xpath('//*[contains(text(), "Mode/topic:")]/following-sibling::*')[0].text_content() #associate policies
    except:
        pass
    try:
        record['first_published'] = meta.xpath('//*[contains(text(), "Published date:")]/following-sibling::*')[0].text_content().strip() # first published date
    except:
        pass
    try:
        record['type'] = meta.xpath('//*[contains(text(), "Type:")]/following-sibling::*')[0].text_content().strip() # type
    except:
        pass
    try:    
        record['date'] = dateutil.parser.parse(record["first_published"], dayfirst=True).date().isoformat() #iso date
    except:
        pass
    
    for node in content.cssselect("div.header"): #drop the header info - we are done with it and don't want it in the body text
        node.drop_tree()
    #record['body'] = html2text.HTML2Text().handle(data=lxml.html.tostring(content,encoding=unicode)) #bodytext
    
    #record['body'] = html2text.HTML2Text().handle(data=lxml.html.tostring(content,encoding="ascii")) #bodytext

    #encoding mess:
    record['body'] = html2text.HTML2Text().handle(data=lxml.html.tostring(content)) #bodytext
    record['body'] = record['body'].replace(u"\xa0", u" ") #non breaking spaces
    record['body'] = record['body'].encode('utf-8')
    #print lxml.html.tostring(content,encoding="ascii")
    #print repr(record['body'])
    
    return record

def News():
    #scraperwiki.sqlite.execute("drop table if exists news")
    scraperwiki.sqlite.execute("create table if not exists news (old_url text, i integer)")
    hurlbatch = scraperwiki.sqlite.execute("select xllinks.i, xllinks.url, html, htmlcache.status from xllinks left join htmlcache on htmlcache.url=xllinks.url left join news on news.i=xllinks.i where xllinks.sheetname='news' and news.old_url is null and htmlcache.url is not null limit 20")
    ldata = [ ]
    print "fetched batch", len(hurlbatch["data"])
    for i, url, html, response_status in hurlbatch["data"]:        
        data = parse_news(i, url, html, response_status)
        if data:
            ldata.append(data)
        else:
            print "Failed to parse", url, html
    scraperwiki.sqlite.save(["i"], ldata, "news")
    return len(ldata)

def parse_speeches(i,url,html, response_status):
    record = {}
    record['old_url'] = url
    record['i'] = i
    if response_status == 404: #don't bother with the 404's
        record['status'] = 404
        return record
    root = lxml.html.fromstring(html.encode('iso-8859-1'))
    record['summary'] = root.cssselect('meta[name="DC.description"]')[0].get('content') #summary from metatag
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
        record['associated_organisations'] = meta.xpath('//*[contains(text(), "Publisher:")]/following-sibling::*')[0].text_content() #associate organisations
    except:
        pass
    try:
        record['delivered_by'] = meta.xpath('//*[contains(text(), "Delivered by:")]/following-sibling::*')[0].text_content() #delivered by
    except:
        pass
    try:
        record['delivered_on_date'] = meta.xpath('//*[contains(text(), "Delivered date:")]/following-sibling::*')[0].text_content().strip() # delivered on date
    except:
        pass
    try:
        record['speech_type'] = meta.xpath('//*[contains(text(), "Type:")]/following-sibling::*')[0].text_content().strip() # speech type
    except:
        pass
    try:
        record['event'] = meta.xpath('//*[contains(text(), "Event:")]/following-sibling::*')[0].text_content().strip() # event
    except:
        pass
    try:
        record['location'] = meta.xpath('//*[contains(text(), "Location:")]/following-sibling::*')[0].text_content().strip() # location
    except:
        pass
    if 'event' in record and 'location' in record:
        record['event_and_location'] = record['event'] + ', ' + record['location'] # event + location 
    try:    
        record['date'] = dateutil.parser.parse(record["delivered_on_date"], dayfirst=True).date().isoformat() #iso date
    except:
        pass
    try:
        record['associated_policies'] = meta.xpath('//*[contains(text(), "Mode/topic:")]/following-sibling::*')[0].text_content() #associate policies
    except:
        pass    
    for node in content.cssselect("div.header"): #drop the header info - we are done with it and don't want it in the body text
        node.drop_tree()
    record['body'] = html2text.HTML2Text().handle(data=lxml.html.tostring(content)) #bodytext
    record['body'] = record['body'].replace(u"\xa0", u" ") #non breaking spaces
    record['body'] = record['body'].encode('utf-8')
    return record

def Speeches():
    #scraperwiki.sqlite.execute("drop table if exists speeches")
    scraperwiki.sqlite.execute("create table if not exists speeches (old_url text, i integer)")
    hurlbatch = scraperwiki.sqlite.execute("select xllinks.i, xllinks.url, html, htmlcache.status from xllinks left join htmlcache on htmlcache.url=xllinks.url left join speeches on speeches.i=xllinks.i where xllinks.sheetname='speeches' and speeches.old_url is null and htmlcache.url is not null limit 20")
    ldata = [ ]
    print "fetched batch", len(hurlbatch["data"])
    for i, url, html, response_status in hurlbatch["data"]:        
        data = parse_speeches(i, url, html, response_status)
        if data:
            ldata.append(data)
        else:
            print "Failed to parse", url, html
    scraperwiki.sqlite.save(["i"], ldata, "speeches")
    return len(ldata)

def parse_consultations(i,url,html, response_status):
    record = {}
    record['old_url'] = url
    record['i'] = i
    if response_status == 404: #don't bother with the 404's
        record['status'] = 404
        return record
    root = lxml.html.fromstring(html)
    record['summary'] = root.cssselect('meta[name="DC.description"]')[0].get('content') #summary from metatag
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
        record['type'] = meta.xpath('//*[contains(text(), "Type:")]/following-sibling::*')[0].text_content() #type
    except:
        pass
    try:
        record['opening_date'] = meta.xpath('//*[contains(text(), "Published date:")]/following-sibling::*')[0].text_content().strip() # opening date
    except:
        pass
    try:
        record['closing_date'] = meta.xpath('//*[contains(text(), "Closing date:")]/following-sibling::*')[0].text_content().strip() # closing date
    except:
        pass
    try:    
        record['opening_date_iso'] = dateutil.parser.parse(record["opening_date"], dayfirst=True).date().isoformat() #iso date
    except:
        pass
    try:    
        record['closing_date_iso'] = dateutil.parser.parse(record["closing_date"], dayfirst=True).date().isoformat() #iso date
    except:
        pass
    for node in content.cssselect("div.header"): #drop the header info - we are done with it and don't want it in the body text
        node.drop_tree()
    record['body'] = html2text.HTML2Text().handle(data=lxml.html.tostring(content)) #bodytext
    #response = content.xpath('//h2[text()="Consultation responses"]//following-sibling::ul')
    responses = content.xpath('//h2[text()="Consultation responses"]//following-sibling::ul[following::h2[text()="Consultation documents"]]')    
    try:
        n = 1
        for r in responses:
            record['response_'+str(n)+'_title'] = r[0][0].text
            record['response_'+str(n)]= r[0][0].attrib['href']
            n = n+1
    except:
        pass
    respond = content.xpath('//h2[@id="respond-to-the-consultation"]//following-sibling::p[following::h2[@id="related"]]')
    #respond = content.xpath('//h2[@id="respond-to-the-consultation"]')
    record['how_to_respond'] = "\n".join(html2text.HTML2Text().handle(data=lxml.html.tostring(p))  for p in respond)
    #respondtext=
    #for r in respond:
    #    print r.text_content()
    links = root.xpath('//div[@property="dc:abstract"]//li/a/.')
    n = 1
    for link in links:
      
       try:
           if 'assets.dft.gov.uk' in link.attrib['href'] or 'webarchive.nationalarchives.gov.uk' in link.attrib['href']:
               record['attachment_'+str(n)] = link.attrib['href']
               record['attachment_'+str(n)+'_title'] = link.text_content()
               n = n+1
       except:
           pass
    #print record
    return record

def Consultations():
    #scraperwiki.sqlite.execute("drop table if exists consultations")
    scraperwiki.sqlite.execute("create table if not exists consultations (old_url text, i integer)")
    hurlbatch = scraperwiki.sqlite.execute("select xllinks.i, xllinks.url, html, htmlcache.status from xllinks left join htmlcache on htmlcache.url=xllinks.url left join consultations on consultations.i=xllinks.i where xllinks.sheetname='consult' and consultations.old_url is null and htmlcache.url is not null limit 20")
    ldata = [ ]
    print "fetched batch", len(hurlbatch["data"])
    for i, url, html, response_status in hurlbatch["data"]:        
        data = parse_consultations(i, url, html.encode('latin-1'), response_status)
        if data:
            ldata.append(data)
            print data
        else:
            print "Failed to parse", url, html
    scraperwiki.sqlite.save(["i"], ldata, "consultations")
    return len(ldata)

def parse_publications(i,url,html, response_status):
    record = {}
    record['old_url'] = url
    print url
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
    
    links = content.xpath('//li/a/.')
    
    n = 1
    jsonattach=[]
    for link in links:
        #print link.attrib['href']
        try:
            if 'assets.dft.gov.uk' in link.attrib['href'] or 'webarchive.nationalarchives.gov.uk' in link.attrib['href']:
                #record['attachment_'+str(n)] = link.attrib['href']
                #record['attachment_'+str(n)+'_title'] = link.text_content()
                jsonattach.append({'link':link.attrib['href'], 'title':link.text_content()})
                n = n+1
            record['jsonattach']=json.dumps(jsonattach)
        except:
            pass

    record['body'] = html2text.HTML2Text().handle(data=lxml.html.tostring(content)) #bodytext
    record['body'] = record['body'].replace(u"\xa0", u" ") #non breaking spaces
    record['body'] = record['body'].encode('utf-8')

    
    return record

def Publications():
    #scraperwiki.sqlite.execute("drop table if exists publications")
    scraperwiki.sqlite.execute("create table if not exists publications (old_url text, i integer)")
    hurlbatch = scraperwiki.sqlite.execute("select xllinks.i, xllinks.url, html, htmlcache.status from xllinks left join htmlcache on htmlcache.url=xllinks.url left join publications on publications.i=xllinks.i where xllinks.sheetname='pubs' and publications.old_url is null and htmlcache.url is not null limit 20") 

    ldata = [ ]
    print "fetched batch", len(hurlbatch["data"])
    for i, url, html, response_status in hurlbatch["data"]:        
        data = parse_publications(i, url, html, response_status)
        if data:
            ldata.append(data)
        else:
            print "Failed to parse", url, html
    print repr(ldata)
    scraperwiki.sqlite.save(["i"], ldata, "publications")
    return len(ldata)

def parse_fois(i,url,html, response_status):
    record = {}
    record['old_url'] = url
    record['i'] = i
    if response_status == 404: #don't bother with the 404's
        record['status'] = 404
        return record
    root = lxml.html.fromstring(html.encode('iso-8859-1'))
    record['summary'] = root.cssselect('meta[name="DC.description"]')[0].get('content') #summary from metatag
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
    try:
        record['URN'] = meta.xpath('//*[contains(text(), "FOI Reference:")]/following-sibling::*')[0].text_content() #delivered by
    except:
        pass 

    for node in content.cssselect("div.header"): #drop the header info - we are done with it and don't want it in the body text
        node.drop_tree()
    
    links = content.cssselect('a')
    if len(links) > 50: #put the page(s) with large number of attachments into a json field
        n = 1
        attachment_json = {}
        for link in links:
            try:
                if 'href' in link.attrib and ('assets.dft.gov.uk' in link.attrib['href'] or 'webarchive.nationalarchives.gov.uk' in link.attrib['href']):
                    attachment_json['attachment_'+str(n)] = link.attrib['href']
                    attachment_json['attachment_'+str(n)+'_title'] = link.text_content()
                    n = n+1
            except:
                pass
        record['manual'] = 1
        record['attachment_json'] = json.dumps(attachment_json)
    else: #process the attachments
        n = 1
        for link in links:
            try:
                if 'href' in link.attrib and ('assets.dft.gov.uk' in link.attrib['href'] or 'webarchive.nationalarchives.gov.uk' in link.attrib['href']):
                    record['attachment_'+str(n)] = link.attrib['href']
                    record['attachment_'+str(n)+'_title'] = link.text_content()
                    n = n+1
            except:
                pass

    record['body'] = html2text.HTML2Text().handle(data=lxml.html.tostring(content)) #bodytext
    record['body'] = record['body'].replace(u"\xa0", u" ") #non breaking spaces
    record['body'] = record['body'].encode('utf-8')
    vcard = root.cssselect("div.vcard")
    vcard = vcard[0]
    record['contact_info'] = html2text.HTML2Text().handle(data=lxml.html.tostring(vcard))
    return record

def FOIs():
    #scraperwiki.sqlite.execute("drop table if exists fois")
    scraperwiki.sqlite.execute("create table if not exists fois (old_url text, i integer)")
    hurlbatch = scraperwiki.sqlite.execute("select xllinks.i, xllinks.url, html, htmlcache.status from xllinks left join htmlcache on htmlcache.url=xllinks.url left join fois on fois.i=xllinks.i where xllinks.sheetname='foi' and fois.old_url is null and htmlcache.url is not null limit 20")
    ldata = [ ]
    print "fetched batch", len(hurlbatch["data"])
    for i, url, html, response_status in hurlbatch["data"]:        
        data = parse_fois(i, url, html, response_status)
        if data:
            ldata.append(data)
        else:
            print "Failed to parse", url, html
    scraperwiki.sqlite.save(["i"], ldata, "fois")
    return len(ldata)

def parse_srs(i,url,html, response_status):
    record = {}
    record['old_url'] = url
    record['i'] = i
    if response_status == 404: #don't bother with the 404's
        record['status'] = 404
        return record
    root = lxml.html.fromstring(html.encode('iso-8859-1'))
    record['summary'] = root.cssselect('meta[name="DC.description"]')[0].get('content') #summary from metatag
    record['type'] = 'release'
    type_img = root.xpath('//img[@alt="National Statistics logo"]')
    if type_img:
        record['type'] = 'National Stats'
    chart = root.xpath('//div[@id="line_chart"]')
    if chart:
        record['chart'] = 'yes'
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
        record['associated_policies'] = meta.xpath('//*[contains(text(), "Statistics topic:")]/following-sibling::*')[0].text_content() #associated policies
    except:
        pass
    try:
        record['associated_organisations'] = meta.xpath('//*[contains(text(), "Publisher:")]/following-sibling::*')[0].text_content() #associate organisations
    except:
        pass
    try:
        record['publication_date'] = meta.xpath('//*[contains(text(), "Published date:")]/following-sibling::*')[0].text_content().replace(u'\xa0', u'')
    except:
        pass
    try:    
        record['publication_date_iso'] = dateutil.parser.parse(record["publication_date"], dayfirst=True).date().isoformat() #iso date
    except:
        pass
    try:
        record['publication_series'] = meta.xpath('//*[contains(text(), "Series:")]/following-sibling::*')[0].text_content() #delivered by
    except:
        pass 
    print record
    for node in content.cssselect("div.header"): #drop the header info - we are done with it and don't want it in the body text
        node.drop_tree()
    
    links = content.cssselect('a')
    if len(links) > 50: #put the page(s) with large number of attachments into a json field
        n = 1
        attachment_json = {}
        for link in links:
            try:
                if 'assets.dft.gov.uk' in link.attrib['href'] or 'webarchive.nationalarchives.gov.uk' in link.attrib['href']:
                    attachment_json['attachment_'+str(n)] = link.attrib['href']
                    attachment_json['attachment_'+str(n)+'_title'] = link.text_content()
                    n = n+1
            except:
                pass
        record['manual'] = 1
        record['attachment_json'] = json.dumps(attachment_json)
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

    record['body'] = html2text.HTML2Text().handle(data=lxml.html.tostring(content)) #bodytext
    record['body'] = record['body'].replace(u"\xa0", u" ") #non breaking spaces
    record['body'] = record['body'].encode('utf-8')
    print record['body']
    return record

def SRs():
    #scraperwiki.sqlite.execute("drop table if exists srs")
    scraperwiki.sqlite.execute("create table if not exists srs(old_url text, i integer)")
    hurlbatch = scraperwiki.sqlite.execute("select xllinks.i, xllinks.url, html, htmlcache.status from xllinks left join htmlcache on htmlcache.url=xllinks.url left join srs on srs.i=xllinks.i where xllinks.sheetname='statsrel' and srs.old_url is null and htmlcache.url is not null limit 20")
    ldata = [ ]
    print "fetched batch", len(hurlbatch["data"])
    for i, url, html, response_status in hurlbatch["data"]:        
        data = parse_srs(i, url, html, response_status)
        if data:
            ldata.append(data)
        else:
            print "Failed to parse", url, html
    scraperwiki.sqlite.save(["i"], ldata, "srs")
    return len(ldata)

def parse_sts(i,url,html, response_status):
    record = {}
    record['old_url'] = url
    record['i'] = i
    if response_status == 404: #don't bother with the 404's
        record['status'] = 404
        return record
    root = lxml.html.fromstring(html.encode('iso-8859-1'))
    record['summary'] = root.cssselect('meta[name="DC.description"]')[0].get('content') #summary from metatag
    
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
        record['geo_scope'] = meta.xpath('//*[contains(text(), "Geographical scope:")]/following-sibling::*')[0].text_content() 
    except:
        pass
    try:
        record['geo_breakdown'] = meta.xpath('//*[contains(text(), "Geographical breakdown:")]/following-sibling::*')[0].text_content() 
    except:
        pass
    try:
        record['urn'] = meta.xpath('//*[contains(text(), "Reference:")]/following-sibling::*')[0].text_content().replace(u'\xa0', u'') #delivered by
    except:
        pass
    try:
        record['associated_policies'] = meta.xpath('//*[contains(text(), "Statistics topic:")]/following-sibling::*')[0].text_content() #associated policies
    except:
        pass
    try:
        record['associated_organisations'] = meta.xpath('//*[contains(text(), "Publisher:")]/following-sibling::*')[0].text_content() #associate organisations
    except:
        pass
    try:
        record['publication_date'] = meta.xpath('//*[contains(text(), "Published date:")]/following-sibling::*')[0].text_content().replace(u'\xa0', u'')
    except:
        pass
    try:    
        record['publication_date_iso'] = dateutil.parser.parse(record["publication_date"], dayfirst=True).date().isoformat() #iso date
    except:
        pass
    try:
        record['publication_series'] = meta.xpath('//*[contains(text(), "Series:")]/following-sibling::*')[0].text_content() #delivered by
    except:
        pass
    try:
        record['type'] = meta.xpath('//*[contains(text(), "Type:")]/following-sibling::*')[0].text_content() #delivered by
    except:
        pass
    for node in content.cssselect("div.header"): #drop the header info - we are done with it and don't want it in the body text
        node.drop_tree()
    for node in content.xpath('div[@id="secondary"]'): #drop the secondary 
        node.drop_tree()
    
    #links = content.xpath('//li/a/.')
    #linksul = content.xpath('//h2[text()="Download table"]//following-sibling::*')
    #for link in linksul:
    #    print link.tag
    links = root.xpath('//div[@id="content"]//li/a/.')
   
    n = 1
    for link in links:
      
       try:
           if 'assets.dft.gov.uk' in link.attrib['href'] or 'webarchive.nationalarchives.gov.uk' in link.attrib['href']:
               record['attachment_'+str(n)] = link.attrib['href']
               record['attachment_'+str(n)+'_title'] = link.text_content()
               n = n+1
       except:
           pass

    record['body'] = html2text.HTML2Text().handle(data=lxml.html.tostring(content)) #bodytext
    record['body'] = record['body'].replace(u"\xa0", u" ") #non breaking spaces
    record['body'] = record['body'].encode('utf-8')
    print record
    return record

def STs():
    #scraperwiki.sqlite.execute("drop table if exists sts")
    scraperwiki.sqlite.execute("create table if not exists sts(old_url text, i integer)")
    hurlbatch = scraperwiki.sqlite.execute("select xllinks.i, xllinks.url, html, htmlcache.status from xllinks left join htmlcache on htmlcache.url=xllinks.url left join sts on sts.i=xllinks.i where xllinks.sheetname='statstab' and sts.old_url is null and htmlcache.url is not null limit 20")
    ldata = [ ]
    print "fetched batch", len(hurlbatch["data"])
    for i, url, html, response_status in hurlbatch["data"]:        
        data = parse_sts(i, url, html, response_status)
        if data:
            ldata.append(data)
        else:
            print "Failed to parse", url, html
    scraperwiki.sqlite.save(["i"], ldata, "sts")
    return len(ldata)

def fixfoi():
    print scraperwiki.sqlite.execute("UPDATE xllinks SET sheetname = 'foi' WHERE sheetname = 'pubs' AND url LIKE 'http://www.dft.gov.uk/foi/%'")
    scraperwiki.sqlite.commit()

scraperwiki.sqlite.execute('drop table publications')
scraperwiki.sqlite.commit()
#exit()
#LoadCSVlinks()
#print "parse CSV done"
#while ScrapeRaw(): pass
#print "RAW done"
#while News():  pass
#while Speeches():  pass
#while Consultations():  pass
#fixfoi()
while Publications():  pass
#while FOIs():  pass
#while SRs():  pass
#while STs():  pass
