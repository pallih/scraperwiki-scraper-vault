import scraperwiki
import lxml.html
from datetime import datetime


def get_temp(timestamp):
    #print datetime.fromtimestamp(timestamp)
    url = "http://www.emhi.ee/index.php?ide=21&v_kaart=0&go=4&ts=%d" % timestamp
    html = scraperwiki.scrape(url)
    #print "Asking %s" % url
    
    root = lxml.html.fromstring(html)
    tables = root.cssselect("table")
    for tr in tables[-2].cssselect("tr"):
        tds = tr.cssselect("td")
        if "Tallinn" in tds[0].text_content():
            return tds[2].text_content()

#dt = datetime.now()
#dt_truncated = datetime(dt.year,dt.month,dt.day,dt.hour)

#timestamp = int(dt.strftime("%s"))
#print get_temp(timestamp)

timestamp = 1359484151
for i in range(360 * 4):
    timestamp = int(datetime.fromtimestamp(timestamp - 60*60*6).strftime("%s"))
    data = {'timestamp': timestamp, 'temp': get_temp(timestamp)}
    scraperwiki.sqlite.save(unique_keys=['timestamp'], data=data)import scraperwiki
import lxml.html
from datetime import datetime


def get_temp(timestamp):
    #print datetime.fromtimestamp(timestamp)
    url = "http://www.emhi.ee/index.php?ide=21&v_kaart=0&go=4&ts=%d" % timestamp
    html = scraperwiki.scrape(url)
    #print "Asking %s" % url
    
    root = lxml.html.fromstring(html)
    tables = root.cssselect("table")
    for tr in tables[-2].cssselect("tr"):
        tds = tr.cssselect("td")
        if "Tallinn" in tds[0].text_content():
            return tds[2].text_content()

#dt = datetime.now()
#dt_truncated = datetime(dt.year,dt.month,dt.day,dt.hour)

#timestamp = int(dt.strftime("%s"))
#print get_temp(timestamp)

timestamp = 1359484151
for i in range(360 * 4):
    timestamp = int(datetime.fromtimestamp(timestamp - 60*60*6).strftime("%s"))
    data = {'timestamp': timestamp, 'temp': get_temp(timestamp)}
    scraperwiki.sqlite.save(unique_keys=['timestamp'], data=data)