import scraperwiki
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation
from dateutil import parser
import urllib, urlparse
import lxml.etree, lxml.html
import re
import json
#import mechanize

limit = 400
offset = 0

sourcescraper = 'australian_stock_exchange'

scraperwiki.sqlite.attach(sourcescraper) 

keys =  scraperwiki.sqlite.execute('select * from `australian_stock_exchange`.swdata limit 0')['keys']
data =  scraperwiki.sqlite.select('* from `australian_stock_exchange`.swdata')

def get_announcements(symbol,name):
    url=('http://www.asx.com.au/asx/research/companyInfo.do?by=asxCode&asxCode='+symbol+'#headlines')
    root = lxml.html.parse(url).getroot()
    announcements=(root.find("body")
    .findall("div")[1]
    .findall("div")[0]
    .findall("div")[1]
    .findall("div")[2]
    .findall("div")[1]
    .findall("table")[5])
    #print lxml.html.tostring(announcements)
    
    for i in announcements[1:]:
        announcement_feed = {}
        date = (i.findall("td")[0].text).split("/")
        announcement_feed["date"]= "%s-%s-%s" %(date[2],date[1],date[0])
        announcement_feed["title"]=i.findall("td")[2].text
        announcement_feed["symbol"]='TPT'
        announcement_feed["company"]=name
       

for row in data:
    if (row.get('symbol')=="CSS" or (row.get('symbol')=="TGR")or(row.get('symbol')=="CAQ")):
        print row.get('symbol')
        name = row.get('name')
        symbol = 'TPT'
        get_announcements('TPT',name)
        
        
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

