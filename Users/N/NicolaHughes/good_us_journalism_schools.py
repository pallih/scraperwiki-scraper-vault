import scraperwiki
import lxml.html
import urlparse

url = 'http://education-portal.com/top_10_journalism_schools.html'

html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)

for tr in root.cssselect("table[class='wikitable'] tr"):
    tds = tr.cssselect("td")
    if len(tds)>1:
        data = {'Name' : tds[0].text_content(),'Address' : tds[2].text_content(),'Phone Number' : tds[3].text_content()}
        print data
        #scraperwiki.sqlite.save(unique_keys=['Name'], data=data)import scraperwiki
import lxml.html
import urlparse

url = 'http://education-portal.com/top_10_journalism_schools.html'

html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)

for tr in root.cssselect("table[class='wikitable'] tr"):
    tds = tr.cssselect("td")
    if len(tds)>1:
        data = {'Name' : tds[0].text_content(),'Address' : tds[2].text_content(),'Phone Number' : tds[3].text_content()}
        print data
        #scraperwiki.sqlite.save(unique_keys=['Name'], data=data)