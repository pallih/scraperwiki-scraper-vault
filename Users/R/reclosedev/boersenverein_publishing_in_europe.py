#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import urlparse
from pprint import pprint

import requests
from requests import async
import lxml.html

import scraperwiki
import scraperwiki.sqlite as db


SKIP_STEP = 10
MAX_REQUESTS = 5
ASYNC = False

#CURRENT_FILTER = 'zwhaendler'
#CURRENT_FILTER = 'verlag'
CURRENT_FILTER = 'haendler'

START_URL = 'http://www.boersenverein.de/de/portal/Mitgliedersuche/158377?suchstring=&plz=&lv=&filter=%s' % CURRENT_FILTER



def scrape(start_url, first_skip=0, last_skip=None):
    if last_skip is None:
        doc = prepare_doc(requests.get('%s&skip=%s' % (start_url, first_skip)).text)
        page_last = doc.xpath('//a[@class="page-last"]/@href')[0]
        last_skip = int(urlparse.parse_qs(page_last)['skip'][0]) + SKIP_STEP  # last page is not really last, is it site bug?


    def process_response(response):
        print response.url
        doc = prepare_doc(response.text)
        gather_items_from(doc)
        db.save_var(response.url, 1, verbose=0)

    def gen_urls():
        for skip in xrange(first_skip, last_skip + SKIP_STEP, SKIP_STEP):
            url = '%s&skip=%s' % (start_url, skip)
            if not db.get_var(url, 0, verbose=0):
                yield url

    if ASYNC:
        # TODO There is some database problems with async mode
        rs = [async.get(url, hooks=dict(response=process_response))
              for url in gen_urls()]
        async.map(rs, size=MAX_REQUESTS)
    else:
        for url in gen_urls():
            process_response(requests.get(url))
        

def prepare_doc(content):
    content = content.replace('<br />', '\n')  # address contains <br />, simpliest way to handle it - replace it with \n
    return lxml.html.fromstring(content)


def gather_items_from(doc):
    entries = [] # speedup by saving all entries in one call    
    names = doc.xpath('//h2[@class="lnb"]')
    for el in names:
        entry = {'name': el.text_content(), 'filter': CURRENT_FILTER}
        el = el.getnext()
        info = []
        while el is not None:
            if el.tag == 'h2':
                break
            info.append(el.text_content())
            el = el.getnext()
        entry['type'] = info[0]
        entry['address'] = info[1]
        if len(info) == 3:
            entry['url'] = info[2]
        entries.append(entry)  
    db.save(['name', 'address', 'filter'], data=entries, verbose=0)


scrape(START_URL, last_skip=6750)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import urlparse
from pprint import pprint

import requests
from requests import async
import lxml.html

import scraperwiki
import scraperwiki.sqlite as db


SKIP_STEP = 10
MAX_REQUESTS = 5
ASYNC = False

#CURRENT_FILTER = 'zwhaendler'
#CURRENT_FILTER = 'verlag'
CURRENT_FILTER = 'haendler'

START_URL = 'http://www.boersenverein.de/de/portal/Mitgliedersuche/158377?suchstring=&plz=&lv=&filter=%s' % CURRENT_FILTER



def scrape(start_url, first_skip=0, last_skip=None):
    if last_skip is None:
        doc = prepare_doc(requests.get('%s&skip=%s' % (start_url, first_skip)).text)
        page_last = doc.xpath('//a[@class="page-last"]/@href')[0]
        last_skip = int(urlparse.parse_qs(page_last)['skip'][0]) + SKIP_STEP  # last page is not really last, is it site bug?


    def process_response(response):
        print response.url
        doc = prepare_doc(response.text)
        gather_items_from(doc)
        db.save_var(response.url, 1, verbose=0)

    def gen_urls():
        for skip in xrange(first_skip, last_skip + SKIP_STEP, SKIP_STEP):
            url = '%s&skip=%s' % (start_url, skip)
            if not db.get_var(url, 0, verbose=0):
                yield url

    if ASYNC:
        # TODO There is some database problems with async mode
        rs = [async.get(url, hooks=dict(response=process_response))
              for url in gen_urls()]
        async.map(rs, size=MAX_REQUESTS)
    else:
        for url in gen_urls():
            process_response(requests.get(url))
        

def prepare_doc(content):
    content = content.replace('<br />', '\n')  # address contains <br />, simpliest way to handle it - replace it with \n
    return lxml.html.fromstring(content)


def gather_items_from(doc):
    entries = [] # speedup by saving all entries in one call    
    names = doc.xpath('//h2[@class="lnb"]')
    for el in names:
        entry = {'name': el.text_content(), 'filter': CURRENT_FILTER}
        el = el.getnext()
        info = []
        while el is not None:
            if el.tag == 'h2':
                break
            info.append(el.text_content())
            el = el.getnext()
        entry['type'] = info[0]
        entry['address'] = info[1]
        if len(info) == 3:
            entry['url'] = info[2]
        entries.append(entry)  
    db.save(['name', 'address', 'filter'], data=entries, verbose=0)


scrape(START_URL, last_skip=6750)

