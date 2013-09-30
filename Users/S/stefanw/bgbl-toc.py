import re

import scraperwiki
import requests

import lxml.html


class BGBLParser(object):
    BASE_URL = 'http://www.bgbl.de/Xaver/'
    START = 'start.xav?startbk=Bundesanzeiger_BGBl'
    BASE_TOC = ('toc.xav?dir=center&start=2&cur=2&op=2&tf=Bundesanzeiger_BGBl_mainFrame'
               '&hlf=Bundesanzeiger_BGBl_mainFrame&qmf=Bundesanzeiger_BGBl_mainFrame&'
               'tocf=Bundesanzeiger_BGBl_tocFrame&bk=Bundesanzeiger_BGBl')
    YEAR_TOC = ('toc.xav?tocf=Bundesanzeiger_BGBl_tocFrame&tf=Bundesanzeiger_BGBl_mainFrame'
                '&qmf=Bundesanzeiger_BGBl_mainFrame&hlf=Bundesanzeiger_BGBl_mainFrame&start=2'
                '&bk=Bundesanzeiger_BGBl&dir=down&op=__docid__&noca=10')
    TEXT = ('text.xav?tocf=Bundesanzeiger_BGBl_tocFrame&'
        'tf=Bundesanzeiger_BGBl_mainFrame&qmf=Bundesanzeiger_BGBl_mainFrame&hlf=Bundesanzeiger_BGBl_mainFrame'
        '&start=%2f%2f*%5B%40node_id%3D%27__docid__%27%5D&bk=Bundesanzeiger_BGBl')

    year_toc = {}
    year_docs = {}
    toc = {}

    def __init__(self):
        self.sid = None

    def login(self):
        response = requests.get(self.BASE_URL + self.START)
        self.sid = response.headers['XaverSID']

    def sessionify(self, url):
        if not self.sid:
            self.login()
        return '%s&SID=%s' % (url, self.sid)

    def scrape(self):
        self.get_main_toc()
        self.get_all_year_tocs()
        self.get_all_tocs()

    def get_main_toc(self):
        response = requests.get(self.sessionify(self.BASE_URL + self.BASE_TOC))
        root = lxml.html.fromstring(response.text)
        for a in root.cssselect('.tocelement a[target="Bundesanzeiger_BGBl_mainFrame"]'):
            try:
                year = int(a.text_content())
            except ValueError:
                continue
            doc_id = re.search('start=%2f%2f\*%5B%40node_id%3D%27(\d+)%27%5D', a.attrib['href'])
            if doc_id is not None:
                self.year_toc[year] = doc_id.group(1)

    def get_all_year_tocs(self):
        for year in self.year_toc:
            self.get_year_toc(year)

    def get_year_toc(self, year):
        year_doc_id = self.year_toc[year]
        url = self.BASE_URL + self.YEAR_TOC.replace('__docid__', year_doc_id)
        response = requests.get(self.sessionify(url))
        root = lxml.html.fromstring(response.text)
        print self.sid, url, year_doc_id
        for a in root.cssselect('.tocelement a[target="Bundesanzeiger_BGBl_mainFrame"]'):
            match = re.search('Nr\. (\d+) vom (\d{2}\.\d{2}\.\d{4})', a.text_content())
            if match is None:
                continue
            number = int(match.group(1))
            date = match.group(2)
            doc_id = re.search('start=%2f%2f\*%5B%40node_id%3D%27(\d+)%27%5D', a.attrib['href'])
            doc_id = doc_id.group(1)
            self.year_docs.setdefault(year, {})
            self.year_docs[year][number] = {'date': date, 'doc_id': doc_id}

    def get_all_tocs(self):
        for year in self.year_docs:
            print year
            for number in self.year_docs[year]:
                self.get_toc(year, number)


    def get_toc(self, year, number):
        year_doc = self.year_docs[year][number]
        doc_id = year_doc['doc_id']
        url = self.BASE_URL + self.TEXT.replace('__docid__', doc_id)
        url = self.sessionify(url)
        response = requests.get(url)
        root = lxml.html.fromstring(response.text)
        toc = []
        for tr in root.cssselect('tr'):
            td = tr.cssselect('td')[1]
            divs = td.cssselect('div')
            if not len(divs):
                continue
            law_date = divs[0].text_content()
            if not law_date.strip():
                law_date = None
            link = divs[1].cssselect('a')[0]
            name = link.text_content().strip()
            href = link.attrib['href']
            href = re.sub('SID=[^&]+&', '', href)
            text = divs[2].text_content().strip()
            match = re.search('aus Nr. (\d+) vom (\d{1,2}\.\d{1,2}\.\d{4}), Seite ?(\d*)$', text)
            page = None
            date = match.group(2)
            if match.group(3):
                page = int(match.group(3))
            kind = 'entry'
            if name in ('Komplette Ausgabe', 'Inhaltsverzeichnis'):
                kind = 'meta'
            d = {
                'year': year, 'toc_doc_id': doc_id,
                'number': number, 'date': date,
                'law_date': law_date, 'kind': kind,
                'name': name, 'href': href, 'page': page
            }
            scraperwiki.sqlite.save(unique_keys=['href'], data=d)
            toc.append(d)
        year_doc['toc'] = toc



bgbl = BGBLParser()
# bgbl.scrape()

bgbl.get_main_toc()
bgbl.get_year_toc(1950)
bgbl.get_toc(1950, 54)
import re

