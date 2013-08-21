# Starting script to get you going fast.  
# Delete code as appropriate

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re
import datetime

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def GetDate(text):
    d = re.match('(\d\d) (\w\w\w), (\d\d\d\d) (\d\d?):(\d\d) (\w\w)', text)
    month = months.index(d.group(2))+1
    h = int(d.group(4))
    if h < 12 and d.group(6) == 'PM':
        h = h + 12 

    return datetime.datetime(int(d.group(3)), month, int(d.group(1)), h, int(d.group(5)))

def articlesforcompany(stockcode):
    url = "http://investegate.co.uk/Rss.aspx?company=%s" % stockcode
    root = lxml.html.parse(url).getroot()

    for item in root.cssselect('item'):
        date = GetDate(item.cssselect('datetime')[0].text + ' ' + item.cssselect('time')[0].text)
        link = item.cssselect('guid')[0].text
        headline = item.cssselect('headline')[0].text
        print date, link, headline
        data = { 'date':date, 'link':link, 'headline':headline, 'stockcode':stockcode }
        scraperwiki.datastore.save(unique_keys=['link'], data=data, date=date)
    
for data in scraperwiki.datastore.getData('takeover-panel-info'):
    stockcode = data.get('OffereeStockCode')
    if stockcode:
        articlesforcompany(stockcode)

                        

# Starting script to get you going fast.  
# Delete code as appropriate

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re
import datetime

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def GetDate(text):
    d = re.match('(\d\d) (\w\w\w), (\d\d\d\d) (\d\d?):(\d\d) (\w\w)', text)
    month = months.index(d.group(2))+1
    h = int(d.group(4))
    if h < 12 and d.group(6) == 'PM':
        h = h + 12 

    return datetime.datetime(int(d.group(3)), month, int(d.group(1)), h, int(d.group(5)))

def articlesforcompany(stockcode):
    url = "http://investegate.co.uk/Rss.aspx?company=%s" % stockcode
    root = lxml.html.parse(url).getroot()

    for item in root.cssselect('item'):
        date = GetDate(item.cssselect('datetime')[0].text + ' ' + item.cssselect('time')[0].text)
        link = item.cssselect('guid')[0].text
        headline = item.cssselect('headline')[0].text
        print date, link, headline
        data = { 'date':date, 'link':link, 'headline':headline, 'stockcode':stockcode }
        scraperwiki.datastore.save(unique_keys=['link'], data=data, date=date)
    
for data in scraperwiki.datastore.getData('takeover-panel-info'):
    stockcode = data.get('OffereeStockCode')
    if stockcode:
        articlesforcompany(stockcode)

                        

# Starting script to get you going fast.  
# Delete code as appropriate

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re
import datetime

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def GetDate(text):
    d = re.match('(\d\d) (\w\w\w), (\d\d\d\d) (\d\d?):(\d\d) (\w\w)', text)
    month = months.index(d.group(2))+1
    h = int(d.group(4))
    if h < 12 and d.group(6) == 'PM':
        h = h + 12 

    return datetime.datetime(int(d.group(3)), month, int(d.group(1)), h, int(d.group(5)))

def articlesforcompany(stockcode):
    url = "http://investegate.co.uk/Rss.aspx?company=%s" % stockcode
    root = lxml.html.parse(url).getroot()

    for item in root.cssselect('item'):
        date = GetDate(item.cssselect('datetime')[0].text + ' ' + item.cssselect('time')[0].text)
        link = item.cssselect('guid')[0].text
        headline = item.cssselect('headline')[0].text
        print date, link, headline
        data = { 'date':date, 'link':link, 'headline':headline, 'stockcode':stockcode }
        scraperwiki.datastore.save(unique_keys=['link'], data=data, date=date)
    
for data in scraperwiki.datastore.getData('takeover-panel-info'):
    stockcode = data.get('OffereeStockCode')
    if stockcode:
        articlesforcompany(stockcode)

                        

# Starting script to get you going fast.  
# Delete code as appropriate

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re
import datetime

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def GetDate(text):
    d = re.match('(\d\d) (\w\w\w), (\d\d\d\d) (\d\d?):(\d\d) (\w\w)', text)
    month = months.index(d.group(2))+1
    h = int(d.group(4))
    if h < 12 and d.group(6) == 'PM':
        h = h + 12 

    return datetime.datetime(int(d.group(3)), month, int(d.group(1)), h, int(d.group(5)))

def articlesforcompany(stockcode):
    url = "http://investegate.co.uk/Rss.aspx?company=%s" % stockcode
    root = lxml.html.parse(url).getroot()

    for item in root.cssselect('item'):
        date = GetDate(item.cssselect('datetime')[0].text + ' ' + item.cssselect('time')[0].text)
        link = item.cssselect('guid')[0].text
        headline = item.cssselect('headline')[0].text
        print date, link, headline
        data = { 'date':date, 'link':link, 'headline':headline, 'stockcode':stockcode }
        scraperwiki.datastore.save(unique_keys=['link'], data=data, date=date)
    
for data in scraperwiki.datastore.getData('takeover-panel-info'):
    stockcode = data.get('OffereeStockCode')
    if stockcode:
        articlesforcompany(stockcode)

                        

