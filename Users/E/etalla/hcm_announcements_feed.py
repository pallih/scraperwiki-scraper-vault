import scraperwiki
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation
from datetime import datetime
import re
import json
import urllib

sourcescraper = 'hcm_stock_announcements'
scraperwiki.sqlite.attach(sourcescraper) 
limit = 400
offset = 0

keys =  scraperwiki.sqlite.execute('select * from `hcm_stock_announcements`.swdata limit 0')['keys']
data =  scraperwiki.sqlite.select('* from `hcm_stock_announcements`.swdata ORDER BY "date" DESC')


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
    <title type='text'>HCM announcements</title>
    <updated>%s</updated>
    <id>http://scraperwikiviews.com/run/hcm_stock_announcements/?</id> 
    <link rel='self' type='application/atom+xml' href='http://scraperwikiviews.com/run/hcm_stock_announcements/?'/>
    <generator uri='http://scraperwikiviews.com/run/hcm_stock_announcements/?' version='1.0'></generator>""" % (updated) 

# rows
for row in data:
    try:
        title = str(row.get('title').strip())
        title = title[5:]
        date = row.get('date')
        symbol = row.get('symbol') 
        company = row.get('company').strip()
        company = (company.replace("Joint Stock Company.","")
                .replace("Joint Stock Company","")
                .replace("JOINT STOCK COMPANY","")
                .replace("Seafood Group Corporation","")
                .replace("Import Export Corporation","")
                .replace("Import-Export And Processing","")
                .replace ("Import & Export","")
                .replace("IMPORT AND EXPORT","")
                .replace("CORPORATION",""))
        link = row.get('link') 
        updated = "%s" % (row.get('date'))
        printable = 1
    except:
        printable = 0

    if printable == 1: 
        print """    <entry>
        <title>  %s - %s - %s </title>
        <link href='%s'/>
        <date> %s </date>
        <updated> %s </updated> 
        <summary type='html'>
        <![CDATA[
            %s - %s <p><a href='%s'>%s</a></p>
        ]]>
        </summary>
        </entry>""" % (company, date, title, link, date, updated, company, date, link, title)

print "</feed>"



