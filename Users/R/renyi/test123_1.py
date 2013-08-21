import scraperwiki
import re
import urllib2
from datetime import datetime, timedelta

# Strips HTML entities
strip_he    = re.compile('&.*?;', re.IGNORECASE|re.DOTALL)

# Make sure value is float, strip other string elements
strip_float = re.compile('[^0-9.]', re.IGNORECASE|re.DOTALL)

today     = datetime.today()
from_date = today - timedelta(days=1)
to_date   = today + timedelta(days=1)

from_date = datetime.strftime(from_date, '%Y/%m/%d')
to_date   = datetime.strftime(to_date, '%Y/%m/%d')
print 'From: %s, To: %s' % (from_date, to_date)

url   = "http://www.prudentialfunds.com.my/historypricing.php"
data  = "scheme=ALL&from=%s&to=%s&submit=Submit" % (from_date, to_date)

# html = scraperwiki.scrape(url)
req  = urllib2.Request(url=url, data=data)
html = urllib2.urlopen(req)

def tryfloat(s):
    try:
        return float(s)
    except ValueError:
        return 0.0

COL_DATE   = 1 # 0
COL_CODE   = 2 # 1
COL_NAME   = 3 # 2
COL_NAV    = 4 # 3
COL_SELL   = 6 # 4
COL_BUY    = 7 # 5
COL_CHANGE = 8 # 6
COL_CHARGE = 10 # 7
COL_FEE    = 11 # 8

from BeautifulSoup import BeautifulSoup
table = BeautifulSoup(html).find("table", { "class" : "graf" })
rows  = table.findAll("tr", { "class" : "bodycopy" })

for r in rows:
    try:
        cols = r.findAll("td")

        if len(cols) == 12:
            data = {}                
            
            data['date']   = strip_he.sub('', cols[COL_DATE].string)
            data['date']   = datetime.strptime(data['date'], '%d/%m/%Y').date()

            data['code']   = strip_he.sub('', cols[COL_CODE].string)
            data['name']   = strip_he.sub('', cols[COL_NAME].string)

            data['nav']    = tryfloat(strip_float.sub('', cols[COL_NAV].string))
            data['sell']   = tryfloat(strip_float.sub('', cols[COL_SELL].string))
            data['buy']    = tryfloat(strip_float.sub('', cols[COL_BUY].string))
            data['change'] = tryfloat(strip_float.sub('', cols[COL_CHANGE].font.string)) if cols[COL_CHANGE].font else tryfloat(strip_float.sub('', cols[COL_CHANGE].string))
            data['charge'] = tryfloat(strip_float.sub('', cols[COL_CHARGE].string))
            data['fee']    = tryfloat(strip_float.sub('', cols[COL_FEE].string))

            data['fid']    = '%s_%s' % (data['date'], data['code'])
            scraperwiki.sqlite.save(unique_keys=['fid'], data=data)
    except Exception, e:
        print '%s' % e
