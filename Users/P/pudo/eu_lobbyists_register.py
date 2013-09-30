from lxml import html
from urlparse import urljoin
from urllib import urlencode
from urllib2 import urlopen, Request
from itertools import count
from cookielib import CookieJar
from pprint import pprint
from datetime import datetime

import scraperwiki

URL_SEARCH = 'http://ec.europa.eu/transparencyregister/public/consultation/search.do'
URL = 'http://ec.europa.eu/transparencyregister/public/consultation/search.do?country=%s&d-4959990-p=%s'

BOXES = {
        'Interest representation activities': {
            'representation activities performed by the organisation': 'lobbying_activties'
            },
        'Financial data': {
            'Financial year': 'financial_year',
            'Estimated costs to the organisation directly': 'lobbying_expenditure',
            'Other (financial) information provided': 'extra_financial_info'
            },
        'Networking': {
            '(i) organisation\'s membership of': 'networking'
            },
        'Activities': {
            'Main EU initiatives covered the year bef': 'activities'
            },
        'Registrant : Organisation or self-employed individual': {},
        'Sections': {
            'Section': 'lobbying_section',
            'and more precisely': 'lobbying_subsection'
            },
        'Person with legal responsibility': {},
        'Permanent person in charge of EU relations': {
            'Person with legal responsibility for the organisation': 'lobbyists_contact_name',
            'Position': 'lobbyists_contact_position'
            },
        'Number of persons engaged in activities falling under the scope of the Transparency Register': {
            'Number of persons': 'num_lobbyists',
            'Complementary information': 'num_lobbyists_extra'
            },
        'Persons accredited for access to European Parliament premises': {},
        'Structure': {
            'Total number of members that are natural persons': 'num_natural_members',
            'Number of member organisations': 'num_org_members',
            'Member organisations': 'org_members',
            'The organisation has members/is represented': 'countries',
            },
        'Fields of interest for e-mail alerts on consultations': {
            'Fields declared by the organisation': 'fields_of_interest'
            },
        'Goals / remit': {
            'Goals / remit of the organisation': 'goals',
            'The organisation\'s fields of interests are': 'area_of_interest'
            },
        'Contact details:': {
            'Contact details of organisation\'s head office': 'head_office_address',
            'Telephone number': 'telephone',
            'Other contact information': 'fax_number'
            },
        'Head of the organisation': {
            'Person legally responsible for the organisation': 'chief_contact_name',
            'Position': 'chief_contact_position'
            },
        'Category of activities': {
            'Category of activity': 'lobbying_section',
            'and more precisely': 'lobbying_subsection'
            },
        'Interest representative': {
            'Name/company name': 'rep_name',
            'Acronym': 'acronym',
            'Legal status': 'legal_status',
            'Website address': 'website'
            }
        }


def get_country_index():
    for country in range(1,999):
        jar = CookieJar()
        req = Request(URL_SEARCH, urlencode({'country': country}))
        res = urlopen(req)
        jar.extract_cookies(res, req)
        for page in count(1):
            req = Request(URL % (country, page))
            jar.add_cookie_header(req)
            doc = html.parse(urlopen(req))
            anchors = list(doc.findall('//table[@id="searchResultsTable"]/tbody//a'))
            for a in anchors:
                get_entry(urljoin(URL, a.get('href')))
            if doc.find('//span[@class="pagelinks"]/a/img[@alt="Next"]') is None:
                break

def get_entry(url):
    doc = html.parse(url)
    entry = {}
    profile = doc.find('//div[@class="box"]')
    entry['name'] = profile.findtext('.//h4/b').strip()
    id, _, registration_date, _, update_date = list(profile.findall('.//span'))
    entry['id'] = id.text.strip()
    entry['register_url'] = url
    entry['retrieved_at'] = datetime.now().isoformat()
    entry['registration_date'] = registration_date.text.strip()
    entry['update_date'] = update_date.text.strip()

    for box in doc.findall('//table//div[@class="box"]'):
        section = box.findtext('h3').strip()
        aliases = BOXES.get(section, {})
        if section not in BOXES:
            print "ALIASES", section
        for tr in box.findall('./table/tbody/tr'):
            tds = tr.findall('td')
            if len(tds) < 2:
                continue
            label = tds[0].text.strip()
            if tds[1].find('ul') is not None:
                value = [l.xpath('string()').strip() for l in tds[1].findall('.//li')]
                value = ";".join(value)
            else:
                value = tds[1].xpath('string()').strip()
            for k, v in aliases.items():
                if k in label:
                    entry[v] = value
    pprint(entry)
    scraperwiki.sqlite.save(unique_keys=["id"], data=entry)


