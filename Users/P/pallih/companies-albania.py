# -*- coding: utf-8 -*-
import scraperwiki
import urllib2
import requests
import json
import lxml.html
import time
import re

#Runtime info setup:
#scraperwiki.sqlite.execute("drop table if exists runtime_info")
#record = {}
#record ['lastnumber'] = '1'
#scraperwiki.sqlite.save(['lastnumber'], data=record, table_name='runtime_info')
#exit()

def process(content):
    xpath = '//tbody/tr/.'
    root = lxml.html.fromstring(content)
    data = []
    for tr in root.xpath(xpath):
        record = {}
        record['name'] =  tr[0][0].text.strip()
        record['trade_name'] =  tr[1][0].text
        record['number'] = tr[2][0].text
        record['type'] = tr[3][0].text
        record['date_time'] = time.strftime("%a %b %e %T %z %Y", time.gmtime())
        record['oid'] = tr.get("oid")
        data.append(record)
    scraperwiki.sqlite.save(['number'], data=data, table_name='albania-companies', verbose=2)

def postvalue(pagenumber):
    postvalue1 = "<grid><sourceType>Grid</sourceType><tableName>ALB_BR_View_SubjectListDEF</tableName> <viewName>Search</viewName><sortColumns>Subject_Name&#x3A;1</sortColumns><groupColumns/><pageNum>"
    postvalue2 = "</pageNum><recsPerPage>400</recsPerPage><cols/><max>-1</max><pagingCookie/><parameters><dblclickHandler>fmCustomEditorX&#x28;&#x27;ctl00_WebPartManagerPanel2_WebPartManager1_gwpGrid1_Grid1_dgx&#x27;&#x2C; &#x27;ALB_BR_View_SubjectListDEF&#x27;&#x2C; &#x27;&#x27;&#x2C; recordID&#x2C; &#x27;ASP.NET/Resources/FM/Dataviewer/Workflow/process.aspx&#x3F;workflow&#x3D;ALB_BR.User.ViewExtract&#x26;id&#x27;&#x2C; &#x27;&#x27;&#x29;&#x3B;</dblclickHandler><rowheight>18</rowheight><showjumpbar>1</showjumpbar></parameters></grid>"
    postvalue = postvalue1+str(pagenumber)+postvalue2
    post = dict(gridXmlString=postvalue)
    return post

def get(post,pagenumber):
    headers = {'content-type': 'application/json; charset=utf-8','User-agent':'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1)'}

    r = requests.post(url, data=json.dumps(post),headers=headers,allow_redirects=True)
    content = r.content
    #print content
    #content = (content.encode('utf-8')).decode('unicode_escape').strip('"')
    content = (content.decode('unicode_escape')).replace('\\/', '/').strip('"')
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
url = 'http://www.qkr.gov.al/nrc/ASP.Net/Resources/FM/RecordsService/GridXDataHandler.asmx/Refresh'
#post = {"gridXmlString":"<grid><sourceType>Grid</sourceType><tableName>ALB_BR_View_SubjectListDEF</tableName> <viewName>Search</viewName><sortColumns>Subject_Name&#x3A;1</sortColumns><groupColumns/><pageNum>1</pageNum><recsPerPage>100</recsPerPage><cols/><max>-1</max><pagingCookie/><parameters><dblclickHandler>fmCustomEditorX&#x28;&#x27;ctl00_WebPartManagerPanel2_WebPartManager1_gwpGrid1_Grid1_dgx&#x27;&#x2C; &#x27;ALB_BR_View_SubjectListDEF&#x27;&#x2C; &#x27;&#x27;&#x2C; recordID&#x2C; &#x27;ASP.NET/Resources/FM/Dataviewer/Workflow/process.aspx&#x3F;workflow&#x3D;ALB_BR.User.ViewExtract&#x26;id&#x27;&#x2C; &#x27;&#x27;&#x29;&#x3B;</dblclickHandler><rowheight>18</rowheight><showjumpbar>1</showjumpbar></parameters></grid>"}

post = postvalue(pagenumber)
content = get(post,pagenumber)
found_numbers = found.findall(content)
pages= (int(found_numbers[0]) / 400)+2
print 'There are ', found_numbers[0], ' companies in ', pages, ' pages'
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