import scraperwiki
import requests

import lxml.html


class BGBLParser(object):
    BASE_URL = 'http://www.bgbl.de/Xaver/'
    START = 'start.xav?startbk=Bundesanzeiger_BGBl'
    BASE_TOC = ('toc.xav?dir=center&start=2&cur=2&op=2&tf=Bundesanzeiger_BGBl_mainFrame'
               '&hlf=Bundesanzeiger_BGBl_mainFrame&qmf=Bundesanzeiger_BGBl_mainFrame&'
               'tocf=Bundesanzeiger_BGBl_tocFrame&bk=Bundesanzeiger_BGBl')
    YEAR_TOC = ('toc.xav?tocf=Bundesanzeiger_BGBl_tocFrame&tf=Bundesanzeiger_BGBl_mainFrame'
                '&qmf=Bundesanzeiger_BGBl_mainFrame&hlf=Bundesanzeiger_BGBl_mainFrame&start=2'
                '&bk=Bundesanzeiger_BGBl&dir=down&op=__docid__&noca=10')
    TEXT = ('text.xav?tocf=Bundesanzeiger_BGBl_tocFrame&'
        'tf=Bundesanzeiger_BGBl_mainFrame&qmf=Bundesanzeiger_BGBl_mainFrame&hlf=Bundesanzeiger_BGBl_mainFrame'
        '&start=%2f%2f*%5B%40node_id%3D%27__docid__%27%5D&bk=Bundesanzeiger_BGBl')

    year_toc = {}
    year_docs = {}
    toc = {}

    def __init__(self):
        self.sid = None

    def login(self):
        response = requests.get(self.BASE_URL + self.START)
        self.sid = response.headers['XaverSID']

    def sessionify(self, url):
        if not self.sid:
            self.login()
        return '%s&SID=%s' % (url, self.sid)

    def scrape(self):
        self.get_main_toc()
        self.get_all_year_tocs()
        self.get_all_tocs()

    def get_main_toc(self):
        response = requests.get(self.sessionify(self.BASE_URL + self.BASE_TOC))
        root = lxml.html.fromstring(response.text)
        for a in root.cssselect('.tocelement a[target="Bundesanzeiger_BGBl_mainFrame"]'):
            try:
                year = int(a.text_content())
            except ValueError:
                continue
            doc_id = re.search('start=%2f%2f\*%5B%40node_id%3D%27(\d+)%27%5D', a.attrib['href'])
            if doc_id is not None:
                self.year_toc[year] = doc_id.group(1)

    def get_all_year_tocs(self):
        for year in self.year_toc:
            self.get_year_toc(year)

    def get_year_toc(self, year):
        year_doc_id = self.year_toc[year]
        url = self.BASE_URL + self.YEAR_TOC.replace('__docid__', year_doc_id)
        response = requests.get(self.sessionify(url))
        root = lxml.html.fromstring(response.text)
        print self.sid, url, year_doc_id
        for a in root.cssselect('.tocelement a[target="Bundesanzeiger_BGBl_mainFrame"]'):
            match = re.search('Nr\. (\d+) vom (\d{2}\.\d{2}\.\d{4})', a.text_content())
            if match is None:
                continue
            number = int(match.group(1))
            date = match.group(2)
            doc_id = re.search('start=%2f%2f\*%5B%40node_id%3D%27(\d+)%27%5D', a.attrib['href'])
            doc_id = doc_id.group(1)
            self.year_docs.setdefault(year, {})
            self.year_docs[year][number] = {'date': date, 'doc_id': doc_id}

    def get_all_tocs(self):
        for year in self.year_docs:
            print year
            for number in self.year_docs[year]:
                self.get_toc(year, number)


    def get_toc(self, year, number):
        year_doc = self.year_docs[year][number]
        doc_id = year_doc['doc_id']
        url = self.BASE_URL + self.TEXT.replace('__docid__', doc_id)
        url = self.sessionify(url)
        response = requests.get(url)
        root = lxml.html.fromstring(response.text)
        toc = []
        for tr in root.cssselect('tr'):
            td = tr.cssselect('td')[1]
            divs = td.cssselect('div')
            if not len(divs):
                continue
            law_date = divs[0].text_content()
            if not law_date.strip():
                law_date = None
            link = divs[1].cssselect('a')[0]
            name = link.text_content().strip()
            href = link.attrib['href']
            href = re.sub('SID=[^&]+&', '', href)
            text = divs[2].text_content().strip()
            match = re.search('aus Nr. (\d+) vom (\d{1,2}\.\d{1,2}\.\d{4}), Seite ?(\d*)$', text)
            page = None
            date = match.group(2)
            if match.group(3):
                page = int(match.group(3))
            kind = 'entry'
            if name in ('Komplette Ausgabe', 'Inhaltsverzeichnis'):
                kind = 'meta'
            d = {
                'year': year, 'toc_doc_id': doc_id,
                'number': number, 'date': date,
                'law_date': law_date, 'kind': kind,
                'name': name, 'href': href, 'page': page
            }
            scraperwiki.sqlite.save(unique_keys=['href'], data=d)
            toc.append(d)
        year_doc['toc'] = toc



bgbl = BGBLParser()
# bgbl.scrape()

bgbl.get_main_toc()
bgbl.get_year_toc(1950)
bgbl.get_toc(1950, 54)
