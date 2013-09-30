from lxml import html
import scraperwiki
from urlparse import urljoin
site = "http://www.cpb.nl/kortetermijnramingen"
page = scraperwiki.scrape(site)
page = html.fromstring(page)
for article in page.cssselect("div.newsitem"):
    link = article.cssselect("div.newsitem a")[0].get("href")
    link = urljoin(site, link)
    title = article.cssselect("h2")[0].text_content()
    data = {"url": link,  "title": title}
    page = scraperwiki.scrape (link)
    page = html.fromstring (link)
    for table in page.cssselect("div.node-published")
    

scraperwiki.sqlite.save(unique_keys=["url"], data=data) 
    
from lxml import html
import scraperwiki
from urlparse import urljoin
site = "http://www.cpb.nl/kortetermijnramingen"
page = scraperwiki.scrape(site)
page = html.fromstring(page)
for article in page.cssselect("div.newsitem"):
    link = article.cssselect("div.newsitem a")[0].get("href")
    link = urljoin(site, link)
    title = article.cssselect("h2")[0].text_content()
    data = {"url": link,  "title": title}
    page = scraperwiki.scrape (link)
    page = html.fromstring (link)
    for table in page.cssselect("div.node-published")
    

scraperwiki.sqlite.save(unique_keys=["url"], data=data) 
    
