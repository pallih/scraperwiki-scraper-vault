import scraperwiki

html = scraperwiki.scrape("http://www.boxofficemojo.com/movies/alphabetical.htm?letter=A&page=2&p=.htm")
import lxml.html           
root = lxml.html.fromstring(html) 
for tr in root.cssselect("table tr"):
    tds = tr.cssselect("td")
    if len(tds)==4:
        data = {
            'title' : tds[0].text_content(),
            'studio' : tds[1].text_content()
        }
        print data

import scraperwiki

html = scraperwiki.scrape("http://www.boxofficemojo.com/movies/alphabetical.htm?letter=A&page=2&p=.htm")
import lxml.html           
root = lxml.html.fromstring(html) 
for tr in root.cssselect("table tr"):
    tds = tr.cssselect("td")
    if len(tds)==4:
        data = {
            'title' : tds[0].text_content(),
            'studio' : tds[1].text_content()
        }
        print data

