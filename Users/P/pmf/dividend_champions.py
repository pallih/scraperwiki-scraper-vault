# Blank Python

import scraperwiki
scraperwiki.sqlite.attach("investment_analysis", 'analysis')
scraperwiki.sqlite.attach("dividend_history", 'dividends')
scraperwiki.sqlite.attach('company_fundamental_financials', 'fundamentals')
scraperwiki.sqlite.attach('lse_stock_index_constituents', 'indices')

from collections import namedtuple
DividendYear = namedtuple('DividendYear', 'year total growth growth_adjusted')


ADVFN_URL = 'http://uk.advfn.com/p.php?pid=financials&symbol=LSE:%(symbol)s'

def main():
    query = ('`ASX`.`url`, `dividend_analysis`.*, `fundamentals`.*, `pe_deciles`.* '
             'FROM `indices`.`ASX` '
             'INNER JOIN `fundamentals`.`fundamentals` '
             'ON `ASX`.`lse_symbol` = `fundamentals`.`symbol` '
             'INNER JOIN `analysis`.`dividend_analysis` '
             'ON `ASX`.`lse_symbol` = `dividend_analysis`.`symbol` '
             'INNER JOIN `analysis`.`pe_deciles` '
             'ON `ASX`.`lse_symbol` = `pe_deciles`.`symbol` '
             'WHERE `fundamentals`.`dividend_cover` > 1.5 '
             'AND `fundamentals`.`dividend_yield` > 4 '
             'AND `pe_deciles`.`decile_ASX` <= 2 '
             'AND `dividend_analysis`.`divi_cagr_5yr` > 3.0 '
             'ORDER BY `dividend_analysis`.`years_growth_0pct` DESC')
    
    print('<html>'
          '<head><link rel="stylesheet" href="https://github.com/necolas/'
          'normalize.css/blob/master/normalize.css" type="text/css" media="screen" />'
          '</head>'
          '<body><h1>Dividend Champions</h1>'
          '<table style="text-align: left;">'
          '<thead>'
          '<tr>'
          '<th>Stock Ticker</th>'
          '<th>Price/Earnings (P/E)</th>'
          '<th>P/E Decile (AllShare)</th>'
          '<th>P/E Decile (industry)</th>'
          '<th>Dividend yield</th>'
          '<th>Dividend cover</th>'
          '<th>Years of dividend increases</th>'
          '<th>Years of dividend increases (5%)</th>'
          '<th>Five-year dividend CAGR</th>'
          '<th>Projected Dividend Yield (3 years)</th>'
          '</tr>'
          '<tbody>')

    for result in scraperwiki.sqlite.select(query):    
        print("<tr>")
        symbol = result['symbol']
        print("<td><a href='%s'>%s</a></td>" % (ADVFN_URL % {'symbol' : symbol}, symbol))
        print("<td>%.1f</td>" % result['pe_ratio'])
        print("<td>%s</td>" % result['decile_ASX'])
        print("<td>%s</td>" % result['decile_industry'])
        print("<td>%.1f %%</td>" % result['dividend_yield'])
        print("<td>%.1f</td>" % result['dividend_cover'])
        print("<td>%d</td>" % result['years_growth_0pct'])
        print("<td>%d</td>" % result['years_growth_5pct'])
        print("<td>%.1f %%</td>" % result['divi_cagr_5yr'])
        print("<td>%.1f %%</td>" % compound(result['dividend_yield'], result['divi_cagr_5yr'], 3))
        print("</tr>")
    print("</tbody></table></html>")    
    
    for result in scraperwiki.sqlite.select(query):
        symbol = result['symbol']
        display_dividend_table(symbol, get_dividend_totals(symbol))                

def compound(number, annual_percent, years):
    cagr = 1.0 + (0.01 * annual_percent)  # ie cagr = 1.1 = 10% p.a.
    return number * (cagr ** years)

