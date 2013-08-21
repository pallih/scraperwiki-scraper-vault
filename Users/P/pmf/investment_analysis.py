# Blank Python
sourcescraper = ''

import scraperwiki
from collections import namedtuple
import operator  # for mul

DividendYear = namedtuple('DividendYear', 'year total growth growth_adjusted')

scraperwiki.sqlite.attach('lse_stock_index_constituents',   'indices')
scraperwiki.sqlite.attach('dividend_history',               'dividends')
scraperwiki.sqlite.attach('company_fundamental_financials', 'fundamentals')

def main():
    nuke_tables()
    calculate_pe_deciles()
    calculate_dividend_analysis()

def calculate_dividend_analysis():
    data = []
    for result in scraperwiki.sqlite.select('lse_symbol FROM indices.ASX'):
        symbol = result['lse_symbol']

        dividends = get_dividend_totals(symbol)
        (dividend_yield, dividend_cover) = get_dividend_yield_and_cover(symbol)
        
        data.append({'symbol' : symbol,
                'years_growth_0pct' : count_years_increases(dividends, 0),
                'years_growth_2pct' : count_years_increases(dividends, 2),
                'years_growth_5pct' : count_years_increases(dividends, 2),
                'divi_cagr_5yr' : calculate_dividend_cagr(dividends, 5),
                })
        
        scraperwiki.sqlite.save(
            table_name='dividend_analysis',
            unique_keys=['symbol'],
            data=data)

def nuke_tables():
    scraperwiki.sqlite.execute("drop table if exists analysis_errors")
    scraperwiki.sqlite.execute("drop table if exists dividend_analysis")
    scraperwiki.sqlite.execute("drop table if exists pe_decile_analysis")
    scraperwiki.sqlite.commit()

def calculate_pe_deciles():
    allshare_deciles = calculate_allshare_deciles()
    industry_deciles = calculate_industry_deciles()
    
    data = []
    for symbol in set(allshare_deciles.keys() + industry_deciles.keys()):
        data.append({'symbol' : symbol,
                     'decile_ASX' : allshare_deciles.get(symbol, None),
                     'decile_industry' : industry_deciles.get(symbol, None)})
    
    scraperwiki.sqlite.save(
        table_name='pe_deciles',
        unique_keys=['symbol'],
        data=data)    

def calculate_allshare_deciles():
    """Create a table of symbol => decile number in the ASX index"""
    results = scraperwiki.sqlite.select("symbol, ep_ratio from `fundamentals` "
                                             "ORDER BY ep_ratio DESC") # value first
    return make_decile_dict(results)

def calculate_industry_deciles():
    deciles = {}  # {symbol : decile}
    industries = [result['industry_sector'] for result in scraperwiki.sqlite.select(
                  'industry_sector FROM `fundamentals` '
                  'WHERE industry_sector NOTNULL '
                  'GROUP BY industry_sector')]
    print(industries)
    for industry in industries:
        results = scraperwiki.sqlite.select("symbol, ep_ratio FROM `fundamentals` "
                                            "WHERE industry_sector='%s' "
                                            "ORDER BY ep_ratio DESC" % industry) # value first

        deciles.update(make_decile_dict(results))
    return deciles

def make_decile_dict(results):
    """results is ordered list of {'symbol' : blah, 'ep_ratio' : blah}, value first"""
    num_in_each = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0}
    deciles = {}
    for (rank, result) in enumerate(results):
        (symbol, ep) = (result['symbol'], result['ep_ratio'])
        decile = 1 + int(float(rank) / (0.1 * len(results)))
        num_in_each[decile] += 1
        deciles[symbol] = decile  

    print(num_in_each)
    return deciles


def calculate_dividend_cagr(dividends, years):
    """
    Returns the compounded annualised growth rate of dividends
    or None if it's not possible to calculate.
    """
    if not dividends:
        return 0.0

    try:
        total = reduce(operator.mul, [1 + dividends[i].growth for i in xrange(years)])
    except TypeError:
        return None

    cagr = total ** (1.0 / float(years))
    return (cagr - 1) * 100

def count_years_increases(dividends, minimum_percent=0):
    if not dividends:
        return 0
    years = 0
    while True:
        try:
            growth = dividends[years].growth
            total = dividends[years].total
        except IndexError:
            break
        else:
            if not total or not growth or (growth * 100) < minimum_percent:
                break
        years += 1

    return years

def get_dividend_totals(symbol):
    """Return a list of DividendYear namedtuples, ordered by most recent year"""
    
    totals = {}
    previous_currency = None
    for result in scraperwiki.sqlite.select("symbol,year,total,currency from dividends.annual_dividend "
                                          "where symbol='%s' ORDER BY year ASC" % symbol):
        totals[int(result['year'])] = float(result['total'])
        currency = result['currency']
        if previous_currency is not None and currency != previous_currency:
            record_error(symbol, "Can't support multi-currency dividend payments.")
            return []
        previous_currency = currency
    if not totals:
        record_error(symbol, "No dividend records found.")
        return []

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

def record_error(symbol, message):
    scraperwiki.sqlite.save(
        table_name='analysis_errors',
        unique_keys=['symbol'],
        data={'symbol' : symbol,
              'message' : message})

def get_dividend_yield_and_cover(symbol):

    results = scraperwiki.sqlite.select("* FROM fundamentals.fundamentals "
                                        "WHERE symbol='%s'" % symbol)
    if len(results) != 1:
        print(results)
        raise RuntimeError("No company fundamentals for %s" % symbol)
    result = results[0]
    try:
        divi_yield = float(result['dividend_yield'])
    except (ValueError, TypeError):
        divi_yield = None

    try:
        divi_cover = float(result['dividend_cover'])
    except (ValueError, TypeError) as e:
        divi_cover = None
    return (divi_yield, divi_cover)
    

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