import urllib
import csv
import scraperwiki

# fill in the input file here
url = "http://api.scraperwiki.com/api/1.0/datastore/getdata?format=csv&name=amex_companies&limit=500&offset=%d"

offset = 0
while True:
    try:
        fin = urllib.urlopen(url % offset)
        lines = fin.readlines()
        clist = list(csv.reader(lines))
        headers = clist.pop(0)

        yahoo="http://ichart.finance.yahoo.com/table.csv?s=%s&a=01&b=01&c=1990&d=01&e=01&f=2011&g=v&ignore=.csv"
        for row in clist:
            try:
                rd = dict(zip(headers, row))
                yurl = yahoo % rd['symbol']
                print "Fetching %s" % rd['symbol']
                divs = urllib.urlopen(yurl)
                lines = divs.readlines()
                print lines
                dlist = list(csv.reader(lines))
                subheaders = dlist.pop(0)
                print subheaders
                for div in dlist:
                    d = dict(zip(subheaders, div))
                    d.update(rd)
                    print "d: ", d
                    scraperwiki.datastore.save(['date_scraped','symbol'], d)
            except IOError, e:
                print "IOError: %s" % e
                continue
        offset += 500
    except IOError, e:
        break

print "FINISHED."



import urllib
import csv
import scraperwiki

# fill in the input file here
url = "http://api.scraperwiki.com/api/1.0/datastore/getdata?format=csv&name=amex_companies&limit=500&offset=%d"

offset = 0
while True:
    try:
        fin = urllib.urlopen(url % offset)
        lines = fin.readlines()
        clist = list(csv.reader(lines))
        headers = clist.pop(0)

        yahoo="http://ichart.finance.yahoo.com/table.csv?s=%s&a=01&b=01&c=1990&d=01&e=01&f=2011&g=v&ignore=.csv"
        for row in clist:
            try:
                rd = dict(zip(headers, row))
                yurl = yahoo % rd['symbol']
                print "Fetching %s" % rd['symbol']
                divs = urllib.urlopen(yurl)
                lines = divs.readlines()
                print lines
                dlist = list(csv.reader(lines))
                subheaders = dlist.pop(0)
                print subheaders
                for div in dlist:
                    d = dict(zip(subheaders, div))
                    d.update(rd)
                    print "d: ", d
                    scraperwiki.datastore.save(['date_scraped','symbol'], d)
            except IOError, e:
                print "IOError: %s" % e
                continue
        offset += 500
    except IOError, e:
        break

print "FINISHED."



