import scraperwiki
utils = scraperwiki.utils.swimport('dividendutils')

class ConvertTableDividendInvestor (utils.ConvertTable):

    def __init__ (self, debug=False):

        utils.ConvertTable.__init__ \
            (
            self, 
            "http://dividendinvestor.co.uk/member-historical.php?exg={0}&symbol={1}",
            8,
            'tr',
            'td',
            debug
            )

    def include (self, index, tds):
        if index == 0:
            return False
        if tds[1] == '':
            return False
        if tds[2] == 'Nov-30--0001':
            return False
        return True

    def stripper (self, t):
        return t.strip()

    def convert (self, index, tds, ticker, url, row):
        data = \
            {
            'Source':          'DividendInvestor',
            'Ticker':          ticker,
            'Type' :           '',
            'Currency':        '',
            'DeclarationDate': utils.convert_date_mon_us (tds[1]),
            'ExDivDate':       utils.convert_date_mon_us (tds[2]),
            'RecordDate':      utils.convert_date_mon_us (tds[3]),
            'PayDate':         utils.convert_date_mon_us (tds[4]),
            'Amount':          self.amount (tds[5]),
            'Url':             url
            }
        return data

converter = ConvertTableDividendInvestor (False)
converter.run ('GB',  utils.tickers())
