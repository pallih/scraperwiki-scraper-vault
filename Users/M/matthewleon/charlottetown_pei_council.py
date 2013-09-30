# Scraper for Charlottetown, PEI city council

import scraperwiki

import lxml.html.soupparser
import re

from urlparse import urljoin

COUNCIL_URL = 'http://www.city.charlottetown.pe.ca/mayorandcouncil.php'

def main():
    html = scraperwiki.scrape(COUNCIL_URL)
    root = lxml.html.soupparser.fromstring(html)
    everyone = root.xpath('//span[@class="Title"]')
    mayornode = everyone[0]
    mayor = {}
    mayor['source_url'] = COUNCIL_URL
    mayor['elected_office'] = 'Mayor'
    mayor['district_name'] = 'Charlottetown'
    mayor['district_id'] = 0
    spantext = ' '.join(mayornode.xpath('.//text()'))
    mayor['name'] = re.search(r'[^(]+', spantext).group(0).strip()
    mayor['photo_url'] = urljoin(COUNCIL_URL, mayornode.xpath('img/@src')[0])
    mayor['email'] = mayornode.xpath('following::a[1]/text()')[0]
    mayor['boundary_url'] = '/boundaries/census-subdivisions/1102075/'
    save(mayor)

    for span in root.xpath('//span[@class="Title"]')[1:]:
        councillor = {}
        councillor['source_url'] = COUNCIL_URL
        councillor['elected_office'] = 'Councillor'
        spantext = ' '.join(span.xpath('.//text()'))
        header = spantext.replace(u'\u2013', '-').split('-')
        if len(header) != 2:
            continue

        name = header[0].strip()
        name = name.replace('Councillor', '')
        name = re.sub(r'\(.+?\)', '', name)
        name = ' '.join(name.split())
        councillor['name'] = name

        councillor['district_name'] = header[1].strip()
        councillor['district_id'] = header[1].split()[1].strip()

        # needed a wacky xpath to deal with ward 8
        photo = span.xpath('preceding::hr[1]/following::img[1]/@src')
        councillor['photo_url'] = urljoin(COUNCIL_URL, photo[0])

#        bodytext = span.xpath('following::*[@class="bodytext"][1]')[0]
        email = span.xpath('following::a[1]/text()')
        if email:
            councillor['email'] = email[0]
        
        save(councillor)

def save(rep):
    scraperwiki.sqlite.save(['district_id'], rep)

if scraperwiki.sqlite.select('name FROM sqlite_master WHERE type="table" AND name="swdata"'):
    scraperwiki.sqlite.execute('DROP TABLE `swdata`')
main()
# Scraper for Charlottetown, PEI city council

import scraperwiki

import lxml.html.soupparser
import re

from urlparse import urljoin

COUNCIL_URL = 'http://www.city.charlottetown.pe.ca/mayorandcouncil.php'

def main():
    html = scraperwiki.scrape(COUNCIL_URL)
    root = lxml.html.soupparser.fromstring(html)
    everyone = root.xpath('//span[@class="Title"]')
    mayornode = everyone[0]
    mayor = {}
    mayor['source_url'] = COUNCIL_URL
    mayor['elected_office'] = 'Mayor'
    mayor['district_name'] = 'Charlottetown'
    mayor['district_id'] = 0
    spantext = ' '.join(mayornode.xpath('.//text()'))
    mayor['name'] = re.search(r'[^(]+', spantext).group(0).strip()
    mayor['photo_url'] = urljoin(COUNCIL_URL, mayornode.xpath('img/@src')[0])
    mayor['email'] = mayornode.xpath('following::a[1]/text()')[0]
    mayor['boundary_url'] = '/boundaries/census-subdivisions/1102075/'
    save(mayor)

    for span in root.xpath('//span[@class="Title"]')[1:]:
        councillor = {}
        councillor['source_url'] = COUNCIL_URL
        councillor['elected_office'] = 'Councillor'
        spantext = ' '.join(span.xpath('.//text()'))
        header = spantext.replace(u'\u2013', '-').split('-')
        if len(header) != 2:
            continue

        name = header[0].strip()
        name = name.replace('Councillor', '')
        name = re.sub(r'\(.+?\)', '', name)
        name = ' '.join(name.split())
        councillor['name'] = name

        councillor['district_name'] = header[1].strip()
        councillor['district_id'] = header[1].split()[1].strip()

        # needed a wacky xpath to deal with ward 8
        photo = span.xpath('preceding::hr[1]/following::img[1]/@src')
        councillor['photo_url'] = urljoin(COUNCIL_URL, photo[0])

#        bodytext = span.xpath('following::*[@class="bodytext"][1]')[0]
        email = span.xpath('following::a[1]/text()')
        if email:
            councillor['email'] = email[0]
        
        save(councillor)

def save(rep):
    scraperwiki.sqlite.save(['district_id'], rep)

if scraperwiki.sqlite.select('name FROM sqlite_master WHERE type="table" AND name="swdata"'):
    scraperwiki.sqlite.execute('DROP TABLE `swdata`')
main()
