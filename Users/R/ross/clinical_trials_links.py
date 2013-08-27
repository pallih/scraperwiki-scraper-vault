import lxml.html
import urlparse
import scraperwiki
import time

def split_anchor(a):
    return a.text_content(), a.attrib.get('href')

site = "http://clinicaltrials.gov/crawl"

for x in range(1, 767):
    url = urlparse.urljoin(site, "/ct2/crawl/%s" % x)
    html = scraperwiki.scrape( url )
    page = lxml.html.fromstring( html )
    links = page.cssselect( 'a')
    data = []
    for link in links:
        name,l = split_anchor(link)
        if not l:
            continue
        name = l.split('/')[ -1 ]
        if not name.startswith("NCT"):
            continue
        l = l.replace("NCT", "record/NCT")
        data.append({'code':name, 'link': urlparse.urljoin(site, l)})

    scraperwiki.sqlite.save(['link'], data, table_name='search_page_links')import lxml.html
import urlparse
import scraperwiki
import time

def split_anchor(a):
    return a.text_content(), a.attrib.get('href')

site = "http://clinicaltrials.gov/crawl"

for x in range(1, 767):
    url = urlparse.urljoin(site, "/ct2/crawl/%s" % x)
    html = scraperwiki.scrape( url )
    page = lxml.html.fromstring( html )
    links = page.cssselect( 'a')
    data = []
    for link in links:
        name,l = split_anchor(link)
        if not l:
            continue
        name = l.split('/')[ -1 ]
        if not name.startswith("NCT"):
            continue
        l = l.replace("NCT", "record/NCT")
        data.append({'code':name, 'link': urlparse.urljoin(site, l)})

    scraperwiki.sqlite.save(['link'], data, table_name='search_page_links')import lxml.html
import urlparse
import scraperwiki
import time

def split_anchor(a):
    return a.text_content(), a.attrib.get('href')

site = "http://clinicaltrials.gov/crawl"

for x in range(1, 767):
    url = urlparse.urljoin(site, "/ct2/crawl/%s" % x)
    html = scraperwiki.scrape( url )
    page = lxml.html.fromstring( html )
    links = page.cssselect( 'a')
    data = []
    for link in links:
        name,l = split_anchor(link)
        if not l:
            continue
        name = l.split('/')[ -1 ]
        if not name.startswith("NCT"):
            continue
        l = l.replace("NCT", "record/NCT")
        data.append({'code':name, 'link': urlparse.urljoin(site, l)})

    scraperwiki.sqlite.save(['link'], data, table_name='search_page_links')