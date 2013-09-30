#Scraper for Windsor, ON city council

import scraperwiki
import urllib2
from BeautifulSoup import BeautifulSoup
import lxml.html.soupparser
import re

import urllib2
from urlparse import urljoin

MAYOR_URL = 'http://www.citywindsor.ca/mayorandcouncil/Pages/Mayor-and-City-Council.aspx'
COUNCIL_URL = 'http://www.citywindsor.ca/mayorandcouncil/City-Councillors/Pages/City-Councillors.aspx'

def getroot(addr):
    html = scraperwiki.scrape(addr)
    return lxml.html.soupparser.fromstring(html)

def main():
    mayor_details(MAYOR_URL)
    url = urllib2.urlopen(COUNCIL_URL).read()
    doc = BeautifulSoup(url)
    councillors = doc.find('ul',{'id':'ctl00_SiteMapNavigation_ctl00_lnmJS'})
    for url in councillors.findAll('a'):        
        councillor_details(urljoin(COUNCIL_URL, url['href']))

def councillor_details(url):
    root = getroot(url)
    councillor = {}
    councillor['url'] = url
    councillor['source_url'] = url
    councillor['elected_office'] = 'Councillor'

    description = root.xpath('//div[@id="CCWMainContent2"]')[0]
    title = description.xpath('//strong/text()')[0]
    header = title.replace(u'\xa0', u' ').split(' - ')
    councillor['name'] = ' '.join(header[0].split()[1:])
    councillor['district_name'] = header[1]
    councillor['district_id'] = header[1].split()[1]

    councillor['email'] = description.xpath('//a[contains(@href, "mailto")]/text()')[0]
    photo = description.xpath('.//img/@src')
    councillor['photo_url'] = urljoin(url, photo[1])
    save(councillor)

def mayor_details(url):
    root = getroot(url)
    mayor = {}
    mayor['url'] = url
    mayor['source_url'] = url
    mayor['elected_office'] = 'Mayor'
    mayor['district_name'] = 'Windsor'
    mayor['district_id'] = 0
    mayor['name'] = root.xpath('//*[@id="ctl00_PlaceHolderMain_ctl02__ControlWrapper_RichHtmlField"]//a/text()')[0]
    mayor['email'] = root.xpath('//a[contains(@href, "mailto")][1]/text()')[0]
    photo = root.xpath('//img[@id="I010"]/@src')
    mayor['photo_url'] = urljoin(url, photo[0])
    mayor['boundary_url'] = '/boundaries/census-subdivisions/3537039/'
    save(mayor)
def save(rep):
    scraperwiki.sqlite.save(['district_id'], rep)

if scraperwiki.sqlite.select('name FROM sqlite_master WHERE type="table" AND name="swdata"'):
    scraperwiki.sqlite.execute('DROP TABLE `swdata`')
main()
#Scraper for Windsor, ON city council

import scraperwiki
import urllib2
from BeautifulSoup import BeautifulSoup
import lxml.html.soupparser
import re

import urllib2
from urlparse import urljoin

MAYOR_URL = 'http://www.citywindsor.ca/mayorandcouncil/Pages/Mayor-and-City-Council.aspx'
COUNCIL_URL = 'http://www.citywindsor.ca/mayorandcouncil/City-Councillors/Pages/City-Councillors.aspx'

def getroot(addr):
    html = scraperwiki.scrape(addr)
    return lxml.html.soupparser.fromstring(html)

def main():
    mayor_details(MAYOR_URL)
    url = urllib2.urlopen(COUNCIL_URL).read()
    doc = BeautifulSoup(url)
    councillors = doc.find('ul',{'id':'ctl00_SiteMapNavigation_ctl00_lnmJS'})
    for url in councillors.findAll('a'):        
        councillor_details(urljoin(COUNCIL_URL, url['href']))

def councillor_details(url):
    root = getroot(url)
    councillor = {}
    councillor['url'] = url
    councillor['source_url'] = url
    councillor['elected_office'] = 'Councillor'

    description = root.xpath('//div[@id="CCWMainContent2"]')[0]
    title = description.xpath('//strong/text()')[0]
    header = title.replace(u'\xa0', u' ').split(' - ')
    councillor['name'] = ' '.join(header[0].split()[1:])
    councillor['district_name'] = header[1]
    councillor['district_id'] = header[1].split()[1]

    councillor['email'] = description.xpath('//a[contains(@href, "mailto")]/text()')[0]
    photo = description.xpath('.//img/@src')
    councillor['photo_url'] = urljoin(url, photo[1])
    save(councillor)

def mayor_details(url):
    root = getroot(url)
    mayor = {}
    mayor['url'] = url
    mayor['source_url'] = url
    mayor['elected_office'] = 'Mayor'
    mayor['district_name'] = 'Windsor'
    mayor['district_id'] = 0
    mayor['name'] = root.xpath('//*[@id="ctl00_PlaceHolderMain_ctl02__ControlWrapper_RichHtmlField"]//a/text()')[0]
    mayor['email'] = root.xpath('//a[contains(@href, "mailto")][1]/text()')[0]
    photo = root.xpath('//img[@id="I010"]/@src')
    mayor['photo_url'] = urljoin(url, photo[0])
    mayor['boundary_url'] = '/boundaries/census-subdivisions/3537039/'
    save(mayor)
def save(rep):
    scraperwiki.sqlite.save(['district_id'], rep)

if scraperwiki.sqlite.select('name FROM sqlite_master WHERE type="table" AND name="swdata"'):
    scraperwiki.sqlite.execute('DROP TABLE `swdata`')
main()
