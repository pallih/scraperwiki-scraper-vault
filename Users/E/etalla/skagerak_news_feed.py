import scraperwiki
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation
from datetime import datetime
import re
import json
import urllib

sourcescraper = 'skagerak_news'
scraperwiki.sqlite.attach(sourcescraper) 
limit = 400
offset = 0

keys =  scraperwiki.sqlite.execute('select * from `skagerak_news`.swdata limit 0')['keys']
data =  scraperwiki.sqlite.select('* from `skagerak_news`.swdata ORDER BY "date" DESC')


#res
ure = re.compile(".*(http.*uid=[0-9]*)", re.DOTALL)
nre = re.compile(".*strong.(.*strong)", re.DOTALL) 
allre = re.compile(".*", re.DOTALL)



#meta
for row in data:
    updated = "%s" % (row.get('date'))
    break

print """<?xml version="1.0" encoding="utf-8"?>

<feed xmlns='http://www.w3.org/2005/Atom'>
    <title type='text'>Skagerak news</title>
    <updated>%s</updated>
    <id>http://scraperwikiviews.com/run/skagerak_news/?</id> 
    <link rel='self' type='application/atom+xml' href='http://scraperwikiviews.com/run/skagerak_news/?'/>
    <generator uri='http://scraperwikiviews.com/run/skagerak_news/?' version='1.0'></generator>""" % (updated) 

# rows
for row in data:
    try:
        title = str(row.get('title').strip())
        date = row.get('date')[:-9]
        summary = row.get('summary') 
        link = row.get('link') 
        updated = "%s" % (row.get('date'))
        printable = 1
    except:
        printable = 0

    if printable == 1: 
        print """    <entry>
        <title>  %s - %s </title>
        <updated> %s </updated> 
        <summary type='html'>
        <![CDATA[
           <p><a href='%s'>%s</a></p>
        ]]>
        </summary>
        </entry>""" % (date, title, updated, link, summary)

print "</feed>"



