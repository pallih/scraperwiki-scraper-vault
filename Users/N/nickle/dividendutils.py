import scraperwiki
from datetime import date 
from lxml.html import fromstring
from lxml.etree import tostring

def tickers ():
    # get the list of tickers of the ftse-350 index

    scraperwiki.sqlite.attach('lse-ftse-350-constituents', 'constituents')
    results = [r['Epic'].encode("utf8","ignore") for r in scraperwiki.sqlite.select("* from constituents.swdata")]
    results.sort()
    return results

def convert_amount (t):
    t = t.strip()
    if t[-1] == 'p':
        return float (t[:-1])
    if ord (t[-1]) >= 128:
        return float (t[:-1])
    return float (t)

mappings0 = {}
for i,m in enumerate ("january,february,march,april,may,june,july,august,september,october,november,december".split(',')):
    mappings0 [m] = str(i+1)
mappings1 = {'sept':'9'}
mappings2 = {}
for i,m in enumerate ('jan,feb,mar,apr,may,jun,jul,aug,sep,oct,nov,dec'.split(',')):
    mappings2 [m] = str(i+1)
mappings = [mappings0, mappings1, mappings2]

specials = \
    {
    }

def convert_date_ymd (parts):
    return date (int (parts[0]), int(parts[1]), int(parts[2]))

def convert_date_dmy (parts):
    if parts[2] == '00':
        return date (2000, int (parts[1]), int(parts[0]))
    elif int (parts[2]) < 50:
        return date (int (parts[2])+2000, int (parts[1]), int(parts[0]))
    elif int (parts[2]) < 100:
        return date (int (parts[2])+1900, int (parts[1]), int(parts[0]))
    return date (int (parts[2]), int (parts[1]), int(parts[0]))

def convert_date_mdy (parts):
    return date (int (parts[2]), int (parts[0]), int(parts[1]))

def convert_date (t):
    if t in specials:
        t = specials[t]
    t = t.strip()
    t = t.lower()
    t = t.replace("\n", " ")
    t = t.replace ("\r", " ")
    t = t.replace ("\t", " ")
    #print t, len (t)
    if t in ['-', '', 'Nov-30--0001']:
        return None
    monthfirst = t[0] in 'abcdefghijklmnopqrstuvwxyz'
    for i in range (3):
        mapping = mappings[i]
        for k, v in mapping.items():
            if k in t:
                t = t.replace (k, " " + str (v) + " ")
    t = t.replace(",", " ").strip()
    t = t.replace(".", " ").strip()
    t = t.replace ('  ', ' ')
    #print '|'+t+'|'
    if len (t.split('/')) == 3:
        parts = t.split ('/')
    elif len (t.split ('-')) == 3:
        parts = t.split ('-')
    else:
        parts = t.split ()
    
    parts[0] = parts[0].strip()
    parts[1] = parts[1].strip()
    parts[2] = parts[2].strip()
    #print parts
    if len  (parts[0]) == 4:
        return convert_date_ymd (parts)
    if monthfirst:
        return convert_date_mdy (parts)
    return convert_date_dmy (parts)

#print convert_date ('16 Nov 2011')
#print convert_date ('1 June 2011')
#print convert_date ('9 May 12')
#print convert_date ('9 Sept 2011')
#print convert_date ('01 July 1997')
#print convert_date ('01July 1997')
#print convert_date ('Nov 17, 2004')
#print convert_date ('Dec 12, 2008')
#print convert_date ('Sept 12, 2008')
#print convert_date ("24 Feb \r\n\t\t\t 1999")
#print convert_date ('22 September 2000')
#print convert_date ('26-Oct-98')
#print convert_date ('12 Oct.2001')
#print convert_date ('11 Oct. 2002')
#print convert_date ('07-Feb-94')

def convert_currency (t):
    t = t.strip()
    if t == 'GBX':
        return 'GBP'
    if t == 'I':
        return 'IRP'
    if t == 'FL':
        return 'GBP'
    return t.strip()

def convert_type (t):
    t = t.strip()
    if t in ['Annual', 'Prelim']:
        return 'Final'
    if t == 'Special Div':
        return 'Special'
    if t == 'A':
        return 'Final'
    if t in ['1st Quarter', '3rd Quarter', 'Quarterly']:
        return 'Interim'
    return t


