import scraperwiki

data = scraperwiki.scrape("url")

import csv
# reader = csv.reader(data.splitlines())

reader = csv.DictReader(data.splitlines()) 

for row in reader:
    if row['MEDIA_CN'] < 450:
        if row['MEDIA_CH'] < 450:
            if row['MEDIA_LC'] < 450:
                if row['MEDIA_MT'] < 450:
                    if row['MEDIA_REDACAO'] < 500:
                        print row['NO_ENTIDADE']