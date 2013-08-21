import csv
import scraperwiki
from StringIO import StringIO

url = 'http://data.seattle.gov/api/views/4enm-t3vn/rows.csv'

data = StringIO()
data.write(scraperwiki.scrape(url))
data.seek(0)

data_csv = csv.DictReader(data)

for row in data_csv:
    normalized = {
        'name': row['agency_name'],
        'organization': row['parent_organization'],
        'latitude': row['xPos'],
        'longitude': row['yPos'],
        'website': row['url'],
        'description': row['description'],
    }
    scraperwiki.sqlite.save(unique_keys=['name'], data=normalized)
