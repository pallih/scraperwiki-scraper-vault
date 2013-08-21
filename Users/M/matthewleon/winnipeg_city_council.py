# Winnipeg city council scraper
# work in progress

import scraperwiki

import lxml.html.soupparser
import re

import urllib2
from urlparse import urljoin

COUNCIL_URL = 'http://winnipeg.ca/council/'


def getroot(addr):
    html = scraperwiki.scrape(addr)
    return lxml.html.soupparser.fromstring(html)

def main():
    root = getroot(COUNCIL_URL)
    for link in root.xpath('//table[2]//a/@href'):
        councillor_details(urljoin(COUNCIL_URL, link))

def councillor_details(url):
    root = getroot(url)
    councillor = {}
    councillor['url'] = url
    councillor['source_url'] = url
    councillor['elected_office'] = 'City councillor'
    councillor['name'] = root.xpath('//span[@class="bg90B"]/text()')
    councillor['district_id'] = 0
    save(councillor)

def mayor_details(url):
    pass

def save(rep):
    scraperwiki.sqlite.save(['district_id'], rep)

scraperwiki.sqlite.execute("DROP TABLE IF EXISTS swdata")
main()