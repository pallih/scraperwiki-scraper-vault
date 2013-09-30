from urllib2 import urlparse

import scraperwiki
import lxml.html

BASE = 'http://www.berlin-airport.de/DE/ReisendeUndBesucher/AnkuenfteAbfluegeAktuell/Ankuenfte/'
START = 'index.php?lang=de&direction=WB'

def get_details_from_url(url_portion):
    """
    >>> res = get_details_from_url("details.php?airport=SXF&amp;id=102191022&amp;flightno=4U+8129&amp;direction=WB")
    >>> res['direction']
    'WB'
    >>> res['airport']
    'SXF'
    >>> res['id']
    '102191022
    >>> res['flightno']
    '4U 8129'
    """
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
            flight["from"]      = row[2].text or ''
            flight["to"]        = row[3].text or ''
            flight["gate"]      = row[4].text or ''
            flight["scheduled"] = row[5].text or ''
            flight["expected"]  = row[6].text or ''
            flight["state"]     = row[7].text or ''
            flight["carrier"]   = get_carrier(row)
            flight["date"]      = date or ''
            flight['alt_flights'] = ''
            flight_url = row[1].cssselect('a.linkbold')[0].attrib['href']
            flight['ref_url']   = BASE + flight_url
            extras = get_details_from_url(flight_url)
            flight['_id'] = extras['id']
            flight['direction'] = extras['direction']
            flight['airport'] = extras['airport']
            
        scraperwiki.sqlite.save(unique_keys=["no", "scheduled", "date", "_id"], data=flight)        
        previous_flight = flight
    return root.cssselect('.content_barrightbottom a')[0].attrib['href']

def main():
    url = BASE + START
    while 1:
        next_page = parse_page(url)
        if next_page:
            url = BASE + next_page
        elif '/Ankuenfte/' in url:
            url = 'http://www.berlin-airport.de/DE/ReisendeUndBesucher/AnkuenfteAbfluegeAktuell/Abfluege/index2.php'
        else:
            break

main()
from urllib2 import urlparse

import scraperwiki
import lxml.html

BASE = 'http://www.berlin-airport.de/DE/ReisendeUndBesucher/AnkuenfteAbfluegeAktuell/Ankuenfte/'
START = 'index.php?lang=de&direction=WB'

def get_details_from_url(url_portion):
    """
    >>> res = get_details_from_url("details.php?airport=SXF&amp;id=102191022&amp;flightno=4U+8129&amp;direction=WB")
    >>> res['direction']
    'WB'
    >>> res['airport']
    'SXF'
    >>> res['id']
    '102191022
    >>> res['flightno']
    '4U 8129'
    """
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
            flight["from"]      = row[2].text or ''
            flight["to"]        = row[3].text or ''
            flight["gate"]      = row[4].text or ''
            flight["scheduled"] = row[5].text or ''
            flight["expected"]  = row[6].text or ''
            flight["state"]     = row[7].text or ''
            flight["carrier"]   = get_carrier(row)
            flight["date"]      = date or ''
            flight['alt_flights'] = ''
            flight_url = row[1].cssselect('a.linkbold')[0].attrib['href']
            flight['ref_url']   = BASE + flight_url
            extras = get_details_from_url(flight_url)
            flight['_id'] = extras['id']
            flight['direction'] = extras['direction']
            flight['airport'] = extras['airport']
            
        scraperwiki.sqlite.save(unique_keys=["no", "scheduled", "date", "_id"], data=flight)        
        previous_flight = flight
    return root.cssselect('.content_barrightbottom a')[0].attrib['href']

def main():
    url = BASE + START
    while 1:
        next_page = parse_page(url)
        if next_page:
            url = BASE + next_page
        elif '/Ankuenfte/' in url:
            url = 'http://www.berlin-airport.de/DE/ReisendeUndBesucher/AnkuenfteAbfluegeAktuell/Abfluege/index2.php'
        else:
            break

main()