get_country_index()




from lxml import html
from urlparse import urljoin
from urllib import urlencode
from urllib2 import urlopen, Request
from itertools import count
from cookielib import CookieJar
from pprint import pprint
from datetime import datetime

import scraperwiki

URL_SEARCH = 'http://ec.europa.eu/transparencyregister/public/consultation/search.do'
URL = 'http://ec.europa.eu/transparencyregister/public/consultation/search.do?country=%s&d-4959990-p=%s'

BOXES = {
        'Interest representation activities': {
            'representation activities performed by the organisation': 'lobbying_activties'
            },
        'Financial data': {
            'Financial year': 'financial_year',
            'Estimated costs to the organisation directly': 'lobbying_expenditure',
            'Other (financial) information provided': 'extra_financial_info'
            },
        'Networking': {
            '(i) organisation\'s membership of': 'networking'
            },
        'Activities': {
            'Main EU initiatives covered the year bef': 'activities'
            },
        'Registrant : Organisation or self-employed individual': {},
        'Sections': {
            'Section': 'lobbying_section',
            'and more precisely': 'lobbying_subsection'
            },
        'Person with legal responsibility': {},
        'Permanent person in charge of EU relations': {
            'Person with legal responsibility for the organisation': 'lobbyists_contact_name',
            'Position': 'lobbyists_contact_position'
            },
        'Number of persons engaged in activities falling under the scope of the Transparency Register': {
            'Number of persons': 'num_lobbyists',
            'Complementary information': 'num_lobbyists_extra'
            },
        'Persons accredited for access to European Parliament premises': {},
        'Structure': {
            'Total number of members that are natural persons': 'num_natural_members',
            'Number of member organisations': 'num_org_members',
            'Member organisations': 'org_members',
            'The organisation has members/is represented': 'countries',
            },
        'Fields of interest for e-mail alerts on consultations': {
            'Fields declared by the organisation': 'fields_of_interest'
            },
        'Goals / remit': {
            'Goals / remit of the organisation': 'goals',
            'The organisation\'s fields of interests are': 'area_of_interest'
            },
        'Contact details:': {
            'Contact details of organisation\'s head office': 'head_office_address',
            'Telephone number': 'telephone',
            'Other contact information': 'fax_number'
            },
        'Head of the organisation': {
            'Person legally responsible for the organisation': 'chief_contact_name',
            'Position': 'chief_contact_position'
            },
        'Category of activities': {
            'Category of activity': 'lobbying_section',
            'and more precisely': 'lobbying_subsection'
            },
        'Interest representative': {
            'Name/company name': 'rep_name',
            'Acronym': 'acronym',
            'Legal status': 'legal_status',
            'Website address': 'website'
            }
        }


def get_country_index():
    for country in range(1,999):
        jar = CookieJar()
        req = Request(URL_SEARCH, urlencode({'country': country}))
        res = urlopen(req)
        jar.extract_cookies(res, req)
        for page in count(1):
            req = Request(URL % (country, page))
            jar.add_cookie_header(req)
            doc = html.parse(urlopen(req))
            anchors = list(doc.findall('//table[@id="searchResultsTable"]/tbody//a'))
            for a in anchors:
                get_entry(urljoin(URL, a.get('href')))
            if doc.find('//span[@class="pagelinks"]/a/img[@alt="Next"]') is None:
                break

def get_entry(url):
    doc = html.parse(url)
    entry = {}
    profile = doc.find('//div[@class="box"]')
    entry['name'] = profile.findtext('.//h4/b').strip()
    id, _, registration_date, _, update_date = list(profile.findall('.//span'))
    entry['id'] = id.text.strip()
    entry['register_url'] = url
    entry['retrieved_at'] = datetime.now().isoformat()
    entry['registration_date'] = registration_date.text.strip()
    entry['update_date'] = update_date.text.strip()

    for box in doc.findall('//table//div[@class="box"]'):
        section = box.findtext('h3').strip()
        aliases = BOXES.get(section, {})
        if section not in BOXES:
            print "ALIASES", section
        for tr in box.findall('./table/tbody/tr'):
            tds = tr.findall('td')
            if len(tds) < 2:
                continue
            label = tds[0].text.strip()
            if tds[1].find('ul') is not None:
                value = [l.xpath('string()').strip() for l in tds[1].findall('.//li')]
                value = ";".join(value)
            else:
                value = tds[1].xpath('string()').strip()
            for k, v in aliases.items():
                if k in label:
                    entry[v] = value
    pprint(entry)
    scraperwiki.sqlite.save(unique_keys=["id"], data=entry)


get_country_index()




