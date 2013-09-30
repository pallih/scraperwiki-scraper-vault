import scraperwiki
import sys, httplib2, urllib, re, random
import urlparse
from lxml import etree
import lxml.html
from StringIO import StringIO
from time import sleep
from datetime import date, datetime


def chunks(l, n):
    ''' 
    http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks-in-python
    '''
    return [l[i:i+n] for i in range(0, len(l), n)]


def data_prep(content):#function to grab urls
    #print content
    doc = lxml.html.document_fromstring(content)
    records = doc.cssselect('div.productitem')
    return scrape(records)
    


def page_load(url): #function to scrape page
    link = []
    h = httplib2.Http(".cache")
    response, content = h.request(url, "GET")
    if response.status != 200:
        sys.stderr.write('Error, returned status: %s\n' % response.status)
        sys.exit(1) #bomb out, non-zero return indicates error
    return data_prep(content)

#wayback = re.match('http://web.archive.org/.*/http://shop.carrefour.co.id/category/161/')

# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    r = lxml.html.fromstring(html)
    # For each item
    def scrape(records): 
        for r in records: 
            data = {}
            data['key'] = random.random()
            data['scrapedate'] = date.today().strftime("%d/%m/%Y")
            for item1 in r.cssselect('a[title]'):
                data['product'] = item1.text
            for item2 in r.cssselect('span.capacity'):
                data['capacity'] = item2.text
            for item3 in r.cssselect('span.promoprice'):    
                data['price'] = item3.text
            scraperwiki.sqlite.save(["key"], data) #Store data in sqlite database
            #print r.cssselect('span.capacity')
    next_link = r.cssselect("span.paginate-previous")
    print next_link
    if next_link:
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        print next_url
        scrape_and_look_for_next_link(next_url)

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
base_url = 'http://www.carrefour.co.id/id/category/Produk_Dairy_93/'
# starting_url = urlparse.urljoin(base_url, '')
# scrape_and_look_for_next_link(starting_url)

# urls = ['http://www.carrefour.co.id/id/category/Produk_Dairy_93/','http://www.carrefour.co.id/id/category/Produk_Dairy_93/?page=2']  

# for u in urls:
#    page_load(u)
#    sleep(1)import scraperwiki
import sys, httplib2, urllib, re, random
import urlparse
from lxml import etree
import lxml.html
from StringIO import StringIO
from time import sleep
from datetime import date, datetime


def chunks(l, n):
    ''' 
    http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks-in-python
    '''
    return [l[i:i+n] for i in range(0, len(l), n)]


def data_prep(content):#function to grab urls
    #print content
    doc = lxml.html.document_fromstring(content)
    records = doc.cssselect('div.productitem')
    return scrape(records)
    


def page_load(url): #function to scrape page
    link = []
    h = httplib2.Http(".cache")
    response, content = h.request(url, "GET")
    if response.status != 200:
        sys.stderr.write('Error, returned status: %s\n' % response.status)
        sys.exit(1) #bomb out, non-zero return indicates error
    return data_prep(content)

#wayback = re.match('http://web.archive.org/.*/http://shop.carrefour.co.id/category/161/')

# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    r = lxml.html.fromstring(html)
    # For each item
    def scrape(records): 
        for r in records: 
            data = {}
            data['key'] = random.random()
            data['scrapedate'] = date.today().strftime("%d/%m/%Y")
            for item1 in r.cssselect('a[title]'):
                data['product'] = item1.text
            for item2 in r.cssselect('span.capacity'):
                data['capacity'] = item2.text
            for item3 in r.cssselect('span.promoprice'):    
                data['price'] = item3.text
            scraperwiki.sqlite.save(["key"], data) #Store data in sqlite database
            #print r.cssselect('span.capacity')
    next_link = r.cssselect("span.paginate-previous")
    print next_link
    if next_link:
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        print next_url
        scrape_and_look_for_next_link(next_url)

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
base_url = 'http://www.carrefour.co.id/id/category/Produk_Dairy_93/'
# starting_url = urlparse.urljoin(base_url, '')
# scrape_and_look_for_next_link(starting_url)

# urls = ['http://www.carrefour.co.id/id/category/Produk_Dairy_93/','http://www.carrefour.co.id/id/category/Produk_Dairy_93/?page=2']  

# for u in urls:
#    page_load(u)
#    sleep(1)