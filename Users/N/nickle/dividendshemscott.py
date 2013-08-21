import scraperwiki
utils = scraperwiki.utils.swimport('dividendutils')

class ConvertTableHemscott (utils.ConvertTable):

    def __init__ (self, debug=False):
        utils.ConvertTable.__init__ \
            (
            self, 
            "http://lt.hemscott.com/SSB/tiles/company-data/financial-data/dividends.jsp?epic={1}&market={0}",
            3,
            'tbody/tr',
            'td',
            debug
            )

    def include (self, index, tds):
        if len(tds) != 3:
            return False
        return True

    def stripper (self, t):
        return t.strip()

    def convert (self, index, tds, ticker, url, row):
        data = \
            {
            'Source':            'Hemscott',
            'Ticker':            ticker,
            'Type':              self.convert_type (row.xpath ('th')[0].text.encode("utf8","ignore")),
            'Currency':          None,
            'DeclarationDate':   None,
            'ExDivDate':         self.convert_date (tds[0]),
            'RecordDate':        None,
            'PayDate':           self.convert_date (tds[1]),
            'Amount':            self.convert_amount (tds[2]),
            'Url':url
            }
        return data

converter = ConvertTableHemscott (False)
converter.run ('LSE',  utils.tickers())    

