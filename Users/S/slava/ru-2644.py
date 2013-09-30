import scraperwiki
import lxml.html
import simplejson
import re
# Blank Python

scraperwiki.sqlite.execute('delete from `data`')




html = scraperwiki.scrape("http://www.promtransbank.ru/branches")
root = lxml.html.document_fromstring(html)
links = root.xpath("//div[@class='b-branches-item']")
i=1
for l in links:
    bName=l.xpath("span[@class='b-branches-office']")[0].text_content()
    bAddress=l.xpath("address")[0].text_content()
    scraperwiki.sqlite.save(unique_keys=['id'], data={'id':i, 'name':bName, 'address': bAddress}, table_name="data")
    i+=1
    

import scraperwiki
import lxml.html
import simplejson
import re
# Blank Python

scraperwiki.sqlite.execute('delete from `data`')




html = scraperwiki.scrape("http://www.promtransbank.ru/branches")
root = lxml.html.document_fromstring(html)
links = root.xpath("//div[@class='b-branches-item']")
i=1
for l in links:
    bName=l.xpath("span[@class='b-branches-office']")[0].text_content()
    bAddress=l.xpath("address")[0].text_content()
    scraperwiki.sqlite.save(unique_keys=['id'], data={'id':i, 'name':bName, 'address': bAddress}, table_name="data")
    i+=1
    

