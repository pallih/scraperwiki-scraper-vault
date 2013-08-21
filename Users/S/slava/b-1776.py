# -*- coding: utf-8 -*-

import scraperwiki
import lxml, lxml.html
import pprint
import re
import json
import simplejson
import demjson
# Blank Python
#
urls = """http://arh.pkb.ru/branch/arkhangelsk/office
http://arh.pkb.ru/branch/volgograd/office
http://arh.pkb.ru/branch/kaliningrad/office
http://arh.pkb.ru/branch/kogalim/office
http://arh.pkb.ru/branch/krasnodar/office
http://arh.pkb.ru/branch/lipetsk/office
http://arh.pkb.ru/branch/moscow/office
http://arh.pkb.ru/branch/nizhny_novgorod/office
http://arh.pkb.ru/branch/novorossiysk/office
http://arh.pkb.ru/branch/novosibirsk/office
http://arh.pkb.ru/branch/perm/office
http://arh.pkb.ru/branch/rostov_on_don/office
http://arh.pkb.ru/branch/sankt_peterburg/office
http://arh.pkb.ru/branch/saratov/office
http://arh.pkb.ru/branch/ufa/office
http://arh.pkb.ru/branch/ukhta/office
http://arh.pkb.ru/branch/chelyabinsk/office"""

#print html 
i=1
for url in urls.split("\n"):
    html = scraperwiki.scrape(url)
    html = html.decode('windows-1251').encode('utf-8')
    addr = re.findall(r'<td>.*?<p>(.+?)<\/p>.*?<a.*?href="(.+?)".*?<td.*?<p>(.+?)<\/p>', html, re.I|re.U|re.S)
    for a in addr:
        data = {'id':i, 'branch_name': a[0], 'url': a[1], 'address': re.sub(r'\n|\r|\t','',a[2],0,re.I|re.U|re.S)}
        scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name="swdata_process")
        i+=1
