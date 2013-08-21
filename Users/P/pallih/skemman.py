# -*- coding: utf-8 -*-
import scraperwiki
import requests
import lxml.html
import re
from datetime import date, timedelta


author_regex = re.compile("(.+) (\d.+)")
locked_until_regex = re.compile("(\d+\.\d+\.\d+)",re.UNICODE)
#scraperwiki.sqlite.save_var('last_page',1) 
#exit()

today_string = date.today().strftime("%Y%m%d")
daysago = date.today() - timedelta(3)

daysago_string = daysago.strftime("%Y%m%d")



def process(trs):
    batch = []
    for tr in trs[1:]:
        record = {}
        record['date'] = tr[0].text.strip()
        record['title'] = tr[1].text_content().strip()
        record['url'] = ('http://skemman.is' + tr[1][0].attrib['href']).split(';')[0].strip()
        record['authors'] = tr[2].text.strip()
        batch.append( record ) 
    return batch 

def go(page):
    url = 'http://skemman.is/browse/dates.itemtable.itemgrid.pager/'+str(page)+'?t:ac='+daysago_string+'_'+today_string #20120930'
    r = requests.get(url)
    html =  r.text
    root = lxml.html.fromstring(html)
    trs = root.xpath('//table[@class="t-data-grid"]//tr')
    items = process(trs)
    if items:
        print 'New urls:', items
        scraperwiki.sqlite.save(unique_keys=["url"], data=items, table_name='publications')
        next_page = page +1
        scraperwiki.sqlite.save_var('last_page', next_page) 
        pagination = root.xpath('//span[@class="current"]/following-sibling::*')
        if pagination:
            go(next_page)
        else:
            print 'no next'

#page = scraperwiki.sqlite.get_var('last_page')
#try:
#    scraperwiki.sqlite.execute("""
#        create table publications
#        ( 
#        id INTEGER PRIMARY KEY AUTOINCREMENT
#        )
#    """)
#except:
#    print "Table probably already exists."
#go(page)

#scraperwiki.sqlite.execute("create table publications_details(url text)")

def process_details(html,url):
    record = {}
    record['url'] = url
    root = lxml.html.fromstring(html)
    content = root.xpath('//div[@id="l_content"]')
    record['type'] = content[0].xpath('//h1')[0].text
    record['institution'] = content[0].xpath('//a[@class="trailInstitution"]')[0].text.strip()
    try:
        record['department'] = content[0].xpath('//a[@class="trailDepartment"]')[0].text.strip()
    except:
        pass
    record['collection'] = content[0].xpath('//a[@class="trailCollection"]')[0].text.strip()
    record['handle'] = content[0].xpath('//p[@class="citation"]/a')[0].attrib['href']
    try:
        record['title'] = content[0].xpath('//p[@class="attrLang_is"]')[0].text.strip()
    except:
        try:
            record['title'] = content[0].xpath('//p[@class="attrLang_en"]')[0].text.strip()
        except:
            record['title'] = ''

    #record['title'] =  content[0].xpath(u'//span[@class="attrLabel"][text()[contains(.,"Titill")]]/following-sibling::*')[0].text_content().strip()

    authors = content[0].xpath('//div[@class="attrContent authorAttrContent"]/ul/li/.')
    author_count = 1
    for author in authors:
        r = author_regex.search(author.text_content().strip())
        try:
            record['author_'+str(author_count)] = r.group(1)
            record['author_'+str(author_count)+'_birthyear'] = r.group(2)
            record['author_'+str(author_count)+'_link'] = 'http://skemman.is' + author[0].attrib['href']
            author_count = author_count+1
        except:
            record['author_'+str(author_count)] = author.text_content().strip()
    advisors = content[0].xpath('//div[@class="attrContent advisorAttrContent"]/ul/li/.')
    advisor_count = 1
    for advisor in advisors:
        r = author_regex.search(advisor.text_content().strip())
        try:
            record['advisor_'+str(advisor_count)] = r.group(1)
            record['advisor_'+str(advisor_count)+'_birthyear'] = r.group(2)
            record['advisor_'+str(advisor_count)+'_link'] = 'http://skemman.is' + advisor[0].attrib['href']
            advisor_count = advisor_count+1
        except:
            pass
    keywords = content[0].xpath('//div[@class="attrContent keywordAttrContent"]/ul/li/.')
    keywords_count = 1
    for keyword in keywords:
        record['keyword_'+str(keywords_count)] = keyword.text_content()
        record['keyword_'+str(keywords_count)+'_link'] = 'http://skemman.is' + keyword[0].attrib['href']
        keywords_count = keywords_count+1
    #record['published_date'] = content[0].xpath('//span[@class="attrLabel" AND contains(text(),"Útgáfa"]/following-sibling::*')[0].text_content().strip()
    try:
        record['published_date'] =  content[0].xpath(u'//span[@class="attrLabel"][text()[contains(.,"Útgáfa")]]/following-sibling::*')[0].text_content().strip()
    except:
        pass
    record['published_date_detailed'] =  content[0].xpath(u'//span[@class="attrLabel"][text()[contains(.,"Birting")]]/following-sibling::*')[0].text_content().strip()
    fileslist = content[0].xpath('//div[@class="dataTable"]//table/tbody/tr')
    filecount = 1
    for x in fileslist:
        record['file_'+str(filecount)+'_name'] =  x.xpath('td[@class="name"]')[0].text_content().strip()
        record['file_'+str(filecount)+'_size'] =  x.xpath('td[@class="size"]')[0].text_content().strip()
        record['file_'+str(filecount)+'_visibility'] =  x.xpath('td[@class="visibility"]')[0].text_content().strip()
        if u'Læst til' in x.xpath('td[@class="visibility"]')[0].text_content().strip():
            r = locked_until_regex.search(record['file_'+str(filecount)+'_visibility'])
            record['file_'+str(filecount)+'_locked_until'] = r.group(1)
        record['file_description_'+str(filecount)] =  x.xpath('td[@class="description"]')[0].text_content().strip()
        record['file_format_'+str(filecount)] =  x.xpath('td[@class="format"]')[0].text_content().strip()
        try:
            record['file_url_'+str(filecount)] =  'http://skemman.is' + x.xpath('td[@class="view"]')[0][0].attrib['href']
        except:
            pass   
    return record

def go_details():
    urlbatch = scraperwiki.sqlite.execute("select publications.url from publications left join publications_details on publications_details.url = publications.url where publications_details.url is null limit 50")
    urlbatch = [u[0]  for u in urlbatch["data"]]
    if not urlbatch:
        return False
    ldata = [ ]
    for url in urlbatch:
        page_req=requests.get(url)
        page_raw=page_req.content
        data = process_details(page_raw,url)
        ldata.append(data)
    print 'New details: ', ldata
    scraperwiki.sqlite.save(["url"], ldata, "publications_details")
    return True

#go_details()

scraperwiki.sqlite.save_var('last_page',1) 
page = 1
go(page)

while go_details():  pass