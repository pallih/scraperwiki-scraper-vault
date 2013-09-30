import urllib
import csv
import scraperwiki

# fill in the input file here
url = "http://dl.dropbox.com/u/4904216/balance.csv"

fin = urllib.urlopen(url)
lines = fin.readlines()
clist = list(csv.reader(lines))

headers = clist.pop(0)


for row in clist[:243]:
    fields = dict(zip(headers, row))

    country = fields['GEO_LAB'].split()[0]
    year = fields['TIME']
    balance = fields['INDICATORS_VALUE']
    print "Country: " + country + " Year: " + year + " Balance: " + balance
    record = { "year" : year, "country" : country, "balance" : balance }
    scraperwiki.datastore.save(["year", "country", "balance"], record) import urllib
import csv
import scraperwiki

# fill in the input file here
url = "http://dl.dropbox.com/u/4904216/balance.csv"

fin = urllib.urlopen(url)
lines = fin.readlines()
clist = list(csv.reader(lines))

headers = clist.pop(0)


for row in clist[:243]:
    fields = dict(zip(headers, row))

    country = fields['GEO_LAB'].split()[0]
    year = fields['TIME']
    balance = fields['INDICATORS_VALUE']
    print "Country: " + country + " Year: " + year + " Balance: " + balance
    record = { "year" : year, "country" : country, "balance" : balance }
    scraperwiki.datastore.save(["year", "country", "balance"], record) 