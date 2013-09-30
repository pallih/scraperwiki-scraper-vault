# Capture daily price movements of fuels in Adelaide region.
#
# The code is currently quite fragile and will break if
# anything changes or individual data is missing (not 
# unheard of).
# 
# Need to add checks and validate assumptions.

import scraperwiki
import lxml.html
from datetime import datetime

def readAUD():
    currData = root.cssselect("div[id='currency_value'] span")
    currText = currData[0].text_content()
    aud = currText.replace("1 AUD = ", "")
    aud = aud.replace(" USD", "")
    data = {
        'dateUTC' : datetime.utcnow(),
        'AUDUSD' : aud
    }

    return data

def readPrices(divName, typeName):
    rows = root.cssselect("div[id='" + divName + "'] tr")
    low = rows[0].cssselect("td")[1].text_content()
    high = rows[1].cssselect("td")[1].text_content()
    avg = rows[2].cssselect("td")[1].text_content()
    data = {
        'dateUTC' : datetime.utcnow(),
        'type' : typeName,
        'low' : low.split(':')[1].split()[0],
        'high' : high.split(':')[1].split()[0],
        'avg' : avg.split(':')[1].split()[0]
    }

    return data

html = scraperwiki.scrape("http://www.raa.com.au/fuelwatch_cheap_petrol.aspx?TerID=1038")
root = lxml.html.fromstring(html)
scraperwiki.sqlite.save(unique_keys=['dateUTC'], data=readPrices('shopCon0','ULP'))
scraperwiki.sqlite.save(unique_keys=['dateUTC'], data=readPrices('shopCon1','E10'))
scraperwiki.sqlite.save(unique_keys=['dateUTC'], data=readPrices('shopCon2','LPG'))
scraperwiki.sqlite.save(unique_keys=['dateUTC'], data=readPrices('shopCon3','Diesel'))

html = scraperwiki.scrape("http://www.google.com/finance?q=AUDUSD")
root = lxml.html.fromstring(html)
scraperwiki.sqlite.save(unique_keys=['dateUTC'], data=readAUD())

#print str(readAUD())
# Capture daily price movements of fuels in Adelaide region.
#
# The code is currently quite fragile and will break if
# anything changes or individual data is missing (not 
# unheard of).
# 
# Need to add checks and validate assumptions.

import scraperwiki
import lxml.html
from datetime import datetime

def readAUD():
    currData = root.cssselect("div[id='currency_value'] span")
    currText = currData[0].text_content()
    aud = currText.replace("1 AUD = ", "")
    aud = aud.replace(" USD", "")
    data = {
        'dateUTC' : datetime.utcnow(),
        'AUDUSD' : aud
    }

    return data

def readPrices(divName, typeName):
    rows = root.cssselect("div[id='" + divName + "'] tr")
    low = rows[0].cssselect("td")[1].text_content()
    high = rows[1].cssselect("td")[1].text_content()
    avg = rows[2].cssselect("td")[1].text_content()
    data = {
        'dateUTC' : datetime.utcnow(),
        'type' : typeName,
        'low' : low.split(':')[1].split()[0],
        'high' : high.split(':')[1].split()[0],
        'avg' : avg.split(':')[1].split()[0]
    }

    return data

html = scraperwiki.scrape("http://www.raa.com.au/fuelwatch_cheap_petrol.aspx?TerID=1038")
root = lxml.html.fromstring(html)
scraperwiki.sqlite.save(unique_keys=['dateUTC'], data=readPrices('shopCon0','ULP'))
scraperwiki.sqlite.save(unique_keys=['dateUTC'], data=readPrices('shopCon1','E10'))
scraperwiki.sqlite.save(unique_keys=['dateUTC'], data=readPrices('shopCon2','LPG'))
scraperwiki.sqlite.save(unique_keys=['dateUTC'], data=readPrices('shopCon3','Diesel'))

html = scraperwiki.scrape("http://www.google.com/finance?q=AUDUSD")
root = lxml.html.fromstring(html)
scraperwiki.sqlite.save(unique_keys=['dateUTC'], data=readAUD())

#print str(readAUD())
