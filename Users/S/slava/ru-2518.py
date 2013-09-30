import scraperwiki
import lxml.html
import simplejson
import re
# Blank Python

html = scraperwiki.scrape("http://www.kubankredit.ru/o_banke/dop_office/")
root = lxml.html.document_fromstring(html)
options = root.xpath("//div[@class='news-list']/ul[@class='dop']/li/ul/li/a")
scraperwiki.sqlite.execute('delete from `data`')

i=1
for option in options:
    #print option

    if option.attrib['href'] != '':
        try:
            html = scraperwiki.scrape("http://www.kubankredit.ru" + option.attrib['href'])
        except:
            continue
        root = lxml.html.document_fromstring(html)
        address = root.xpath("//div[@class='item'][1]/div[@class='description'][1]/p[@class='strong'][1]")
        #print address
        address = address[0].text_content()
        #print address
        #exit()
        
        scraperwiki.sqlite.save(unique_keys=['id'], data={'id':i, 'name':option.text_content(), 'address':address }, table_name='data')
        i+=1

import scraperwiki
import lxml.html
import simplejson
import re
# Blank Python

html = scraperwiki.scrape("http://www.kubankredit.ru/o_banke/dop_office/")
root = lxml.html.document_fromstring(html)
options = root.xpath("//div[@class='news-list']/ul[@class='dop']/li/ul/li/a")
scraperwiki.sqlite.execute('delete from `data`')

i=1
for option in options:
    #print option

    if option.attrib['href'] != '':
        try:
            html = scraperwiki.scrape("http://www.kubankredit.ru" + option.attrib['href'])
        except:
            continue
        root = lxml.html.document_fromstring(html)
        address = root.xpath("//div[@class='item'][1]/div[@class='description'][1]/p[@class='strong'][1]")
        #print address
        address = address[0].text_content()
        #print address
        #exit()
        
        scraperwiki.sqlite.save(unique_keys=['id'], data={'id':i, 'name':option.text_content(), 'address':address }, table_name='data')
        i+=1

