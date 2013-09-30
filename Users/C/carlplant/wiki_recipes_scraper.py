import scraperwiki

# Blank Python
import scraperwiki
import urlparse
import lxml.html
import datetime
now = datetime.datetime.now()
import re
from BeautifulSoup import BeautifulSoup


def scrape_table(next_url):
    html2 = scraperwiki.scrape(next_url)
    print html2
    root2 = lxml.html.fromstring(html2)
    title_cell = root2.cssselect('div.row-title.clear div h1')
    print title_cell[0].text
    
    
    
def scrape_next_link(base_url):
    html = scraperwiki.scrape(base_url)
    #print html
    root = lxml.html.fromstring(html)
    #scrape_table(root)
    next_link = root.cssselect("div.text h3")
    for row in next_link:
        cells = row.cssselect("a")
        if cells:
            next_url = urlparse.urljoin(base_url, cells[0].attrib.get('href'))
            scrape_table(next_url)
            print next_url
            
           

base_url = 'http://www.nhs.uk/Livewell/healthy-recipes/Pages/Healthy-recipes.aspx'
scrape_next_link(base_url)

import scraperwiki

# Blank Python
import scraperwiki
import urlparse
import lxml.html
import datetime
now = datetime.datetime.now()
import re
from BeautifulSoup import BeautifulSoup


def scrape_table(next_url):
    html2 = scraperwiki.scrape(next_url)
    print html2
    root2 = lxml.html.fromstring(html2)
    title_cell = root2.cssselect('div.row-title.clear div h1')
    print title_cell[0].text
    
    
    
def scrape_next_link(base_url):
    html = scraperwiki.scrape(base_url)
    #print html
    root = lxml.html.fromstring(html)
    #scrape_table(root)
    next_link = root.cssselect("div.text h3")
    for row in next_link:
        cells = row.cssselect("a")
        if cells:
            next_url = urlparse.urljoin(base_url, cells[0].attrib.get('href'))
            scrape_table(next_url)
            print next_url
            
           

base_url = 'http://www.nhs.uk/Livewell/healthy-recipes/Pages/Healthy-recipes.aspx'
scrape_next_link(base_url)