def display_dividend_table(symbol, dividends):
    print("<table style='font-size: 12; width:200px' border='1'>"
           "<tr><th colspan='3'>%s dividends</tr>"
           "<tr><th>Year</th><th>Dividend</th><th>Growth</th></tr>"% symbol)
    for entry in dividends:
        print("<tr>")
        print("<td>%s</td>" % entry.year)
        print("<td>%.2f</td>" % entry.total)
        if entry.growth is not None:
            print("<td>%.1f%%</td>" % (100 * entry.growth,))
        else:
            print("<td>-</td>")
        print("</tr>")
    print("</table>")

def get_dividend_totals(symbol):
    """Return a list of DividendYear namedtuples, ordered by most recent year"""
    
    totals = {}
    previous_currency = None
    for result in scraperwiki.sqlite.select("symbol,year,total,currency from dividends.annual_dividend "
                                          "where symbol='%s' ORDER BY year ASC" % symbol):
        totals[int(result['year'])] = float(result['total'])
        currency = result['currency']
        if previous_currency is not None and currency != previous_currency:
            return []
        previous_currency = currency
    
    totals = fill_missing_years(totals)
    dividends = []  # DividendYear
    previous_total = None
        
    for year in sorted(totals.iterkeys()):
        total = totals[year]
        (growth, growth_adjusted) = calculate_growth(total, previous_total)
        
        previous_total = total
        dividends.append(DividendYear(
                             year=year,
                             total=totals[year],
                             growth=growth,
                             growth_adjusted=growth_adjusted))
    return list(reversed(dividends))

def calculate_growth(total, previous_total):
    if previous_total:
        growth = (total - previous_total) / previous_total
    else:
        growth = None

    return (growth, calculate_adjusted_growth(growth))

def calculate_adjusted_growth(growth):
    if growth is not None:
        return growth - 0.03

def fill_missing_years(totals):
    """Populate zeroes into years without a dividend payment record."""
    last_definite_year = 2012
    for year in xrange(min(totals.keys()), 2012 + 1):
        if year not in totals:
            totals[year] = 0.0
    return totals

def _calculate_growth(dividends, years):
    now = 2012
    try:
        growth = 1 + (dividends[now] - dividends[now - years]) / dividends[now - years]
        growth_cagr = (growth ** (1.0 / years)) - 1
    except KeyError:
        growth_cagr = 0.0

    return growth_cagr


main()
# Blank Python

import scraperwiki
scraperwiki.sqlite.attach("investment_analysis", 'analysis')
scraperwiki.sqlite.attach("dividend_history", 'dividends')
scraperwiki.sqlite.attach('company_fundamental_financials', 'fundamentals')
scraperwiki.sqlite.attach('lse_stock_index_constituents', 'indices')

from collections import namedtuple
DividendYear = namedtuple('DividendYear', 'year total growth growth_adjusted')


ADVFN_URL = 'http://uk.advfn.com/p.php?pid=financials&symbol=LSE:%(symbol)s'

