import scraperwiki
import urlparse
import lxml.html

def linkage(html):
    content = lxml.html.etree.HTML(html)
    linkage = content.xpath("/html/body/div/div/h2/a/@href")
    for links in linkage:
        record = { "link" : links }
        scraperwiki.datastore.save(["link"], record)

def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    linkage(html)
    next_link = root.cssselect("a.older")
    print next_link
    if next_link:
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        print next_url
        scrape_and_look_for_next_link(next_url)

base_url = 'http://cor7ana.tumblr.com/'
starting_url = 'http://cor7ana.tumblr.com/'
scrape_and_look_for_next_link(starting_url)