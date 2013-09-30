import scraperwiki
import csv

data = scraperwiki.scrape("https://dl.dropbox.com/s/yzvflulowbstiwx/alberta_wind_farms.csv?dl=1")
reader = csv.DictReader(data.splitlines())
for row in reader:
     if row['name']:
        if row['lat']:
            row['lat'] = float(row['lat'])
            row['lon'] = float(row['lon'])
        else:
            row['lat'] = None
            row['lon'] = None
        
        scraperwiki.sqlite.save(unique_keys=['name'], data=row)

import scraperwiki
import csv

data = scraperwiki.scrape("https://dl.dropbox.com/s/yzvflulowbstiwx/alberta_wind_farms.csv?dl=1")
reader = csv.DictReader(data.splitlines())
for row in reader:
     if row['name']:
        if row['lat']:
            row['lat'] = float(row['lat'])
            row['lon'] = float(row['lon'])
        else:
            row['lat'] = None
            row['lon'] = None
        
        scraperwiki.sqlite.save(unique_keys=['name'], data=row)

