#News feed for announcements of selected Thai listed companies

import scraperwiki
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation
from datetime import datetime
import re
import json
import urllib

sourcescraper = 'thai_stock_exchange_announcements'
scraperwiki.sqlite.attach(sourcescraper) 
limit = 400
offset = 0

keys =  scraperwiki.sqlite.execute('select * from `thai_stock_exchange_announcements`.swdata limit 0')['keys']
data =  scraperwiki.sqlite.select('* from `thai_stock_exchange_announcements`.swdata ORDER BY "date" DESC')

ure = re.compile(".*(http.*uid=[0-9]*)", re.DOTALL)
nre = re.compile(".*strong.(.*strong)", re.DOTALL) 
allre = re.compile(".*", re.DOTALL)

for row in data:
    updated = "%s" % (row.get('date'))
    print updated
    break

print """<?xml version="1.0" encoding="utf-8"?>

<feed xmlns='http://www.w3.org/2005/Atom'>
    <title type='text'>Thai stock announcements</title>
    <updated>%s</updated>
    <id>http://scraperwikiviews.com/run/thai_stock_exchange_announcements/?</id> 
    <link rel='self' type='application/atom+xml' href='http://scraperwikiviews.com/run/thai_stock_exchange_announcements/?'/>
    <generator uri='http://scraperwikiviews.com/run/thai_stock_exchange_announcements/?' version='1.0'></generator>""" % (updated) 


for row in data:
    print """    <entry>
        <title>  %s - %s - %s </title>
        <link href='%s'/>
        <date> %s </date>
        <updated> %s </updated> 
        <summary type='html'>
        <![CDATA["%s - %s <p><a href='%s'>%s</a></p>"]]>
        </summary>
        </entry>""" % (row.get('date'), row.get('company'), row.get('title'), row.get('link'), row.get('date'), updated, row.get('symbol'), row.get('company'),row.get('link'),row.get('title'))

print "</feed>"

