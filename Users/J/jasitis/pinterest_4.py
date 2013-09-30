import scraperwiki
data = scraperwiki.scrape("http://dl.dropbox.com/u/571015/pinterest%20-%20Home.csv")
import csv
reader = csv.reader(data.splitlines())
for row in reader:
    print " title %s url %s date %s summary %s name%s " % (row[0], row[1], row[2], row[3], row[4])
reader = csv.DictReader(data.splitlines())
scraperwiki.sqlite.save(unique_keys=['Title', 'URL', 'Date Created', 'Summary', 'Sheet Name'], data=row)


import scraperwiki
data = scraperwiki.scrape("http://dl.dropbox.com/u/571015/pinterest%20-%20Home.csv")
import csv
reader = csv.reader(data.splitlines())
for row in reader:
    print " title %s url %s date %s summary %s name%s " % (row[0], row[1], row[2], row[3], row[4])
reader = csv.DictReader(data.splitlines())
scraperwiki.sqlite.save(unique_keys=['Title', 'URL', 'Date Created', 'Summary', 'Sheet Name'], data=row)


