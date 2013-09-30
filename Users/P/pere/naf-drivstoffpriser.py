# -*- coding: UTF-8 -*-
import scraperwiki
from BeautifulSoup import BeautifulSoup
import datetime 
import dateutil.parser
import string
import time
import re
import sys
import traceback

def formatExceptionInfo(maxTBlevel=5):
    cla, exc, trbk = sys.exc_info()
    excName = cla.__name__
    try:
        excArgs = exc.__dict__["args"]
    except KeyError:
        excArgs = "<no args>"
    excTb = traceback.format_tb(trbk, maxTBlevel)
    return (excName, excArgs, excTb)

def url_from_id(id):
    url = "http://drivstoffpriser.no/priser/%d" % id
    return url

def product_to_table(product):
    return {
        'Blyfri 95' : 'gas95prices',
        'Blyfri 98' : 'gas98prices',
        'Diesel' : 'diselprices'
    }[product]

def scrape(url):
    for n in [1, 2, 3]:
        try:
            return scraperwiki.scrape(url)
        except:
            continue
    return scraperwiki.scrape(url)


# <div id="center">
# <h1><a href="/bensinstasjoner/1-Esso-Nesttun">Esso Nesttun</a>: Blyfri 95,  5. februar kl. 21:31</h1>
# <p>
#  <b>Pris:</b>
#  12.0<br>
#  <b>Observert:</b>
#  2009-02-05 21:31:18 +0100<br>
#  <b>Sist oppdatert:</b>
#  2012-02-07 22:38:03 +0100<br>
#  <b>Stasjon:</b>
#  <a href="/bensinstasjoner/1-Esso-Nesttun">Esso Nesttun</a>, 
#  <a href="/steder/36-Bergen">Bergen</a><br>
#  <b>Produkt:</b>
#  Blyfri 95<br>
#</p>
#<p>
#</p>
#...

def scrape_price(id, scrapedurl):
    scrapestamputc = datetime.datetime.now()
    html = scrape(scrapedurl)
    soup = BeautifulSoup(html)
    centerblock = soup.findAll(name = "div", attrs={"id" : "center"})
    para = centerblock[0].p
    if -1 == str(para).find("Observert:"):
        msg = "Bad ID " + str(id)
        scraperwiki.sqlite.save(unique_keys=['when'], data={'when':scrapestamputc, 'msg' : msg}, table_name='errors')
        print  msg
        return False
    price = float(para.next.next.next.next)
    when = para.next.next.next.next.next.next.next.next.next.strip()
    stationid = 1
    stationaref = para.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next
    product = para.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next
    stationid = str(stationaref).split("/")[2].split("-")[0]
    data = {
        'priceid' : int(id),
        'stationid' : int(stationid),
        'price' : price,
        'when' : dateutil.parser.parse(when),
        'scrapestamputc' : scrapestamputc,
        'scrapedurl' : scrapedurl,
    }
    tablename = product_to_table(product.strip())
    #print tablename, data
    scraperwiki.sqlite.save(unique_keys=['when', 'stationid'], data=data, table_name=tablename)
    return True

def find_max():
    # The front page rarely have the last price listed.  Bergen on the other hand seem to
    # Have many updates.
    urls = ["http://www.drivstoffpriser.no/", "http://drivstoffpriser.no/steder/36-Bergen"]
    maxpriceid = 0
    for url in urls:
        html = scrape(url)
        soup = BeautifulSoup(html)

# Looking at all links, not just the ones in the center block, because I do not
# know how to find links in a ResultSet
#    centerblock = soup.findAll(name = "div", attrs={"id" : "pricesFront"})
#    print centerblock
        for link in soup.findAll('a', href=True):
            href = link.get('href')
            if -1 != href.find("/priser/") and -1 == href.find("/priser/ny"):
                #print(link.get('href'))
                priceid = str(href).split("/")[2].split("-")[0]
                #print priceid
                if priceid > maxpriceid:
                    maxpriceid = int(priceid)
    #print "MAX: " + str(maxpriceid)
    return maxpriceid

