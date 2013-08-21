import scraperwiki

# Blank Python


#scraperwiki.sqlite.execute('drop table swdata') #clears datastore
#scraperwiki.sqlite.commit()


print "PSE Watched Stocks EOD"

from BeautifulSoup import BeautifulSoup
import urllib2


from datetime import datetime
from dateutil import tz

from_zone = tz.gettz('UTC')
to_zone = tz.gettz('Asia/Manila')

utc = datetime.utcnow()

utc = utc.replace(tzinfo=from_zone)

manilatime = utc.astimezone(to_zone)

pubdate = manilatime.strftime("%Y-%m-%d %H:%M")

MNLdate = manilatime.strftime("%I:%M%p %a %b-%d ")

print MNLdate, (" Manila Time")

#now = datetime.datetime.now()

#pubdate = now.strftime("%Y-%m-%d %H:%M")

#print pubdate




#First Stock
url = urllib2.urlopen('http://www.bloomberg.com/quote/MJIC:PM')

soup = BeautifulSoup(url)

#tagdate = soup.find('p')

#print tagdate

#print tagdate.string


tag = soup.find('h3')

#print tag

print tag.string


tagprice = soup.find('span', { 'class' : ' price'})

#print tagprice

print tagprice.text

#pubdatestring = str(pubdate)

#guid = pubdatestring + tag.string

data = {'pubdate' : pubdate, 'MNLdate' : MNLdate, 'tag' : tag.string, 'tagprice' : tagprice.text } # column names and value
scraperwiki.sqlite.save(['tag'], data) # save the records



#Second Stock

url = urllib2.urlopen('http://www.bloomberg.com/quote/SMDC:PM')

soup = BeautifulSoup(url)


tag = soup.find('h3')

#print tag

print tag.string


tagprice = soup.find('span', { 'class' : ' price'})

#print tagprice

print tagprice.text


#pubdatestring = str(pubdate)

#guid = pubdatestring + tag.string

data = {'pubdate' : pubdate, 'MNLdate' : MNLdate, 'tag' : tag.string, 'tagprice' : tagprice.text } # column names and value
scraperwiki.sqlite.save(['tag'], data) # save the records




#Third Stock

url = urllib2.urlopen('http://www.bloomberg.com/quote/GMA7:PM')

soup = BeautifulSoup(url)


tag = soup.find('h3')

#print tag

print tag.string


tagprice = soup.find('span', { 'class' : ' price'})

#print tagprice

print tagprice.text


#pubdatestring = str(pubdate)

#guid = pubdatestring + tag.string

data = {'pubdate' : pubdate, 'MNLdate' : MNLdate, 'tag' : tag.string, 'tagprice' : tagprice.text } # column names and value
scraperwiki.sqlite.save(['tag'], data) # save the records






#Fourth Stock

url = urllib2.urlopen('http://www.bloomberg.com/quote/NI:PM')

soup = BeautifulSoup(url)


tag = soup.find('h3')

#print tag

print tag.string


tagprice = soup.find('span', { 'class' : ' price'})

#print tagprice

print tagprice.text



#pubdatestring = str(pubdate)

#guid = pubdatestring + tag.string

data = {'pubdate' : pubdate, 'MNLdate' : MNLdate, 'tag' : tag.string, 'tagprice' : tagprice.text } # column names and value
scraperwiki.sqlite.save(['tag'], data) # save the records






#Fifth Stock

url = urllib2.urlopen('http://www.bloomberg.com/quote/TA:PM')

soup = BeautifulSoup(url)


tag = soup.find('h3')

#print tag

print tag.string


tagprice = soup.find('span', { 'class' : ' price'})

#print tagprice

print tagprice.text



#pubdatestring = str(pubdate)

#guid = pubdatestring + tag.string

data = {'pubdate' : pubdate, 'MNLdate' : MNLdate, 'tag' : tag.string, 'tagprice' : tagprice.text } # column names and value
scraperwiki.sqlite.save(['tag'], data) # save the records
