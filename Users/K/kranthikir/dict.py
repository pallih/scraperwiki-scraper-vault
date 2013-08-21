import scraperwiki

# Blank Python


print "PSE Watched Stocks EOD"

from BeautifulSoup import BeautifulSoup
import urllib2


import datetime
now = datetime.datetime.now()
pubdate = now.strftime("%Y-%m-%d %H:%M")




#First Stock
url = urllib2.urlopen('http://www.epexspot.com/en/market-data/intraday')

soup = BeautifulSoup(url)

tagdate = soup.find('p')

#print tagdate

print tagdate.string


tag = soup.find('h3')

#print tag

print tag.string


tagprice = soup.find('span', { 'class' : ' price'})

#print tagprice

print tagprice.text

data = {'pubdate' : pubdate, 'tagdate' : tagdate.string, 'tag' : tag.string, 'tagprice' : tagprice.text } # column names and value
scraperwiki.sqlite.save(['tag'], data) # save the records

