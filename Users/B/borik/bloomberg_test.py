import scraperwiki

# Blank Python

# scraperwiki.sqlite.execute('drop table swdata') #clears datastore
# scraperwiki.sqlite.commit()

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

#symbols = ['CEZ:CP' , 'CEZ:CP']

#Stock:CEZ:CP

url = urllib2.urlopen('http://www.bloomberg.com/quote/CEZ:CP')
soup = BeautifulSoup(url)

#52w high and low
#################
table = soup.find('table', 'snapshot_table')
row = table.find('tr', 'bottom')
cells = row.findChildren(['th', 'td'])
numbers = cells[3].text
wlow, trail = numbers.split(" ",1)
whigh = re.search(r'[\d,.]+$', trail).group(0)
print 'low:', wlow, 'high:', whigh 

# Symbol lookup
###############
tag = soup.find('h3')
# print tag
print tag.string

#Price lookup
##############
tagprice_currency = soup.find('span', { 'class' : ' price'}).text

print tagprice_currency

tagprice = re.search(r'[\d,.]+', tagprice_currency).group(0)
tagcurrency = re.search(r'[A-Z]+', tagprice_currency).group(0)

print tagprice
print tagcurrency

data = {'pubdate' : pubdate, 'PRGdate' : PRGdate, 'tag' : tag.string, 'tagprice' : tagprice, 'tagcurrency' : tagcurrency, 'wlow' : wlow, 'whigh' : whigh } # column names and value

#Key Statistics
###############

data2 = {}

stats = soup.find('table', 'key_stat_data')
stats_rows = stats.findAll('tr')

for tr in stats_rows:
    stats_name = tr.th
    stats_value = tr.td
    stats_name = re.sub('[^A-Za-z0-9]+', '', stats_name.text)
    stats_value = stats_value.text.replace(' ', '')
    print stats_name
    print stats_value
    data3 = {stats_name : stats_value}
    data2.update(data3),

data.update(data2)

#Exchange
#########

data2 = {}

exchange = soup.find('div', 'exchange_type').ul

#print exchange

for li in exchange.findAll('li'):
    keys = li.text.split(':')
    data2 = { keys[0] : keys[1] }
    data.update(data2),

print data

#exchange_li = exchange.findAll('li')
#data.update(data2)

#Save data
##########

scraperwiki.sqlite.save(['tag'], data) # save the records
import scraperwiki

# Blank Python

# scraperwiki.sqlite.execute('drop table swdata') #clears datastore
# scraperwiki.sqlite.commit()

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

#symbols = ['CEZ:CP' , 'CEZ:CP']

#Stock:CEZ:CP

url = urllib2.urlopen('http://www.bloomberg.com/quote/CEZ:CP')
soup = BeautifulSoup(url)

#52w high and low
#################
table = soup.find('table', 'snapshot_table')
row = table.find('tr', 'bottom')
cells = row.findChildren(['th', 'td'])
numbers = cells[3].text
wlow, trail = numbers.split(" ",1)
whigh = re.search(r'[\d,.]+$', trail).group(0)
print 'low:', wlow, 'high:', whigh 

# Symbol lookup
###############
tag = soup.find('h3')
# print tag
print tag.string

#Price lookup
##############
tagprice_currency = soup.find('span', { 'class' : ' price'}).text

print tagprice_currency

tagprice = re.search(r'[\d,.]+', tagprice_currency).group(0)
tagcurrency = re.search(r'[A-Z]+', tagprice_currency).group(0)

print tagprice
print tagcurrency

data = {'pubdate' : pubdate, 'PRGdate' : PRGdate, 'tag' : tag.string, 'tagprice' : tagprice, 'tagcurrency' : tagcurrency, 'wlow' : wlow, 'whigh' : whigh } # column names and value

#Key Statistics
###############

data2 = {}

stats = soup.find('table', 'key_stat_data')
stats_rows = stats.findAll('tr')

for tr in stats_rows:
    stats_name = tr.th
    stats_value = tr.td
    stats_name = re.sub('[^A-Za-z0-9]+', '', stats_name.text)
    stats_value = stats_value.text.replace(' ', '')
    print stats_name
    print stats_value
    data3 = {stats_name : stats_value}
    data2.update(data3),

data.update(data2)

#Exchange
#########

data2 = {}

exchange = soup.find('div', 'exchange_type').ul

#print exchange

for li in exchange.findAll('li'):
    keys = li.text.split(':')
    data2 = { keys[0] : keys[1] }
    data.update(data2),

print data

#exchange_li = exchange.findAll('li')
#data.update(data2)

#Save data
##########

scraperwiki.sqlite.save(['tag'], data) # save the records
