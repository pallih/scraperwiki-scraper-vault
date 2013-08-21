import urllib
import csv
import scraperwiki

# a new line to make an edit
# fill in the input file here
url = "http://www.fingal.ie/datasets/csv/Beaches.csv"

# the above link no longer exists

fin = urllib.urlopen(url)
lines = fin.readlines()
clist = list(csv.reader(lines))

headers = clist.pop(0)
print "There are %d columns and %d rows" % (len(headers), len(clist))
print "Headers:", headers

for row in clist:
    data = dict(zip(headers, row))
    print data
    scraperwiki.datastore.save(unique_keys=['ID'], data=data, latlng=[float(data.get('LONG')), float(data.get('LAT'))])




import urllib
import csv
import scraperwiki

# a new line to make an edit
# fill in the input file here
url = "http://www.fingal.ie/datasets/csv/Beaches.csv"

# the above link no longer exists

fin = urllib.urlopen(url)
lines = fin.readlines()
clist = list(csv.reader(lines))

headers = clist.pop(0)
print "There are %d columns and %d rows" % (len(headers), len(clist))
print "Headers:", headers

for row in clist:
    data = dict(zip(headers, row))
    print data
    scraperwiki.datastore.save(unique_keys=['ID'], data=data, latlng=[float(data.get('LONG')), float(data.get('LAT'))])




import urllib
import csv
import scraperwiki

# a new line to make an edit
# fill in the input file here
url = "http://www.fingal.ie/datasets/csv/Beaches.csv"

# the above link no longer exists

fin = urllib.urlopen(url)
lines = fin.readlines()
clist = list(csv.reader(lines))

headers = clist.pop(0)
print "There are %d columns and %d rows" % (len(headers), len(clist))
print "Headers:", headers

for row in clist:
    data = dict(zip(headers, row))
    print data
    scraperwiki.datastore.save(unique_keys=['ID'], data=data, latlng=[float(data.get('LONG')), float(data.get('LAT'))])




import urllib
import csv
import scraperwiki

# a new line to make an edit
# fill in the input file here
url = "http://www.fingal.ie/datasets/csv/Beaches.csv"

# the above link no longer exists

fin = urllib.urlopen(url)
lines = fin.readlines()
clist = list(csv.reader(lines))

headers = clist.pop(0)
print "There are %d columns and %d rows" % (len(headers), len(clist))
print "Headers:", headers

for row in clist:
    data = dict(zip(headers, row))
    print data
    scraperwiki.datastore.save(unique_keys=['ID'], data=data, latlng=[float(data.get('LONG')), float(data.get('LAT'))])




