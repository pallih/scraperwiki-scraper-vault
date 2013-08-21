import scraperwiki

# http://packages.python.org/pyquery/
from pyquery import PyQuery as pq
import urllib
# http://lxml.de/api/
from lxml import etree

BASE_URL = 'http://www.tripadvisor.com'
SEARCH_URL = BASE_URL + '/Restaurants-g293974-Istanbul.html'

def multiply(prefix, in_list, out_map):
    for e in in_list:
        out_map[prefix + e] = True  

def extract_details(details):
    details_map = {}
    for detail in details:
        detail_text_iter = detail.itertext()
        while(True):
            key = detail_text_iter.next().replace(':', '')
            if len(key.strip()) != 0 : break
        value = detail_text_iter.next()
        if key.lower().startswith('Cuisines'):
            # details_map['cooking_type'] = map( lambda e : e.strip().lower(), value.split(',') )
            multiply( 'cooking_type__', map( lambda e : e.strip().lower().replace(' ', '-').replace("\'", '').replace('&', 'y'), value.split(',') ), details_map )
        elif key.lower().startswith('possibility'):
            value = value.lower()
        elif key.lower().startswith('per'):
            # details_map['categories'] = rename_category( map( lambda e : e.strip().lower(), value.split(',') ) )
            multiply( 'category__', map( lambda e : e.strip().lower(), value.split(',') ), details_map )
        elif key.lower().startswith('price range'):
            prices = sorted( map( lambda e : str(e), value.replace(u'\u20ac', '').split('-') ) )
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
    extended_address  = page('span.extended-address').text()
    #stars = page('span.rate.rate_cl_gry.cl_gry40')
           
    country         = page('span.country-name').text()
    email           = page('div.taLnk.hvrIE6.fl') and page('div.taLnk.hvrIE6.fl')[0].get('onclick') or None
    print 'email', email
    telephone       = page('div.fl').text()
    telephone = telephone.split (' ')[0]
    print 'telephone', telephone

    website         = page('a.taLnk.hvrIE6') and page('a.taLnk.hvrIE6')[0].get('href') or None

    postal_code = None
    locality    = None
    try:
        for span in page('span.locality')[0].getchildren():
            if span.get('property') == 'v:postal-code': postal_code = span.text
            if span.get('property') == 'v:locality'   : city    = span.text

    except BaseException as e:
        print 'ERROR while parsing locality:', e

    try:
        email = email and email.split(',')[6].replace("'", '')
        print 'parsing email:', email  
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

    data['url']         = url
    data['name']        = restaurant_name
    #data['stars'] = stars
    data['address']     = street_address
    data['extended-address']     = extended_address  
    data['telephone']   = telephone
    data['postal_code'] = postal_code
    data['city']        = city
    data['country']     = country
    #data['lat']         = location and location[0]
    #data['lon']         = location and location[1]
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