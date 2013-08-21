import scraperwiki
import csv
from datetime import date
import StringIO

urltemplate = 'http://ichart.finance.yahoo.com/table.csv?s=%s.%s&b=%d&a=%02d&c=%d&e=%d&d=%03d&f=%d&g=d&ignore=.csv'

def convert_date_iso (t):
    parts = t.split ('-')
    return date (int (parts[0]), int(parts[1]), int(parts[2]))

def get_yahoo_prices (exchange, ticker, start, end):
    yahoo_ticker = ticker.replace (".", "-")
    url = urltemplate  % (yahoo_ticker, exchange, start.day, start.month-1, start.year, end.day, end.month-1, end.year)
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
            data = {}
            raw = line.split(",")
            data['Ticker'] = ticker
            data['Source'] = 'Yahoo'
            data['Exchange'] = exchange
            data['Date']     = convert_date_iso (raw[0])
            data['Open']     = float (raw[1])
            data['High']     = float (raw[2])
            data['Low']      = float (raw[3])
            data['Close']    = float (raw[4])
            data['Volume']   = float (raw[5])
            data['AdjClose'] = float (raw[6])
            alldata.append (data)
    scraperwiki.sqlite.save (unique_keys=["Ticker", "Source", "Exchange", "Date"], data=alldata)

def tickers ():
    scraperwiki.sqlite.attach('lse-ftse-350-constituents', 'constituents')
    results = [r['epic'].encode("utf8","ignore") for r in scraperwiki.sqlite.select("* from constituents.swdata")]
    return results

start = date (2001, 1, 1)
end   = date.today()

for ticker in tickers():
    get_yahoo_prices ('L', ticker, start, end)

#get_yahoo_prices ('L', 'BT.A', start, end)
