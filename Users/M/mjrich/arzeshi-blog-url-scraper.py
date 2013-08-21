import scraperwiki
import sys, httplib2, urllib, re
from lxml import etree
from StringIO import StringIO
from time import sleep



def scrape(content, page): 
    for href in content:
        data = {}
        data['page'] = page
        data['url'] = href.attrib['href']
        scraperwiki.sqlite.save(["url"], data) #Store data in sqlite database


def data_prep(content, page):#function to grab urls
    records = []
    doc = etree.parse(StringIO(content), parser=etree.HTMLParser())
    hrefs = doc.xpath('//*[@id="content"]/div/div[2]/a')
    print hrefs
    #for href in hrefs:
        #print href.attrib['href']
    return scrape(hrefs, page)


def page_load(page): #function to scrape JPAL page
    link = []
    url = "http://pw-arzeshi.com/members.php?page=%s" % (page)
    h = httplib2.Http(".cache")
    response, content = h.request(url, "GET")
    if response.status != 200:
        sys.stderr.write('Error, returned status: %s\n' % response.status)
        sys.exit(1) #bomb out, non-zero return indicates error
    return data_prep(content, page)


for page in range(1, 97):
    page_load(page)
    sleep(1)