def main():
    query = ('`ASX`.`url`, `dividend_analysis`.*, `fundamentals`.*, `pe_deciles`.* '
             'FROM `indices`.`ASX` '
             'INNER JOIN `fundamentals`.`fundamentals` '
             'ON `ASX`.`lse_symbol` = `fundamentals`.`symbol` '
             'INNER JOIN `analysis`.`dividend_analysis` '
             'ON `ASX`.`lse_symbol` = `dividend_analysis`.`symbol` '
             'INNER JOIN `analysis`.`pe_deciles` '
             'ON `ASX`.`lse_symbol` = `pe_deciles`.`symbol` '
             'WHERE `fundamentals`.`dividend_cover` > 1.5 '
             'AND `fundamentals`.`dividend_yield` > 4 '
             'AND `pe_deciles`.`decile_ASX` <= 2 '
             'AND `dividend_analysis`.`divi_cagr_5yr` > 3.0 '
             'ORDER BY `dividend_analysis`.`years_growth_0pct` DESC')
    
    print('<html>'
          '<head><link rel="stylesheet" href="https://github.com/necolas/'
          'normalize.css/blob/master/normalize.css" type="text/css" media="screen" />'
          '</head>'
          '<body><h1>Dividend Champions</h1>'
          '<table style="text-align: left;">'
          '<thead>'
          '<tr>'
          '<th>Stock Ticker</th>'
          '<th>Price/Earnings (P/E)</th>'
          '<th>P/E Decile (AllShare)</th>'
          '<th>P/E Decile (industry)</th>'
          '<th>Dividend yield</th>'
          '<th>Dividend cover</th>'
          '<th>Years of dividend increases</th>'
          '<th>Years of dividend increases (5%)</th>'
          '<th>Five-year dividend CAGR</th>'
          '<th>Projected Dividend Yield (3 years)</th>'
          '</tr>'
          '<tbody>')

    for result in scraperwiki.sqlite.select(query):    
        print("<tr>")
        symbol = result['symbol']
        print("<td><a href='%s'>%s</a></td>" % (ADVFN_URL % {'symbol' : symbol}, symbol))
        print("<td>%.1f</td>" % result['pe_ratio'])
        print("<td>%s</td>" % result['decile_ASX'])
        print("<td>%s</td>" % result['decile_industry'])
        print("<td>%.1f %%</td>" % result['dividend_yield'])
        print("<td>%.1f</td>" % result['dividend_cover'])
        print("<td>%d</td>" % result['years_growth_0pct'])
        print("<td>%d</td>" % result['years_growth_5pct'])
        print("<td>%.1f %%</td>" % result['divi_cagr_5yr'])
        print("<td>%.1f %%</td>" % compound(result['dividend_yield'], result['divi_cagr_5yr'], 3))
        print("</tr>")
    print("</tbody></table></html>")    
    
    for result in scraperwiki.sqlite.select(query):
        symbol = result['symbol']
        display_dividend_table(symbol, get_dividend_totals(symbol))                

def compound(number, annual_percent, years):
    cagr = 1.0 + (0.01 * annual_percent)  # ie cagr = 1.1 = 10% p.a.
    return number * (cagr ** years)

def display_dividend_table(symbol, dividends):
    print("<table style='font-size: 12; width:200px' border='1'>"
           "<tr><th colspan='3'>%s dividends</tr>"
           "<tr><th>Year</th><th>Dividend</th><th>Growth</th></tr>"% symbol)
    for entry in dividends:
        print("<tr>")
        print("<td>%s</td>" % entry.year)
        print("<td>%.2f</td>" % entry.total)
        if entry.growth is not None:
            print("<td>%.1f%%</td>" % (100 * entry.growth,))
        else:
            print("<td>-</td>")
        print("</tr>")
    print("</table>")

def get_dividend_totals(symbol):
    """Return a list of DividendYear namedtuples, ordered by most recent year"""
    
    totals = {}
    previous_currency = None
    for result in scraperwiki.sqlite.select("symbol,year,total,currency from dividends.annual_dividend "
                                          "where symbol='%s' ORDER BY year ASC" % symbol):
        totals[int(result['year'])] = float(result['total'])
        currency = result['currency']
        if previous_currency is not None and currency != previous_currency:
            return []
        previous_currency = currency
    
    totals = fill_missing_years(totals)
    dividends = []  # DividendYear
    previous_total = None
        
    for year in sorted(totals.iterkeys()):
        total = totals[year]
        (growth, growth_adjusted) = calculate_growth(total, previous_total)
        
        previous_total = total
        dividends.append(DividendYear(
                             year=year,
                             total=totals[year],
                             growth=growth,
                             growth_adjusted=growth_adjusted))
    return list(reversed(dividends))

def calculate_growth(total, previous_total):
    if previous_total:
        growth = (total - previous_total) / previous_total
    else:
        growth = None

    return (growth, calculate_adjusted_growth(growth))

def calculate_adjusted_growth(growth):
    if growth is not None:
        return growth - 0.03

def fill_missing_years(totals):
    """Populate zeroes into years without a dividend payment record."""
    last_definite_year = 2012
    for year in xrange(min(totals.keys()), 2012 + 1):
        if year not in totals:
            totals[year] = 0.0
    return totals

def _calculate_growth(dividends, years):
    now = 2012
    try:
        growth = 1 + (dividends[now] - dividends[now - years]) / dividends[now - years]
        growth_cagr = (growth ** (1.0 / years)) - 1
    except KeyError:
        growth_cagr = 0.0

    return growth_cagr


main()
