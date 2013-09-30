import scraperwiki
import urllib
url = 'http://share.find.coop/wiki/raw/dcp/directories.csv?name=tip&file=dcp/directories.csv&m=text/csv'

f = urllib.urlopen(url)
lines = f.readlines()

import csv
clist = list(csv.reader(lines))

header = clist.pop(0)
for row in clist:
    record = dict(zip(header, row))
    scraperwiki.sqlite.save(["Name of directory"], record)
import scraperwiki
import urllib
url = 'http://share.find.coop/wiki/raw/dcp/directories.csv?name=tip&file=dcp/directories.csv&m=text/csv'

f = urllib.urlopen(url)
lines = f.readlines()

import csv
clist = list(csv.reader(lines))

header = clist.pop(0)
for row in clist:
    record = dict(zip(header, row))
    scraperwiki.sqlite.save(["Name of directory"], record)
