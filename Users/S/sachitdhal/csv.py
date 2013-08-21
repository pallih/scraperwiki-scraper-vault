import scraperwiki
data = scraperwiki.scrape("http://www.azliquor.gov/query/master.csv")
import csv
reader = csv.reader(data.splitlines())

for row in reader:
    print "£%s spent on %s" % (row[7], row[3])

reader = csv.DictReader(data.splitlines())
for row in reader:
#    if row['Transaction Number']:
#        row['Amount'] = float(row['Amount'])
        scraperwiki.sqlite.save(unique_keys=['License'], data=row)

