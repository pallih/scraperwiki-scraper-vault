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
html = scraperwiki.scrape("http://www.atb.su/vse_otdeleniya_aziatsko_tikhookeanskogo_banka.html")

i=1
branches = re.findall(r'class="fn org">.*?<strong>(.+?)</strong.*?adr displayInline">(.+?)</div', html, re.I|re.U|re.S)

for branch in branches:
    branch_name = branch[0] if len(branch)>0 else ''
    #print branch
    if len(branch)==2:
        postal_code = re.findall(r'class="postal-code">(.+?)</span', branch[1], re.I|re.U|re.S)
        country = re.findall(r'class="country-name">(.+?)</span', branch[1], re.I|re.U|re.S)
        region = re.findall(r'class="region">(.+?)</span', branch[1], re.I|re.U|re.S)
        locality = re.findall(r'class="locality">(.+?)</span', branch[1], re.I|re.U|re.S)
        street = re.findall(r'class="street-address">(.+?)</span', branch[1], re.I|re.U|re.S)
        
        data = {'id': i,\
                'branch_name' : branch_name, \
                'postal-code': postal_code[0] if len(postal_code)>0 else '', \
                'country': country[0] if len(country)>0 else '', \
                'region': region[0] if len(region)>0 else '', \
                'locality' : locality[0] if len(locality)>0 else '',\
                'street'  : street[0] if len(street) > 0 else ''}
        scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name="swdata_process")
        i+=1

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
html = scraperwiki.scrape("http://www.atb.su/vse_otdeleniya_aziatsko_tikhookeanskogo_banka.html")

i=1
branches = re.findall(r'class="fn org">.*?<strong>(.+?)</strong.*?adr displayInline">(.+?)</div', html, re.I|re.U|re.S)

for branch in branches:
    branch_name = branch[0] if len(branch)>0 else ''
    #print branch
    if len(branch)==2:
        postal_code = re.findall(r'class="postal-code">(.+?)</span', branch[1], re.I|re.U|re.S)
        country = re.findall(r'class="country-name">(.+?)</span', branch[1], re.I|re.U|re.S)
        region = re.findall(r'class="region">(.+?)</span', branch[1], re.I|re.U|re.S)
        locality = re.findall(r'class="locality">(.+?)</span', branch[1], re.I|re.U|re.S)
        street = re.findall(r'class="street-address">(.+?)</span', branch[1], re.I|re.U|re.S)
        
        data = {'id': i,\
                'branch_name' : branch_name, \
                'postal-code': postal_code[0] if len(postal_code)>0 else '', \
                'country': country[0] if len(country)>0 else '', \
                'region': region[0] if len(region)>0 else '', \
                'locality' : locality[0] if len(locality)>0 else '',\
                'street'  : street[0] if len(street) > 0 else ''}
        scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name="swdata_process")
        i+=1

