import scraperwiki
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation
import urllib, urlparse
import datetime
import lxml.etree, lxml.html
import re
import json
#import mechanize

limit = 400
offset = 0

sourcescraper = 'athens_stock_exchange'

scraperwiki.sqlite.attach(sourcescraper) 

keys =  scraperwiki.sqlite.execute('select * from `athens_stock_exchange`.swdata limit 0')['keys']
data =  scraperwiki.sqlite.select('* from `athens_stock_exchange`.swdata')

def get_announcements(symbol,CID,name):
    url=('http://www.ase.gr/content/en/Companies/ListedCo/Profiles/pr_press.asp?Cid='+CID)
    root = lxml.html.parse(url).getroot()
    announcements=(root.find("body/table")
        .findall("tr")[8]
        .findall("td")[1]
        .find("table/tr")
        .findall("td")[1]
        .findall("table")[1]
        .find("td/table"))
    print lxml.html.tostring(announcements)
    for i in announcements[4:]:
        if len(i.findall("td"))==2: # weeds out feeds with no press releases. See CID 825 for example.
            announcement_feed = {}
            date = i.findall("td")[0].text
            day, month, year = map(int, date.split("/"))
            announcement_feed["date"] = datetime.date(year, month, day)
            announcement_feed["link"]="http://www.ase.gr"+i.findall("td")[1].find("a").get("href")
            announcement_feed["title"]=i.findall("td")[1].find("a").text.strip()
            announcement_feed["symbol"]=symbol
            announcement_feed["company"]=name
            announcement_feed["CID"]=CID
            scraperwiki.sqlite.save(['link'],announcement_feed)

for row in data:
    if (row.get('symbol')=="DIFF") or (row.get('symbol')=="NIR") or (row.get('symbol')=="SELO"):
        print row.get('symbol')
        CID = row.get('CID')
        name = row.get('name')
        symbol = row.get('symbol')
        get_announcements(symbol,CID,name)
import scraperwiki
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation
import urllib, urlparse
import datetime
import lxml.etree, lxml.html
import re
import json
#import mechanize

limit = 400
offset = 0

sourcescraper = 'athens_stock_exchange'

scraperwiki.sqlite.attach(sourcescraper) 

keys =  scraperwiki.sqlite.execute('select * from `athens_stock_exchange`.swdata limit 0')['keys']
data =  scraperwiki.sqlite.select('* from `athens_stock_exchange`.swdata')

def get_announcements(symbol,CID,name):
    url=('http://www.ase.gr/content/en/Companies/ListedCo/Profiles/pr_press.asp?Cid='+CID)
    root = lxml.html.parse(url).getroot()
    announcements=(root.find("body/table")
        .findall("tr")[8]
        .findall("td")[1]
        .find("table/tr")
        .findall("td")[1]
        .findall("table")[1]
        .find("td/table"))
    print lxml.html.tostring(announcements)
    for i in announcements[4:]:
        if len(i.findall("td"))==2: # weeds out feeds with no press releases. See CID 825 for example.
            announcement_feed = {}
            date = i.findall("td")[0].text
            day, month, year = map(int, date.split("/"))
            announcement_feed["date"] = datetime.date(year, month, day)
            announcement_feed["link"]="http://www.ase.gr"+i.findall("td")[1].find("a").get("href")
            announcement_feed["title"]=i.findall("td")[1].find("a").text.strip()
            announcement_feed["symbol"]=symbol
            announcement_feed["company"]=name
            announcement_feed["CID"]=CID
            scraperwiki.sqlite.save(['link'],announcement_feed)

for row in data:
    if (row.get('symbol')=="DIFF") or (row.get('symbol')=="NIR") or (row.get('symbol')=="SELO"):
        print row.get('symbol')
        CID = row.get('CID')
        name = row.get('name')
        symbol = row.get('symbol')
        get_announcements(symbol,CID,name)
