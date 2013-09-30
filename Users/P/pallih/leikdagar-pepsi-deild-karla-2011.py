# -*- coding: utf-8 -*


import scraperwiki,re
#from lxml import etree
import lxml.html
import time
import datetime

url = 'http://www.ksi.is/mot/motalisti/urslit-stada/?MotNumer=23425'

html = scraperwiki.scrape(url)

print html

root = lxml.html.fromstring(html)

content = root.xpath ('//table[@id="leikir-tafla"]//tr[@class="alt"]/. | //table[@id="leikir-tafla"]//tr[@class=""]/.')

print content

for m in content:
    #print m.text_content()
    record={}
    record['numer'] = m[0].text
    record['dagur'] = m[1].text
    record['klukkan'] = m[2].text
    record['leikur'] = m[3].text
    record['stadur'] = m[4].text
    record['urslit'] = m[5].text

    scraperwiki.sqlite.save(['numer'], data=record, table_name='leikdagar_pepsi_deild_karla_2011')

# -*- coding: utf-8 -*


import scraperwiki,re
#from lxml import etree
import lxml.html
import time
import datetime

url = 'http://www.ksi.is/mot/motalisti/urslit-stada/?MotNumer=23425'

html = scraperwiki.scrape(url)

print html

root = lxml.html.fromstring(html)

content = root.xpath ('//table[@id="leikir-tafla"]//tr[@class="alt"]/. | //table[@id="leikir-tafla"]//tr[@class=""]/.')

print content

for m in content:
    #print m.text_content()
    record={}
    record['numer'] = m[0].text
    record['dagur'] = m[1].text
    record['klukkan'] = m[2].text
    record['leikur'] = m[3].text
    record['stadur'] = m[4].text
    record['urslit'] = m[5].text

    scraperwiki.sqlite.save(['numer'], data=record, table_name='leikdagar_pepsi_deild_karla_2011')

