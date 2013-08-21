from lxml import html
import scraperwiki
from urlparse import urljoin

# Blank Python

site = "http://www.senternovem.nl/stralingsbescherming/verleende_vergunningen/index.asp"
page = scraperwiki.scrape(site)
page = html.fromstring(page)

for year in page.cssselect("a.content"):    
    url = year.get("href")
    url = urljoin(site,url)
    page = scraperwiki.scrape(url)
    page = html.fromstring(page)
    for link in page.cssselect("a.content"): 
    url = year.get("href")        
        print link