import lxml.html           
import scraperwiki

SEARCH_URL = "https://www.crtmoorings.com/auctions/search.php"
SEARCH_PARAMS = {
    'search_type': 'basic',
    'keywords': '',
    'min_length': '',
    'min_width': '',
    'county': '',
    'waterway': '',
    'mooring_use': '2',      # 2 == 'residential'
    'postcode': 'WC2B+6NH',
    'distance': '50',
    'vacancy_type': '1',     # 1 == 'any',
    'sort_by': '0',          # 0 == 'closingdate'
    'sort_type': 'asc',
    'ended': '0',
    'vsearch': 'Start+search',
}

URL = SEARCH_URL + '?' + '&'.join(k + '=' + v for k, v in SEARCH_PARAMS.items())

html = scraperwiki.scrape(URL)
root = lxml.html.fromstring(html)

for h3 in root.cssselect("h3.vacancy_summary"):
    data = {}
    _, txt = h3.text.split('Auction: ', 1)
    data['id'], data['title'] = txt.split(' - ', 1)
    
    details = h3.getnext()

    image = details.cssselect("div.vacancy_main_img img")
    data['image_url'] = image[0].get('src')

    data['full_details_url'] = details.cssselect('a.view_full_details_button')[0].get('href')
    
    scraperwiki.sqlite.save(unique_keys=['id'], data=data)

import lxml.html           
import scraperwiki

SEARCH_URL = "https://www.crtmoorings.com/auctions/search.php"
SEARCH_PARAMS = {
    'search_type': 'basic',
    'keywords': '',
    'min_length': '',
    'min_width': '',
    'county': '',
    'waterway': '',
    'mooring_use': '2',      # 2 == 'residential'
    'postcode': 'WC2B+6NH',
    'distance': '50',
    'vacancy_type': '1',     # 1 == 'any',
    'sort_by': '0',          # 0 == 'closingdate'
    'sort_type': 'asc',
    'ended': '0',
    'vsearch': 'Start+search',
}

URL = SEARCH_URL + '?' + '&'.join(k + '=' + v for k, v in SEARCH_PARAMS.items())

html = scraperwiki.scrape(URL)
root = lxml.html.fromstring(html)

for h3 in root.cssselect("h3.vacancy_summary"):
    data = {}
    _, txt = h3.text.split('Auction: ', 1)
    data['id'], data['title'] = txt.split(' - ', 1)
    
    details = h3.getnext()

    image = details.cssselect("div.vacancy_main_img img")
    data['image_url'] = image[0].get('src')

    data['full_details_url'] = details.cssselect('a.view_full_details_button')[0].get('href')
    
    scraperwiki.sqlite.save(unique_keys=['id'], data=data)

