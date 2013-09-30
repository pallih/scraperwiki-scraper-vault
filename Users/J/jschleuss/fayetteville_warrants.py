import scraperwiki

# Blank Python

import scraperwiki
html = scraperwiki.scrape("http://warrants.accessfayetteville.org/index.cfm?start=&#results")
print html

import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("table tr"):
    tds = tr.cssselect("td")
    if len(tds)==5 :
        data = {
            'name_first' : tds[0].text_content().split(" ,")[-1],
            'name_last' : tds[0].text_content().split(" , ")[0],
            'charge' : tds[1].text_content(),
            'dob' : tds[2].text_content(),
            'warrant' : tds[3].text_content(),
            'warrant_date' : tds[4].text_content(),
        }
        print data

        scraperwiki.sqlite.save(unique_keys=['name_first'], data=data)
import scraperwiki

# Blank Python

import scraperwiki
html = scraperwiki.scrape("http://warrants.accessfayetteville.org/index.cfm?start=&#results")
print html

import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("table tr"):
    tds = tr.cssselect("td")
    if len(tds)==5 :
        data = {
            'name_first' : tds[0].text_content().split(" ,")[-1],
            'name_last' : tds[0].text_content().split(" , ")[0],
            'charge' : tds[1].text_content(),
            'dob' : tds[2].text_content(),
            'warrant' : tds[3].text_content(),
            'warrant_date' : tds[4].text_content(),
        }
        print data

        scraperwiki.sqlite.save(unique_keys=['name_first'], data=data)
