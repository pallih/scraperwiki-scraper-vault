# Extract postings from a blog at foobar.blogspot[.com|.co.uk|.de] year-wise

import scraperwiki
import lxml.etree
import sys
import dateutil.parser     
import urllib2

blog_id = "dierotenschuhe"
base_url = "http://" + blog_id + ".blogspot.de/feeds/posts/default"
url_postfix = "&orderby=updated&max-results=1000&alt=rss"

# TODO: These dates should be extracted from the RSS feed
first_year = 2009
last_year = 2013

def scrape_year(current_year):

    published_min = "?published-min=" + str(current_year) + "-01-01T00:00:00%2B01:00"
    published_max = "&published-max=" + str(current_year+1) + "-01-01T00:00:00%2B01:00"
    page_url = base_url + published_min + published_max + url_postfix
    print "scraping", page_url

    try:
        rss = scraperwiki.scrape(page_url)
    except urllib2.HTTPError, err:
        if err.code == 404:
            return False
        else:
            raise

    rss = rss.replace('atom:updated', 'updated') # Flatten XML namespace
    root = lxml.etree.fromstring(rss)
    items = root.xpath('//item')

    if len(items) == 0:
        return False

    for item in items:
        title = item.xpath('title')[0].text
        text = item.xpath('description')[0].text
        url = item.xpath('link')[0].text
        published = dateutil.parser.parse(item.xpath('pubDate')[0].text).date()
        updated = dateutil.parser.parse(item.xpath('updated')[0].text).date()
        row = { 'url': url, 'title': title, 'text': text, 'published': published, 'updated': updated }
        scraperwiki.sqlite.save(['url'], row)
        print row

    return True

for current_year in range(first_year, last_year):
    scrape_year(current_year)
# Extract postings from a blog at foobar.blogspot[.com|.co.uk|.de] year-wise

import scraperwiki
import lxml.etree
import sys
import dateutil.parser     
import urllib2

blog_id = "dierotenschuhe"
base_url = "http://" + blog_id + ".blogspot.de/feeds/posts/default"
url_postfix = "&orderby=updated&max-results=1000&alt=rss"

# TODO: These dates should be extracted from the RSS feed
first_year = 2009
last_year = 2013

def scrape_year(current_year):

    published_min = "?published-min=" + str(current_year) + "-01-01T00:00:00%2B01:00"
    published_max = "&published-max=" + str(current_year+1) + "-01-01T00:00:00%2B01:00"
    page_url = base_url + published_min + published_max + url_postfix
    print "scraping", page_url

    try:
        rss = scraperwiki.scrape(page_url)
    except urllib2.HTTPError, err:
        if err.code == 404:
            return False
        else:
            raise

    rss = rss.replace('atom:updated', 'updated') # Flatten XML namespace
    root = lxml.etree.fromstring(rss)
    items = root.xpath('//item')

    if len(items) == 0:
        return False

    for item in items:
        title = item.xpath('title')[0].text
        text = item.xpath('description')[0].text
        url = item.xpath('link')[0].text
        published = dateutil.parser.parse(item.xpath('pubDate')[0].text).date()
        updated = dateutil.parser.parse(item.xpath('updated')[0].text).date()
        row = { 'url': url, 'title': title, 'text': text, 'published': published, 'updated': updated }
        scraperwiki.sqlite.save(['url'], row)
        print row

    return True

for current_year in range(first_year, last_year):
    scrape_year(current_year)
