import scraperwiki
import mechanize
import re
import time
import string
import lxml.html 


def getUSDrate():
    html = scraperwiki.scrape("http://www.google.com/finance?q=CADUSD") 
    root = lxml.html.fromstring(html)

    el = root.cssselect("div#currency_value span span")
    return float(el[0].text.strip(string.letters+string.whitespace))


def getINGrates():
    val = scraperwiki.scrape("http://www.ingdirect.ca/en/datafiles/rates/usselling.html")
    selling = float(val )
    val = scraperwiki.scrape("http://www.ingdirect.ca/en/datafiles/rates/usbuying.html")
    buying = float(val )
    return (selling, buying)


def getRoyalRates():
    br = mechanize.Browser()
    br.set_handle_robots( False )
    br.addheaders = [('User-agent', 'Firefox')]
    br.open( "http://www.rbcroyalbank.com/cgi-bin/travel/fxconvert.pl" )

    keep = set(string.digits + '.')

    br.select_form(nr=2)
    br.form['amount'] = '1'
    br['buy_from']= ['CAD']
    br['buy_to']= ['USD']
    br.submit()
    html = br.response().read()
    root = lxml.html.fromstring(html)
    _selling = root.cssselect("span.disclaimer")[0].text

    selling = 1/ float( ''.join(c for c in _selling if c in keep) )

    br.select_form(nr=2)
    br.form['amount'] = '1'
    br['buy_from']= ['USD']
    br['buy_to']= ['CAD']
    br.submit()
    html = br.response().read()
    root = lxml.html.fromstring(html)
    _buying = root.cssselect("span.disclaimer")[0].text

    buying = 1/ float(''.join(c for c in _buying if c in keep))

    return (selling, buying)


def getScotia():
    keep = set(string.digits + '.')
    html = scraperwiki.scrape("https://www.scotiamocatta-estore.scotiabank.com/stores/scotiamocatta/Catalog/catalog.aspx" )
    root = lxml.html.fromstring(html)

    _rate = root.cssselect("span#ctl00_MPH_tblProducts_ctl00_ctl04_lblCADEstimate + span")[0].text
    return float(''.join(c for c in _rate if c in keep))


# database setup
'''
nowTime = 1
nowTimeString = "initial date string"
scraperwiki.sqlite.save(unique_keys=["timestamp"], data={"timestamp":nowTime, "dateStamp":nowTimeString}, table_name="financialNumbers")

rate = 0.09
scraperwiki.sqlite.save(unique_keys=["timestamp"], data={"timestamp":nowTime,"rate":rate}, table_name="financialNumbers")

ingSelling,ingBuying = 1.1,2.2
scraperwiki.sqlite.save(unique_keys=["timestamp"], data={"timestamp":nowTime,"ING_SELLING":ingSelling, "ING_BUYING":ingBuying}, table_name="financialNumbers")

rbcSelling,rbcBuying = 3.3,4.4
scraperwiki.sqlite.save(unique_keys=["timestamp"], data={"timestamp":nowTime,"RBC_SELLING":rbcSelling, "RBC_BUYING":rbcBuying}, table_name="financialNumbers")

exit()
'''


nowTime = int(time.time())
nowDayOfWeek=time.strftime('%w')
nowTimeString = time.strftime('%Y.%m.%d %H:%M',time.gmtime(nowTime - (4*60*60)))

if int(time.strftime('%w',time.gmtime(nowTime - (4*60*60)))) in range(1,6): 
    rate = getUSDrate()
    
    ingSelling,ingBuying = getINGrates()
    
    rbcSelling,rbcBuying = getRoyalRates()
    
    scotiaRate = getScotia()
    
    collectedData={"timestamp":nowTime, "dateStamp":nowTimeString, "rate":rate,
                   "ING_SELLING":ingSelling, "ING_BUYING":ingBuying, 
                   "RBC_SELLING":rbcSelling, "RBC_BUYING":rbcBuying,
                   "SCOTIA":scotiaRate }
    scraperwiki.sqlite.save(unique_keys=["timestamp"], data=collectedData, table_name="financialNumbers")

