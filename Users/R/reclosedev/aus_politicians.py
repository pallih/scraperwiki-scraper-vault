#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Request: https://groups.google.com/d/topic/scraperwiki/tCMJ_79nXZA/discussion
import functools
import re
from pprint import pprint
from urlparse import urljoin
from collections import deque

import requests
from requests import async
import lxml.html

import scraperwiki.sqlite as db

print requests.__version__
PER_PAGE = 25
URLS = [
'http://www.aph.gov.au/Senators_and_Members/Parliamentarian_Search_Results?q=&mem=1&par=-1&gen=0&ps=%s' % PER_PAGE,
'http://www.aph.gov.au/Senators_and_Members/Parliamentarian_Search_Results?q=&sen=1&par=-1&gen=0&ps=%s' % PER_PAGE,
]
BASE = 'http://www.aph.gov.au/Senators_and_Members/'

def main():
    for url in URLS:
        process_one_query(url)

def process_one_query(base_url):
    s = requests.Session()
    text = s.get(base_url).content
    doc = lxml.html.fromstring(text)
    last_button = doc.cssselect('li.button.last a')
    if last_button:
        last = int(re.search(r'page=(\d)', last_button[0].get('href')).group(1))
    else:
        last = 1

    process_doc(doc)
    for page in range(2, last + 1):
        url = base_url+ '&page=%s' % page
        text = s.get(url).content
        process_doc(lxml.html.fromstring(text))
        print '** Done with %s' % page


def process_doc(doc):
    entries = list(iter_senators_info(doc))

    reqs = (async.get(urljoin(BASE, entry['profile']),
                      hooks={'response': functools.partial(add_info_from_details_page, entry)})
            for entry in entries)
    
    async.map(reqs, size=5)
    db.save(['profile'], entries, verbose=0)


def iter_senators_info(doc):
    for li in doc.xpath('//ul[contains(@class, "search-filter-results")]//li'):
        entry = {'name': li.xpath('./p[@class="title"]')[0].text_content(),
                 'profile': li.xpath('./p[@class="title"]/a/@href')[0]}

        for dt, dd in zip(li.xpath('./dl/dt'), li.xpath('./dl/dd[not(a)]')):
            entry[norm_key(dt.text_content())] = dd.text_content()
        
        entry.update(parse_links(li))
        yield entry


def parse_links(li):
    links = li.xpath('./dl/dd/a')
    result = {}
    for typ in ('mail', 'facebook', 'twitter', 'contact'):
        for link in links:
            if typ in link.get('class', ''):
                result[typ] = link.get('href')
    return result


def add_info_from_details_page(entry, response):
    print entry['name']
    doc = lxml.html.fromstring(response.content)
    for a in doc.xpath('//div[contains(@class, "col-third col-last")]/dl/dd/a'):
        text, href = norm_key(a.text_content()), a.get('href')
        if 'mailto' in href or any(word in text for word in ('twitter', 'facebook', 'contact')):
            continue
        if 'personal_website' in text:
            entry[text] = href
        else:
            if 'other_sites' in entry:
                entry['other_sites'] += ' | ' + href
            else:
                entry['other_sites'] = href


def norm_key(s):
    k = s.replace('(s)', '').lower()
    return re.sub(r'\W', '_', k)


if __name__ in ('scraper', 'main'):
    main()


#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Request: https://groups.google.com/d/topic/scraperwiki/tCMJ_79nXZA/discussion
import functools
import re
from pprint import pprint
from urlparse import urljoin
from collections import deque

import requests
from requests import async
import lxml.html

import scraperwiki.sqlite as db

print requests.__version__
PER_PAGE = 25
URLS = [
'http://www.aph.gov.au/Senators_and_Members/Parliamentarian_Search_Results?q=&mem=1&par=-1&gen=0&ps=%s' % PER_PAGE,
'http://www.aph.gov.au/Senators_and_Members/Parliamentarian_Search_Results?q=&sen=1&par=-1&gen=0&ps=%s' % PER_PAGE,
]
BASE = 'http://www.aph.gov.au/Senators_and_Members/'

def main():
    for url in URLS:
        process_one_query(url)

def process_one_query(base_url):
    s = requests.Session()
    text = s.get(base_url).content
    doc = lxml.html.fromstring(text)
    last_button = doc.cssselect('li.button.last a')
    if last_button:
        last = int(re.search(r'page=(\d)', last_button[0].get('href')).group(1))
    else:
        last = 1

    process_doc(doc)
    for page in range(2, last + 1):
        url = base_url+ '&page=%s' % page
        text = s.get(url).content
        process_doc(lxml.html.fromstring(text))
        print '** Done with %s' % page


def process_doc(doc):
    entries = list(iter_senators_info(doc))

    reqs = (async.get(urljoin(BASE, entry['profile']),
                      hooks={'response': functools.partial(add_info_from_details_page, entry)})
            for entry in entries)
    
    async.map(reqs, size=5)
    db.save(['profile'], entries, verbose=0)


def iter_senators_info(doc):
    for li in doc.xpath('//ul[contains(@class, "search-filter-results")]//li'):
        entry = {'name': li.xpath('./p[@class="title"]')[0].text_content(),
                 'profile': li.xpath('./p[@class="title"]/a/@href')[0]}

        for dt, dd in zip(li.xpath('./dl/dt'), li.xpath('./dl/dd[not(a)]')):
            entry[norm_key(dt.text_content())] = dd.text_content()
        
        entry.update(parse_links(li))
        yield entry


def parse_links(li):
    links = li.xpath('./dl/dd/a')
    result = {}
    for typ in ('mail', 'facebook', 'twitter', 'contact'):
        for link in links:
            if typ in link.get('class', ''):
                result[typ] = link.get('href')
    return result


def add_info_from_details_page(entry, response):
    print entry['name']
    doc = lxml.html.fromstring(response.content)
    for a in doc.xpath('//div[contains(@class, "col-third col-last")]/dl/dd/a'):
        text, href = norm_key(a.text_content()), a.get('href')
        if 'mailto' in href or any(word in text for word in ('twitter', 'facebook', 'contact')):
            continue
        if 'personal_website' in text:
            entry[text] = href
        else:
            if 'other_sites' in entry:
                entry['other_sites'] += ' | ' + href
            else:
                entry['other_sites'] = href


def norm_key(s):
    k = s.replace('(s)', '').lower()
    return re.sub(r'\W', '_', k)


if __name__ in ('scraper', 'main'):
    main()


