import scraperwiki
import lxml.etree
import sys
import dateutil.parser     
import urllib2

# Read RSS feed from a blog and get entire archive of text for feeding into Overview

url = "http://emerge2012.net/"

def scrape_one_rss_page(number):
    //page_url = url + str(number)
    print "scraping", page_url

    try:
        rss = scraperwiki.scrape(page_url)
    except urllib2.HTTPError, err:
        if err.code == 404:
            return False
        else:
            raise

    rss = rss.replace('content:encoded', 'content_encoded') # I hate XML namespaces
    root = lxml.etree.fromstring(rss)
    items = root.xpath('//item')

    if len(items) == 0:
        return False

    for item in items:
        print item.text_content()
        row_title = item.xpath('title')[0].text
        row_text = item.xpath('content_encoded')[0].text
        row_url = item.xpath('guid')[0].text
        row_when = dateutil.parser.parse(item.xpath('pubDate')[0].text).date()
        row = { 'url': row_url, 'text': row_text, 'title': row_title, 'when': row_when }
        scraperwiki.sqlite.save(['url'], row)
        print row

    return True

page = 5
while scrape_one_rss_page(page):
    print page
    page = page + 1


