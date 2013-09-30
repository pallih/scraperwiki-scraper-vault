# encoding=utf-8
"""
To fetch prices in different currencies, we need to fetch the game details
page from a UK, US and European IP address. This is done by using public
open proxies. I hope they don't mind, this is a quite legitimate and
purposeful activity compared to most of their users. :)
"""

import scraperwiki
import lxml.html
import urllib, urllib2
import re

# God damn. I'd use CoDeeN proxies here (http://codeen.cs.princeton.edu/),
# but ScraperWiki admins block port 3128
#
# So we have to do with shady CGI proxies on port 80
# If these break, get new ones from:
# http://www.publicproxyservers.com/proxy/list_uptime1.html

eu_proxy = 'http://2bgoodproxy.uk.tc/browse.php?u=%s'
us_proxy = 'http://alivebyspeed.info/browse.php?u=%s'

####
# Functions to set/get crawling state for next run

def set_state(key, value):
    scraperwiki.sqlite.save(unique_keys=['key'], data={'key': key, 'value': value}, table_name='state')

def get_state(key, default):
    try:
        res = scraperwiki.sqlite.select('value from state where key=?', key)
    except scraperwiki.sqlite.NoSuchTableSqliteError:
        return default

    if res:
        return res[0]['value']

    return default

#### GAMES INDEX

known_games = set()
games_list = [] # duplicated to retain ordering
TESTING = False

def fetch_index_page(page):
    global known_games, games_list
    count = 0

    html = scraperwiki.scrape('http://www.desura.com/games/browse/page/%d' % page)
    root = lxml.html.fromstring(html)

    for row in root.cssselect('div.row h4 a'):
        parts = row.get('href').split('/')
        assert parts[0] == '' and parts[1] == 'games', "parts=%r" % parts
        slug = parts[2]

        if slug in known_games:
            # We've already seen this game -- reached the last page
            return 0
        known_games.add(slug)
        games_list.append(slug)

        #data = {
        #    'slug': slug,
        #    'name': row.text_content(),
        #}
        count += 1
        #print 'page', page, 'row', data

        #scraperwiki.sqlite.save(unique_keys=['slug'], data=data, table_name='index')

    print "Page %d: %d games" % (page, count)
    return count

def fetch_games_index():
    if TESTING:
        maxpages = 2
    else:
        maxpages = 300 # sanity limit

    for i in xrange(1, maxpages):
        count = fetch_index_page(i)
        if count == 0:
            break

#### GAME DETAILS

digit_re = re.compile(r'-?[,.0-9]+')
def clean_number(text):
    l = digit_re.findall(text)
    if not l:
        return None
    # ',' is used as a thousands separator
    number = l[0].replace(',', '')
    return number

attr_name_re = re.compile(r'[^a-z]+')
def attr_name(text):
    return attr_name_re.sub('_', text.lower())

def get_el_text(el, selector):
    elements = el.cssselect(selector)
    if not elements:
        return None
    return elements[0].text_content().strip()

def get_el_bool(el, selector):
    elements = el.cssselect(selector)
    if elements:
        return 'yes'
    else:
        return 'no'

def store_attr(data, key, value_el):
    key = attr_name(key)
    value = value_el.text_content().strip()

    if not key:
        return

    # No useful data here
    if key == 'contact':
        return

    # plural/singular depending on value; normalize to plural
    if key == 'platform':
        key = 'platforms'

    # normalize
    elif key == 'developer_publisher':
        key = 'developer'

    # use URL instead of link title
    elif key == 'official_page':
        a = value_el.cssselect('a')
        if a:
            value = a[0].get('href')
        else:
            value = None

    # parse numeric fields
    elif key in ['rank', 'watchers', 'visits', 'news', 'reviews', 'files', 'mods', 'addons']:
        value = clean_number(value)

    # Store value
    if value:
        data['attr_' + key] = value

def store_price(data, root):
    # XXX There may be multiple prices for different versions; we only use the 1st one
    price_el = root.cssselect('.price')
    if not price_el:
        return

    price_el = price_el[0]

    # Don't use the "sale price" -- original price is in the <span>
    # <span class="price"><span>7,39€</span>6,65€</span>
    # Original price was 7.39, current sale price 6.65
    if price_el.cssselect('.price span'):
        price_el = price_el.cssselect('.price span')[0]

    # Other values use ',' as thousands separator, but price uses it as decimal point. Fix it up
    price = price_el.text_content().replace(',', '.')
    amount = clean_number(price)
    if u'€' in price:
        data['price_eur'] = amount
    elif '$' in price:
        data['price_usd'] = amount
    elif u'£' in price:
        data['price_gbp'] = amount
    else:
        print "Warning: Price in unknown currency: %s" % price
        data['price'] = amount

