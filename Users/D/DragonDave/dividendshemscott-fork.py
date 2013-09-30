import scraperwiki
import BeautifulSoup, time
from datetime import date 
from lxml.html import fromstring
    
def tickers ():
    scraperwiki.sqlite.attach('lse-ftse-350-constituents', 'constituents')
    results = [r['Epic'].encode("utf8","ignore") for r in scraperwiki.sqlite.select("* from constituents.swdata")]
    return results

def convert_date_uk (t):
    if t == '-':
        return None
    parts = t.split ('/')
    return date (int (parts[2]), int (parts[1]), int(parts[0]))

hemscott_url = "http://lt.hemscott.com/SSB/tiles/company-data/financial-data/dividends.jsp?epic=%s&market=%s"

def get_hemscott_data (exchange, ticker):
    url = hemscott_url % (ticker, exchange)
    try:
        html = scraperwiki.scrape (url)
    except:
        print 'Cannot find %s:%s' % (exchange, ticker)
        return
    root = fromstring(html)
    table=root.cssselect("table")[3]
    alldata = []
    for row in table.cssselect('tr'):
        tds = [td.text.encode("utf8","ignore") for td in row.cssselect('td')]
        if len(tds) != 3:
            continue
        try:
            data = \
                {
                'Source':'Hemscott',
                'Type': row.th.text,
                'Currency': None,
                'Ticker':ticker,
                'DeclarationDate':None,
                'ExDivDate':convert_date_uk (tds[0]),
                'RecordDate':None,
                'PayDate':convert_date_uk (tds[1]),
                'Amount':float(tds[2]) / 100.0
                }
            alldata.append (data)
        except:
            print "Failed ", ticker, tds
    
    return alldata
    
t0=time.clock()
get_hemscott_data ('LSE','ATST')
t1=time.clock()
print t1-t0
    

import scraperwiki
import BeautifulSoup, time
from datetime import date 
from lxml.html import fromstring
    
def tickers ():
    scraperwiki.sqlite.attach('lse-ftse-350-constituents', 'constituents')
    results = [r['Epic'].encode("utf8","ignore") for r in scraperwiki.sqlite.select("* from constituents.swdata")]
    return results

def convert_date_uk (t):
    if t == '-':
        return None
    parts = t.split ('/')
    return date (int (parts[2]), int (parts[1]), int(parts[0]))

hemscott_url = "http://lt.hemscott.com/SSB/tiles/company-data/financial-data/dividends.jsp?epic=%s&market=%s"

def get_hemscott_data (exchange, ticker):
    url = hemscott_url % (ticker, exchange)
    try:
        html = scraperwiki.scrape (url)
    except:
        print 'Cannot find %s:%s' % (exchange, ticker)
        return
    root = fromstring(html)
    table=root.cssselect("table")[3]
    alldata = []
    for row in table.cssselect('tr'):
        tds = [td.text.encode("utf8","ignore") for td in row.cssselect('td')]
        if len(tds) != 3:
            continue
        try:
            data = \
                {
                'Source':'Hemscott',
                'Type': row.th.text,
                'Currency': None,
                'Ticker':ticker,
                'DeclarationDate':None,
                'ExDivDate':convert_date_uk (tds[0]),
                'RecordDate':None,
                'PayDate':convert_date_uk (tds[1]),
                'Amount':float(tds[2]) / 100.0
                }
            alldata.append (data)
        except:
            print "Failed ", ticker, tds
    
    return alldata
    
t0=time.clock()
get_hemscott_data ('LSE','ATST')
t1=time.clock()
print t1-t0
    

