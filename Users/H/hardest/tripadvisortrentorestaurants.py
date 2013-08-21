import scraperwiki

# http://packages.python.org/pyquery/
from pyquery import PyQuery as pq
import urllib
# http://lxml.de/api/
from lxml import etree

BASE_URL = 'http://www.tripadvisor.it'
SEARCH_URL = BASE_URL + '/Restaurants-g1493737-Trentino_Trentino_Alto_Adige.html'  #'/RestaurantSearch?geo=187861&pid=&q=Trento%2C+Italia'

def rename_category(categories):
    translation = {
        'romantico'              : 'romantic',
        'affari'                 : 'business',
        'cucina locale'          : 'local_cousine',
        'occasioni speciali'     : 'special_event',
        'intrattenere i clienti' : 'entertainment',
        'adatto ai bambini'      : 'children',
        'gruppi numerosi'        : 'large_groups',
        'pasti economici'        : 'cheap',
        'dehors'                 : 'outside',
        'scena da bar'           : 'bar'
    }
    return map(lambda e : translation.get(e,e), categories)

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
        value = detail_text_iter.next()
        if key.lower().startswith('cucina'):
            # details_map['cooking_type'] = map( lambda e : e.strip().lower(), value.split(',') )
            multiply( 'cooking_type__', map( lambda e : e.strip().lower(), value.split(',') ), details_map )
        elif key.lower().startswith('possibilit'):
            value = value.lower()
            if 'prenotazion' in value: details_map['booking']        = True
            if 'colazione'   in value: details_map['breakfast']      = True
            if 'pranzo'      in value: details_map['lunch']          = True
            if 'cena'        in value: details_map['dinner']         = True
            if 'mezzanotte'  in value: details_map['after_midnight'] = True
        elif key.lower().startswith('per'):
            # details_map['categories'] = rename_category( map( lambda e : e.strip().lower(), value.split(',') ) )
            multiply( 'category__', rename_category( map( lambda e : e.strip().lower(), value.split(',') ) ), details_map )
        elif key.lower().startswith('fascia prezzo'):
            prices = sorted( map( lambda e : float(e), value.replace(u'\u20ac', '').split('-') ) )
            details_map['min_price'] = prices[0]
            details_map['max_price'] = prices[1]
        else:
            details_map[key] = value
    return details_map

def extract_rating(restaurant_page):
    rating_value = None
    rating_base  = None
    for meta in restaurant_page('span.rate')('meta') : 
        key   = meta.get('itemprop')
        value = meta.get('content')
        if 'ratingValue' == key: rating_value = float(value)
        if 'bestRating'  == key: rating_base  = float(value)
    if rating_value and rating_base: 
        return rating_value / rating_base 
    else:
        return None

STATICMAP_CENTER = 'http://maps.google.com/maps/api/staticmap?channel=ta.PRODUCTION&center='

def extract_location(restaurant_page):
    scripts = restaurant_page('body')('script')
    for script in scripts:
        script_text = script.text
        if script_text and STATICMAP_CENTER in script_text :
            lazy_map_src = script_text
            break
    begin = lazy_map_src.index(STATICMAP_CENTER) + len(STATICMAP_CENTER)
    end   = lazy_map_src.index('&', begin)
    return map (lambda e : float(e), lazy_map_src[begin:end].split(',') )

def process_restaurant_page(url):
    page = pq(url=url)

    restaurant_name = page('h1#HEADING').text()    
    street_address  = page('span.street-address').text()
    country         = page('span.country-name').text()
    email           = page('div.fkLnk.hvrIE6.fl') and page('div.fkLnk.hvrIE6.fl')[0].get('onclick') or None
    website         = page('a.fkLnk.hvrIE6') and page('a.fkLnk.hvrIE6')[0].get('href') or None

    postal_code = None
    locality    = None
    try:
        for span in page('span.locality')[0].getchildren():
            if span.get('property') == 'v:postal-code': postal_code = span.text
            if span.get('property') == 'v:locality'   : locality    = span.text
    except BaseException as e:
        print 'ERROR while parsing locality:', e

    try:
        email = email and email.split(',')[3].replace("'", '')
    except BaseException:
        print 'ERROR while parsing email:', email                 
        email = None

    try:
        website = website and website.split('.')[3].split('-')[0] \
                                                   .replace('%253A', ':') \
                                                   .replace('__5F____5F__2E__5F____5F__', '.') \
                                                   .replace('__5F____5F__2D__5F____5F__', '.') \
                                                   .replace('__5F____5F__2F__5F____5F__', '/') \
                                                   .replace('%253A__5F____5F__2F__5F____5F____5F____5F__2F__5F____5F__', '://')
    except IndexError:        
        print 'ERROR while parsing website ', website 
        website = None

    details_node = page('div.listing_details')('div.detail')
    data = extract_details(details_node)    
    
    location = None
    try:
        location = extract_location(page) 
    except BaseException as e:
        print 'ERROR while extracting location from page:', url, e

    data['url']         = url
    data['name']        = restaurant_name
    data['address']     = street_address
    data['postal_code'] = postal_code
    data['locality']    = locality
    data['country']     = country
    data['lat']         = location and location[0]
    data['lon']         = location and location[1]
    data['email']       = email
    data['website']     = website
    data['rating']      = extract_rating(page)

    print 'DATA', data
    scraperwiki.sqlite.save(unique_keys=['url'], data=data)

def process_pagination(result_page):
    for result in result_page('a.property_title'):
        print( 'Processing page: ' + result.get('href'))
        process_restaurant_page(BASE_URL + result.get('href'))

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