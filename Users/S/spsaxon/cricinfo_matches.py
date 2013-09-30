import scraperwiki
import itertools
import re
import lxml.html

BASE_URL = "http://www.espncricinfo.com"

PRE_SQL = [
"""
            DROP TABLE IF EXISTS matches
""",
"""            CREATE TABLE matches (
                series_id INTEGER,
                FOREIGN KEY(series_id) REFERENCES series(id)
            )
""",
"""
            DROP TABLE IF EXISTS series
""",
]

for s in PRE_SQL:
    try:
        scraperwiki.sqlite.execute(s, verbose=4)
    except scraperwiki.sqlite.SqliteError, e:
        print str(e)


def scrape_years():
    URL = '/ci/engine/series/index.html'
    html = scraperwiki.scrape(BASE_URL + URL)
    
    #root = lxml.html.fromstring(html.replace("\n","")) # Get rid of windows line endings
    root = lxml.html.fromstring(html)
    return [ {"year": el.text, "link":el.attrib['href']} for el in root.cssselect("p.arhvDecade a") ]

def scrape_matches(series = []):    
    data = []
    for a_series in series[:2]:
        html = scraperwiki.scrape(BASE_URL + a_series['link'])
        root = lxml.html.fromstring(html.replace("\n",""))
        id = itertools.count(0)
        titles = root.cssselect("p.potMatchHeading")
        for title in titles:
            match = {
                        'id': id.next(),
                    'title': re.sub(r'\s+', " ", title.text_content()),
                'series_id': a_series['id'],
            }
            _links_iter = itertools.takewhile(lambda el : el.tag == 'p', title.itersiblings())
            for (k, el) in ( (el.attrib['class'].split(' ')[1][4:], el) for el in _links_iter ):
                if k == 'links':
                    links = el.cssselect("span a")
                    for link in links:
                        match[re.sub(r'\(\d+\)', "", link.text_content()) + '_link'] = link.attrib['href']
                else:
                    match[k] = re.sub(r'\s+', " ", el.text_content())
            data.append(match)
    return data

def scrape_series():
    years = scrape_years()
    
    data = []
    id = itertools.count(0)
    for year in years[:2]:
        url = BASE_URL + year['link']
        html = scraperwiki.scrape(url)
        
        root = lxml.html.fromstring(html.replace("\n","")) 
        for el1 in root.cssselect("p.ciGrndSubHead"):
            for el2 in el1.getnext().cssselect("dl.seasnResult"):
                series = el2.getchildren()[0].getchildren()[0]  
                status = el2.getchildren()[1].text
                if status:
                    status = status.strip()
                data.append({ "id": id.next(), "status": status, "class": el1.text, "title": series.text, "link": series.attrib['href'], "year": year['year'] })
    return data

series = scrape_series()
matches = scrape_matches(series)

scraperwiki.sqlite.save(unique_keys=[], data=series, table_name="series")
scraperwiki.sqlite.save(unique_keys=[], data=matches, table_name="matches")



import scraperwiki
import itertools
import re
import lxml.html

BASE_URL = "http://www.espncricinfo.com"

PRE_SQL = [
"""
            DROP TABLE IF EXISTS matches
""",
"""            CREATE TABLE matches (
                series_id INTEGER,
                FOREIGN KEY(series_id) REFERENCES series(id)
            )
""",
"""
            DROP TABLE IF EXISTS series
""",
]

for s in PRE_SQL:
    try:
        scraperwiki.sqlite.execute(s, verbose=4)
    except scraperwiki.sqlite.SqliteError, e:
        print str(e)


def scrape_years():
    URL = '/ci/engine/series/index.html'
    html = scraperwiki.scrape(BASE_URL + URL)
    
    #root = lxml.html.fromstring(html.replace("\n","")) # Get rid of windows line endings
    root = lxml.html.fromstring(html)
    return [ {"year": el.text, "link":el.attrib['href']} for el in root.cssselect("p.arhvDecade a") ]

def scrape_matches(series = []):    
    data = []
    for a_series in series[:2]:
        html = scraperwiki.scrape(BASE_URL + a_series['link'])
        root = lxml.html.fromstring(html.replace("\n",""))
        id = itertools.count(0)
        titles = root.cssselect("p.potMatchHeading")
        for title in titles:
            match = {
                        'id': id.next(),
                    'title': re.sub(r'\s+', " ", title.text_content()),
                'series_id': a_series['id'],
            }
            _links_iter = itertools.takewhile(lambda el : el.tag == 'p', title.itersiblings())
            for (k, el) in ( (el.attrib['class'].split(' ')[1][4:], el) for el in _links_iter ):
                if k == 'links':
                    links = el.cssselect("span a")
                    for link in links:
                        match[re.sub(r'\(\d+\)', "", link.text_content()) + '_link'] = link.attrib['href']
                else:
                    match[k] = re.sub(r'\s+', " ", el.text_content())
            data.append(match)
    return data

def scrape_series():
    years = scrape_years()
    
    data = []
    id = itertools.count(0)
    for year in years[:2]:
        url = BASE_URL + year['link']
        html = scraperwiki.scrape(url)
        
        root = lxml.html.fromstring(html.replace("\n","")) 
        for el1 in root.cssselect("p.ciGrndSubHead"):
            for el2 in el1.getnext().cssselect("dl.seasnResult"):
                series = el2.getchildren()[0].getchildren()[0]  
                status = el2.getchildren()[1].text
                if status:
                    status = status.strip()
                data.append({ "id": id.next(), "status": status, "class": el1.text, "title": series.text, "link": series.attrib['href'], "year": year['year'] })
    return data

series = scrape_series()
matches = scrape_matches(series)

scraperwiki.sqlite.save(unique_keys=[], data=series, table_name="series")
scraperwiki.sqlite.save(unique_keys=[], data=matches, table_name="matches")



