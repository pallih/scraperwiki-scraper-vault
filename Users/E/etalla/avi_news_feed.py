import scraperwiki
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation
from datetime import date
import re
import json
import urllib

sourcescraper = 'avi_news_scraper'
scraperwiki.sqlite.attach(sourcescraper) 
limit = 400
offset = 0

keys =  scraperwiki.sqlite.execute('select * from `avi_news_scraper`.swdata limit 0')['keys']
data =  scraperwiki.sqlite.select('* from `avi_news_scraper`.swdata ORDER BY "date" DESC')


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
    <title type='text'>AVI news and SENS announcements</title>
    <updated>%s</updated>
    <id>http://scraperwikiviews.com/run/avi_news_scraper/?</id> 
    <link rel='self' type='application/atom+xml' href='http://scraperwikiviews.com/run/avi_news_scraper/?'/>
    <generator uri='http://scraperwikiviews.com/run/avi_news_scraper/?' version='1.0'></generator>""" % (updated) 

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
        <link href='%s'/>
        <updated> %s </updated> 
        <summary type='html'>
        <![CDATA[
           <p><a href='%s'>%s</a></p>
        ]]>
        </summary>
        </entry>""" % (date, title, link, updated, link, summary)

print "</feed>"