# We need to use a proxy to get the price in other currencies.
# This is crude, but we really want those prices!
def store_fetch_other_prices(data, url):
    for proxy in [eu_proxy, us_proxy]:
        #html = urllib.urlopen(url, proxies={'http': 'http://' + proxy}).read()
        #html = scraperwiki.scrape(proxy % urllib.quote(url))

        req = urllib2.Request(proxy % urllib.quote(url))
        req.add_header('Referer', proxy % '') # These proxies need Referer header
        html = urllib2.urlopen(req).read()

        root = lxml.html.fromstring(html)
        store_price(data, root)

def fetch_game_page(slug):
    url = 'http://www.desura.com/games/%s' % slug
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    data = {}
    data['slug']  = slug
    data['title'] = get_el_text(root, '.title h2')
    data['score'] = clean_number(get_el_text(root, '.tablerating .score'))
    data['platform_windows'] = get_el_bool(root, '.platformpc')
    data['platform_linux']   = get_el_bool(root, '.platformlinux')
    data['platform_linux64'] = get_el_bool(root, '.platformlinux64')

    store_price(data, root)
    store_fetch_other_prices(data, url)

    for attr in root.cssselect('.tablemenu .row'):
        key = get_el_text(attr, 'h5')
        value_el = attr.cssselect('.summary')

        if key and value_el:
            store_attr(data, key, value_el[0])

    print slug, data
    scraperwiki.sqlite.save(unique_keys=['slug'], data=data, table_name='game')

def fetch_game_details():
    last_idx = get_state('last_game', 0)

    for i, slug in enumerate(games_list):
        # This is a bit crude. Indexes can change if the list page changes.
        # However, it's better than nothing
        if i < last_idx:
            continue

        fetch_game_page(slug)
        set_state('last_game', i)

    # Done: next time start from beginning
    set_state('last_game', 0)

#### MAIN

fetch_games_index()
fetch_game_details()

# encoding=utf-8
"""
To fetch prices in different currencies, we need to fetch the game details
page from a UK, US and European IP address. This is done by using public
open proxies. I hope they don't mind, this is a quite legitimate and
purposeful activity compared to most of their users. :)
"""

import scraperwiki
import lxml.html
import urllib, urllib2
import re

# God damn. I'd use CoDeeN proxies here (http://codeen.cs.princeton.edu/),
# but ScraperWiki admins block port 3128
#
# So we have to do with shady CGI proxies on port 80
# If these break, get new ones from:
# http://www.publicproxyservers.com/proxy/list_uptime1.html

eu_proxy = 'http://2bgoodproxy.uk.tc/browse.php?u=%s'
us_proxy = 'http://alivebyspeed.info/browse.php?u=%s'

####
# Functions to set/get crawling state for next run

def set_state(key, value):
    scraperwiki.sqlite.save(unique_keys=['key'], data={'key': key, 'value': value}, table_name='state')

def get_state(key, default):
    try:
        res = scraperwiki.sqlite.select('value from state where key=?', key)
    except scraperwiki.sqlite.NoSuchTableSqliteError:
        return default

    if res:
        return res[0]['value']

    return default

#### GAMES INDEX

known_games = set()
games_list = [] # duplicated to retain ordering
TESTING = False

def fetch_index_page(page):
    global known_games, games_list
    count = 0

    html = scraperwiki.scrape('http://www.desura.com/games/browse/page/%d' % page)
    root = lxml.html.fromstring(html)

    for row in root.cssselect('div.row h4 a'):
        parts = row.get('href').split('/')
        assert parts[0] == '' and parts[1] == 'games', "parts=%r" % parts
        slug = parts[2]

        if slug in known_games:
            # We've already seen this game -- reached the last page
            return 0
        known_games.add(slug)
        games_list.append(slug)

        #data = {
        #    'slug': slug,
        #    'name': row.text_content(),
        #}
        count += 1
        #print 'page', page, 'row', data

        #scraperwiki.sqlite.save(unique_keys=['slug'], data=data, table_name='index')

    print "Page %d: %d games" % (page, count)
    return count

