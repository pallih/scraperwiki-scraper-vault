import os, sys

import lxml.html
import lxml.etree
import urllib2
import urlparse
import requests

import scraperwiki

base_url = 'http://www.rcog.org.uk/guidelines?filter0%5B%5D=10' 
html = scraperwiki.scrape(base_url)
page = lxml.html.fromstring(html)
table = page.cssselect( 'div.view-content-clinical-health-documents table')[0]
for row in table.cssselect('tbody tr'):
    href = row[0][0]
    
    title = href.text_content()

    fullpage = urlparse.urljoin( base_url, href.attrib.get('href') )
    published = row[1].text_content()
    
    newpage_html = scraperwiki.scrape(fullpage)
    newpage = lxml.html.fromstring(newpage_html)
    for a in newpage.cssselect('a'):
        h = urlparse.urljoin( base_url, a.attrib.get('href') )
        if '.pdf' in h:
            t = a.text_content()
            if t and not t =='here':
                title = t
            
            r = requests.head(h)
            size = r.headers['content-length']
            if int(size) == 0:
                continue

            kwlist = [x.lower() for x in title.split(' ') if not x.lower() in ['the', 'of', 'in', 'and', 'its']]
            keywords = ','.join(kwlist)
            pubmonth,pubyear = published.split(' ')

            d = {'title': title, 'published_month': pubmonth, 'published_year':pubyear, 'link' : h, 'keywords': keywords, 'size': size}
            scraperwiki.sqlite.save(['title'], d)