class ConvertTable:

    def __init__ (self, template, tableindex, rowpath, colpath, debug=False):
        self.template = template
        self.tableindex = tableindex
        self.rowpath = rowpath
        self.colpath = colpath
        self.debug = debug

    def read (self, exchange, ticker):
        if self.debug:
            print 
            print exchange, ticker
        url = self.template.format (exchange, self.ticker (ticker))
        if self.debug:
            print url
        try:
            html = scraperwiki.scrape (url)
        except:
            print 'Cannot find %s:%s' % (exchange, ticker)
            return []
        root = fromstring (html)
        if self.debug:
            print tostring (root)
        try:
            table = root.xpath ('//table')[self.tableindex]
            if self.debug:
                print tostring (table)
        except:
            print 'No dividends for %s.%s'  % (exchange, ticker)
            return []
        alldata = []
        index = 0
        for row in table.xpath (self.rowpath):
            if self.debug:
                print tostring (row)
            tds = [self.stripper (tostring(td, method="text", encoding="utf-8")) for td in row.xpath (self.colpath)]
            if self.include (index, tds):
                if self.debug:
                    data = self.convert (index, tds, ticker, url, row)
                try:
                    data = self.convert (index, tds, ticker, url, row)
                except:
                    print "Bad data", tds
                    continue
                alldata.append (data)
            index += 1
        return alldata

    def included (self, index, tds):
        raise NotImplemented

    def convert (self, index, tds, ticker, url, row):
        raise NotImpemented
        
    def stripper (self, t):
        return t

    def ticker (self, t):
        return t
    
    '''
    def convert_amount (self, t):
        return float (t)

    def convert_date_iso (self, t):
        parts = t.split ('-')
        return date (int (parts[0]), int(parts[1]), int(parts[2]))
    
    def convert_date_dmy (self, t):
        parts = t.split ('/')
        if parts[2] == '00':
            return date (2000, int (parts[1]), int(parts[0]))
        elif int (parts[2]) < 50:
            return date (int (parts[2])+2000, int (parts[1]), int(parts[0]))
        elif int (parts[2]) < 100:
            return date (int (parts[2])+1900, int (parts[1]), int(parts[0]))
        return date (int (parts[2]), int (parts[1]), int(parts[0]))
    
    months = 'Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec'.split(',')
    
    def convert_date_mon (self, t):
        t = t.strip()
        parts = t.split (' ')
        return date (int (parts[2]), self.months.index (parts[1])+1, int(parts[0]))
    
    def convert_date_mon_us (self, t):
        t = t.strip()
        if t == 'Nov-30--0001':
            return None
        parts = t.split ('-')
        return date (int (parts[2]), self.months.index (parts[0])+1, int(parts[1]))
    
    def convert_date (self, t):
        t = t.strip()
        #print t, len (t)
        if t in ['-', '', 'Nov-30--0001']:
            return None
        if len (t) == 8:
            return self.convert_date_dmy (t)
        if len (t) in [9, 10]:
            if '-' in t:
                return self.convert_date_iso (t)
            return self.convert_date_dmy (t)
        if len (t) == 11:
            if t[0] in '0123456789':
                return self.convert_date_mon (t)
            return self.convert_date_mon_us (t)
        raise "BadData"

    def convert_currency (self, t):
        t = t.strip()
        if t == 'GBX':
            return 'GBP'
        if t == 'I':
            return 'IRP'
        if t == 'FL':
            return 'GBP'
        return t.strip()

    def convert_type (self, t):
        t = t.strip()
        if t in ['Annual', 'Prelim']:
            return 'Final'
        if t == 'Special Div':
            return 'Special'
        if t == 'A':
            return 'Final'
        if t in ['1st Quarter', '3rd Quarter', 'Quarterly']:
            return 'Interim'
        return t
    '''

    def run (self, exchange, tickers, limit=99999):
        for ticker in tickers:
            alldata = self.read (exchange, ticker)
            if len(alldata) > 0:
                scraperwiki.sqlite.save (unique_keys=["Source", "Ticker", "ExDivDate", "Type"], data=alldata)
            limit -= 1
            if limit <= 0:
                return

from datetime import datetime, date, timedelta


# UK holidays

