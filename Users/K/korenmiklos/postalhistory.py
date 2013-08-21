import scraperwiki
import lxml.html
import sys
import re

# define some constants
URL = 'http://www.postalhistory.com/postoffices.asp?task=display'
STATES = ['AL',     'AK',     'AS',     'AZ',     'AR',     'CA',     'CO',     'CT',     'DE',     'DC',     'FM',     'FL',     'GA',     'GU',     'HI',     'ID',     'IL',     'IN',     'IA',     'KS',     'KY',     'LA',     'ME',     'MH',     'MD',     'MA',     'MI',     'MN',     'MS',     'MO',     'MT',     'NE',     'NV',     'NH',     'NJ',     'NM',     'NY',     'NC',     'ND',     'MP',     'OH',     'OK',     'OR',     'PW',     'PA',     'PR',     'RI',     'SC',     'SD',     'TN',     'TX',     'UT',     'VT',     'VI',     'VA',     'WA',     'WV',     'WI',     'WY']                                                             
PATTERN = re.compile('<BR>(.*?\(\d{4}.*?\))')


import csv, codecs, cStringIO


class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

def return_cells(html):
    root = lxml.html.fromstring(html)
    cells = []
    rows = root.iter("p")
    for row in rows:
        
        cells.append(row.text_content())
    return cells

def download_data(state='MA'):

    data = []

    # loop through pages
    pages = range(2)
    for page in pages:
        html = scraperwiki.scrape(URL + '&state=%s&pagenum=%d' % (state, page))
        data.extend(return_cells(html))
    return data

def save_data(params,sheet):
    for row in sheet:
        if row:
            data = params
            c = 1
            for column in row:
                data['cell%d' % c] = column
                c += 1
            if data['buy']:
                data['buy'] = 'buy'
            else:
                data['buy'] = 'sell' 
            scraperwiki.sqlite.save(unique_keys=[], data=data)


data = download_data()
print data


