import BeautifulSoup
from scraperwiki import scrape, sqlite
import datetime, re, json

html = scrape('http://tinyurl.com/tulevat-tanssit')
restrict = BeautifulSoup.SoupStrainer(["h2","dl"])

conversion = BeautifulSoup.BeautifulStoneSoup.ALL_ENTITIES
page = BeautifulSoup.BeautifulStoneSoup(html, parseOnlyThese=restrict,convertEntities=conversion)

dates = page.findAll("h2")

for d in dates:
    wday, dinfo = d.a.contents[0].split()
    record = {'weekday': wday }
    mdate = re.match("(\d+)\.(\d+)\.(\d\d\d\d)", dinfo)
    date = datetime.date(int(mdate.group(3)), int(mdate.group(2)), int(mdate.group(1)))
    dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None
    date = json.dumps(date, default = dthandler)
    record['date'] = date
    data = d.nextSibling
    try:
        record['place'] = data.dt.a.text
    except Exception, e:
        print data
    record['artists'] = data.dd.text.replace('&',' & ').replace(',',', ')
    sqlite.save(unique_keys=['place', 'date'], data=record, date=date)
    


import BeautifulSoup
from scraperwiki import scrape, sqlite
import datetime, re, json

html = scrape('http://tinyurl.com/tulevat-tanssit')
restrict = BeautifulSoup.SoupStrainer(["h2","dl"])

conversion = BeautifulSoup.BeautifulStoneSoup.ALL_ENTITIES
page = BeautifulSoup.BeautifulStoneSoup(html, parseOnlyThese=restrict,convertEntities=conversion)

dates = page.findAll("h2")

for d in dates:
    wday, dinfo = d.a.contents[0].split()
    record = {'weekday': wday }
    mdate = re.match("(\d+)\.(\d+)\.(\d\d\d\d)", dinfo)
    date = datetime.date(int(mdate.group(3)), int(mdate.group(2)), int(mdate.group(1)))
    dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None
    date = json.dumps(date, default = dthandler)
    record['date'] = date
    data = d.nextSibling
    try:
        record['place'] = data.dt.a.text
    except Exception, e:
        print data
    record['artists'] = data.dd.text.replace('&',' & ').replace(',',', ')
    sqlite.save(unique_keys=['place', 'date'], data=record, date=date)
    


