import scraperwiki
import lxml.html
import urlparse

url = 'http://www.thecompleteuniversityguide.co.uk/league-tables/rankings?y=2011'

html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)

for tr in root.cssselect("table[class='wikitable'] tr"):
    tds = tr.cssselect("td")
    if len(tds)>1:
        data = {'Raking' : tds[0].text_content(),'Name' : tds[2].text_content(),'Standard' : tds[3].text_content()}
        scraperwiki.sqlite.save(unique_keys=['Ranking'], data=data)
import scraperwiki
import lxml.html
import urlparse

url = 'http://www.thecompleteuniversityguide.co.uk/league-tables/rankings?y=2011'

html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)

for tr in root.cssselect("table[class='wikitable'] tr"):
    tds = tr.cssselect("td")
    if len(tds)>1:
        data = {'Raking' : tds[0].text_content(),'Name' : tds[2].text_content(),'Standard' : tds[3].text_content()}
        scraperwiki.sqlite.save(unique_keys=['Ranking'], data=data)
