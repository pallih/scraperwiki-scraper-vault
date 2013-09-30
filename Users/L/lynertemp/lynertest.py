import scraperwiki           
html = scraperwiki.scrape('http://bpe.bursastation.com/prices.pl?type=15&view=1')
print html

import lxml.html           
root = lxml.html.fromstring(html)
for tr in root.cssselect("table.tblBursaSummMainHeader tr"):
    tds = tr.cssselect("td")
    if len(tds)==1:
        data = {
            'code' : tds[1].text_content()
        }
        print data

        scraperwiki.sqlite.save(unique_keys=['code'], data=data)




import scraperwiki           
html = scraperwiki.scrape('http://bpe.bursastation.com/prices.pl?type=15&view=1')
print html

import lxml.html           
root = lxml.html.fromstring(html)
for tr in root.cssselect("table.tblBursaSummMainHeader tr"):
    tds = tr.cssselect("td")
    if len(tds)==1:
        data = {
            'code' : tds[1].text_content()
        }
        print data

        scraperwiki.sqlite.save(unique_keys=['code'], data=data)




