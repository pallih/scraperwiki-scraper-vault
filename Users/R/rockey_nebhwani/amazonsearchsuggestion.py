import scraperwiki
import json
import re
import urlparse
import lxml.html
import csv           

try:
    scraperwiki.sqlite.execute("""
        create table swdata
        (
        Deeplink
        )
    """)

purge = scraperwiki.scrape("http://graph.facebook.com/dunkindonuts")

websiteData = json.loads(purge)


except:
    print "Table probably already exists."

data = scraperwiki.scrape("http://leapgradient.com/Search_terms.csv")

reader = csv.reader(data.splitlines())

for row in reader:
    print "Keyword: %s" % (row[0])

reader = csv.DictReader(data.splitlines())

for row in reader:           
        scraperwiki.sqlite.save(unique_keys=['SearchTerm'], data=row)




import scraperwiki
import json
import re
import urlparse
import lxml.html
import csv           

try:
    scraperwiki.sqlite.execute("""
        create table swdata
        (
        Deeplink
        )
    """)

purge = scraperwiki.scrape("http://graph.facebook.com/dunkindonuts")

websiteData = json.loads(purge)


except:
    print "Table probably already exists."

data = scraperwiki.scrape("http://leapgradient.com/Search_terms.csv")

reader = csv.reader(data.splitlines())

for row in reader:
    print "Keyword: %s" % (row[0])

reader = csv.DictReader(data.splitlines())

for row in reader:           
        scraperwiki.sqlite.save(unique_keys=['SearchTerm'], data=row)




import scraperwiki
import json
import re
import urlparse
import lxml.html
import csv           

try:
    scraperwiki.sqlite.execute("""
        create table swdata
        (
        Deeplink
        )
    """)

purge = scraperwiki.scrape("http://graph.facebook.com/dunkindonuts")

websiteData = json.loads(purge)


except:
    print "Table probably already exists."

data = scraperwiki.scrape("http://leapgradient.com/Search_terms.csv")

reader = csv.reader(data.splitlines())

for row in reader:
    print "Keyword: %s" % (row[0])

reader = csv.DictReader(data.splitlines())

for row in reader:           
        scraperwiki.sqlite.save(unique_keys=['SearchTerm'], data=row)




import scraperwiki
import json
import re
import urlparse
import lxml.html
import csv           

try:
    scraperwiki.sqlite.execute("""
        create table swdata
        (
        Deeplink
        )
    """)

purge = scraperwiki.scrape("http://graph.facebook.com/dunkindonuts")

websiteData = json.loads(purge)


except:
    print "Table probably already exists."

data = scraperwiki.scrape("http://leapgradient.com/Search_terms.csv")

reader = csv.reader(data.splitlines())

for row in reader:
    print "Keyword: %s" % (row[0])

reader = csv.DictReader(data.splitlines())

for row in reader:           
        scraperwiki.sqlite.save(unique_keys=['SearchTerm'], data=row)




