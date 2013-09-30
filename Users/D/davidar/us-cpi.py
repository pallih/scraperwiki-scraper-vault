import calendar
import datetime
import scraperwiki

header_size = 17

text = scraperwiki.scrape('ftp://ftp.bls.gov/pub/special.requests/cpi/cpiai.txt')
lines = text.split('\r\n')[header_size:]
for line in lines:
    line = line.strip()
    if line:
        row = line.split()
        year = int(row[0])
        for month in xrange(1, min(13, len(row))):
            day = calendar.monthrange(year, month)[1]
            date = datetime.date(year, month, day)
            cpi = float(row[month])
            scraperwiki.datastore.save(['date'], {'date':date, 'cpi':cpi})

import calendar
import datetime
import scraperwiki

header_size = 17

text = scraperwiki.scrape('ftp://ftp.bls.gov/pub/special.requests/cpi/cpiai.txt')
lines = text.split('\r\n')[header_size:]
for line in lines:
    line = line.strip()
    if line:
        row = line.split()
        year = int(row[0])
        for month in xrange(1, min(13, len(row))):
            day = calendar.monthrange(year, month)[1]
            date = datetime.date(year, month, day)
            cpi = float(row[month])
            scraperwiki.datastore.save(['date'], {'date':date, 'cpi':cpi})

