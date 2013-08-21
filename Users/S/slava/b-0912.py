# -*- coding: utf-8 -*-

import scraperwiki
import lxml, lxml.html
import pprint
import re
# Blank Python

#
urls = """http://www.minbank.ru/include/ajax_map.php?region=95
http://www.minbank.ru/include/ajax_map.php?region=175
http://www.minbank.ru/include/ajax_map.php?region=190
http://www.minbank.ru/include/ajax_map.php?region=178
http://www.minbank.ru/include/ajax_map.php?region=192
http://www.minbank.ru/include/ajax_map.php?region=187
http://www.minbank.ru/include/ajax_map.php?region=260
http://www.minbank.ru/include/ajax_map.php?region=184
http://www.minbank.ru/include/ajax_map.php?region=180
http://www.minbank.ru/include/ajax_map.php?region=177
http://www.minbank.ru/include/ajax_map.php?region=188
http://www.minbank.ru/include/ajax_map.php?region=194
http://www.minbank.ru/include/ajax_map.php?region=163
http://www.minbank.ru/include/ajax_map.php?region=193
http://www.minbank.ru/include/ajax_map.php?region=179
http://www.minbank.ru/include/ajax_map.php?region=196
http://www.minbank.ru/include/ajax_map.php?region=198
http://www.minbank.ru/include/ajax_map.php?region=307
http://www.minbank.ru/include/ajax_map.php?region=266
http://www.minbank.ru/include/ajax_map.php?region=195
http://www.minbank.ru/include/ajax_map.php?region=181
http://www.minbank.ru/include/ajax_map.php?region=174
http://www.minbank.ru/include/ajax_map.php?region=191
http://www.minbank.ru/include/ajax_map.php?region=173
http://www.minbank.ru/include/ajax_map.php?region=197
http://www.minbank.ru/include/ajax_map.php?region=187
http://www.minbank.ru/include/ajax_map.php?region=96
http://www.minbank.ru/include/ajax_map.php?region=382
http://www.minbank.ru/include/ajax_map.php?region=182"""


pm = re.compile("""point\s=\snew\sYMaps\.GeoPoint\(([\d\.]+?)\s*,\s*([\d\.]+?)\).+?\.innerHTML\s=\s"(.+?)";""", re.I | re.U | re.S)
branch_re = re.compile("""<p>(.+?)</p>.+?<b>Адрес</b>(.+?)<br><br/>""", re.I | re.U | re.S)

i=0
for url1 in urls.split("\n"):

    html = scraperwiki.scrape(url1)
    m = pm.findall(html)

    for d in m:
        #print d
        #d[2] = d[2].decode('windows-1251').encode('utf-8')
        branch = branch_re.findall(d[2])

        i+=1
        #.decode('windows-1251').encode('utf-8')
        
        if len(branch)>0:
            address = branch[0][1]
            branch_name = branch[0][0]
        else:
            address = ''
            branch_name = ''

        data = {'id':i, 'lat':d[1],'lon':d[0], 'branch_data':d[2], 'branch_name':branch_name , 'address':address }
        #print data
        scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name="swdata_process")
