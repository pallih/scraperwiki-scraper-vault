import scraperwiki
import sys, httplib2, urllib, re
from lxml import etree
from StringIO import StringIO
from time import sleep



def scrape(content, country): 
    for r in content:
        data = {}
        data['key'] = '%s-%s' % (r[1], country)
        data['country'] = country
        data['site'] = r[0]
        data['rank'] = r[1]
        data['url'] = r[2]
#        data['rank'] = r[0]
#        data['url'] = r[1]
        scraperwiki.sqlite.save(["key"], data) #Store data in sqlite database


def data_prep(content, country):#function to grab urls
    records = []
    doc = etree.parse(StringIO(content), parser=etree.HTMLParser())
    for num in range(1,25):
        xpath_string_rank = '//*[@id="topsites-countries"]/div/ul/li[%d]/div[1]' % (num)
        xpath_string_url = '//*[@id="topsites-countries"]/div/ul/li[%d]/div[2]/h2/a'  % (num)
        xpath_string_site = '//*[@id="topsites-countries"]/div/ul/li[%d]/div[2]/span[@class="small topsites-label"]'  % (num)
#        print doc.xpath(xpath_string_site)[0].text
#        records += [(doc.xpath(xpath_string_rank)[0].text, doc.xpath(xpath_string_url)[0].text)]
        records += [(doc.xpath(xpath_string_site)[0].text, doc.xpath(xpath_string_rank)[0].text, doc.xpath(xpath_string_url)[0].text)]


    #for r in records:
        #print r
    return scrape(records, country)


def page_load(country,page): #function to scrape page
    link = []
    url = "http://www.alexa.com/topsites/countries%s/%s" % (page,country)
    h = httplib2.Http(".cache")
    response, content = h.request(url, "GET")
    if response.status != 200:
        sys.stderr.write('Error, returned status: %s\n' % response.status)
        sys.exit(1) #bomb out, non-zero return indicates error
    return data_prep(content, country)

countries_str = '''IR'''

countries = countries_str.split()

pages = ["", ";1", ";2", ";3", ";4", ";5", ";6", ";7", ";8", ";9", ";10", ";11", ";12", ";13", ";14", ";15", ";16", ";17", ";18", ";19", ";20"] 

for c in countries:
    for p in pages:
        page_load(c,p)
        sleep(1)


