import scraperwiki

# Blank Python

#scraperwiki.sqlite.execute('drop table swdata') #clears datastore
#scraperwiki.sqlite.commit()

print "PSE Watched Stocks EOD"

from BeautifulSoup import BeautifulSoup
import urllib2
import re

from datetime import datetime
from dateutil import tz

from_zone = tz.gettz('UTC')
to_zone = tz.gettz('Europe/Prague')

utc = datetime.utcnow()
utc = utc.replace(tzinfo=from_zone)

praguetime = utc.astimezone(to_zone)
pubdate = praguetime.strftime("%Y-%m-%d %H:%M")
PRGdate = praguetime.strftime("%I:%M%p %a %b-%d ")

print PRGdate, (" Prague Time")

#now = datetime.datetime.now()
#pubdate = now.strftime("%Y-%m-%d %H:%M")
#print pubdate


# Test
# url = urllib2.urlopen('http://www.bloomberg.com/quote/CEZ:CP')
# soup = BeautifulSoup(url)
#print(soup.prettify())


#First Stock

url = urllib2.urlopen('http://www.bloomberg.com/quote/SPY:US')
soup = BeautifulSoup(url)

#tagdate = soup.find('p')
#print tagdate
#print tagdate.string

#52w high and low
#################
table = soup.find('table', 'snapshot_table')
row = table.find('tr', 'bottom')
cells = row.findChildren(['th', 'td'])
numbers = cells[3].text
wlow, trail = numbers.split(" ",1)
whigh = re.search(r'[\d,.]+$', trail).group(0)

print 'low:', wlow, 'high:', whigh 
