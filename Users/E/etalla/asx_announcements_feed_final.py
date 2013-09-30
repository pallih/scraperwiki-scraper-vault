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
        announcement_feed["key"] = (str(symbol) +" -- " + str(announcement_feed["title"]) +" -- " +str(announcement_feed["date"]))
        scraperwiki.sqlite.save(['key'],announcement_feed)

for row in data:
    if (row.get('symbol')=="TPT"):
        print row.get('symbol')
        name = row.get('name')
        symbol = 'TPT'
        get_announcements('TPT',name)
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
        announcement_feed["key"] = (str(symbol) +" -- " + str(announcement_feed["title"]) +" -- " +str(announcement_feed["date"]))
        scraperwiki.sqlite.save(['key'],announcement_feed)

for row in data:
    if (row.get('symbol')=="TPT"):
        print row.get('symbol')
        name = row.get('name')
        symbol = 'TPT'
        get_announcements('TPT',name)
