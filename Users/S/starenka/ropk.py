#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, unicodedata
from pyquery import PyQuery as pq

import scraperwiki

URI_BASE = 'http://www.ropk.sk/index/index.php'
URI_FIRST = '%s?ids=553&p=0&status[3]=1&status[3]=1&orderBy=desc' % URI_BASE

re_trim = re.compile(r'[\n\r\t]')
base = pq(url='%s?ids=553&p=0&status[3]=1&status[3]=1&orderBy=desc' % URI_BASE)

pages = [URI_FIRST] + ['%s%s' % (URI_BASE, pq(page).attr('href')) for page in base.find('.strankovanie a')]

def remove_accents(input_str):
    nkfd_form = unicodedata.normalize('NFKD', unicode(input_str))
    only_ascii = nkfd_form.encode('ASCII', 'ignore')
    return only_ascii


data = []
for one in pages:
    doc = pq(url=one)
    for one in doc.find('.listItem-g'):
        one = pq(one)
        title = one.find('.listItem-nadpis a')
        i = {'title': title.text(), 'url': '%s%s' % (URI_BASE, title.attr('href')),
             'region': one.find('.listItem-oblast').text()}
        for date in one.find('.listItem-datumy').html().replace('&#13;', '').split('<br />'):
            d = re.sub(re_trim, '', date).split(': ')
            i[remove_accents(d[0])] = d[1]
        i['price'] = one.find('span.f12').text().split(':')[1].strip()
        scraperwiki.sqlite.save(unique_keys=["title"], data=i)#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, unicodedata
from pyquery import PyQuery as pq

import scraperwiki

URI_BASE = 'http://www.ropk.sk/index/index.php'
URI_FIRST = '%s?ids=553&p=0&status[3]=1&status[3]=1&orderBy=desc' % URI_BASE

re_trim = re.compile(r'[\n\r\t]')
base = pq(url='%s?ids=553&p=0&status[3]=1&status[3]=1&orderBy=desc' % URI_BASE)

pages = [URI_FIRST] + ['%s%s' % (URI_BASE, pq(page).attr('href')) for page in base.find('.strankovanie a')]

def remove_accents(input_str):
    nkfd_form = unicodedata.normalize('NFKD', unicode(input_str))
    only_ascii = nkfd_form.encode('ASCII', 'ignore')
    return only_ascii


data = []
for one in pages:
    doc = pq(url=one)
    for one in doc.find('.listItem-g'):
        one = pq(one)
        title = one.find('.listItem-nadpis a')
        i = {'title': title.text(), 'url': '%s%s' % (URI_BASE, title.attr('href')),
             'region': one.find('.listItem-oblast').text()}
        for date in one.find('.listItem-datumy').html().replace('&#13;', '').split('<br />'):
            d = re.sub(re_trim, '', date).split(': ')
            i[remove_accents(d[0])] = d[1]
        i['price'] = one.find('span.f12').text().split(':')[1].strip()
        scraperwiki.sqlite.save(unique_keys=["title"], data=i)