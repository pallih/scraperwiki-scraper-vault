import scraperwiki

# http://packages.python.org/pyquery/
from pyquery import PyQuery as pq
import urllib
from unidecode import unidecode
from BeautifulSoup import UnicodeDammit
# http://lxml.de/api/
from lxml import etree

BASE_URL = 'http://www.tripadvisor.es'
#SEARCH_URL = BASE_URL + '/Restaurants-g2697408-Maldonado_Department.html' #Maldonado
#SEARCH_URL = BASE_URL + '/Restaurants-g2697404-Colonia_Department.html' #Colonia
SEARCH_URL = BASE_URL + '/Restaurants-g2697415-Rocha_Department.html' #Rocha
#SEARCH_URL = BASE_URL + '/Restaurants-g294323-Montevideo_Montevideo_Department.html' #Montevideo
#SEARCH_URL = BASE_URL + '/Restaurants-g303506-Rio_de_Janeiro_State_of_Rio_de_Janeiro.html' #Rio
#SEARCH_URL = BASE_URL + '/Restaurants-g303631-Sao_Paulo_State_of_Sao_Paulo.html' #SP


def multiply(prefix, in_list, out_map):
    for e in in_list:
        out_map[prefix + e] = True  

def extract_details(details):
    details_map = {}
    for detail in details:
        detail_text_iter = detail.itertext()
        while(True):
            key = detail_text_iter.next()
            if len(key.strip()) != 0 : break
        value =  decode_html(detail_text_iter.next())
        if key.lower().startswith('cocina'):
            # details_map['cooking_type'] = map( lambda e : e.strip().lower(), value.split(',') )
            #multiply( 'cocina_', map( lambda e : e.strip().lower().replace(' ', '-').replace("\'", '').replace('&', 'y'), value.split(',') ), details_map )
             details_map['cocina'] = value.lower()
        elif key.lower().startswith('opciones para'):
            value = value.lower()
        elif key.lower().startswith('bueno para'):
            # details_map['categories'] = rename_category( map( lambda e : e.strip().lower(), value.split(',') ) )
            #multiply( 'category__', map( lambda e : e.strip().lower().replace(' ', '-').replace("\'", '').replace('&', 'y'), value.split(',') ), details_map )
            details_map['categories'] = value.lower()
        elif key.lower().startswith('barrio'):
            value = value.lower()
        elif key.lower().startswith('intervalo de precios'):
            prices = sorted( map( lambda e : float(e), value.replace(u'\u20ac', '').split('-') ) )
            details_map['min_price'] = prices[0]
            details_map['max_price'] = prices[1]
        else:
            details_map[key] = value
    return details_map

def extract_rating(restaurant_page):
    meta = None
    if(restaurant_page('span')('.rate_no')):
        meta = restaurant_page('span')('.rate_no')[0].get('class')
        meta = meta.replace('rate rate_no no', '')

    if meta: 
        return meta
    else:
        return None


def process_restaurant_page(url):
    page = pq(url=url)

    restaurant_name = page('h1#HEADING').text()    
    street_address  = page('span.street-address').text()
    country         = page('span.country-name').text()

    locality    = None
    try:
        for span in page('span.locality')[0].getchildren():
            if span.get('property') == 'v:postal-code': postal_code = span.text
            if span.get('property') == 'v:locality'   : locality    = span.text
    except BaseException as e:
        print 'ERROR while parsing locality:', e


    except IndexError:        
        print 'ERROR while parsing website ', website 
        website = None

    details_node = page('div.listing_details')('div.detail')
    data = extract_details(details_node)    
    

    data['country']     = country
    data['locality']    = locality
    data['name']        = restaurant_name
    data['rating']      = extract_rating(page)
    data['url']         = url
    data['address']     = street_address

    print 'DATA', data
    scraperwiki.sqlite.save(unique_keys=['url'], data=data)

def process_pagination(result_page):
    for result in result_page('a.property_title'):
        print( 'Processing page: ' + result.get('href'))
        process_restaurant_page(BASE_URL + result.get('href'))

def decode_html(html_string):
    converted = UnicodeDammit(html_string, isHTML=True)
    if not converted.unicode:
        raise UnicodeDecodeError(
            "Failed to detect encoding, tried [%s]",
            ', '.join(converted.triedEncodings))
    return converted.unicode


def iterate_search(url):
    print 'Processing pagination:', url
    page = pq(url=url)
    process_pagination(page)
    try:
        next_page_url = page('span.pageDisplay').nextAll('a')[0].get('href')
        print  next_page_url
    except IndexError:
        print 'No more pages'
        return
    iterate_search(BASE_URL + next_page_url)    

iterate_search(SEARCH_URL)