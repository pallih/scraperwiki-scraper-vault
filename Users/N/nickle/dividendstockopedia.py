import scraperwiki

utils = scraperwiki.utils.swimport('dividendutils')

class ConvertTableStockopedia (utils.ConvertTable):

    def __init__ (self, debug=False):

        utils.ConvertTable.__init__ \
            (
            self, 
            "http://www.stockopedia.co.uk/share-prices/{0}:{1}/dividends/",
            0,
            'tbody/tr',
            'td',
            debug
            )

    def include (self, index, tds):
        if tds[0] == 'Company':
            return False
        if len (tds) != 6:
            return False
        return True

    def convert (self, index, tds, ticker, url, row):
        data = \
            {
            'Source':          'Stockopedia',
            'Type':            self.convert_type (tds[2]),
            'Currency':        self.convert_currency (tds[4]),
            'Ticker':          ticker,
            'DeclarationDate': None,
            'ExDivDate':       self.convert_date  (tds[0]),
            'RecordDate':      None,
            'PayDate':         self.convert_date (tds[1]),
            'Amount':          self.convert_amount (tds[3]),
            'Url':url
            }
        return data


converter = ConvertTableStockopedia ()
converter.run ('LON', utils.tickers())

