import scraperwiki
import BeautifulSoup
import re
import time
from email import Utils
from scraperwiki import datastore

print 'imports complete'

arrivals = scraperwiki.scrape('http://www.shj-airport.gov.ae/fids/fidailyflta.htm')
departures = scraperwiki.scrape('http://www.shj-airport.gov.ae/fids/fidailyfltd.htm')

print 'data loaded'

arrpage = BeautifulSoup.BeautifulSoup(arrivals)
deptpage = BeautifulSoup.BeautifulSoup(departures)

print 'parsers initialised'

arrivalrows = [[item.string for item in tr.findAll('td')] for tr in arrpage.findAll('tr', attrs = {'id': 'a1'})]
departurerows = [[item.string for item in tr.findAll('td')] for tr in deptpage.findAll('tr', attrs = {'id': 'a1'})]
outlist = []

print 'parsing complete'

def timehandler(rawtime):
    timeinput = re.split('[\s:-]', rawtime)
    timeinput.insert(2, year)
    t1 = ' '.join(timeinput)
    timeobject = time.strptime(t1, "%d %b %Y %H %M")
    unixtime = time.mktime(timeobject)
    date = Utils.formatdate(unixtime)
    return unixtime, date

print 'timehandler created'

for item in arrivalrows:
    item.insert(2, u'Sharjah')
    rawtime, source, destination, airline, flightno, notes = item
    timedata = timehandler(rawtime)
    unixtime, date = timedata
    flight = dict(zip((outputkeys),(airline, flightno, source, destination, date, notes, unixtime)))
    outlist.append(flight)

print 'arrivals processed' 
    
for item in departurerows:
    item.insert(1, u'Sharjah')
    rawtime, source, destination, airline, flightno, notes = item
    timedata = timehandler(rawtime)
    unixtime, date = timedata
    flight = dict(zip((outputkeys),(airline, flightno, source, destination, timeout, date, unixtime)))
    outlist.append(flight)
    
print 'departures processed'

sorted = outlist.sort(key=flight["unixtime"])
print 'sorted'

for flight in sorted:
    uniquekey = ["unixtime"]
    print flight
    datastore.save(unique_keys=uniquekey, data=flight)
    

