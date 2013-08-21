import scraperwiki
import lxml.html

# -*- coding: utf-8 -*-

i = 1
id = 1
counter = 1
url = ''
ip = ''
agency = ''
status = ''
date = ''

while i<10:
    html = scraperwiki.scrape("http://antizapret.info/?p=" + str(i))
    root = lxml.html.fromstring(html)
    counter = 1

    for el in root.cssselect("table tr td"):
        if counter > 4:
            if counter % 4 == 1:
                date = el.text
            elif counter % 4 == 2:
                for elem in el.cssselect("a"):
                    url = elem.text   
            elif counter % 4 == 3:
                ip = el.text.strip() 
            elif counter % 4 == 0:
                for elem in el.cssselect("a"):
                    agency = elem.text.strip()   
                if len(el.cssselect("b"))==0:
                    status = 1
                else:
                    status = 0 
                data = {
                'id' : id,
                'date' : date,
                'url' : url,
                'ip' : ip,
                'agency' : agency.encode('utf-8'),
                'status' : status
                }
                id += 1
                scraperwiki.sqlite.save(unique_keys=['id'], data=data)
        
        counter += 1
    i += 1
