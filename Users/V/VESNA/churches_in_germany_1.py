#coding=utf-8
import itertools
import scraperwiki
import requests
from lxml.html import fromstring as parse


WIKIPEDIA_MUNCHEN = 'http://de.wikipedia.org/wiki/Liste_der_Kirchengeb%C3%A4ude_in_M%C3%BCnchen'
WIKIPEDIA_LEIPZIG = 'http://de.wikipedia.org/wiki/Liste_der_Kirchengeb%C3%A4ude_in_Leipzig'
HEADERS = {
    'User-agent': 'Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11',
}
ROW_SCHEMA = [
    'name', 'confession',
    'address', 'location',
    'wikipedia_url', 'thumbnail_url',
    'info',
]
ROW_KEY = [
    'confession', 'location', 'name',
]

store = scraperwiki.sqlite.save

def scrape(url):
    return requests.get(url, headers=HEADERS).text

class Dict(dict):
    """A dict that allows for object-like property access syntax."""
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self.__setitem__(name, value)

def Row(**kwargs):
    row = Dict((field, None) for field in ROW_SCHEMA)
    row.update(kwargs)
    return row
    
def scrape_munchen(confession, markerid):
    html = parse(scrape(WIKIPEDIA_MUNCHEN))
    marker = html.get_element_by_id(markerid)
    assert marker is not None, "bad scrape - missing element"
    table = iter(marker.getparent().getnext())
    # ignore first row
    header = table.next()
    for tr in table:
        row = Row(confession=confession, location='München')
        tds = tr.cssselect('td')
        elems = tds[1].cssselect('a')
        if elems:
            row.name = (elems[0].text or '').strip()
            row.wikipedia_url = elems[0].get('href')
        else:
            name = tds[1].text_content()
            discard, div, name = name.rpartition('!')
            row.name = name
        if not row.name:
            continue
        elem = tds[2]
        location = (elem[-1].text_content() or '').strip()
        address = elem.text_content()
        if address and address.lower().endswith('(standort)'):
            address = address[:-len('(standort)')]
        row.address = ','.join(address.split())
        row.info = tds[4].text_content()
        yield row

def scrape_leipzig():
    html = parse(scrape(WIKIPEDIA_LEIPZIG))
    for table in html.cssselect('table.wikitable'):
        print table

def MunchenScraper():
    rows = itertools.chain(
        scrape_munchen('Catholic', 'R.C3.B6misch-katholische_Kirchen'),
        scrape_munchen('Orthodox', 'Altorientalische.2C_orthodoxe_und_altkatholische_Kirchen'),
        scrape_munchen('Lutheran (Bavaria)', 'Kirchen_der_Evangelisch-Lutherischen_Kirche_in_Bayern'),
    )
    for row in rows:
        store(unique_keys=ROW_KEY, data=dict(row))

scrape_leipzig()


