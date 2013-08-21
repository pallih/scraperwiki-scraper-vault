#Scraper for London, ON city council

import scraperwiki

import lxml.html.soupparser
import re

import urllib2
from urlparse import urljoin

MAYOR_URL = 'http://www.london.ca/d.aspx?s=/Mayors_Office/team.htm'
COUNCIL_URL = 'http://www.london.ca/d.aspx?s=/City_Council/ccm_councillors_ward.htm'

def getroot(addr):
    html = scraperwiki.scrape(addr)
    return lxml.html.soupparser.fromstring(html)

def main():
    mayor_details(MAYOR_URL)
    root = getroot(COUNCIL_URL)
    for url in root.xpath('//table[@id="table1"]//a/@href'):
        councillor_details(urljoin(COUNCIL_URL, url))
        
def councillor_details(url):
    root = getroot(url)
    councillor = {}
    councillor['url'] = url
    councillor['source_url'] = url
    councillor['elected_office'] = 'Councillor'
    header = re.search(r'(Ward \d+).+- (.+)', root.xpath('//h1[1]/text()')[0])
    councillor['name'] = header.group(2)
    councillor['district_name'] = header.group(1)
    councillor['district_id'] = re.search(r'\d+', header.group(1)).group(0)
    raw_email = root.xpath('//table//script/text()')
    if len(raw_email) > 0:
        councillor['email'] = process_email(raw_email[0])
    photo = root.xpath('//img[contains(@alt, "Councillor")]/@src')
    councillor['photo_url'] = urljoin(url, photo[0])
    save(councillor)

def mayor_details(url):
    root = getroot(url)
    mayor = {}
    mayor['url'] = url
    mayor['source_url'] = url
    mayor['elected_office'] = 'Mayor'
    mayor['district_name'] = 'London'
    mayor['district_id'] = 0
    header = root.xpath('//h1[1]/text()')[0]
    mayor['name'] = re.search('Mayor (.+)', header).group(1).strip()
    mayor['email'] = process_email(root.xpath('//table//script/text()')[0])

    #get photo
    url = 'http://www.london.ca/d.aspx?s=/Mayors_Office/default.htm'
    root = getroot(url)
    photo = root.xpath('//img[contains(@alt, "Mayor")]/@src')
    mayor['photo_url'] = urljoin(url, photo[0])
    mayor['boundary_url'] = '/boundaries/census-subdivisions/3539036/'
    save(mayor)

def process_email(jselem):
    emailelems = re.findall('[\'"](.+?)[\'"]', jselem)
    return '%s@%s.%s' % tuple(emailelems[:3])

def save(rep):
    scraperwiki.sqlite.save(['district_id'], rep)

if scraperwiki.sqlite.select('name FROM sqlite_master WHERE type="table" AND name="swdata"'):
    scraperwiki.sqlite.execute('DROP TABLE `swdata`')
main()
