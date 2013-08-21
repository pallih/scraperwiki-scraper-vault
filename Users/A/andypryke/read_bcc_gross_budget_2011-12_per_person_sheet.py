## Source: https://scraperwiki.com/docs/python/python_csv_guide/
import scraperwiki

data = scraperwiki.scrape("https://docs.google.com/spreadsheet/pub?key=0AhkGS4DSOWWQdDNYZDh4THhtbl9FRUo1VFBzeGxEZ2c&single=true&gid=0&output=csv")

import csv
#reader = csv.reader(data.splitlines())
reader = csv.DictReader(data.splitlines())

for row in reader: print "Row: %s" % (row)

reader = csv.DictReader(data.splitlines()) 

for row in reader:
    row['Spend in thousand pounds'] = float(row['Spend in thousand pounds'])
    row['Spend per Person in pounds'] = float(row['Spend per Person in pounds'])
    scraperwiki.sqlite.save(unique_keys=['Area', 'Sub-Area'], data=row)

