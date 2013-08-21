import scraperwiki, lxml.html, feedparser
import urllib
from pyPdf import PdfFileReader

def fetch_pdf(url):
    """Fetch the pdf and extract the text."""
    
    filename, http = urllib.urlretrieve(url) 
    print url
    input1 = PdfFileReader(file(filename, "rb"))

    p = input1.getPage(0)

    print p

    #return p.extractText()

def fetch_rss_feed(url):
    """Fetch the rss and process it."""

    return feedparser.parse(url)

def process_menu(menu):
    """Take the text from the pdf and break out the days"""

    print menu

url = "http://molescroftprimaryoffice.posterous.com/rss.xml"    
feed = fetch_rss_feed(url)

for entry in feed['entries']:
    # find menu entries
    if entry['title'].lower().startswith('menu'):
        html = lxml.html.fromstring(entry['summary_detail']['value'])

        if html:
            for link in html.iterlinks():
                # we are only interested in pdf files
                if len(link) > 3 and link[2].endswith('pdf'):
                    menu = fetch_pdf(link[2])
                    process_menu(menu)