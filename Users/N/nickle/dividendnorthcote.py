import scraperwiki
utils = scraperwiki.utils.swimport('dividendutils')
from BeautifulSoup import BeautifulSoup


def tickers ():
    scraperwiki.sqlite.attach('lse-ftse-350-constituents', 'constituents')
    results = \
        [
        (r['Epic'].encode("utf8","ignore"),r['Ncode'].encode("utf8","ignore")) 
        for r in scraperwiki.sqlite.select("* from constituents.swdata")
        ]
    return results

class ConvertTableNorthCote (utils.ConvertTable):

    def __init__ (self, debug=False):
        utils.ConvertTable.__init__ \
            (
            self, 
            "http://www.northcote.co.uk/company_links/?SEC={1}&SDL={0}",
            20,
            'tr',
            'td',
            debug
            )

    def read (self, exchange, ticker):
        if self.debug:
            print exchange, ticker
        url = self.template.format (exchange, self.ticker (ticker))
        if self.debug:
            print url
        try:
            html = scraperwiki.scrape (url)
        except:
            print 'Cannot find %s:%s' % (exchange, ticker)
            return []
        soup = BeautifulSoup (html)
        if self.debug:
            print soup
        try:
            table = soup.findAll ('table')[self.tableindex]
            if self.debug:
                print table
        except:
            print 'No dividends for %s.%s'  % (exchange, ticker)
            return []
        alldata = []
        index = 0
        for row in table.findAll(self.rowpath):
            if self.debug:
                print row
            tds = [self.stripper (td.text.encode("utf8","ignore")) for td in row.findAll ('td')]
            if self.include (index, tds):
                alldata.append (self.convert (index, tds, ticker, url, row))
            index += 1
        return alldata
    
    def include (self, index, tds):
        if index < 5:
            return False
        if tds[0] == '':
            return False
        if len (tds) != 4:
            return False
        if tds[1] == '':
            return False
        if float(tds[2][:-1]) == 0.0:
            return False
        return True

    def stripper (self, t):
        return t.strip().replace('&nbsp;','')

    def convert_amount (self, t):
        return float (t[:-1])

    def convert (self, index, tds, ticker, url, row):
        data = \
            {
            'Source':'NorthCote',
            'Ticker':ticker,
            'Type' : self.convert_type (tds[0]),
            'Currency': self.convert_currency (tds[3]),
            'DeclarationDate':None,
            'ExDivDate':self.convert_date (tds[1]),
            'RecordDate':'',
            'PayDate':self.convert_date (tds[1]),
            'Amount':self.convert_amount (tds[2]),
            'Url':url
            }
        return data



converter = ConvertTableNorthCote (False)
for ticker, ncode in tickers():
    converter.run (ncode, [ticker])
