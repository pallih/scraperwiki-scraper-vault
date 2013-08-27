import csv
import scraperwiki

url = "http://www.connectingforhealth.nhs.uk/systemsandservices/data/ods/datafiles/tr.csv"
open('data.csv', 'w').write(scraperwiki.scrape(url))

r = csv.reader(open('data.csv', 'rU'))
for row in r:
    scraperwiki.sqlite.save(['code'], {
            'code': row[0],
            'name': row[1],
            'postcode' : row[9],
    
        })


import csv
import scraperwiki

url = "http://www.connectingforhealth.nhs.uk/systemsandservices/data/ods/datafiles/tr.csv"
open('data.csv', 'w').write(scraperwiki.scrape(url))

r = csv.reader(open('data.csv', 'rU'))
for row in r:
    scraperwiki.sqlite.save(['code'], {
            'code': row[0],
            'name': row[1],
            'postcode' : row[9],
    
        })


import csv
import scraperwiki

url = "http://www.connectingforhealth.nhs.uk/systemsandservices/data/ods/datafiles/tr.csv"
open('data.csv', 'w').write(scraperwiki.scrape(url))

r = csv.reader(open('data.csv', 'rU'))
for row in r:
    scraperwiki.sqlite.save(['code'], {
            'code': row[0],
            'name': row[1],
            'postcode' : row[9],
    
        })


