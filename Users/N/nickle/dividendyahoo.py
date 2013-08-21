import scraperwiki
from datetime import date 
import csv

def convert_date (t):
    parts = t.split ('-')
    return date (int (parts[0]), int(parts[1]), int(parts[2]))


def tickers ():
    scraperwiki.sqlite.attach('lse-ftse-350-constituents', 'constituents')
    results = [r['Epic'].encode("utf8","ignore") for r in scraperwiki.sqlite.select("* from constituents.swdata")]
    results.sort()
    return results

start = date (2001, 1, 1)
end   = date.today()

def get_ticker (t):
    if t == 'BT.A':
        return 'BT-A'
    if t[-1] == '.':
        return t[0:-1]
    return t

url_template = 'http://ichart.finance.yahoo.com/table.csv?s=%s.%s&b=%d&a=%02d&c=%d&e=%d&d=%03d&f=%d&g=v&ignore=.csv'

def get_data (exchange, ticker, start, end):
    yahoo_ticker = get_ticker (ticker)
    url = url_template % (yahoo_ticker, exchange, start.day, start.month-1, start.year, end.day, end.month-1, end.year)
    try:
        csv = scraperwiki.scrape (url)
    except:
        print 'Cannot find %s:%s' % (exchange, ticker)
        return
    first = True
    alldata = []
    for line in csv.split("\n"):
        if first:
            headers = [h.replace (" ", "") for h in line.split (",")]
            first = False
        elif line == '':
            continue
        else:
            tds = line.split(',')
            data = \
                {
                'Source':'Yahoo',
                'Type':'',
                'Currency': None,
                'Ticker':ticker,
                'DeclarationDate':None,
                'ExDivDate': convert_date (tds[0]),
                'RecordDate':None,
                'PayDate':None,
                'Amount':float(tds[1]),
                'Url':url
                }
            alldata.append (data)
    scraperwiki.sqlite.save (unique_keys=["Source", "Ticker", "ExDivDate", "Type"], data=alldata)

for ticker in tickers():
    get_data ('L',ticker, start, end)