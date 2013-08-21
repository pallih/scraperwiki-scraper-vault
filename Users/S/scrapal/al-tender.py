# -*- coding: utf-8 -*-
import scraperwiki
import urllib2
import requests
import json
import lxml.html
import time
import re

#Runtime info setup:
scraperwiki.sqlite.execute("drop table if exists runtime_info")
scraperwiki.sqlite.execute("create table runtime_info (lastnumber VARCHAR(10), name VARCHAR(500), trade_name VARCHAR(500), number VARCHAR(500), type VARCHAR(500), date_time DATETIME, oid VARCHAR(500))")
record = {}
record ['lastnumber'] = '1'
scraperwiki.sqlite.save(['lastnumber'], data=record, table_name='runtime_info')
#exit()

#Runtime info setup:
#scraperwiki.sqlite.execute("drop table if exists runtime_info")
#record = {}
#record ['lastnumber'] = '1'
#scraperwiki.sqlite.save(['lastnumber'], data=record, table_name='runtime_info')
#exit()

def process(content):
    xpath = '//tbody/tr/.'
    root = lxml.html.fromstring(content)
    for tr in root.xpath(xpath):
        record = {}
        record['name'] =  tr[0][0].text.strip()
        record['trade_name'] =  tr[1][0].text
        record['number'] = tr[2][0].text
        record['type'] = tr[3][0].text
        record['date_time'] = time.strftime("%a %b %e %T %z %Y", time.gmtime())
        record['oid'] = tr.get("oid")
        print record
        scraperwiki.sqlite.save(['number'], data=record, table_name='alb-tender', verbose=2)

def postvalue(pagenumber):
    postvalue1 = "<grid><sourceType>Lookup</sourceType><tableName>AX_EP_call_for_tenders</tableName><viewName>default</viewName><sortColumns>Number&#x3A;0</sortColumns><groupColumns/><grouping>false</grouping><allowover>false</allowover><pageNum>"
    postvalue2 = "</pageNum><recsPerPage>15</recsPerPage><enableMultiSort>true</enableMultiSort><searchSelector>false</searchSelector><parameters><autorefresh>1</autorefresh><bodyheight>285px</bodyheight><externalFilter/><filterValue>&#x25;sistem</filterValue><filterColumn>Name</filterColumn></parameters></grid>"
    postvalue = postvalue1+str(pagenumber)+postvalue2
    post = dict(gridXmlString=postvalue)
    return post



def get(post,pagenumber):
    headers = {'content-type': 'application/json; charset=utf-8','User-agent':'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1)'}

    r = requests.post(url, data=json.dumps(post),headers=headers,allow_redirects=True, verify=False)
    content = r.content
    #print content
    #exit()
    #print content
    #content = (content.encode('utf-8')).decode('unicode_escape').strip('"')
    #content = (content.decode('unicode_escape')).replace('\\/', '/').strip('"')
    #content = (content.encode('utf-8')).decode('string_escape').replace('\\/', '/').strip('"')
    #content = content.encode('utf-8').replace('\\/', '/').strip('"')
    #print content
    #exit()
    update_statement= 'update runtime_info SET lastnumber='+ '"' +str(pagenumber)+ '"'    
    scraperwiki.sqlite.execute(update_statement)
    scraperwiki.sqlite.commit()
    return content
    
selection_statement = '* from runtime_info'
search_string = scraperwiki.sqlite.select(selection_statement)
pagenumber = search_string[0]
pagenumber = str(pagenumber['lastnumber'])

found = re.compile('found=\"(\d+)\"')
url = 'https://www.app.gov.al/ep/ASP.Net/Resources/FM/RecordsService/GridXDataHandler.asmx/Refresh'
#post = {"gridXmlString":"<grid><sourceType>Lookup</sourceType><tableName>AX_EP_call_for_tenders</tableName><viewName>default</viewName><sortColumns>Number&#x3A;0</sortColumns><groupColumns/><grouping>false</grouping><allowover>false</allowover><pageNum>1</pageNum><recsPerPage>15</recsPerPage><enableMultiSort>true</enableMultiSort><searchSelector>false</searchSelector><parameters><autorefresh>1</autorefresh><bodyheight>285px</bodyheight><externalFilter/><filterValue>&#x25;sistem</filterValue><filterColumn>Name</filterColumn></parameters></grid>"}

post = postvalue(pagenumber)
print post

content = get(post,pagenumber)
print content

found_numbers = found.findall(content)
pages= (int(found_numbers[0]) / 400)+2
print 'There are ', found_numbers[0], ' tendersin ', pages, ' pages'
print 'Starting from page: ', pagenumber
todo = range(int(pagenumber),int(pages))


#do all pages
for pagenumber in todo:
    post = postvalue(pagenumber)
    content = get(post,pagenumber) 
    process(content)
    print 'Done with page ', pagenumber

#reset the last pagenumber done
record = {}
record ['lastnumber'] = '1'
scraperwiki.sqlite.execute("drop table if exists runtime_info")
scraperwiki.sqlite.save(['lastnumber'], data=record, table_name='runtime_info')


