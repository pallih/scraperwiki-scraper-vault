import urllib
import csv

# fill in the input file here
url = "http://media.scraperwiki.com/example.csv"

fin = urllib.urlopen(url)
lines = fin.readlines()
clist = list(csv.reader(lines))

headers = clist.pop(0)
print "There are %d columns and %d rows" % (len(headers), len(clist))
print "Headers:", headers

for row in clist[:10]:
    print dict(zip(headers, row))
    #Uncomment these two lines to store in ScraperWiki datastore
    #unique_keys = headers # Change this to the fields that uniquely identify a row
    #scraperwiki.datastore.save(unique_keys, dict(zip(headers, row)))


import urllib
import csv

# fill in the input file here
url = "http://media.scraperwiki.com/example.csv"

fin = urllib.urlopen(url)
lines = fin.readlines()
clist = list(csv.reader(lines))

headers = clist.pop(0)
print "There are %d columns and %d rows" % (len(headers), len(clist))
print "Headers:", headers

for row in clist[:10]:
    print dict(zip(headers, row))
    #Uncomment these two lines to store in ScraperWiki datastore
    #unique_keys = headers # Change this to the fields that uniquely identify a row
    #scraperwiki.datastore.save(unique_keys, dict(zip(headers, row)))


import urllib
import csv

# fill in the input file here
url = "http://media.scraperwiki.com/example.csv"

fin = urllib.urlopen(url)
lines = fin.readlines()
clist = list(csv.reader(lines))

headers = clist.pop(0)
print "There are %d columns and %d rows" % (len(headers), len(clist))
print "Headers:", headers

for row in clist[:10]:
    print dict(zip(headers, row))
    #Uncomment these two lines to store in ScraperWiki datastore
    #unique_keys = headers # Change this to the fields that uniquely identify a row
    #scraperwiki.datastore.save(unique_keys, dict(zip(headers, row)))


import urllib
import csv

# fill in the input file here
url = "http://media.scraperwiki.com/example.csv"

fin = urllib.urlopen(url)
lines = fin.readlines()
clist = list(csv.reader(lines))

headers = clist.pop(0)
print "There are %d columns and %d rows" % (len(headers), len(clist))
print "Headers:", headers

for row in clist[:10]:
    print dict(zip(headers, row))
    #Uncomment these two lines to store in ScraperWiki datastore
    #unique_keys = headers # Change this to the fields that uniquely identify a row
    #scraperwiki.datastore.save(unique_keys, dict(zip(headers, row)))


