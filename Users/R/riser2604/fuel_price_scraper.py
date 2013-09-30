# Capture daily price movements of fuels in Sydney region.
#
# The code is currently quite fragile and will break if
# anything changes or individual data is missing (not 
# unheard of).
# 
# TODO: Need to add checks and validate assumptions.
# TODO: Rewrite retrieval code so the retrieves aren't global
# TODO: Retrieve 'MOPS95 Petrol' values, and maybe even 'WTI Crude' prices if useful.
# TODO: Probably need to redo the schema and put fuel in one table & other values in another.
#
###########################################
# History
#
# 20130116 - Changed AUDUSD source from finance.google.com to 
#            more reliable google docs-based spreadsheet.
# 20130330 - Added 'Dated Brent' spot price data in $US/Brl
#
###########################################

import scraperwiki
import lxml.html
from datetime import datetime

# The old method of hitting finance.google.com directly yielded
# unreliable results (probably due to slight differences in structure
# for open/closed sessions) so now using a more stable Google Docs
# spreadsheet which accesses finance data via the API, updates the data
# on a trigger and publishes the results via HTML (for anyone else who's 
# interested in how this is done. I got my introduction to this technique
# from http://currencyfeed.com).
#
# I'm probably not doing this at all efficiently but for now it's working
# fine.
def readAUDUSD():
    for el in root.cssselect("table#tblMain tr"):
        # Expected row structure: 5 cells, 1st & 5th ignored; [1]=name (eg 'AUDUSD'), [2]=timestamp, [3]=value
        kids = el.getchildren()
        if kids[1].text == "AUDUSD":
            return {
                'dateUTC' : datetime.utcnow(),
                'AUDUSD' : kids[3].text
            }
            
def readFuelPrices(divName, typeName):
    rows = root.cssselect("div[id='" + divName + "'] tr")
    low = rows[0].cssselect("td")[1].text_content()
    high = rows[1].cssselect("td")[1].text_content()
    avg = rows[2].cssselect("td")[1].text_content()
    return {
        'dateUTC' : datetime.utcnow(),
        'type' : typeName,
        'low' : low.split(':')[1].split()[0],
        'high' : high.split(':')[1].split()[0],
        'avg' : avg.split(':')[1].split()[0]
    }

def readDatedBrentSpot():
    for el in root.cssselect("div[id='divDaily']"):
        # Expected structure is 3 children: h1, span (class=dailyPrice) and div (class=dailyText).  The span's text is the data we're after.
        return {
            'dateUTC' : datetime.utcnow(),
            'DatedBrentUSBrl' : el[1].text_content()
        }
    
html = scraperwiki.scrape("http://www.mynrma.com.au/motoring/car-care/fuel-prices.htm")
root = lxml.html.fromstring(html)
scraperwiki.sqlite.save(unique_keys=['dateUTC'], data=readFuelPrices('shopCon0','ULP'))
scraperwiki.sqlite.save(unique_keys=['dateUTC'], data=readFuelPrices('shopCon1','E10'))
scraperwiki.sqlite.save(unique_keys=['dateUTC'], data=readFuelPrices('shopCon2','LPG'))
scraperwiki.sqlite.save(unique_keys=['dateUTC'], data=readFuelPrices('shopCon3','Diesel'))

html = scraperwiki.scrape("https://docs.google.com/spreadsheet/pub?key=0AvP8OjyD5-Q8dGx2OXhybmlpYUlPTlNsWE1qOE9hSlE&gid=0")
root = lxml.html.fromstring(html)
scraperwiki.sqlite.save(unique_keys=['dateUTC'], data=readAUDUSD())

html = scraperwiki.scrape("http://www.indexmundi.com/commodities/?commodity=crude-oil-brent")
root = lxml.html.fromstring(html)
scraperwiki.sqlite.save(unique_keys=['dateUTC'], data=readDatedBrentSpot())

