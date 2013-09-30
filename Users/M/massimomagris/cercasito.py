import scraperwiki
import sys

# Test CSV

data = scraperwiki.scrape("http://www.ammcomputer.com/tmp/RAGIONESOCIALE.txt")

import csv           
reader = csv.reader(data.splitlines(),delimiter=';')

print reader

for row in reader:
    try:           
        print "AZIENDA: %s CAP %s" % (row[0],row[1])
        search="http://www.metacrawler.com/search/web?fcoid=417&fcop=topnav&fpid=2&q=AZIENDA+CAP&ql="
        search = search.replace ("CAP",row[1])
        search = search.replace ("AZIENDA",row[0])
        print search
    except Exception, err:
            sys.stderr.write('ERROR: %s\n' % str(err))




import scraperwiki
import sys

# Test CSV

data = scraperwiki.scrape("http://www.ammcomputer.com/tmp/RAGIONESOCIALE.txt")

import csv           
reader = csv.reader(data.splitlines(),delimiter=';')

print reader

for row in reader:
    try:           
        print "AZIENDA: %s CAP %s" % (row[0],row[1])
        search="http://www.metacrawler.com/search/web?fcoid=417&fcop=topnav&fpid=2&q=AZIENDA+CAP&ql="
        search = search.replace ("CAP",row[1])
        search = search.replace ("AZIENDA",row[0])
        print search
    except Exception, err:
            sys.stderr.write('ERROR: %s\n' % str(err))




