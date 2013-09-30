import scraperwiki
from datetime import datetime
import re
import json
import urllib

sourcescraper = 'santiago_stock_exchange'

scraperwiki.sqlite.attach(sourcescraper) 

keys =  scraperwiki.sqlite.execute('select * from `santiago_stock_exchange`.swdata limit 0')['keys']
data =  scraperwiki.sqlite.select('* from `santiago_stock_exchange`.swdata ORDER BY "date" DESC')


#meta
for row in data:
    updated = "%s" % (row.get('date'))
    break

print """<?xml version="1.0" encoding="utf-8"?>

<feed xmlns='http://www.w3.org/2005/Atom'>
    <title type='text'>Santiago Stock Exchange News</title>
    <updated>%s</updated>
    <id>http://scraperwikiviews.com/run/santiago_stock_exchange/?</id> 
    <link rel='self' type='application/atom+xml' href='http://scraperwikiviews.com/run/santiago_stock_exchange/?'/>
    <generator uri='http://scraperwikiviews.com/run/santiago_stock_exchange/?' version='1.0'></generator>""" % (updated) 

# rows
for row in data:
    title = row.get('title')
    date = row.get('date')
    summary = row.get('title')
    link = row.get('link')
    company = row.get('company')

    updated = "%s" % (row.get('date')[:-9])
    printable = 1
    print """    <entry>
    <title>  %s - %s </title>
    <updated> %s </updated> 
    <summary type='html'>
    <![CDATA[
       <p>%s</p>
       <p><a href='%s'>%s</a></p>
    ]]>
    </summary>
    </entry>""" % (date[:-9],title, updated, company, link, summary)
print '</feed>'







import scraperwiki
from datetime import datetime
import re
import json
import urllib

sourcescraper = 'santiago_stock_exchange'

scraperwiki.sqlite.attach(sourcescraper) 

keys =  scraperwiki.sqlite.execute('select * from `santiago_stock_exchange`.swdata limit 0')['keys']
data =  scraperwiki.sqlite.select('* from `santiago_stock_exchange`.swdata ORDER BY "date" DESC')


#meta
for row in data:
    updated = "%s" % (row.get('date'))
    break

print """<?xml version="1.0" encoding="utf-8"?>

<feed xmlns='http://www.w3.org/2005/Atom'>
    <title type='text'>Santiago Stock Exchange News</title>
    <updated>%s</updated>
    <id>http://scraperwikiviews.com/run/santiago_stock_exchange/?</id> 
    <link rel='self' type='application/atom+xml' href='http://scraperwikiviews.com/run/santiago_stock_exchange/?'/>
    <generator uri='http://scraperwikiviews.com/run/santiago_stock_exchange/?' version='1.0'></generator>""" % (updated) 

# rows
for row in data:
    title = row.get('title')
    date = row.get('date')
    summary = row.get('title')
    link = row.get('link')
    company = row.get('company')

    updated = "%s" % (row.get('date')[:-9])
    printable = 1
    print """    <entry>
    <title>  %s - %s </title>
    <updated> %s </updated> 
    <summary type='html'>
    <![CDATA[
       <p>%s</p>
       <p><a href='%s'>%s</a></p>
    ]]>
    </summary>
    </entry>""" % (date[:-9],title, updated, company, link, summary)
print '</feed>'







