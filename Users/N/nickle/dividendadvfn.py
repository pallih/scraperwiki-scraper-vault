import scraperwiki
utils = scraperwiki.utils.swimport('dividendutils')

class ConvertTableADVFN (utils.ConvertTable):

    def __init__ (self, debug=False):
        utils.ConvertTable.__init__ \
            (
            self, 
            'http://uk.advfn.com/p.php?pid=financials&symbol={1}',
            23,
            'tr',
            'td',
            debug
            )

    def include (self, index, tds):
        if index == 0:
            return False
        if len(tds) == 0:
            return False
        if tds[1] == '':
            return False
        if tds[3] == '-':
            return False
        if tds[8] == '-':
            return False
        return True

    def convert (self, index, tds, ticker, url, row):
        if tds[6] == '-':
            tds[6] = tds[8]
        data = \
            {
            'Source':           'Advfn',
            'Ticker':           ticker,
            'Type' :            self.convert_type      (tds[1]),
            'Currency':         self.convert_currency  (tds[2]),
            'DeclarationDate':  self.convert_date      (tds[0]),
            'ExDivDate':        self.convert_date      (tds[6]),
            'RecordDate':       self.convert_date      (tds[7]),
            'PayDate':          self.convert_date      (tds[8]),
            'Amount':           self.convert_amount    (tds[3]),
            'Url':              url
            }
        return data

converter = ConvertTableADVFN (False)
converter.run ('LSE',  utils.tickers())

