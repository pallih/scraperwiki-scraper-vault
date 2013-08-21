import scraperwiki
import sys, httplib2, urllib, re
from lxml import etree
from StringIO import StringIO
from time import sleep



def scrape(content, country): 
    for r in content:
        data = {}
        data['key'] = '%s-%s' % (r[0], country)
        data['country'] = country
        data['rank'] = r[0]
        data['site'] = r[1]
        scraperwiki.sqlite.save(["key"], data) #Store data in sqlite database


def data_prep(content, country):#function to grab urls
    records = []
    doc = etree.parse(StringIO(content), parser=etree.HTMLParser())
    for num in range(1,11):
        xpath_string_rank = '//*[@id="topsites-countries"]/div[1]/ul/li[%d]/div[1]' % (num)
        xpath_string_url = '//*[@id="topsites-countries"]/div[1]/ul/li[%d]/div[2]/h2/a'  % (num)
        records += [(doc.xpath(xpath_string_rank)[0].text, doc.xpath(xpath_string_url)[0].text)]
    #for r in records:
        #print r
    return scrape(records, country)


def page_load(country): #function to scrape page
    link = []
    url = "http://www.alexa.com/topsites/countries/%s" % (country)
    h = httplib2.Http(".cache")
    response, content = h.request(url, "GET")
    if response.status != 200:
        sys.stderr.write('Error, returned status: %s\n' % response.status)
        sys.exit(1) #bomb out, non-zero return indicates error
    return data_prep(content, country)

countries_str = '''AR
AU
BE
BR
CA
CL
CO
CZ
EG
FR
DE
GB
HK
HU
IN
IE
IL
IT
JP
JO
MY
MX
MA
NL
NZ
PE
PH
PL
RU
SA
SG
ZA
KR
ES
SE
TW
AE
US
'''

countries = countries_str.split()

for c in countries:
    page_load(c)
    sleep(1)


