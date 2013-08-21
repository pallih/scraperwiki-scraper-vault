import scraperwiki           
import lxml.html
import re

BASE_URL = 'http://www.gamberorosso.it'
RESULTS_PAGE = BASE_URL + '/index.php?option=com_k2&view=itemlist&task=tag&id=3&tag=Trentino+Alto+Adige&Itemid=6&show=23&lang=it'

def extract_attributes(restaurant_page):
    attributes_map = { 
        'parcheggio'        : 'parking',
        'aria_condizionata' : 'air_conditioning',
        'fumatori'          : 'smokers',
        'tavoli_aperto'     : 'outside',
        'disabili'          : 'disabled',
        'disabili_aiuto'    : 'disabled_help',
        'vegetariano'       : 'vegetarian',
        'animali'           : 'pets',
        'birra'             : 'bar',
        'card'              : 'card'
    }
    attributes = {}
    for attribute, translation in attributes_map.items():
        if restaurant_page.cssselect('image[src="/images/Ristoranti/' + attribute + '_on.png"]'):
            attributes[translation] = 1
        else:
            attributes[translation] = 0
    return attributes

# via Runch, 11 39036 Pedraces/Pedratsches (BZ)
def split_address(address, data):    
    try:
        parts1 = address.split(',')
        parts2 = parts1[1].split(' ')
        data['address']     = parts1[0] + ' ' + parts2[1]
        data['postal_code'] = parts2[2]
        data['locality']    = " ".join( parts2[3:-1] )
    except BaseException as e:
        print 'Error while splitting address.', e

def extract_geo_coordinates(restaurant_page_html):
    try:
        regex = re.compile("GLatLng\(\s*(\d+\.\d+)\s*\,\s*(\d+\.\d+)\s*\)")
        matches = regex.search(restaurant_page_html)
        return matches.groups()
    except BaseException as e:
        print 'Error while extracting coordinates.', e
        return None

def extract_scores(restaurant_page, data):
    try:
        scores = []
        for elem in restaurant_page.cssselect('div.itemHeader p[style="float:left;"]'):
            stripped = elem.text.strip()                
            if stripped != '-' : scores.append(stripped)
            else: scores.append(None)
        data['service'] = scores[0]
        data['cooking'] = scores[1]
        data['winery' ] = scores[2]
        data['bonus'  ] = scores[3]
    except BaseException as e:
        print 'Error while extracting scores.', e

def process_restaurant(link):
    try:
        restaurant_page_html = scraperwiki.scrape(link)
    except BaseException as e:
        print 'Error while parsing page', link, ':', e 
        return
    
    restaurant_page = lxml.html.fromstring(restaurant_page_html)
    name        = restaurant_page.cssselect('div.itemHeader div table tr td h2')[0].text  
    price       = restaurant_page.cssselect('div.itemHeader td p:last-child')[2].text
    sidebox     = restaurant_page.cssselect('div.itemHeader td[style="vertical-align:middle"]')
    address     = sidebox[1].text
    phone       = sidebox[3].text
    links       = restaurant_page.cssselect('div.itemHeader td[style="vertical-align:middle"] a')
    
    try:
        email       = links[0].attrib['href'].split(':')[1]
    except BaseException as e:
        print 'Error while parsing email', e

    website     = len(links) > 1 and links[1].attrib['href'] or None
    description = restaurant_page.cssselect('div.itemFullText')[0].text

    data = {}
    data['url']          = link
    data['name']         = name
    data['full_address'] = address
    split_address(address, data)
    geo = extract_geo_coordinates(restaurant_page_html)
    
    if geo:
        data['lat']     = geo[0]
        data['lon']     = geo[1]
    
    data['email']       = email
    data['website']     = website
    data['price']       = price
    data['description'] = description
    
    for attribute, value in extract_attributes(restaurant_page).items():
        data[attribute] = value
    extract_scores(restaurant_page, data)
    
    print 'DATA', data
    scraperwiki.sqlite.save(unique_keys=['url'], data=data)


def process_pagination(pagination_url):
    print 'Processing pagination:', pagination_url
    result_page_html = scraperwiki.scrape(pagination_url)
    result_page = lxml.html.fromstring(result_page_html)
    for restaurant_link in result_page.cssselect('div.genericItemList tr td a'):
        print 'Processing restaurant:', restaurant_link.attrib['href']
        process_restaurant( BASE_URL + restaurant_link.attrib['href'].encode("utf8") )
    try:
        next_page_url = result_page.cssselect('div.k2Pagination a[title="Succ."]')[0].get('href')
    except: return
    process_pagination(BASE_URL + next_page_url)

process_pagination(RESULTS_PAGE)
