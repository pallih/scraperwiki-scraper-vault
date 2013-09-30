# Quick hack before we put CSV export back in for SQLite

import scraperwiki
import csv
import sys

scraperwiki.sqlite.attach('northern_ireland_charity_commission_-_list_of_char', 'n')

data = scraperwiki.sqlite.execute('select * from n.swdata')

csvout = csv.writer(sys.stdout)
csvout.writerow(data['keys'])

for row in data['data']:
    row = [ r.encode('utf-8') for r in row ]
    csvout.writerow(row)
# Quick hack before we put CSV export back in for SQLite

import scraperwiki
import csv
import sys

scraperwiki.sqlite.attach('northern_ireland_charity_commission_-_list_of_char', 'n')

data = scraperwiki.sqlite.execute('select * from n.swdata')

csvout = csv.writer(sys.stdout)
csvout.writerow(data['keys'])

for row in data['data']:
    row = [ r.encode('utf-8') for r in row ]
    csvout.writerow(row)
