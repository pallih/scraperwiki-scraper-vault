INDICES = [
    'UKX',   # FTSE 100
    'MCX',   # FTSE 250
    'NMX',   # FTSE 350 (100 + 250)
    'ASX',   # FTSE AllShare
    'SMX',   # FTSE SmallCap
    'E3X',   # FTSE Eurotop 300
    'AIM5',  # FTSE AIM UK 50
    'AIM1',  # FTSE AIM 100
    'AXX',   # FTSE AIM AllShare
    'T1X',   # FTSE techMARK Focus
    'TASX',  # FTSE techMARK AllShare
]

import scraperwiki
import re
import time
from BeautifulSoup import BeautifulSoup

USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:16.0) Gecko/20100101 Firefox/16.0'
BASE_URL = 'http://www.londonstockexchange.com'
CONSTITUENT_URL = (BASE_URL + '/exchange/prices-and-markets'
                   '/stocks/indices/constituents-indices.html?index=%(index_symbol)s&page=%(page)s')

STOCK_URL = (BASE_URL + '/exchange/prices-and-markets'
             '/stocks/summary/company-summary.html?fourWayKey=%(lse_key)s')

def main():
    nuke_tables()
    for index_symbol in INDICES:
        scrape_index(index_symbol)

def nuke_tables():
    for symbol in INDICES:
        scraperwiki.sqlite.execute("drop table if exists %s" % symbol)
    
    scraperwiki.sqlite.commit()

def scrape_index(index_symbol):
    current_page = 1
    while True:
        results_this_page = 0
        url = CONSTITUENT_URL % {'index_symbol': index_symbol,
                                 'page': current_page}
        print("Downloading %s page %s: %s" % (index_symbol, current_page, url))
        html = scraperwiki.scrape(url, user_agent=USER_AGENT)
        soup = BeautifulSoup(html)

        table = soup.find('table')
        if not table:
            raise RuntimeError("Failed to find matching table of companies.")
        
        for tr in find_stock_trs(table):
            lse_key = extract_four_way_key(tr)
            data = {'lse_symbol': extract_symbol(tr),
                    'company_name': extract_name(tr),
                    'lse_key': lse_key,
                    'url': STOCK_URL % {'lse_key' : lse_key},
                    }
            scraperwiki.sqlite.save(
                table_name=index_symbol,
                unique_keys=['lse_symbol', 'lse_key'],
                data=data)
            results_this_page += 1

        print("Got %d results." % results_this_page)
        current_page += 1        

        if detect_last_page(soup):
            print("I think that was the last page of data. Exiting.")
            break


def find_stock_trs(table):
    """
    Find the <tr> by looking for a specific <a> used for each stock, then yield the
    parent <tr>
    """
    stock_a_tags = table.findAll('a', attrs={'title' : 'View detailed prices page'})
    if not stock_a_tags:
        raise RuntimeError("Failed to find any table rows from matching <a> tags")
    for a_tag in stock_a_tags:
        yield a_tag.findParent('tr')

def extract_name(tr):
    return tr.find('a', attrs={'title' : 'View detailed prices page'}).text

def extract_symbol(tr):
    return tr.find('td', attrs={'scope' : 'row', 'class': 'name'}).text

KEY_RE = re.compile(r'/exchange/prices-and-markets/stocks/summary/company-summary.html\?fourWayKey=(.+)')
def extract_four_way_key(tr):
    a_tag = tr.find('a', attrs={'href': KEY_RE})
    match = KEY_RE.match(a_tag['href'])
    if match:
        return match.groups()[0]
    else:
        raise RuntimeError("Couldn't find fourWayKey <a> tag.")

PAGE_RE = re.compile(r'&nbsp;Page (\d+) of (\d+)')
def detect_last_page(soup):
    """
    <p class="floatsx">&nbsp;Page 1 of 6</p>
    """
    page_x_of_y = soup.find('p', text=PAGE_RE)
    if page_x_of_y is None:
        raise RuntimeError("Failed to find page number text (ie 1 of 6) from page")
    match = PAGE_RE.match(page_x_of_y)
    if not match:
        raise RuntimeError("Failed to extract page number (ie 1 of 6) from text")
    current_page = int(match.groups()[0])
    total_pages = int(match.groups()[1])
    
    print("Site reported page %d of %s." % (current_page, total_pages))
    if current_page == total_pages:
        return True

