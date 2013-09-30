import scraperwiki
import re

data = []
unique_keys = ['year']
rawtext = scraperwiki.scrape("http://www.census.gov/srd/www/genhol/easter500.txt")

for line in rawtext.split('\n'):
    parts = re.split('\s+', line.strip())
    if len(parts) == 3:
        day = int(parts[1])
        month = int(parts[0])
        year = int(parts[2])
        data.append({'year': year, 'month': month, 'day': day})

scraperwiki.sqlite.save(unique_keys=unique_keys, data=data)
import scraperwiki
import re

data = []
unique_keys = ['year']
rawtext = scraperwiki.scrape("http://www.census.gov/srd/www/genhol/easter500.txt")

for line in rawtext.split('\n'):
    parts = re.split('\s+', line.strip())
    if len(parts) == 3:
        day = int(parts[1])
        month = int(parts[0])
        year = int(parts[2])
        data.append({'year': year, 'month': month, 'day': day})

scraperwiki.sqlite.save(unique_keys=unique_keys, data=data)
