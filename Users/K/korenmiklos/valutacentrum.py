import scraperwiki
import lxml.html
import sys

# define some constants
EUR = 6
USD = 18
BUDAPEST = 1
BP_COUNTY = 20

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
    rows = root.cssselect("table#rounded-corner-basic tr")
    for row in rows:
        cells.append([x.text_content() for x in row.iter('td')])
    return cells

def download_data(currency=EUR,county=BP_COUNTY,city=BUDAPEST,buy=True):
    if buy:
        group = 'vetel'
    else:
        group = 'eladas'

    data = []

    # loop through pages
    pages = range(6)
    for page in pages:
        limit = page*15
        html = scraperwiki.scrape('http://www.valutacentrum.hu/index.php?option=com_content&view=article&id=67&limit=%d' % limit, dict(money=currency,county=county,city=1,group1=group,widget=0,e_group=0,district=0))
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

currencies = (EUR,USD)
flows = (True,False)

for currency in currencies:
    for buy in flows:
        params = dict(currency=currency,county=BP_COUNTY,city=BUDAPEST,buy=buy)
        data = download_data(**params)
        save_data(params,data)


