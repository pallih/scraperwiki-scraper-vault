import scraperwiki

# Blank Python

import scraperwiki
html = scraperwiki.scrape("http://services.co.benton.ar.us/dcn/inmateGrid.aspx?n=")
print html

import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("table tr"):
    tds = tr.cssselect("td")
    if len(tds)==8 :
        data = {
            'name_first' : tds[1].text_content(),
            'name_middle' : tds[2].text_content(),
            'name_last' : tds[3].text_content(),
            'age' : tds[4].text_content(),
            'race' : tds[5].text_content(),
            'sex' : tds[6].text_content(),
            'admit_date' : tds[7].text_content(),
        }
        print data

        scraperwiki.sqlite.save(unique_keys=['name_first'], data=data)
import scraperwiki

# Blank Python

import scraperwiki
html = scraperwiki.scrape("http://services.co.benton.ar.us/dcn/inmateGrid.aspx?n=")
print html

import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("table tr"):
    tds = tr.cssselect("td")
    if len(tds)==8 :
        data = {
            'name_first' : tds[1].text_content(),
            'name_middle' : tds[2].text_content(),
            'name_last' : tds[3].text_content(),
            'age' : tds[4].text_content(),
            'race' : tds[5].text_content(),
            'sex' : tds[6].text_content(),
            'admit_date' : tds[7].text_content(),
        }
        print data

        scraperwiki.sqlite.save(unique_keys=['name_first'], data=data)
