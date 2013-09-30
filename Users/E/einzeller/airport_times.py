from urllib2 import urlparse

import scraperwiki
import lxml.html
import datetime

ARRIVAL =   'http://www.berlin-airport.de/DE/ReisendeUndBesucher/AnkuenfteAbfluegeAktuell/Ankuenfte/'
DEPARTURE = 'http://www.berlin-airport.de/DE/ReisendeUndBesucher/AnkuenfteAbfluegeAktuell/Abfluege/'
START = 'index2.php?lang=de'

def get_details_from_url(url_portion):
    res = urlparse.parse_qs(url_portion.partition('?')[2])
    if not res: # might happen in the case of someone not submitting a URL with "details.php?" at the start
        res = url_portion 
    for key in res.keys():
        res[key] = res[key][0]
    return res

def get_alternate_flights(row):
    print row[-1].text, row[-1].text_content()
    return row[-1].text.partition(': ')[2] or ''

def get_carrier(row):
    td = row.cssselect('a.linkbold')[0]
    carrier = td.attrib['title'].rsplit('(')[-1][:-1]
    return carrier or '' 

def get_date(row):
    return row.text_content().replace(u'\xa0', ' ').strip() or ''

def is_codeshare(row):
    return any('codeshare' in img.attrib['alt'] for img in row.iterdescendants('img'))

def is_date(row):
    return len(row.cssselect('th')) == 2

def is_column_heading(row):
    return 'Flug' in row.text_content()

def parse_page(url):
    root = lxml.html.parse(url).getroot()
    previous_flight = None
    date = None
    if root is not None:
        for row in root.cssselect('tbody.content_tblsearch tr'):
            if is_date(row):
                date = get_date(row)
                continue
            elif is_codeshare(row):
                flight = previous_flight
                flight['alt_flights'] = get_alternate_flights(row)
            elif len(row) < 8 or is_column_heading(row):
                continue
            else:
                flight = {}
                flight["no"]        = row[1].text_content().replace(u'\xa0', ' ')
                flight["c_from"]    = row[2].text.encode('utf-8').replace("\xc2\xa0", " ") or ''
                flight["c_to"]      = row[3].text.encode('utf-8').replace("\xc2\xa0", " ") or ''
                flight["gate"]      = row[4].text or ''
                flight["scheduled"] = row[5].text or ''
                flight["expected"]  = row[6].text or ''
                flight["state"]     = row[7].text or ''
                flight["carrier"]   = get_carrier(row)
                flight["date"]      = date or ''
                flight['alt_flights'] = ''
                flight['date_scraped'] = datetime.datetime.today()
                for key, val in get_details_from_url(row[1].cssselect('a.linkbold')[0].attrib['href']).iteritems():
                    flight[key] = val
            scraperwiki.sqlite.save(unique_keys=["no"], data=flight)        
            previous_flight = flight
        if len(root.cssselect('.content_barrightbottom a')) > 0:
            return root.cssselect('.content_barrightbottom a')[0].attrib['href']
        else:
            return None
    else:
        return None

def main():
    scraperwiki.sqlite.execute("drop table if exists swdata")
    scraperwiki.sqlite.commit()

    url = ARRIVAL + START
    while 1:
        next_page = parse_page(url)
        if next_page:
            url = ARRIVAL + next_page
        else:
            break

    url = DEPARTURE + START
    while 1:
        next_page = parse_page(url)
        if next_page:
            url = DEPARTURE + next_page
        else:
            break

main()
from urllib2 import urlparse

import scraperwiki
import lxml.html
import datetime

ARRIVAL =   'http://www.berlin-airport.de/DE/ReisendeUndBesucher/AnkuenfteAbfluegeAktuell/Ankuenfte/'
DEPARTURE = 'http://www.berlin-airport.de/DE/ReisendeUndBesucher/AnkuenfteAbfluegeAktuell/Abfluege/'
START = 'index2.php?lang=de'

def get_details_from_url(url_portion):
    res = urlparse.parse_qs(url_portion.partition('?')[2])
    if not res: # might happen in the case of someone not submitting a URL with "details.php?" at the start
        res = url_portion 
    for key in res.keys():
        res[key] = res[key][0]
    return res

def get_alternate_flights(row):
    print row[-1].text, row[-1].text_content()
    return row[-1].text.partition(': ')[2] or ''

def get_carrier(row):
    td = row.cssselect('a.linkbold')[0]
    carrier = td.attrib['title'].rsplit('(')[-1][:-1]
    return carrier or '' 

def get_date(row):
    return row.text_content().replace(u'\xa0', ' ').strip() or ''

def is_codeshare(row):
    return any('codeshare' in img.attrib['alt'] for img in row.iterdescendants('img'))

def is_date(row):
    return len(row.cssselect('th')) == 2

def is_column_heading(row):
    return 'Flug' in row.text_content()

def parse_page(url):
    root = lxml.html.parse(url).getroot()
    previous_flight = None
    date = None
    if root is not None:
        for row in root.cssselect('tbody.content_tblsearch tr'):
            if is_date(row):
                date = get_date(row)
                continue
            elif is_codeshare(row):
                flight = previous_flight
                flight['alt_flights'] = get_alternate_flights(row)
            elif len(row) < 8 or is_column_heading(row):
                continue
            else:
                flight = {}
                flight["no"]        = row[1].text_content().replace(u'\xa0', ' ')
                flight["c_from"]    = row[2].text.encode('utf-8').replace("\xc2\xa0", " ") or ''
                flight["c_to"]      = row[3].text.encode('utf-8').replace("\xc2\xa0", " ") or ''
                flight["gate"]      = row[4].text or ''
                flight["scheduled"] = row[5].text or ''
                flight["expected"]  = row[6].text or ''
                flight["state"]     = row[7].text or ''
                flight["carrier"]   = get_carrier(row)
                flight["date"]      = date or ''
                flight['alt_flights'] = ''
                flight['date_scraped'] = datetime.datetime.today()
                for key, val in get_details_from_url(row[1].cssselect('a.linkbold')[0].attrib['href']).iteritems():
                    flight[key] = val
            scraperwiki.sqlite.save(unique_keys=["no"], data=flight)        
            previous_flight = flight
        if len(root.cssselect('.content_barrightbottom a')) > 0:
            return root.cssselect('.content_barrightbottom a')[0].attrib['href']
        else:
            return None
    else:
        return None

def main():
    scraperwiki.sqlite.execute("drop table if exists swdata")
    scraperwiki.sqlite.commit()

    url = ARRIVAL + START
    while 1:
        next_page = parse_page(url)
        if next_page:
            url = ARRIVAL + next_page
        else:
            break

    url = DEPARTURE + START
    while 1:
        next_page = parse_page(url)
        if next_page:
            url = DEPARTURE + next_page
        else:
            break

main()