def scrape_station(id):
    scrapedurl = "http://drivstoffpriser.no/bensinstasjoner/%d" % id
    scrapestamputc = datetime.datetime.now()
    html = scrape(scrapedurl)

    glatlng = re.compile("GLatLng\(([^)]+)\)")
    match = glatlng.findall(html)
    print match[0]
    latitude, longitude = match[0].split(",")

    soup = BeautifulSoup(html)
    centerblock = soup.findAll(name = "div", attrs={"id" : "center"})
    para = centerblock[0].table
    #print para
    fieldmap = {
        'Kjede:'   : 'label',
        'Adresse:' : 'address',
        'Sted:'    : 'place',
    }
    entry = {
        'stationid' : int(id),
        'latitude' : float(latitude),
        'longitude' : float(longitude),
        'scrapedurl' : scrapedurl,
    }
    for tr in para.findAll("tr"):
        tds = tr.findAll("td")
        field = tds[0].text
        value = tds[1].text
        if field in fieldmap:
            entry[fieldmap[field]] = value
    #print entry
    scraperwiki.sqlite.save(unique_keys=['stationid'], data=entry, table_name='stations')

def scrape_stations():
    try:
        data = scraperwiki.sqlite.select("distinct stationid from gas95prices where stationid not in (select stationid from stations order by stationid)")
    except scraperwiki.sqlite.SqliteError:
        formatExceptionInfo()
        data = scraperwiki.sqlite.select("distinct stationid from gas95prices order by stationid")
#    print data
    for e in data:
        id = int(e['stationid'])
        scrape_station(id)

max = find_max()

print "Starting the scrape, staying below " + str(max)

min = 0
try:
    min = scraperwiki.sqlite.select("max(priceid) as max from gas95prices")[0]['max'] + 1
    if min > max:
        max = min
except:
    min = 1 # Start here

end = min + 2200

if end > max:
    end = max + 30 # Go a bit further, to see if there are some newer not listed on the front/Bergen page
count = 0
for id in range(min,end):
    if scrape_price(id, url_from_id(id)):
        count = count + 1
    time.sleep(0.3)

print "Scraped %d prices, from %d to %d" % (count, min, end)

scrape_stations()
# -*- coding: UTF-8 -*-
import scraperwiki
from BeautifulSoup import BeautifulSoup
import datetime 
import dateutil.parser
import string
import time
import re
import sys
import traceback

def formatExceptionInfo(maxTBlevel=5):
    cla, exc, trbk = sys.exc_info()
    excName = cla.__name__
    try:
        excArgs = exc.__dict__["args"]
    except KeyError:
        excArgs = "<no args>"
    excTb = traceback.format_tb(trbk, maxTBlevel)
    return (excName, excArgs, excTb)

def url_from_id(id):
    url = "http://drivstoffpriser.no/priser/%d" % id
    return url

def product_to_table(product):
    return {
        'Blyfri 95' : 'gas95prices',
        'Blyfri 98' : 'gas98prices',
        'Diesel' : 'diselprices'
    }[product]

def scrape(url):
    for n in [1, 2, 3]:
        try:
            return scraperwiki.scrape(url)
        except:
            continue
    return scraperwiki.scrape(url)


# <div id="center">
# <h1><a href="/bensinstasjoner/1-Esso-Nesttun">Esso Nesttun</a>: Blyfri 95,  5. februar kl. 21:31</h1>
# <p>
#  <b>Pris:</b>
#  12.0<br>
#  <b>Observert:</b>
#  2009-02-05 21:31:18 +0100<br>
#  <b>Sist oppdatert:</b>
#  2012-02-07 22:38:03 +0100<br>
#  <b>Stasjon:</b>
#  <a href="/bensinstasjoner/1-Esso-Nesttun">Esso Nesttun</a>, 
#  <a href="/steder/36-Bergen">Bergen</a><br>
#  <b>Produkt:</b>
#  Blyfri 95<br>
#</p>
#<p>
#</p>
#...

