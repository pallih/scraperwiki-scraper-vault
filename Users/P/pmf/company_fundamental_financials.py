import scraperwiki
from BeautifulSoup import BeautifulSoup
from urllib2 import HTTPError
import datetime
import re

URL = 'http://uk.advfn.com/p.php?pid=financials&symbol=LSE:%(symbol)s'

# TODO: UPDATE fundamentals SET dividend_cover=eps_basic / dividend_ps WHERE dividend_cover ISNULL AND eps_basic NOTNULL AND dividend_ps NOTNULL AND dividend_ps > 0 AND eps_basic > 0

def main():
    for symbol in get_constituents('ASX'):
        url = URL % {'symbol': symbol}
        print("Downloading %s: %s" % (symbol, url))
        try:
            html = scraperwiki.scrape(url)
        except HTTPError, e:
            print("ERROR opening that URL.")
            scraperwiki.sqlite.save(
                table_name='errors',
                data={'url' : url,
                      'symbol' : symbol},
                unique_keys=['symbol', 'url'])
            continue
        
        soup = BeautifulSoup(html)
        key_figures_table = find_table(soup)
        
        fields = {'market_cap'              : ('Market Cap.', commafloat, None),
                  'pe_ratio'                : ('PE Ratio', commafloat, None),
                  'dividend_yield'          : ('Dividend Yield', commafloat, None),
                  'eps_basic'               : ('EPS - basic', commafloat, None),
                  'dividend_ps'             : ('Dividend PS', commafloat, None),
                  'dividend_cover'          : ('Dividend Cover', commafloat, None),
                  'cashflow_ps'             : ('Cash Flow PS', commafloat, None),
                  'return_on_equity'        : ('Return On Equity (ROE)', commafloat, None),
                  'operating_margin'        : ('Operating Margin', commafloat, None),
                  'peg_factor'              : ('PEG Factor', commafloat, None),
                  'eps_growth_rate'         : ('EPS Growth Rate', commafloat, None),
                  'dividend_ps_growth_rate' : ('Dividends PS Growth Rate', commafloat, None),
                  'net_debt'                : ('Net Debt', commafloat, None),
                  'gross_gearing'           : ('Gross Gearing', commafloat, None),
                  'quick_assets'            : ('Quick Assets', commafloat, None),
                  'net_working_capital'     : ('Net Working Capital', commafloat, None),
                  'fixed_assets'            : ('Intangibles&nbsp;/&nbsp;Fixed Assets', commafloat, None),
                  'turnover_ps'             : ('Turnover PS', commafloat, None),
                  'pretax_profit_ps'        : ('Pre-Tax Profit PS', commafloat, None),
                  'retained_profit_ps'      : ('Retained Profit PS', commafloat, None),
                  'cash_ps'                 : ('Cash PS', commafloat, None),
                  'net_cash_ps'             : ('Net Cash PS', commafloat, None),
                  'net_tangible_asset_value_ps' : ('Net Tangible Asset Value PS&nbsp;*', commafloat, None),
                  'net_asset_value_ps'      : ('Net Asset Value PS', commafloat, None),
                  'spread'                  : ('Spread', decode_spread, None),
            } # TODO: more of these!

        data = {'symbol' : symbol,
                'url' : url}        
        for (field, (descriptor, func, default)) in fields.items():
            data[field] = extract_table_value(key_figures_table, descriptor, func, default)
        
        data['ep_ratio'] = calculate_ep_ratio(data['pe_ratio'])
        (sector_name, sector_id) = extract_industry_sector(soup)
        data['industry_sector'] = sector_name
        data['industry_sector_id'] = sector_id

        scraperwiki.sqlite.save(
            table_name='fundamentals',
            data=data,
            unique_keys=['symbol'])

def get_constituents(index_symbol):
    """Return a generator of stock symbols for the given LSE index symbol"""
    scraperwiki.sqlite.attach('lse_stock_index_constituents', 'indices')
    for result in scraperwiki.sqlite.select("lse_symbol from indices.%s" % index_symbol):
        # list of {'lse_symbol' : 'symbol'}
        yield result['lse_symbol']