import scraperwiki
import mechanize
import re
import time
import string
import lxml.html 


def getUSDrate():
    html = scraperwiki.scrape("http://www.google.com/finance?q=CADUSD") 
    root = lxml.html.fromstring(html)

    el = root.cssselect("div#currency_value span span")
    return float(el[0].text.strip(string.letters+string.whitespace))


def getINGrates():
    val = scraperwiki.scrape("http://www.ingdirect.ca/en/datafiles/rates/usselling.html")
    selling = float(val )
    val = scraperwiki.scrape("http://www.ingdirect.ca/en/datafiles/rates/usbuying.html")
    buying = float(val )
    return (selling, buying)


def getRoyalRates():
    br = mechanize.Browser()
    br.set_handle_robots( False )
    br.addheaders = [('User-agent', 'Firefox')]
    br.open( "http://www.rbcroyalbank.com/cgi-bin/travel/fxconvert.pl" )

    keep = set(string.digits + '.')

    br.select_form(nr=2)
    br.form['amount'] = '1'
    br['buy_from']= ['CAD']
    br['buy_to']= ['USD']
    br.submit()
    html = br.response().read()
    root = lxml.html.fromstring(html)
    _selling = root.cssselect("span.disclaimer")[0].text

    selling = 1/ float( ''.join(c for c in _selling if c in keep) )

    br.select_form(nr=2)
    br.form['amount'] = '1'
    br['buy_from']= ['USD']
    br['buy_to']= ['CAD']
    br.submit()
    html = br.response().read()
    root = lxml.html.fromstring(html)
    _buying = root.cssselect("span.disclaimer")[0].text

    buying = 1/ float(''.join(c for c in _buying if c in keep))

    return (selling, buying)


def getScotia():
    keep = set(string.digits + '.')
    html = scraperwiki.scrape("https://www.scotiamocatta-estore.scotiabank.com/stores/scotiamocatta/Catalog/catalog.aspx" )
    root = lxml.html.fromstring(html)

    _rate = root.cssselect("span#ctl00_MPH_tblProducts_ctl00_ctl04_lblCADEstimate + span")[0].text
    return float(''.join(c for c in _rate if c in keep))


# database setup
'''
nowTime = 1
nowTimeString = "initial date string"
scraperwiki.sqlite.save(unique_keys=["timestamp"], data={"timestamp":nowTime, "dateStamp":nowTimeString}, table_name="financialNumbers")

rate = 0.09
scraperwiki.sqlite.save(unique_keys=["timestamp"], data={"timestamp":nowTime,"rate":rate}, table_name="financialNumbers")

ingSelling,ingBuying = 1.1,2.2
scraperwiki.sqlite.save(unique_keys=["timestamp"], data={"timestamp":nowTime,"ING_SELLING":ingSelling, "ING_BUYING":ingBuying}, table_name="financialNumbers")

rbcSelling,rbcBuying = 3.3,4.4
scraperwiki.sqlite.save(unique_keys=["timestamp"], data={"timestamp":nowTime,"RBC_SELLING":rbcSelling, "RBC_BUYING":rbcBuying}, table_name="financialNumbers")

exit()
'''


nowTime = int(time.time())
nowDayOfWeek=time.strftime('%w')
nowTimeString = time.strftime('%Y.%m.%d %H:%M',time.gmtime(nowTime - (4*60*60)))

if int(time.strftime('%w',time.gmtime(nowTime - (4*60*60)))) in range(1,6): 
    rate = getUSDrate()
    
    ingSelling,ingBuying = getINGrates()
    
    rbcSelling,rbcBuying = getRoyalRates()
    
    scotiaRate = getScotia()
    
    collectedData={"timestamp":nowTime, "dateStamp":nowTimeString, "rate":rate,
                   "ING_SELLING":ingSelling, "ING_BUYING":ingBuying, 
                   "RBC_SELLING":rbcSelling, "RBC_BUYING":rbcBuying,
                   "SCOTIA":scotiaRate }
    scraperwiki.sqlite.save(unique_keys=["timestamp"], data=collectedData, table_name="financialNumbers")