# Testing
#print str(readAUDUSD())
# Capture daily price movements of fuels in Sydney region.
#
# The code is currently quite fragile and will break if
# anything changes or individual data is missing (not 
# unheard of).
# 
# TODO: Need to add checks and validate assumptions.
# TODO: Rewrite retrieval code so the retrieves aren't global
# TODO: Retrieve 'MOPS95 Petrol' values, and maybe even 'WTI Crude' prices if useful.
# TODO: Probably need to redo the schema and put fuel in one table & other values in another.
#
###########################################
# History
#
# 20130116 - Changed AUDUSD source from finance.google.com to 
#            more reliable google docs-based spreadsheet.
# 20130330 - Added 'Dated Brent' spot price data in $US/Brl
#
###########################################

import scraperwiki
import lxml.html
from datetime import datetime

# The old method of hitting finance.google.com directly yielded
# unreliable results (probably due to slight differences in structure
# for open/closed sessions) so now using a more stable Google Docs
# spreadsheet which accesses finance data via the API, updates the data
# on a trigger and publishes the results via HTML (for anyone else who's 
# interested in how this is done. I got my introduction to this technique
# from http://currencyfeed.com).
#
# I'm probably not doing this at all efficiently but for now it's working
# fine.
def readAUDUSD():
    for el in root.cssselect("table#tblMain tr"):
        # Expected row structure: 5 cells, 1st & 5th ignored; [1]=name (eg 'AUDUSD'), [2]=timestamp, [3]=value
        kids = el.getchildren()
        if kids[1].text == "AUDUSD":
            return {
                'dateUTC' : datetime.utcnow(),
                'AUDUSD' : kids[3].text
            }
            
def readFuelPrices(divName, typeName):
    rows = root.cssselect("div[id='" + divName + "'] tr")
    low = rows[0].cssselect("td")[1].text_content()
    high = rows[1].cssselect("td")[1].text_content()
    avg = rows[2].cssselect("td")[1].text_content()
    return {
        'dateUTC' : datetime.utcnow(),
        'type' : typeName,
        'low' : low.split(':')[1].split()[0],
        'high' : high.split(':')[1].split()[0],
        'avg' : avg.split(':')[1].split()[0]
    }

def readDatedBrentSpot():
    for el in root.cssselect("div[id='divDaily']"):
        # Expected structure is 3 children: h1, span (class=dailyPrice) and div (class=dailyText).  The span's text is the data we're after.
        return {
            'dateUTC' : datetime.utcnow(),
            'DatedBrentUSBrl' : el[1].text_content()
        }
    
html = scraperwiki.scrape("http://www.mynrma.com.au/motoring/car-care/fuel-prices.htm")
root = lxml.html.fromstring(html)
scraperwiki.sqlite.save(unique_keys=['dateUTC'], data=readFuelPrices('shopCon0','ULP'))
scraperwiki.sqlite.save(unique_keys=['dateUTC'], data=readFuelPrices('shopCon1','E10'))
scraperwiki.sqlite.save(unique_keys=['dateUTC'], data=readFuelPrices('shopCon2','LPG'))
scraperwiki.sqlite.save(unique_keys=['dateUTC'], data=readFuelPrices('shopCon3','Diesel'))

html = scraperwiki.scrape("https://docs.google.com/spreadsheet/pub?key=0AvP8OjyD5-Q8dGx2OXhybmlpYUlPTlNsWE1qOE9hSlE&gid=0")
root = lxml.html.fromstring(html)
scraperwiki.sqlite.save(unique_keys=['dateUTC'], data=readAUDUSD())

html = scraperwiki.scrape("http://www.indexmundi.com/commodities/?commodity=crude-oil-brent")
root = lxml.html.fromstring(html)
scraperwiki.sqlite.save(unique_keys=['dateUTC'], data=readDatedBrentSpot())

# Testing
#print str(readAUDUSD())
