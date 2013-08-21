import csv
import mechanize
import scraperwiki

BASE_URL = 'http://data.carync.gov/datasets/PARK_INFO.csv'

def download_parks():
    url = 'http://data.carync.gov/datasets/PARK_INFO.csv'
    br = mechanize.Browser()
    print 'Downloading {0}'.format(url)
    f = br.retrieve(url)[0]
    print 'Saved temporary file {0}'.format(f)
    with open(f) as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        for row in reader:
            scraperwiki.sqlite.save(unique_keys=['NAME'], data=row)

download_parks()
