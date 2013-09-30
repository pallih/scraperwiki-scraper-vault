import scraperwiki
import csv

url = 'google.com'

data = scraperwiki.scrape(url)
data = data.splitlines()
reader = csv.DictReader(data)

for record in reader:
    #record['Name'] = record['Name'].decode("cp1252")
    print record 
    #for scraperwiki only:
    scraperwiki.sqlite.save(['Value'], record) 


import scraperwiki
import csv

url = 'google.com'

data = scraperwiki.scrape(url)
data = data.splitlines()
reader = csv.DictReader(data)

for record in reader:
    #record['Name'] = record['Name'].decode("cp1252")
    print record 
    #for scraperwiki only:
    scraperwiki.sqlite.save(['Value'], record) 


