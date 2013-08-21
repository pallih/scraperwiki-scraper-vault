import scraperwiki
import sys, httplib2, urllib, re, random
from lxml import etree
import lxml.html
from StringIO import StringIO
from time import sleep


#def chunks(l, n):
#    ''' 
#    http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks-in-python
#    '''
#    return [l[i:i+n] for i in range(0, len(l), n)]


def scrape(records): 
    for r in records: 
        data = {}
        data['key'] = random.random()
        for item1 in r.cssselect('a[title]'):
            data['product'] = item1.text
        for item2 in r.cssselect('span.capacity'):
            data['capacity'] = item2.text
        for item3 in r.cssselect('b') or r.cssselect('span.promoprice'):    
            data['price'] = item3.text
        scraperwiki.sqlite.save(["key"], data) #Store data in sqlite database
        #print r.cssselect('span.capacity')
        

#def scrape(links):
    #for l in links:
        #doc = lxml.html.document_fromstring(l)
    

def data_prep(content):#function to grab urls
    #print content
    doc = lxml.html.document_fromstring(content)
    links = doc.cssselect('a[href]')
    return links
    #return scrape(linksTrue)
    #return scrape(records)
    


def page_load(url): #function to scrape page
    link = []
    h = httplib2.Http(".cache")
    response, content = h.request(url, "GET")
    if response.status != 200:
        sys.stderr.write('Error, returned status: %s\n' % response.status)
        sys.exit(1) #bomb out, non-zero return indicates error
    return data_prep(content)

#wayback = re.match('http://web.archive.org/.*/http://shop.carrefour.co.id/category/161/')

urls = ['http://www.ruseffect.com/about', 'links']  

for u in urls:
    page_load(u)
    sleep(1)


