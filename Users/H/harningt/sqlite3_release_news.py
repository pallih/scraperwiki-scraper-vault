import scraperwiki

import urllib
import urlparse

import requests

from lxml import etree
from lxml import html
from cStringIO import StringIO

import dateutil.parser


URL_LIST = [
    "http://sqlite.org/news.html",
    "http://sqlite.org/oldnews.html"
]

def processURL(url, entries):
    response = requests.get(url)
    
    if response.status_code != 200:
        # Failed
        scraperwiki.utils.log("URL '%s' reported failure '%s'" % (url, response))
        # All failures result in no more processing
        return False

    parser = etree.HTMLParser(strip_cdata = False)
    #tree = etree.fromstring(response.content, parser)
    #tree.make_links_absolute("http://sqlite.org")
    tree = html.fromstring(response.content)
    tree.make_links_absolute("http://sqlite.org")

    for entry in tree.findall('.//h3'):
        linkElement = entry.getprevious()
        key = linkElement.attrib.get("name")

        output = StringIO()

        if entry.text:
            output.write(entry.text)
        for element in entry.iterchildren():
            output.write(etree.tostring(element))
        if entry.tail:
            output.write(entry.tail)
        entryTitle = output.getvalue()
        date = dateutil.parser.parse(entryTitle.split(None, 1)[0].replace("Jly", "July"))

        content = etree.tostring(entry.getnext())

        entries.append({ "key":key, "content": content, "date": date, "title": entryTitle, "source": url })

    return True

entries = []

for url in URL_LIST:
    processURL(url, entries)

scraperwiki.sqlite.save(unique_keys = ['key'], data = entries, table_name = "news_items")
