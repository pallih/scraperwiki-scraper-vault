
import scraperwiki           



scraperwiki.sqlite.attach("rubbish_scraper")

data = scraperwiki.sqlite.select('''* from rubbish_scraper.swdata''')

import csv
import sys


csvout = csv.writer(sys.stdout)


keys=['propertyID','location','address','price','img']
csvout.writerow(keys)

for dwelling in data:
    row = [ dwelling[att].encode('utf-8') for att in keys ]
    csvout.writerow(row)



