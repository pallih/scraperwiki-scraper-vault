from lxml import html
import scraperwiki
import mechanize
from urlparse import urljoin

site = "http://www.desan.nl/net/DoSearch/Search.aspx"
page = scraperwiki.scrape (site)
page = html.fromstring (page)
vs = page.cssselect("input")[0].get("value")

for jaar in range(2000,2011):
    br = mechanize.Browser()
    br.open(site)
    br.select_form("aspnetForm")
    br['zoeken_jaar'] = [str(jaar)]
    resp = br.submit().read()
    overzicht = html.fromstring(resp)   
    for doc in overzicht.cssselect("a.fd"):
        print urljoin (site, doc.get("href"))

    