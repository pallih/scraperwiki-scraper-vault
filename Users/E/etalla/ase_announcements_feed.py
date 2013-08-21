import scraperwiki
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation
from datetime import date
import re
import json

sourcescraper = 'athens_stock_announcements'
scraperwiki.sqlite.attach(sourcescraper) 


limit = 400
offset = 0

keys =  scraperwiki.sqlite.execute('select * from `athens_stock_announcements`.swdata limit 0')['keys']
data =  scraperwiki.sqlite.select('* from `athens_stock_announcements`.swdata ORDER BY "date" DESC')


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
    <title type='text'>Athens stock exchange announcements</title>
    <updated>%s</updated>
    <id>http://scraperwikiviews.com/run/athens_stock_announcements/?</id> 
    <link rel='self' type='application/atom+xml' href='http://scraperwikiviews.com/run/athens_stock_announcements/?'/>
    <generator uri='http://scraperwikiviews.com/run/athens_stock_announcements/?' version='1.0'></generator>""" % (updated) 

# rows
for row in data:
    try:
        title = row.get('title')
        link = row.get('link')
        date = row.get('date')
        symbol = row.get('symbol') 
        company = row.get('company') 
        updated = "%s" % (row.get('date'))
        printable = 1
    except:
        printable = 0

    if printable == 1: 
        print """    <entry>
        <title> %s - %s - %s </title>
        <link href='%s'/>
        <date> %s </date>
        <updated>%s</updated> 
        <summary type='html'>
        <![CDATA[
            %s - %s <p> %s </p> %s 
        ]]>
        </summary>
        <author>
            <name>Eva</name>
            <uri>http://scraperwiki.com/scrapers/athens_stock_announcements/</uri>
        </author>
        </entry>""" % (symbol, title, date, link, date, updated, company, symbol,title,link)

print "</feed>"

