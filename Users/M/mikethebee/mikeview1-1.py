###############################################################################
# Basic scraper
# Example from SW of csv scraper​
from scraperwiki import scrape
from scraperwiki.datastore import save
from csv import reader
from cStringIO import StringIO

url = "http://mattholmes.eu/consultants%20fees%20wbc%20wh.csv"​

data = list(reader(StringIO(scrape(url))))

keys = data[0]

for row in data[1:]:
    if row[0] == '':
        continue

    record = {}
    for i, d in enumerate(row):
        record[keys[i]] = d
    save(['Transaction Number'], record)

###############################################################################

###############################################################################
# Basic scraper
# Example from SW of csv scraper​
from scraperwiki import scrape
from scraperwiki.datastore import save
from csv import reader
from cStringIO import StringIO

url = "http://mattholmes.eu/consultants%20fees%20wbc%20wh.csv"​

data = list(reader(StringIO(scrape(url))))

keys = data[0]

for row in data[1:]:
    if row[0] == '':
        continue

    record = {}
    for i, d in enumerate(row):
        record[keys[i]] = d
    save(['Transaction Number'], record)

###############################################################################

