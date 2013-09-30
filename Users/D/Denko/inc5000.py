import scraperwiki

# Blank Python

html = scraperwiki.scrape("http://www.inc.com/inc5000/list/2011/100//")

import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==8:
        data = {
            'rank' : tds[0].text_content(),
            'company name' : int(tds[1].text_content())
#            '3-year growth' : int(tds[2].text_content())
#            'revenue' : int(tds[3].text_content())
#            'industry' : int(tds[4].text_content())
#            'employees' : int(tds[5].text_content())
#           'city' : int(tds[6].text_content())
#            'state' : int(tds[7].text_content())        }
#        print data
import scraperwiki

# Blank Python

html = scraperwiki.scrape("http://www.inc.com/inc5000/list/2011/100//")

import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==8:
        data = {
            'rank' : tds[0].text_content(),
            'company name' : int(tds[1].text_content())
#            '3-year growth' : int(tds[2].text_content())
#            'revenue' : int(tds[3].text_content())
#            'industry' : int(tds[4].text_content())
#            'employees' : int(tds[5].text_content())
#           'city' : int(tds[6].text_content())
#            'state' : int(tds[7].text_content())        }
#        print data
