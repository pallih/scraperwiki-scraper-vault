import scraperwiki

import csv
import urllib
import datetime
from decimal import Decimal
from pprint import pprint
from collections import deque
from StringIO import StringIO


class MovingAverage(object):
    def __init__(self, windowsize):
        self._windowsize = windowsize
        self._window = []

    def push(self, value):
        if len(self._window) == self._windowsize:
            self._window.pop(0)
        self._window.append(value)

    def value(self):
        if len(self._window) == 0:
            return 0
        else:
            return sum(self._window) / len(self._window)

    def weighted(self):
        if len(self._window) == 0:
            return 0
        else:
            accum = Decimal('0')
            count = Decimal('0')
            for (weight, value) in enumerate(self._window, start=1):
                accum += (value * weight)
                count += weight
            return accum / count
            
def main():
    url = 'http://www.federalreserve.gov/datadownload/Output.aspx'
    params = {
        'rel': 'Z1',
        'series': '0c26ea0130f873240b74c6c9a99325ac',
        'lastObs': '',
        'from': '12/31/1951',
        'to': '12/31/3000',
        'filetype': 'csv',
        'label': 'omit',
        'layout': 'seriescolumn',
    }
    csvstring = scraperwiki.scrape(url, params)
    print 'Downloaded {0} bytes from {1}?{2}'.format(len(csvstring), url, urllib.urlencode(params))
    csvfile = StringIO(csvstring)
    # Drop the first line because the column headers are on the second line
    csvfile.readline()


    rdr = csv.DictReader(csvfile)
    rows = list(rdr)
    print 'Processing {0} rows from CSV data'.format(len(rows))

    quarter_end_dates = {
        '1': {'month': 3, 'day': 31},
        '2': {'month': 6, 'day': 30},
        '3': {'month': 9, 'day': 30},
        '4': {'month': 12, 'day': 31}
    }
    latest_date = datetime.date(1900, 1, 1)
    for row in rows:
        # Sample row:
        # {'FL103164103.Q': '14276632.0', 'Time Period': '2011Q4', 'FL102090005.Q': '16355038.9'}
        #pprint(row)
        (year, quarter) = row['Time Period'].split('Q')
        quarter_kwargs = quarter_end_dates[quarter]
        row['Date'] = datetime.date(year=int(year), **quarter_kwargs)
        row['FL103164103'] = Decimal(row['FL103164103.Q'])
        row['FL102090005'] = Decimal(row['FL102090005.Q'])
        # The scraperwiki datastore can't handle periods in the keys
        if row['Date'] > latest_date:
            latest_date = row['Date']
        del row['FL103164103.Q']
        del row['FL102090005.Q']
        row['QRATIO'] = row['FL103164103'] / row['FL102090005']

    mean_qratio = sum((row['QRATIO'] for row in rows)) / len(rows)
    print "Mean: {0}".format(mean_qratio)
    print "Latest date: {0}".format(latest_date)

    moving_average_qratio = MovingAverage(windowsize=4)
    for row in rows:
        row['QRATIO_NORMALIZED'] = row['QRATIO'] / mean_qratio
        moving_average_qratio.push(row['QRATIO'])
        row['QRATIO_4QMAVG'] = moving_average_qratio.weighted()
        row['QRATIO_4QMAVG_NORMALIZED'] = row['QRATIO_4QMAVG'] / mean_qratio

    for row in rows:
        scraperwiki.sqlite.save(['Time Period'], row)



if __name__ in ("__main__", "scraper"):
    main()