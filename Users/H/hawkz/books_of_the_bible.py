import scraperwiki

import scraperwiki           
html = scraperwiki.scrape("http://www.biblegateway.com/versions/New-King-James-Version-NKJV-Bible/")

import lxml.html
root = lxml.html.fromstring(html)

data = {}
a = 0

for tr in root.cssselect("table.infotable"):
    for td in tr:
        tds = td.cssselect("td")
        if tds:
            a +=1
            data = {'book_order': a, 'book_name': tds[0].text_content(), 'total_chapters': int(tds[1].text_content().strip().split('\n')[-1:][0]) }
            scraperwiki.sqlite.save(unique_keys=['book_name'], data=data)

print dataimport scraperwiki

import scraperwiki           
html = scraperwiki.scrape("http://www.biblegateway.com/versions/New-King-James-Version-NKJV-Bible/")

import lxml.html
root = lxml.html.fromstring(html)

data = {}
a = 0

for tr in root.cssselect("table.infotable"):
    for td in tr:
        tds = td.cssselect("td")
        if tds:
            a +=1
            data = {'book_order': a, 'book_name': tds[0].text_content(), 'total_chapters': int(tds[1].text_content().strip().split('\n')[-1:][0]) }
            scraperwiki.sqlite.save(unique_keys=['book_name'], data=data)

print data