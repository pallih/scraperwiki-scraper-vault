import scraperwiki
utils = scraperwiki.utils.swimport('dividendutils')

class ConvertTableProActive (utils.ConvertTable):

    def __init__ (self, debug=False):
        utils.ConvertTable.__init__ \
            (
            self, 
            'http://www.proactiveinvestors.co.uk/{0}:{1}/index/news/dividends',
            0,
            'tr',
            'td',
            debug
            )

    def include (self, index, tds):
        if len(tds) == 0:
            return False
        return True

    def stripper (self, t):
        return t.strip()

    def convert (self, index, tds, ticker, url, row):
        data = \
            {
            'Source':         'ProActive',
            'Ticker':          ticker,
            'Type' :           '',
            'Currency':        self.convert_currency (tds[4]),
            'DeclarationDate': None,
            'ExDivDate':       self.convert_date (tds[1]),
            'RecordDate':      None,
            'PayDate':         self.convert_date (tds[2]),
            'Amount':          self.convert_amount(tds[3]),
            'Url':             url
            }
        return data

converter = ConvertTableProActive (False)
converter.run ('LON',  utils.tickers())import scraperwiki
utils = scraperwiki.utils.swimport('dividendutils')

class ConvertTableProActive (utils.ConvertTable):

    def __init__ (self, debug=False):
        utils.ConvertTable.__init__ \
            (
            self, 
            'http://www.proactiveinvestors.co.uk/{0}:{1}/index/news/dividends',
            0,
            'tr',
            'td',
            debug
            )

    def include (self, index, tds):
        if len(tds) == 0:
            return False
        return True

    def stripper (self, t):
        return t.strip()

    def convert (self, index, tds, ticker, url, row):
        data = \
            {
            'Source':         'ProActive',
            'Ticker':          ticker,
            'Type' :           '',
            'Currency':        self.convert_currency (tds[4]),
            'DeclarationDate': None,
            'ExDivDate':       self.convert_date (tds[1]),
            'RecordDate':      None,
            'PayDate':         self.convert_date (tds[2]),
            'Amount':          self.convert_amount(tds[3]),
            'Url':             url
            }
        return data

converter = ConvertTableProActive (False)
converter.run ('LON',  utils.tickers())