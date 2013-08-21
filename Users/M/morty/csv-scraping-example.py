from scraperwiki import scrape
from scraperwiki.sqlite import save
from csv import reader
from cStringIO import StringIO

url = "https://s3-eu-west-1.amazonaws.com/ukhmgdata-cabinetoffice/Spend-data-2010-11-01/Spend-Transactions-with-descriptions-HMT-09-Sep-2010.csv"

data = list(reader(StringIO(scrape(url))))

keys = data[0]

for row in data[1:]:
    if row[0] == '':
        continue

    record = {}
    for i, d in enumerate(row):
        record[keys[i]] = d
    save(['Transaction Number'], record)
