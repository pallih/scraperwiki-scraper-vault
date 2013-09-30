import lxml.html
import scraperwiki
import urlparse

base_url = "http://verejna-sprava.kr-moravskoslezsky.cz/zastupitelstvo.html"
html = scraperwiki.scrape(base_url)
page = lxml.html.fromstring(html)

for href in page.xpath("//table/tr/td/a/@href"):
    url = urlparse.urljoin(base_url, href)
    party_html = scraperwiki.scrape(url)
    data = { 'url': url, 'html': party_html }
    scraperwiki.sqlite.save(unique_keys=['url'], data=data)
import lxml.html
import scraperwiki
import urlparse

base_url = "http://verejna-sprava.kr-moravskoslezsky.cz/zastupitelstvo.html"
html = scraperwiki.scrape(base_url)
page = lxml.html.fromstring(html)

for href in page.xpath("//table/tr/td/a/@href"):
    url = urlparse.urljoin(base_url, href)
    party_html = scraperwiki.scrape(url)
    data = { 'url': url, 'html': party_html }
    scraperwiki.sqlite.save(unique_keys=['url'], data=data)