main()
INDICES = [
    'UKX',   # FTSE 100
    'MCX',   # FTSE 250
    'NMX',   # FTSE 350 (100 + 250)
    'ASX',   # FTSE AllShare
    'SMX',   # FTSE SmallCap
    'E3X',   # FTSE Eurotop 300
    'AIM5',  # FTSE AIM UK 50
    'AIM1',  # FTSE AIM 100
    'AXX',   # FTSE AIM AllShare
    'T1X',   # FTSE techMARK Focus
    'TASX',  # FTSE techMARK AllShare
]

import scraperwiki
import re
import time
from BeautifulSoup import BeautifulSoup

USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:16.0) Gecko/20100101 Firefox/16.0'
BASE_URL = 'http://www.londonstockexchange.com'
CONSTITUENT_URL = (BASE_URL + '/exchange/prices-and-markets'
                   '/stocks/indices/constituents-indices.html?index=%(index_symbol)s&page=%(page)s')

STOCK_URL = (BASE_URL + '/exchange/prices-and-markets'
             '/stocks/summary/company-summary.html?fourWayKey=%(lse_key)s')

def main():
    nuke_tables()
    for index_symbol in INDICES:
        scrape_index(index_symbol)

def nuke_tables():
    for symbol in INDICES:
        scraperwiki.sqlite.execute("drop table if exists %s" % symbol)
    
    scraperwiki.sqlite.commit()

def scrape_index(index_symbol):
    current_page = 1
    while True:
        results_this_page = 0
        url = CONSTITUENT_URL % {'index_symbol': index_symbol,
                                 'page': current_page}
        print("Downloading %s page %s: %s" % (index_symbol, current_page, url))
        html = scraperwiki.scrape(url, user_agent=USER_AGENT)
        soup = BeautifulSoup(html)

        table = soup.find('table')
        if not table:
            raise RuntimeError("Failed to find matching table of companies.")
        
        for tr in find_stock_trs(table):
            lse_key = extract_four_way_key(tr)
            data = {'lse_symbol': extract_symbol(tr),
                    'company_name': extract_name(tr),
                    'lse_key': lse_key,
                    'url': STOCK_URL % {'lse_key' : lse_key},
                    }
            scraperwiki.sqlite.save(
                table_name=index_symbol,
                unique_keys=['lse_symbol', 'lse_key'],
                data=data)
            results_this_page += 1

        print("Got %d results." % results_this_page)
        current_page += 1        

        if detect_last_page(soup):
            print("I think that was the last page of data. Exiting.")
            break


def find_stock_trs(table):
    """
    Find the <tr> by looking for a specific <a> used for each stock, then yield the
    parent <tr>
    """
    stock_a_tags = table.findAll('a', attrs={'title' : 'View detailed prices page'})
    if not stock_a_tags:
        raise RuntimeError("Failed to find any table rows from matching <a> tags")
    for a_tag in stock_a_tags:
        yield a_tag.findParent('tr')

def extract_name(tr):
    return tr.find('a', attrs={'title' : 'View detailed prices page'}).text

def extract_symbol(tr):
    return tr.find('td', attrs={'scope' : 'row', 'class': 'name'}).text

KEY_RE = re.compile(r'/exchange/prices-and-markets/stocks/summary/company-summary.html\?fourWayKey=(.+)')
def extract_four_way_key(tr):
    a_tag = tr.find('a', attrs={'href': KEY_RE})
    match = KEY_RE.match(a_tag['href'])
    if match:
        return match.groups()[0]
    else:
        raise RuntimeError("Couldn't find fourWayKey <a> tag.")

PAGE_RE = re.compile(r'&nbsp;Page (\d+) of (\d+)')
def detect_last_page(soup):
    """
    <p class="floatsx">&nbsp;Page 1 of 6</p>
    """
    page_x_of_y = soup.find('p', text=PAGE_RE)
    if page_x_of_y is None:
        raise RuntimeError("Failed to find page number text (ie 1 of 6) from page")
    match = PAGE_RE.match(page_x_of_y)
    if not match:
        raise RuntimeError("Failed to extract page number (ie 1 of 6) from text")
    current_page = int(match.groups()[0])
    total_pages = int(match.groups()[1])
    
    print("Site reported page %d of %s." % (current_page, total_pages))
    if current_page == total_pages:
        return True

main()
