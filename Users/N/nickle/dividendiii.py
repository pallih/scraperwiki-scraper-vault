import scraperwiki
utils = scraperwiki.utils.swimport('dividendutils')

class ConvertTableIII (utils.ConvertTable):
    def __init__ (self, debug=False):
        utils.ConvertTable.__init__ \
            (
            self, 
            'http://www.iii.co.uk/investment/detail?code=cotn:{1}.{0}&display=fundamentals&it=le',
            3,
            'tbody/tr',
            'td',
            debug
            )

    def include (self, index, tds):
        if len(tds) == 0:
            return False
        if tds[1] == '':
            return False
        return True

    def stripper (self, t):
        return t.strip().replace ("\xc2\xa0", "")

    def ticker (self, t):
        return t.replace ('.', '-')

    def convert (self, index, tds, ticker, url, row):
        paydate = self.convert_date (tds[3])
        if paydate == None:
            paydate == utils.convert_date_dmy (tds[1])
        data = \
            {
            'Source':           'III',
            'Ticker':           ticker,
            'Type' :            self.convert_type (tds[5]),
            'Currency':         '',
            'DeclarationDate':  None,
            'ExDivDate':        self.convert_date (tds[1]),
            'RecordDate':       self.convert_date (tds[2]),
            'PayDate':          paydate,
            'Amount':           self.convert_amount (tds[4]),
            'Url':url
            }
        return data

converter = ConvertTableIII (False)
converter.run ('L',  utils.tickers())