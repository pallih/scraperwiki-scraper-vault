#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from urlparse import urljoin

import requests
import lxml.html

import scraperwiki.sqlite as db
from scraperwiki.geo import extract_gb_postcode, gb_postcode_to_latlng

URL = "http://publicaccess.preston.gov.uk/portal/servlets/ApplicationSearchServlet"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.162 Safari/535.19",}

INITIAL_DATA = {
    "ExistingRefNo": '', "FullAddress": '',
    "ReceivedDateFrom": '01/01/2011', "ReceivedDateTo": '16/04/2012',
    "Decision": '', "ApplicantAddressName": '',
    "AgentAddressName": '', "ValidDateFrom": '', "ValidDateTo": '',
    "DecisionDateFrom": '', "DecisionDateTo": '', "AppealRefNumber": '',
    "AppealLodgedDateFrom": '', "AppealLodgedDateTo": '',
    "AppealDecisionDateFrom": '',
    "AppealDecisionDateTo": '',
    }
STEP = 20
STOP_STRING = "Sorry, but your query did not return any results"
COLUMN_NAMES = ('ref_number',  'valid_date', 'site_location', 'proposed_development', 'decision')
DATE_FORMAT = '%d/%m/%Y'


class NoMoreResults(Exception):
    pass


def main():
    s = requests.Session(headers=HEADERS)
    process_page(s.post(URL, data=INITIAL_DATA).text)

    data = {'LAST_ROW_ID': STEP, 'DIRECTION': 'F', 'RECORDS': STEP, 'forward': 'Next+results'}
    while True:
        print 'Query: LAST_ROW_ID=%s ' % data['LAST_ROW_ID']
        text = s.post(URL, data=data).text
        process_page(text)
        data['LAST_ROW_ID'] += STEP


def process_page(text):
    if STOP_STRING in text:
        raise NoMoreResults('All done or bad query')

    doc = lxml.html.fromstring(text)
    entries = list(entries_from_doc(doc))
    db.save(['ref_number'], data=entries, verbose=0)


def entries_from_doc(doc):
    for row in doc.xpath('//div[@class="tablecontainer"]//tr'):
        columns  = [col.text_content().strip() for col in row.xpath('./td')]
        if not columns:
            continue
        entry = {name: value for name, value in zip(COLUMN_NAMES, columns)}
        try:
            entry['valid_date'] = datetime.strptime(entry['valid_date'], DATE_FORMAT)
        except ValueError:
            pass
        entry['details_url'] = urljoin(URL, row.xpath('.//a/@href')[0])
        postcode = extract_gb_postcode(entry['site_location'])
        if postcode:        
            entry['postcode'] = postcode
            #latlng = gb_postcode_to_latlng(postcode)
            #if latlng:            
            #    entry['lat'], entry['lng'] = latlng
        yield entry


def tests():
    pc = extract_gb_postcode('10 Romford Road Preston Lancashire')
    print pc, gb_postcode_to_latlng(pc)


##
## Main
##
try:
    #tests()    
    main()
except NoMoreResults as e:
    print e