def scrape_price(id, scrapedurl):
    scrapestamputc = datetime.datetime.now()
    html = scrape(scrapedurl)
    soup = BeautifulSoup(html)
    centerblock = soup.findAll(name = "div", attrs={"id" : "center"})
    para = centerblock[0].p
    if -1 == str(para).find("Observert:"):
        msg = "Bad ID " + str(id)
        scraperwiki.sqlite.save(unique_keys=['when'], data={'when':scrapestamputc, 'msg' : msg}, table_name='errors')
        print  msg
        return False
    price = float(para.next.next.next.next)
    when = para.next.next.next.next.next.next.next.next.next.strip()
    stationid = 1
    stationaref = para.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next
    product = para.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next
    stationid = str(stationaref).split("/")[2].split("-")[0]
    data = {
        'priceid' : int(id),
        'stationid' : int(stationid),
        'price' : price,
        'when' : dateutil.parser.parse(when),
        'scrapestamputc' : scrapestamputc,
        'scrapedurl' : scrapedurl,
    }
    tablename = product_to_table(product.strip())
    #print tablename, data
    scraperwiki.sqlite.save(unique_keys=['when', 'stationid'], data=data, table_name=tablename)
    return True

def find_max():
    # The front page rarely have the last price listed.  Bergen on the other hand seem to
    # Have many updates.
    urls = ["http://www.drivstoffpriser.no/", "http://drivstoffpriser.no/steder/36-Bergen"]
    maxpriceid = 0
    for url in urls:
        html = scrape(url)
        soup = BeautifulSoup(html)

# Looking at all links, not just the ones in the center block, because I do not
# know how to find links in a ResultSet
#    centerblock = soup.findAll(name = "div", attrs={"id" : "pricesFront"})
#    print centerblock
        for link in soup.findAll('a', href=True):
            href = link.get('href')
            if -1 != href.find("/priser/") and -1 == href.find("/priser/ny"):
                #print(link.get('href'))
                priceid = str(href).split("/")[2].split("-")[0]
                #print priceid
                if priceid > maxpriceid:
                    maxpriceid = int(priceid)
    #print "MAX: " + str(maxpriceid)
    return maxpriceid

def scrape_station(id):
    scrapedurl = "http://drivstoffpriser.no/bensinstasjoner/%d" % id
    scrapestamputc = datetime.datetime.now()
    html = scrape(scrapedurl)

    glatlng = re.compile("GLatLng\(([^)]+)\)")
    match = glatlng.findall(html)
    print match[0]
    latitude, longitude = match[0].split(",")

    soup = BeautifulSoup(html)
    centerblock = soup.findAll(name = "div", attrs={"id" : "center"})
    para = centerblock[0].table
    #print para
    fieldmap = {
        'Kjede:'   : 'label',
        'Adresse:' : 'address',
        'Sted:'    : 'place',
    }
    entry = {
        'stationid' : int(id),
        'latitude' : float(latitude),
        'longitude' : float(longitude),
        'scrapedurl' : scrapedurl,
    }
    for tr in para.findAll("tr"):
        tds = tr.findAll("td")
        field = tds[0].text
        value = tds[1].text
        if field in fieldmap:
            entry[fieldmap[field]] = value
    #print entry
    scraperwiki.sqlite.save(unique_keys=['stationid'], data=entry, table_name='stations')

def scrape_stations():
    try:
        data = scraperwiki.sqlite.select("distinct stationid from gas95prices where stationid not in (select stationid from stations order by stationid)")
    except scraperwiki.sqlite.SqliteError:
        formatExceptionInfo()
        data = scraperwiki.sqlite.select("distinct stationid from gas95prices order by stationid")
#    print data
    for e in data:
        id = int(e['stationid'])
        scrape_station(id)

max = find_max()

print "Starting the scrape, staying below " + str(max)

min = 0
try:
    min = scraperwiki.sqlite.select("max(priceid) as max from gas95prices")[0]['max'] + 1
    if min > max:
        max = min
except:
    min = 1 # Start here

end = min + 2200

if end > max:
    end = max + 30 # Go a bit further, to see if there are some newer not listed on the front/Bergen page
count = 0
for id in range(min,end):
    if scrape_price(id, url_from_id(id)):
        count = count + 1
    time.sleep(0.3)

print "Scraped %d prices, from %d to %d" % (count, min, end)

scrape_stations()
