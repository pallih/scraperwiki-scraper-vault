# Scraper for Regina City Councilors with their respective wards

# Gathers the following data:
# ward_id, ward_name, Councillor name, elected_office, source_url, photo_url


# councilors listed at following url
# http://www.saskatoon.ca/CITY%20COUNCIL/Your%20Ward%20Councillors/Pages/default.aspx


import scraperwiki

import json
import lxml.html
import urlparse

import re
import pprint

BASE_URL = 'http://saskatoon.ca'
phone_re = re.compile(r"Phone:\s*(\d{3}-\d{3}-\d{4})")

# parses councilor urls
def parse_councilor(councilor_url):
    councilor_data = {}
    
    councilor_data['source_url'] = councilor_data['url'] = BASE_URL + councilor_url
    councilor_data['elected_office'] = "City councillor"
    
    html = scraperwiki.scrape(BASE_URL + councilor_url)
    root = lxml.html.fromstring(html)
    
    name_label = root.cssselect('#content h1')[0].text
    name_re = re.compile(r".+ - Councillor (.+)$")
    name_match = name_re.match(name_label)
    councilor_data['name'] = name_match.group(1)
    
    ward_label_re = re.compile(r"^Ward (\d+) (.+)$")
    
    ward_re = re.compile(r"^Ward (.+) - .+$")
    ward_match = ward_re.match(name_label)
    councilor_data['district_id'] = ward_match.group(1)
    councilor_data['district_name'] = "Ward " + str(ward_match.group(1))

    councilor_data['photo_url'] = BASE_URL + root.cssselect('#contentcontainer img[src]')[0].get('src', '')
    phone_search = phone_re.search(root.cssselect('#contentcontainer')[0].text_content())
    if (phone_search):
        councilor_data['offices'] = json.dumps([{"tel": phone_search.group(1)}])

    scraperwiki.sqlite.save(['district_id'], councilor_data)


# The main function. Grabs all councillor urls
def main():
    ward_urls = []
    councilor_urls = []
    mayor_url = ''
    
    list_url = 'http://regina.ca/residents/council-committees/meet-city-council/'

    html = scraperwiki.scrape(list_url)
    root = lxml.html.fromstring(html)

    mayor_name_re = re.compile(r"^Mayor (.+)$")
    mayor_a = root.cssselect('.sub_menu a[href*="-biography"]')[0]
    if mayor_a is not None:
        mayor_url = BASE_URL + mayor_a.get('href', '')
        mayor_name = mayor_name_re.match(mayor_a.text_content()).group(1)
        mayor_html = scraperwiki.scrape(mayor_url)
        mayor_root = lxml.html.fromstring(mayor_html)
        # @todo scrape data from http://regina.ca/residents/regina-mayor/contact_mayor/
        scraperwiki.sqlite.save(['district_id'], {
            'boundary_url':'/boundaries/census-subdivisions/4706027/', # Regina
            'district_id': 0,
            'elected_office': 'Mayor',
            'source_url': mayor_url,
            'url': mayor_url,
            'photo_url': BASE_URL + mayor_root.cssselect('#contentcontainer img[src]')[0].get('src', ''),
            'name': mayor_name,
        })

    all_links = root.cssselect('.sub_menu a')
    councilor_re = re.compile(r"^/residents/council-committees/meet-city-council/councill?or-.+/$")
    
    for link in all_links:
        url = link.attrib.get('href', '')
        if councilor_re.match(url):
            councilor_urls.append(url)

    for councilor_url in councilor_urls:
        parse_councilor(councilor_url)

main()

