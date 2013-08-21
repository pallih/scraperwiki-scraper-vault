import scraperwiki
import lxml.html
import urlparse

url = 'http://www.espncricinfo.com/rankings/content/page/211271.html'

html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)

for tr in root.cssselect("table[class='wikitable'] tr"):
    tds = tr.cssselect("td")
    if len(tds)>1:
        data = {'Team' : tds[0].text_content(),'Matches' : tds[2].text_content(),'Points' : tds[3].text_content(),'Rating' : tds[4].text_content()}
        scraperwiki.sqlite.save(unique_keys=['Team'], data=data)