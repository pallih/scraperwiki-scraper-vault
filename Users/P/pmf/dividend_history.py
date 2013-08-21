import scraperwiki
from BeautifulSoup import BeautifulSoup
from urllib2 import HTTPError
import datetime
import re

URL = 'http://www.stockopedia.co.uk/share-prices/%(market)s:%(symbol)s/dividends/'

help(scraperwiki.sqlite.save)

def main():
    for symbol in get_constituents('ASX'):
        url = URL % {'market': 'LON', 'symbol': symbol}
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
        table = find_table(soup) # returns None if genuinely no dividends
        if not table:
            print("No dividend for stock %s" % symbol)
            continue

        for data in extract_annual_dividends(table):
            data['symbol'] = symbol
            data['key'] = "%s:%s" % (data['symbol'], data['year'])
            scraperwiki.sqlite.save(table_name='annual_dividend', data=data, unique_keys=['key'])

def get_constituents(index_symbol):
    """Return a generator of stock symbols for the given LSE index symbol"""
    scraperwiki.sqlite.attach('lse_stock_index_constituents', 'indices')
    for result in scraperwiki.sqlite.select("lse_symbol from indices.%s" % index_symbol):
        # list of {'lse_symbol' : 'symbol'}
        yield result['lse_symbol']

def find_table(soup):
    tables = soup.findAll('table', attrs={'class': 'tablesorter'})
    if len(tables) != 1:
        if soup.find('span', text=re.compile('There have been no recent dividends.*')):
            return None
        else:
            raise RuntimeError("Failed to find single match for dividend <table> (%d matches)" % len(tables))
    return tables[0]

def extract_annual_dividends(table):
    column_numbers = decode_header_to_column_numbers(table)

    for tr in table.findChild('tbody').findAll('tr'):
        td_tags = tr.findAll('td')
        if len(td_tags) not in (6, 7):
            raise RuntimeError("Expected 6 or 7 columns, got %d" % len(td_tags))
        try:
            ex_date = td_tags[column_numbers['ex_dividend_date']].text
            total = td_tags[column_numbers['total']].text
            currency = td_tags[column_numbers['currency']].text
        except KeyError:
            raise RuntimeError("Failed to identify one of the columns from <th> headers")
        except IndexError:
            raise RuntimeError("Identified a column number which wasn't present in the table body.")

        if total:  # discard lines which don't contain a total
            yield {'year' : ex_date.split('-')[0],
                    'currency': currency,
                    'total': float(total)}

def decode_header_to_column_numbers(table):
    translation = {'Ex-Divi Date': 'ex_dividend_date',
                   'Pay Date': 'pay_date',
                   'Total': 'total',
                   'Dividend': 'dividend',
                   'Curr.': 'currency',
                   'Total': 'total'}

    names_to_cols = {}
    for (column_number, tr) in enumerate(table.findChild('thead').findAll('th')):
        if tr.text in translation:
            names_to_cols[translation[tr.text]] = column_number
    return names_to_cols

main()