def find_table(soup):
    market_cap_a_tag = soup.find('a', attrs={'href':'/Help/market-capitalisation-119.html'})
    if not market_cap_a_tag:
        raise RuntimeError("Failed to find 'Market Cap.' a tag in main table.")
    return market_cap_a_tag.findParent('table')

def extract_table_value(table, descriptor, translation_func, default_value):
    a_tag = table.find('a', text=descriptor)
    if not a_tag:
        raise RuntimeError("Failed to find <a> tag in table with text '%s'" % descriptor)
    descriptor_td = a_tag.findParent('td')
    
    if not descriptor_td:
        raise RuntimeError("Failed to find parent <td> tag of <a>%s</a>" % descriptor)

    value_td = descriptor_td.findNextSibling('td')
    if not value_td:
        raise RuntimeError("Failed to find net sibling <td> tag containing value for %s" % descriptor)
    
    if value_td.text == '-':
        value = default_value
    else:
        return translation_func(value_td.text)

SECTOR_HREF_RE = re.compile(r'/p.php\?pid=morebysector.*sectorid\=(\d+).*$')
def extract_industry_sector(soup):
    sector_a_tag = soup.find('a', attrs={'href' : SECTOR_HREF_RE})
    if not sector_a_tag:
        print("Failed to find market sector <a> tag.")
        return (None, None)
    
    sector_text = sector_a_tag.findPreviousSibling('span').text.replace(r'\n', ' ')
    match = SECTOR_HREF_RE.match(sector_a_tag['href'])
    if match:
        sector_id = int(match.groups()[0])
    else:
        sector_id = None
    return (sector_text, sector_id)
        

def commafloat(text):
    return float(text.replace(',', ''))

def commaint(text):
    return int(text.replace(',', ''))

SPREAD_VALUE_RE = re.compile(r'.+&nbsp;\((.+)%\)')
def decode_spread(text):
    match = SPREAD_VALUE_RE.match(text)
    if match:
        return commafloat(match.groups()[0])

def calculate_ep_ratio(pe_ratio):
    if pe_ratio is None:
        return 0.0  # pe is infinity due to no earnings
    else:
        return 1.0 / pe_ratio

main()

import scraperwiki
from BeautifulSoup import BeautifulSoup
from urllib2 import HTTPError
import datetime
import re

URL = 'http://uk.advfn.com/p.php?pid=financials&symbol=LSE:%(symbol)s'

# TODO: UPDATE fundamentals SET dividend_cover=eps_basic / dividend_ps WHERE dividend_cover ISNULL AND eps_basic NOTNULL AND dividend_ps NOTNULL AND dividend_ps > 0 AND eps_basic > 0

