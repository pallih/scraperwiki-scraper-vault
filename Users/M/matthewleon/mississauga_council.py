#Scraper for Mississauga

import scraperwiki

import lxml.html.soupparser
import re

import urllib2
from urlparse import urljoin

COUNCIL_URL = 'http://www.mississauga.ca/portal/cityhall/mayorandcouncil'


def getroot(addr):
    html = scraperwiki.scrape(addr)
    return lxml.html.soupparser.fromstring(html)

def main():
    root = getroot(COUNCIL_URL)
    for url in root.xpath('//area/@href'):
        if 'mayor' in url:
            mayor_details(urljoin(COUNCIL_URL, url))
        else:
            councillor_details(urljoin(COUNCIL_URL, url))

def councillor_details(url):
    root = getroot(url)
    councillor = {}
    councillor['url'] = url
    councillor['source_url'] = url
    councillor['elected_office'] = 'Councillor'
    district = re.search('Ward (\d+)', root.xpath('//title/text()')[0])
    councillor['district_name'] = district.group(0)
    councillor['district_id'] = district.group(1)
    councillor['name'] = root.xpath('//strong[1]/text()')[0]
    councillor['email'] = re.search('[a-z.-]+@mississauga.ca', lxml.html.tostring(root)).group(0)
    photo = root.xpath('//img[contains(@src, "/file/COM/")]/@src')
    councillor['photo_url'] = urljoin(url, photo[0])
    site = root.xpath('//p[contains(text(), "Website")]/a/@href')
    if site:
        councillor['personal_url'] = site[0]
    save(councillor)

def mayor_details(url):
    root = getroot(url)
    mayor = {}
    mayor['url'] = url
    mayor['source_url'] = url
    mayor['elected_office'] = 'Mayor'
    mayor['district_name'] = 'Mississauga'
    mayor['district_id'] = 0
    photo = root.xpath('//img[contains(@src, "/file/COM/")]/@src')
    mayor['photo_url'] = urljoin(url, photo[0])
    
    # name and e-mail on separate page
    url = 'http://www.mississauga.ca/portal/cityhall/contactthemayor'
    root = getroot(url)
    nametext = root.xpath('//p[contains(text(), "Worship Mayor")]/text()')[0]
    mayor['name'] = ' '.join(nametext.split()[3:])
    mayor['email'] = root.xpath('//a[contains(@href, "mailto")]/text()')[0]
    mayor['boundary_url'] = '/boundaries/census-subdivisions/3521005/'
    save(mayor)

def save(rep):
    scraperwiki.sqlite.save(['district_id'], rep)

if scraperwiki.sqlite.select('name FROM sqlite_master WHERE type="table" AND name="swdata"'):
    scraperwiki.sqlite.execute('DROP TABLE `swdata`')
main()