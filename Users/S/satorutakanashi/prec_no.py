# -*- coding: utf-8 -*-
import scraperwiki
import lxml.html
import re

url='http://www.data.jma.go.jp/obd/stats/etrn/select/prefecture00.php'

html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)

for el in root.cssselect("map[name='point'] area"):
    m = re.search(r'prec_no=(\d{2})', el.attrib['href'])
    data = {'prec_no':int(m.group(1)),'name':el.attrib['alt']}
    scraperwiki.sqlite.save(unique_keys=['prec_no'], data=data)
# -*- coding: utf-8 -*-
import scraperwiki
import lxml.html
import re

url='http://www.data.jma.go.jp/obd/stats/etrn/select/prefecture00.php'

html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)

for el in root.cssselect("map[name='point'] area"):
    m = re.search(r'prec_no=(\d{2})', el.attrib['href'])
    data = {'prec_no':int(m.group(1)),'name':el.attrib['alt']}
    scraperwiki.sqlite.save(unique_keys=['prec_no'], data=data)
