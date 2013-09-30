# TMZ.com RSS feed scraper

import scraperwiki
import feedparser
import lxml.html

FEED_URL = 'http://www.tmz.com/rss.xml'

def parse_feed(url):
    links = []
    feed = feedparser.parse(url)
    for item in feed['items']:
        links.append(item['link'])
    return links

def scrape_page(url):
    html = scraperwiki.scrape(url)
    dom = lxml.html.fromstring(html)
    return dom

def get_title(dom):
    title_node = dom.cssselect('div#single-post-headline')[0]
    return get_node_text(title_node)

def get_content(dom):    
    content_node = dom.cssselect('div.all-post-body')[0]
    # Remove non relevant nodes
    for node in content_node.findall('div'):
        content_node.remove(node)
    for node in content_node.findall('script'):
        content_node.remove(node)
    for node in content_node.findall('object'):
        content_node.remove(node)
    return content_node.text_content().strip()

def get_node_text(node):
    text = ''
    for d in node.iterdescendants():
        # Replace <br> with line breaks
        if d.tag == 'br':
            text += '\n'
        else:
            text += d.text
    return text.strip().title()

for url in parse_feed(FEED_URL):
    article = {'url':url}
    dom = scrape_page(url)
    article['title'] = get_title(dom)
    article['content'] = get_content(dom)
    scraperwiki.sqlite.save(unique_keys=['url'], data=article)# TMZ.com RSS feed scraper

import scraperwiki
import feedparser
import lxml.html

FEED_URL = 'http://www.tmz.com/rss.xml'

def parse_feed(url):
    links = []
    feed = feedparser.parse(url)
    for item in feed['items']:
        links.append(item['link'])
    return links

def scrape_page(url):
    html = scraperwiki.scrape(url)
    dom = lxml.html.fromstring(html)
    return dom

def get_title(dom):
    title_node = dom.cssselect('div#single-post-headline')[0]
    return get_node_text(title_node)

def get_content(dom):    
    content_node = dom.cssselect('div.all-post-body')[0]
    # Remove non relevant nodes
    for node in content_node.findall('div'):
        content_node.remove(node)
    for node in content_node.findall('script'):
        content_node.remove(node)
    for node in content_node.findall('object'):
        content_node.remove(node)
    return content_node.text_content().strip()

def get_node_text(node):
    text = ''
    for d in node.iterdescendants():
        # Replace <br> with line breaks
        if d.tag == 'br':
            text += '\n'
        else:
            text += d.text
    return text.strip().title()

for url in parse_feed(FEED_URL):
    article = {'url':url}
    dom = scrape_page(url)
    article['title'] = get_title(dom)
    article['content'] = get_content(dom)
    scraperwiki.sqlite.save(unique_keys=['url'], data=article)