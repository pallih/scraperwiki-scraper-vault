import urllib
import csv
import datetime
import scraperwiki
import re

def genlines():
    # Here is an example CSV file
    url = "http://www.trafford.gov.uk/opendata/sets/supplierspend/2010_04.csv"
    f = urllib.urlopen(url)
    t = ""
    while True:
        t1 = f.read(100)
        if not t1:
            break
        t = t + t1
        try:
            i = t.index('\r')
            yield(t[:i] + '\n')
            t = t[i+1:]
        except ValueError:
            pass
        
c = csv.reader(genlines())
titles = c.next()
print titles
for dat in c:
    data = dict(zip(titles, dat))
    mdate = re.match('(\d\d)/(\d\d)/(\d\d\d\d)', data['Date'])
    data['Date'] = datetime.date(int(mdate.group(3)), int(mdate.group(2)), int(mdate.group(1)))
    scraperwiki.sqlite.save(unique_keys=['Transaction number'], data=data)


import urllib
import csv
import datetime
import scraperwiki
import re

def genlines():
    # Here is an example CSV file
    url = "http://www.trafford.gov.uk/opendata/sets/supplierspend/2010_04.csv"
    f = urllib.urlopen(url)
    t = ""
    while True:
        t1 = f.read(100)
        if not t1:
            break
        t = t + t1
        try:
            i = t.index('\r')
            yield(t[:i] + '\n')
            t = t[i+1:]
        except ValueError:
            pass
        
c = csv.reader(genlines())
titles = c.next()
print titles
for dat in c:
    data = dict(zip(titles, dat))
    mdate = re.match('(\d\d)/(\d\d)/(\d\d\d\d)', data['Date'])
    data['Date'] = datetime.date(int(mdate.group(3)), int(mdate.group(2)), int(mdate.group(1)))
    scraperwiki.sqlite.save(unique_keys=['Transaction number'], data=data)


