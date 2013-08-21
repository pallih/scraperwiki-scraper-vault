#Scraper for Ottawa City Councilors with their respective wards

import scraperwiki

import lxml.html.soupparser
import re

import urllib2
from urlparse import urljoin
from pprint import pprint

COUNCIL_URL = 'http://ottawa.ca/en/city_hall/councilcommittees/mayor_council/councillors/index.html'
MAYOR_URL = 'http://ottawa.ca/en/city_hall/councilcommittees/mayor_council/mayor/index.html'


def getroot(addr):
    html = scraperwiki.scrape(addr)
    pprint(html)
    return lxml.html.soupparser.fromstring(html)

def main():
    #mayor
    root = getroot(MAYOR_URL)
    mayor = {}
    mayor['source_url'] = MAYOR_URL
    mayor['elected_office'] = 'Mayor'
    mayor['name'] = root.xpath('//h1/text()')[0][6:] # strip "Mayor " prefix
    mayor['url'] = MAYOR_URL
    mayor['district_name'] = 'Ottawa'
    mayor['district_id'] = 0
    mayor['email'] = root.xpath('//a[contains(text(), "@")]/text()')[0].strip()
    mayor['boundary_url'] = '/boundaries/census-subdivisions/3506008/'
    further_details(mayor)
    save(mayor)

    # councillors
    root = getroot(COUNCIL_URL)

    for header in root.xpath('//h3'):
        councillor = {}
        link = header.xpath('a')[0]
        if link is not None:
            councillor['source_url'] = COUNCIL_URL
            councillor['elected_office'] = 'City councillor'
            councillor['name'] = link.text[11:] # cut off "Councillor" prefix
            councillor['url'] = urljoin(COUNCIL_URL, link.xpath('@href')[0])
            district = header.xpath('following-sibling::p[1]/a[1]/text()')[0]
            dist_info = re.search(r'(\d+)\W+(.+)', district).groups(0)
            councillor['district_id'] = dist_info[0]
            councillor['district_name'] = dist_info[1]
            mailto = header.xpath('following-sibling::p[1]/a[starts-with(@href, "mailto")]/@href')[0]
            councillor['email'] = mailto[7:] # cut off "mailto:" prefix
            further_details(councillor)
            save(councillor)

def further_details(councillor):
    resp = urllib2.urlopen(councillor['url'])
    councillor['url'] = resp.geturl() # use final redirect url
    root = lxml.html.soupparser.fromstring(resp.read())
    personal_url_list = root.xpath(
        '//strong/em[contains(string(), "Website")]/../following-sibling::a[1]/@href')
    if len(personal_url_list) > 0:
        councillor['personal_url'] = personal_url_list[0]
    
    photo_elem = root.xpath('//img[contains(@alt, "' + councillor['name'] + '")]/@src')
    councillor['photo_url'] = urljoin(COUNCIL_URL, photo_elem[0])

def save(rep):
    scraperwiki.sqlite.save(['district_id'], rep)

scraperwiki.sqlite.execute("DROP TABLE IF EXISTS swdata")
main()