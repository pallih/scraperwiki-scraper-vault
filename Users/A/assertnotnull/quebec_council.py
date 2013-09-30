# Scraper for Charlottetown, PEI city council

import scraperwiki

import lxml.html.soupparser
import re

from urlparse import urljoin

COUNCIL_URL = 'http://www.ville.quebec.qc.ca/apropos/vie_democratique/elus/conseil_municipal/membres.aspx'
BASE_URL = COUNCIL_URL[0:COUNCIL_URL.find('/',8)]

def parsedetails(node):
    details = list()
    for string in node.xpath('text()'):
        if (len(string.strip()) is not 0):
            details.append(string)
    return details

def main():
    html = scraperwiki.scrape(COUNCIL_URL)
    root = lxml.html.soupparser.fromstring(html)
    everyone = root.xpath('//div[starts-with(@class,"ligne")]')
    allthesection = root.xpath('//div[@id="texte"]')

    mayornode = everyone[0]
    #print lxml.html.tostring(mayornode)
    mayor = {}
    mayor['url'] = COUNCIL_URL
    mayor['source_url'] = COUNCIL_URL
    mayor['elected_office'] = 'Mayor'
    mayor['district_name'] = 'Québec'
    mayor['district_id'] = 0
    mayor['name'] = ' '.join(mayornode.xpath('h3//text()'))
    mayor['photo_url'] = ''.join([BASE_URL, mayornode.xpath('p[@class="ph_elus"]//img/@src')[0]])
    details = parsedetails(mayornode)
    mayor['boundary_url'] = '/boundaries/census-subdivisions/2423027/'
    
    save(mayor)

    for span in root.xpath('//div[starts-with(@class,"ligne")]')[1:]:
        councillor = {}
        councillor['source_url'] = COUNCIL_URL
        councillor['elected_office'] = 'Councillor'
        councillor['name'] = ' '.join(span.xpath('h3//text()'))
        councillor['district_name'] = re.sub(r'District électoral( de)?', '', span.xpath('a//text()')[0])
        district_pdf_url = span.xpath('a')[0].get('href')
        councillor['district_id'] = district_pdf_url[district_pdf_url.find('_')+1:district_pdf_url.find('.')-1]
        councillor['photo_url'] = ''.join([BASE_URL, span.xpath('p[@class="ph_elus"]//img/@src')[0]])
                
        save(councillor)

def save(rep):
    scraperwiki.sqlite.save(['district_id'], rep)

scraperwiki.sqlite.execute("DELETE FROM swdata")
main()
# Scraper for Charlottetown, PEI city council

import scraperwiki

import lxml.html.soupparser
import re

from urlparse import urljoin

COUNCIL_URL = 'http://www.ville.quebec.qc.ca/apropos/vie_democratique/elus/conseil_municipal/membres.aspx'
BASE_URL = COUNCIL_URL[0:COUNCIL_URL.find('/',8)]

def parsedetails(node):
    details = list()
    for string in node.xpath('text()'):
        if (len(string.strip()) is not 0):
            details.append(string)
    return details

def main():
    html = scraperwiki.scrape(COUNCIL_URL)
    root = lxml.html.soupparser.fromstring(html)
    everyone = root.xpath('//div[starts-with(@class,"ligne")]')
    allthesection = root.xpath('//div[@id="texte"]')

    mayornode = everyone[0]
    #print lxml.html.tostring(mayornode)
    mayor = {}
    mayor['url'] = COUNCIL_URL
    mayor['source_url'] = COUNCIL_URL
    mayor['elected_office'] = 'Mayor'
    mayor['district_name'] = 'Québec'
    mayor['district_id'] = 0
    mayor['name'] = ' '.join(mayornode.xpath('h3//text()'))
    mayor['photo_url'] = ''.join([BASE_URL, mayornode.xpath('p[@class="ph_elus"]//img/@src')[0]])
    details = parsedetails(mayornode)
    mayor['boundary_url'] = '/boundaries/census-subdivisions/2423027/'
    
    save(mayor)

    for span in root.xpath('//div[starts-with(@class,"ligne")]')[1:]:
        councillor = {}
        councillor['source_url'] = COUNCIL_URL
        councillor['elected_office'] = 'Councillor'
        councillor['name'] = ' '.join(span.xpath('h3//text()'))
        councillor['district_name'] = re.sub(r'District électoral( de)?', '', span.xpath('a//text()')[0])
        district_pdf_url = span.xpath('a')[0].get('href')
        councillor['district_id'] = district_pdf_url[district_pdf_url.find('_')+1:district_pdf_url.find('.')-1]
        councillor['photo_url'] = ''.join([BASE_URL, span.xpath('p[@class="ph_elus"]//img/@src')[0]])
                
        save(councillor)

def save(rep):
    scraperwiki.sqlite.save(['district_id'], rep)

scraperwiki.sqlite.execute("DELETE FROM swdata")
main()
