from lxml import html
import scraperwiki
import base64
from urlparse import urljoin
site = "http://www.cpb.nl/publicaties?page=1&filters=-language%3Aen%20type%3Apublicatie%20ss_cck_field_typepublicatie%3A%22CPB%20Newsletter%22&solrsort=sort_ss_cck_field_publicatiedatum%20desc/"
def scrapePagina(site):
    page = scraperwiki.scrape(site)
    page = html.fromstring(page)
    succes = False
    for article in page.cssselect("ol.list.search_results li"):
        succes = True
        link = article.cssselect("a.download-pdf")[0].get("href")
        link = urljoin(site, link)
        doc = base64.b64encode(scraperwiki.scrape(link))
        title = article.cssselect("h2")[0].text_content()
        data = {"url": link,  "title": title, "document": doc}
        scraperwiki.sqlite.save(unique_keys=["url"], data=data) 
    return succes


for i in range(100):
    site = "http://www.cpb.nl/publicaties?page="
    site += str(i)
    site += "&filters=-language%3Aen%20type%3Apublicatie%20ss_cck_field_typepublicatie%3A%22CPB%20Newsletter%22&solrsort=sort_ss_cck_field_publicatiedatum%20desc/"
    if not scrapePagina(site):
        breakfrom lxml import html
import scraperwiki
import base64
from urlparse import urljoin
site = "http://www.cpb.nl/publicaties?page=1&filters=-language%3Aen%20type%3Apublicatie%20ss_cck_field_typepublicatie%3A%22CPB%20Newsletter%22&solrsort=sort_ss_cck_field_publicatiedatum%20desc/"
def scrapePagina(site):
    page = scraperwiki.scrape(site)
    page = html.fromstring(page)
    succes = False
    for article in page.cssselect("ol.list.search_results li"):
        succes = True
        link = article.cssselect("a.download-pdf")[0].get("href")
        link = urljoin(site, link)
        doc = base64.b64encode(scraperwiki.scrape(link))
        title = article.cssselect("h2")[0].text_content()
        data = {"url": link,  "title": title, "document": doc}
        scraperwiki.sqlite.save(unique_keys=["url"], data=data) 
    return succes


for i in range(100):
    site = "http://www.cpb.nl/publicaties?page="
    site += str(i)
    site += "&filters=-language%3Aen%20type%3Apublicatie%20ss_cck_field_typepublicatie%3A%22CPB%20Newsletter%22&solrsort=sort_ss_cck_field_publicatiedatum%20desc/"
    if not scrapePagina(site):
        break