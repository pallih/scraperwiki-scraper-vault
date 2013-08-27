import scraperwiki
import csv

print scraperwiki.sqlite.execute("delete from swdata where region=?", ['region'])

"""
open('/tmp/csv', 'wb').write(scraperwiki.scrape(f))
reader = csv.reader(open("/tmp/csv", 'rU'))

counter = 0
rows = []
for row in reader:
    # code, lat, lng, region
    counter = counter + 1
    rows.append(dict(code=row[0],lat=row[1], lng=row[2], region=row[3]))
    if counter % 100 == 0:
        scraperwiki.sqlite.save(['code'], rows)
        rows = []
"""import scraperwiki
import csv

print scraperwiki.sqlite.execute("delete from swdata where region=?", ['region'])

"""
open('/tmp/csv', 'wb').write(scraperwiki.scrape(f))
reader = csv.reader(open("/tmp/csv", 'rU'))

counter = 0
rows = []
for row in reader:
    # code, lat, lng, region
    counter = counter + 1
    rows.append(dict(code=row[0],lat=row[1], lng=row[2], region=row[3]))
    if counter % 100 == 0:
        scraperwiki.sqlite.save(['code'], rows)
        rows = []
"""import scraperwiki
import csv

print scraperwiki.sqlite.execute("delete from swdata where region=?", ['region'])

"""
open('/tmp/csv', 'wb').write(scraperwiki.scrape(f))
reader = csv.reader(open("/tmp/csv", 'rU'))

counter = 0
rows = []
for row in reader:
    # code, lat, lng, region
    counter = counter + 1
    rows.append(dict(code=row[0],lat=row[1], lng=row[2], region=row[3]))
    if counter % 100 == 0:
        scraperwiki.sqlite.save(['code'], rows)
        rows = []
"""