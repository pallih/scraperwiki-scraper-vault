# -*- coding: utf-8 -*-

import scraperwiki
import lxml.html           
# Blank Python

link = "http://exmo.svobodainfo.org/exmo2010/monitoring/27/rating/"
html = scraperwiki.scrape(link)  
html.decode('utf-8')     
root = lxml.html.fromstring(html)
count = 1

for tr in root.cssselect("div#organization_list tr"):
    a1 = tr.cssselect("tr a")[0]
    a2 = tr.cssselect("tr a")[0]
    a3 = tr.cssselect("tr a")[1]
    if count == 54 : 
        a4 = tr.cssselect("tr td")[2]
    else :
        a4 = tr.cssselect("tr td")[3]
    data = {
        'link' : a1.attrib['href'],
        'offsite' : a3.attrib['href'],
        'rating': count,
        'rate' : a4.text,
        'name' : unicode(a2.text),
    }
    scraperwiki.sqlite.save(unique_keys=['offsite'], data=data)
    count = count + 1
    if count == 84 :
        break

print 'Готово'