def fetch_games_index():
    if TESTING:
        maxpages = 2
    else:
        maxpages = 300 # sanity limit

    for i in xrange(1, maxpages):
        count = fetch_index_page(i)
        if count == 0:
            break

#### GAME DETAILS

digit_re = re.compile(r'-?[,.0-9]+')
def clean_number(text):
    l = digit_re.findall(text)
    if not l:
        return None
    # ',' is used as a thousands separator
    number = l[0].replace(',', '')
    return number

attr_name_re = re.compile(r'[^a-z]+')
def attr_name(text):
    return attr_name_re.sub('_', text.lower())

def get_el_text(el, selector):
    elements = el.cssselect(selector)
    if not elements:
        return None
    return elements[0].text_content().strip()

def get_el_bool(el, selector):
    elements = el.cssselect(selector)
    if elements:
        return 'yes'
    else:
        return 'no'

def store_attr(data, key, value_el):
    key = attr_name(key)
    value = value_el.text_content().strip()

    if not key:
        return

    # No useful data here
    if key == 'contact':
        return

    # plural/singular depending on value; normalize to plural
    if key == 'platform':
        key = 'platforms'

    # normalize
    elif key == 'developer_publisher':
        key = 'developer'

    # use URL instead of link title
    elif key == 'official_page':
        a = value_el.cssselect('a')
        if a:
            value = a[0].get('href')
        else:
            value = None

    # parse numeric fields
    elif key in ['rank', 'watchers', 'visits', 'news', 'reviews', 'files', 'mods', 'addons']:
        value = clean_number(value)

    # Store value
    if value:
        data['attr_' + key] = value

def store_price(data, root):
    # XXX There may be multiple prices for different versions; we only use the 1st one
    price_el = root.cssselect('.price')
    if not price_el:
        return

    price_el = price_el[0]

    # Don't use the "sale price" -- original price is in the <span>
    # <span class="price"><span>7,39€</span>6,65€</span>
    # Original price was 7.39, current sale price 6.65
    if price_el.cssselect('.price span'):
        price_el = price_el.cssselect('.price span')[0]

    # Other values use ',' as thousands separator, but price uses it as decimal point. Fix it up
    price = price_el.text_content().replace(',', '.')
    amount = clean_number(price)
    if u'€' in price:
        data['price_eur'] = amount
    elif '$' in price:
        data['price_usd'] = amount
    elif u'£' in price:
        data['price_gbp'] = amount
    else:
        print "Warning: Price in unknown currency: %s" % price
        data['price'] = amount

# We need to use a proxy to get the price in other currencies.
# This is crude, but we really want those prices!
def store_fetch_other_prices(data, url):
    for proxy in [eu_proxy, us_proxy]:
        #html = urllib.urlopen(url, proxies={'http': 'http://' + proxy}).read()
        #html = scraperwiki.scrape(proxy % urllib.quote(url))

        req = urllib2.Request(proxy % urllib.quote(url))
        req.add_header('Referer', proxy % '') # These proxies need Referer header
        html = urllib2.urlopen(req).read()

        root = lxml.html.fromstring(html)
        store_price(data, root)

def fetch_game_page(slug):
    url = 'http://www.desura.com/games/%s' % slug
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    data = {}
    data['slug']  = slug
    data['title'] = get_el_text(root, '.title h2')
    data['score'] = clean_number(get_el_text(root, '.tablerating .score'))
    data['platform_windows'] = get_el_bool(root, '.platformpc')
    data['platform_linux']   = get_el_bool(root, '.platformlinux')
    data['platform_linux64'] = get_el_bool(root, '.platformlinux64')

    store_price(data, root)
    store_fetch_other_prices(data, url)

    for attr in root.cssselect('.tablemenu .row'):
        key = get_el_text(attr, 'h5')
        value_el = attr.cssselect('.summary')

        if key and value_el:
            store_attr(data, key, value_el[0])

    print slug, data
    scraperwiki.sqlite.save(unique_keys=['slug'], data=data, table_name='game')

def fetch_game_details():
    last_idx = get_state('last_game', 0)

    for i, slug in enumerate(games_list):
        # This is a bit crude. Indexes can change if the list page changes.
        # However, it's better than nothing
        if i < last_idx:
            continue

        fetch_game_page(slug)
        set_state('last_game', i)

    # Done: next time start from beginning
    set_state('last_game', 0)

#### MAIN

fetch_games_index()
fetch_game_details()

