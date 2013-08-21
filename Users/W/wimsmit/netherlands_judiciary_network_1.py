# -*- coding=utf8 -*-

import string
import scraperwiki
import requests
import lxml.html
from lxml.cssselect import CSSSelector

search_url = 'http://namenlijst.rechtspraak.nl/Default.aspx'
results_url = 'http://namenlijst.rechtspraak.nl/ResultPage.aspx'

functions = [
    #"Coördinerend vice-president",
    #"Coördinerend vice-president senior",
    #"Deskundig lid",
    #"Directeur",
    #"Gerechtsauditeur",
    #"Griffier",
    #"Militair kantonrechter",
    #"Militair lid",
    #"Plaatsvervangend procureur-generaal",
    #"President",
    #"Procureur-generaal",
    #"Raadsheer",
    #"Raadsheer in buitengewone dienst",
    #"Raadsheer-plaatsvervanger",
    #"Rechter",
    #"Rechter-plaatsvervanger",
    #"Sectorvoorzitter",
    #"Senior-gerechtsauditeur",
    #"Substituut-griffier",
    "Vice-president",
    "senior rechter A",
    "Voorzitter van het bestuur",
    "rechtelijk ambtenaar in opleiding",
    "senior gerechtsauditeur",
    "senior raadsheer",
    "senior rechter",
]

save = scraperwiki.sqlite.save
parse = lxml.html.fromstring
POST = requests.post
GET = requests.get
result_selector = CSSSelector('tr.result')


SCHEMA = ['name', 'role', 'entity']
UNIQUE_KEYS = SCHEMA

def search(id, function, filter1=None, filter2=None):
    payload = {
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '_ctl0:ContentPlaceHolder1:chklInstances:' + id: 'on',
        '_ctl0:ContentPlaceHolder1:btnSearch': 'Search',
        '_ctl0:ContentPlaceHolder1:ddlFunctions': function,
    }
    if filter1:
        payload['_ctl0:ContentPlaceHolder1:chklCourtsOfAppeal:' + filter1] = 'on'
    if filter2:
        payload['_ctl0:ContentPlaceHolder1:chklCourts:' + filter2] = 'on'
    #for letter in string.ascii_uppercase:
    payload['_ctl0:ContentPlaceHolder1:txtSearchKenmerken'] = '*'
    session = requests.session()
    url = search_url
    while True:
        response = session.post(url, data=payload)
        print response.status_code
        html = parse(response.content)
        for tr in result_selector(html):
            row = [None] * 3
            for i, td in enumerate(tr):
                if i:
                    row[i] = td.text_content().strip()
                else:
                    link = td[0]
                    #row[0] = link.get('id')
                    row[0] = link.text.strip()
            yield row
        next = html.get_element_by_id('_ctl0_ContentPlaceHolder1_lbNext', None)
        if next is None:
            break
        print 'next'
        payload.clear()
        payload = {
            '__EVENTTARGET': '_ctl0$ContentPlaceHolder1$lbNext',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': html.get_element_by_id('__VIEWSTATE', '').get('value'),
        }
        print payload
        url = results_url


def store(row):
    save(
        unique_keys=UNIQUE_KEYS,
        data=dict(zip(SCHEMA, row))
    )
    
for function in functions:
    for id in '12345':
        if id == '4':
            for filter in '12345':
                for result in search(id, function, filter1=filter):
                    store(result)
        elif id == '5':
            for filter in range(1, 20):
                filter = str(filter)
                for result in search(id, function, filter2=filter):
                    store(result)
        else:
            for result in search(id , function):
                store(result)