holidaystrs = \
    [
    '2000-01-03',
    '2000-04-21',
    '2000-04-24',
    '2000-05-01',
    '2000-05-29',
    '2000-08-28',
    '2001-01-01',
    '2001-04-13',
    '2001-04-16',
    '2001-05-07',
    '2001-05-28',
    '2001-08-27',
    '2001-12-25',
    '2001-12-26',
    '2002-03-29',
    '2002-04-01',
    '2002-05-06',
    '2002-06-03',
    '2002-06-04',
    '2002-08-26',
    '2003-04-18',
    '2003-04-21',
    '2003-05-05',
    '2003-05-26',
    '2003-08-25',
    '2004-04-09',
    '2004-04-12',
    '2004-05-03',
    '2004-05-31',
    '2004-08-30',
    '2004-12-27',
    '2004-12-28',
    '2005-01-03',
    '2005-03-25',
    '2005-03-28',
    '2005-05-02',
    '2005-05-30',
    '2005-08-29',
    '2005-12-27',
    '2006-01-02',
    '2006-04-14',
    '2006-04-17',
    '2006-05-01',
    '2006-05-29',
    '2006-08-28',
    '2007-04-06',
    '2007-04-09',
    '2007-05-07',
    '2007-05-28',
    '2007-08-27',
    '2008-01-01',
    '2008-03-21',
    '2008-03-24',
    '2008-05-05',
    '2008-05-26',
    '2008-08-25',
    '2008-12-25',
    '2008-12-26',
    '2009-01-01',
    '2009-04-10',
    '2009-04-13',
    '2009-05-04',
    '2009-05-25',
    '2009-08-31',
    '2009-12-25',
    '2009-12-28',
    '2010-01-01',
    '2010-04-02',
    '2010-04-05',
    '2010-05-03',
    '2010-05-31',
    '2010-08-30',
    '2010-12-27',
    '2010-12-28',
    '2011-01-03',
    '2011-04-22',
    '2011-04-25',
    '2011-04-29',
    '2011-05-02',
    '2011-05-30',
    '2011-08-29',
    '2011-12-26',
    '2011-12-27',
    '2012-01-02',
    '2012-04-06',
    '2012-04-09',
    '2012-05-07',
    '2012-06-04',
    '2012-06-05',
    '2012-08-27',
    '2012-12-25',
    '2012-12-26',
    '2013-01-01',
    '2013-03-29',
    '2013-04-01',
    '2013-05-06',
    '2013-05-27',
    '2013-08-26',
    '2013-12-25',
    '2013-12-26',
    '2014-01-01',
    '2014-04-18',
    '2014-04-21',
    '2014-05-05',
    '2014-05-26',
    '2014-08-25',
    '2014-12-25',
    '2014-12-26',
    '2015-01-01',
    '2015-04-03',
    '2015-04-06',
    '2015-05-04',
    '2015-05-25',
    '2015-08-31',
    '2015-12-25',
    '2015-12-28',
    '2016-01-01',
    '2016-03-25',
    '2016-03-28',
    '2016-05-02',
    '2016-05-30',
    '2016-08-29',
    '2016-12-26',
    '2016-12-27',
    '2017-01-02',
    '2017-04-14',
    '2017-04-17',
    '2017-05-01',
    '2017-05-29',
    '2017-08-28',
    '2017-12-25',
    '2017-12-26',
    '2018-01-01',
    '2018-03-30',
    '2018-04-02',
    '2018-05-07',
    '2018-05-28',
    '2018-08-27',
    '2018-12-25',
    '2018-12-26',
    '2019-01-01',
    '2019-04-19',
    '2019-04-22',
    '2019-05-06',
    '2019-05-27',
    '2019-08-26',
    '2019-12-25',
    '2019-12-26',
    '2020-01-01',
    '2020-04-10',
    '2020-04-13',
    '2020-05-04',
    '2020-05-25',
    '2020-08-31',
    '2020-12-25',
    '2020-12-28'
    ]

holidays = {}

for s in holidaystrs:
    d = datetime.strptime (s, '%Y-%m-%d').date()
    holidays [d] = True

def is_holiday (d):
    global holidays
    if d.weekday() >= 6:
        return True
    return d in holidays

forward = timedelta (1)
backward = timedelta (-1)

def add_business_days (d, offset):
    if offset < 0:
        # get first working day
        while is_holiday (d):
            d = d + backward
        for i in range (-offset):
            d = d + backward
            while is_holiday (d):
                d = d + backward
    else:
        while is_holiday (d):
            d = d + forward
        for i in range (offset):
            d = d + forward
            while is_holiday (d):
                d = d + forward
    return d

def test():
    for i in range (10):
        d = date (2012, 5, i+1)
        print d, d.weekday(), add_business_days (d, -2), add_business_days (d, 2)