def main():
    for symbol in get_constituents('ASX'):
        url = URL % {'symbol': symbol}
        print("Downloading %s: %s" % (symbol, url))
        try:
            html = scraperwiki.scrape(url)
        except HTTPError, e:
            print("ERROR opening that URL.")
            scraperwiki.sqlite.save(
                table_name='errors',
                data={'url' : url,
                      'symbol' : symbol},
                unique_keys=['symbol', 'url'])
            continue
        
        soup = BeautifulSoup(html)
        key_figures_table = find_table(soup)
        
        fields = {'market_cap'              : ('Market Cap.', commafloat, None),
                  'pe_ratio'                : ('PE Ratio', commafloat, None),
                  'dividend_yield'          : ('Dividend Yield', commafloat, None),
                  'eps_basic'               : ('EPS - basic', commafloat, None),
                  'dividend_ps'             : ('Dividend PS', commafloat, None),
                  'dividend_cover'          : ('Dividend Cover', commafloat, None),
                  'cashflow_ps'             : ('Cash Flow PS', commafloat, None),
                  'return_on_equity'        : ('Return On Equity (ROE)', commafloat, None),
                  'operating_margin'        : ('Operating Margin', commafloat, None),
                  'peg_factor'              : ('PEG Factor', commafloat, None),
                  'eps_growth_rate'         : ('EPS Growth Rate', commafloat, None),
                  'dividend_ps_growth_rate' : ('Dividends PS Growth Rate', commafloat, None),
                  'net_debt'                : ('Net Debt', commafloat, None),
                  'gross_gearing'           : ('Gross Gearing', commafloat, None),
                  'quick_assets'            : ('Quick Assets', commafloat, None),
                  'net_working_capital'     : ('Net Working Capital', commafloat, None),
                  'fixed_assets'            : ('Intangibles&nbsp;/&nbsp;Fixed Assets', commafloat, None),
                  'turnover_ps'             : ('Turnover PS', commafloat, None),
                  'pretax_profit_ps'        : ('Pre-Tax Profit PS', commafloat, None),
                  'retained_profit_ps'      : ('Retained Profit PS', commafloat, None),
                  'cash_ps'                 : ('Cash PS', commafloat, None),
                  'net_cash_ps'             : ('Net Cash PS', commafloat, None),
                  'net_tangible_asset_value_ps' : ('Net Tangible Asset Value PS&nbsp;*', commafloat, None),
                  'net_asset_value_ps'      : ('Net Asset Value PS', commafloat, None),
                  'spread'                  : ('Spread', decode_spread, None),
            } # TODO: more of these!

        data = {'symbol' : symbol,
                'url' : url}        
        for (field, (descriptor, func, default)) in fields.items():
            data[field] = extract_table_value(key_figures_table, descriptor, func, default)
        
        data['ep_ratio'] = calculate_ep_ratio(data['pe_ratio'])
        (sector_name, sector_id) = extract_industry_sector(soup)
        data['industry_sector'] = sector_name
        data['industry_sector_id'] = sector_id

        scraperwiki.sqlite.save(
            table_name='fundamentals',
            data=data,
            unique_keys=['symbol'])

def get_constituents(index_symbol):
    """Return a generator of stock symbols for the given LSE index symbol"""
    scraperwiki.sqlite.attach('lse_stock_index_constituents', 'indices')
    for result in scraperwiki.sqlite.select("lse_symbol from indices.%s" % index_symbol):
        # list of {'lse_symbol' : 'symbol'}
        yield result['lse_symbol']

def find_table(soup):
    market_cap_a_tag = soup.find('a', attrs={'href':'/Help/market-capitalisation-119.html'})
    if not market_cap_a_tag:
        raise RuntimeError("Failed to find 'Market Cap.' a tag in main table.")
    return market_cap_a_tag.findParent('table')

def extract_table_value(table, descriptor, translation_func, default_value):
    a_tag = table.find('a', text=descriptor)
    if not a_tag:
        raise RuntimeError("Failed to find <a> tag in table with text '%s'" % descriptor)
    descriptor_td = a_tag.findParent('td')
    
    if not descriptor_td:
        raise RuntimeError("Failed to find parent <td> tag of <a>%s</a>" % descriptor)

    value_td = descriptor_td.findNextSibling('td')
    if not value_td:
        raise RuntimeError("Failed to find net sibling <td> tag containing value for %s" % descriptor)
    
    if value_td.text == '-':
        value = default_value
    else:
        return translation_func(value_td.text)

SECTOR_HREF_RE = re.compile(r'/p.php\?pid=morebysector.*sectorid\=(\d+).*$')
def extract_industry_sector(soup):
    sector_a_tag = soup.find('a', attrs={'href' : SECTOR_HREF_RE})
    if not sector_a_tag:
        print("Failed to find market sector <a> tag.")
        return (None, None)
    
    sector_text = sector_a_tag.findPreviousSibling('span').text.replace(r'\n', ' ')
    match = SECTOR_HREF_RE.match(sector_a_tag['href'])
    if match:
        sector_id = int(match.groups()[0])
    else:
        sector_id = None
    return (sector_text, sector_id)
        

def commafloat(text):
    return float(text.replace(',', ''))

def commaint(text):
    return int(text.replace(',', ''))

SPREAD_VALUE_RE = re.compile(r'.+&nbsp;\((.+)%\)')
def decode_spread(text):
    match = SPREAD_VALUE_RE.match(text)
    if match:
        return commafloat(match.groups()[0])

def calculate_ep_ratio(pe_ratio):
    if pe_ratio is None:
        return 0.0  # pe is infinity due to no earnings
    else:
        return 1.0 / pe_ratio

main()

