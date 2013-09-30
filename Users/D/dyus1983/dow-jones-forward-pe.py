import scraperwiki
from BeautifulSoup import BeautifulSoup
import re
import datetime

# define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['Date scraped', 'Ticker', 'Description', 'Value'])

# retrieve a page
index_url = 'http://finance.yahoo.com/q/cp?s=^DJI+Components'
html = scraperwiki.scrape(index_url)
soup = BeautifulSoup(html)

linktable = soup.find(text=re.compile("Symbol")).findPrevious('table')

baseurl = "http://finance.yahoo.com/q/ks?s="
baseurltail = "+Key+Statistics"

date_scraped = datetime.date.today()
print date_scraped

def scrapetickerpage(url, ticker):
    pagehtml = scraperwiki.scrape(url)
    tickersoup = BeautifulSoup(pagehtml)
    ForwardPEValue = tickersoup.find(text=re.compile("Forward P/E")).findNext('td').text
    record = {}
    record['Date scraped'] = date_scraped
    record['Description'] = tickersoup.find(text=re.compile("Forward P/E"))
    record['Value'] = ForwardPEValue
    record['Ticker'] = ticker
    print record
    scraperwiki.datastore.save(["Date scraped", "Ticker"], record)

i = 1
while (i < 31):
    ticker = linktable('tr')[i].td.text
    tickerurl = baseurl + ticker + baseurltail
    scrapetickerpage(tickerurl , ticker)
    i = i + 1





    
#mytable = soup.findAll(id="yfncsumtab")
#mysubtable = mytable.findAll('table')
#print mysubtable

#ForwardPEValue = soup.find(text=re.compile("Forward P/E")).findNext('td').text # Nahodit frazu "Forward P/E" i vydaet znachenie v sleduyshei yacheike

#ili po drugomu:
#MarketCap = soup.find(text=re.compile("Market Cap"))
#MarketCapTag = MarketCap.findNext('td').text

#record = {soup.find(text=re.compile("Forward P/E")):ForwardPEValue}
#scraperwiki.datastore.save([soup.find(text=re.compile("Forward P/E"))], record) 


#mytable = soup('table',limit =10)[9] #Otkryvaet 9-u po scetu tablicu na stranice
#tds = mytable.findAll('td')
#for td in tds:
#    print td
#print mytable.prettify()
#print mytable('tr',limit = 3)[2].prettify()


#for td in tds:
#    print td
#    record = { "td" : td.text }
    # save records to the datastore
#    scraperwiki.datastore.save(["td"], record) import scraperwiki
from BeautifulSoup import BeautifulSoup
import re
import datetime

# define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['Date scraped', 'Ticker', 'Description', 'Value'])

# retrieve a page
index_url = 'http://finance.yahoo.com/q/cp?s=^DJI+Components'
html = scraperwiki.scrape(index_url)
soup = BeautifulSoup(html)

linktable = soup.find(text=re.compile("Symbol")).findPrevious('table')

baseurl = "http://finance.yahoo.com/q/ks?s="
baseurltail = "+Key+Statistics"

date_scraped = datetime.date.today()
print date_scraped

def scrapetickerpage(url, ticker):
    pagehtml = scraperwiki.scrape(url)
    tickersoup = BeautifulSoup(pagehtml)
    ForwardPEValue = tickersoup.find(text=re.compile("Forward P/E")).findNext('td').text
    record = {}
    record['Date scraped'] = date_scraped
    record['Description'] = tickersoup.find(text=re.compile("Forward P/E"))
    record['Value'] = ForwardPEValue
    record['Ticker'] = ticker
    print record
    scraperwiki.datastore.save(["Date scraped", "Ticker"], record)

i = 1
while (i < 31):
    ticker = linktable('tr')[i].td.text
    tickerurl = baseurl + ticker + baseurltail
    scrapetickerpage(tickerurl , ticker)
    i = i + 1





    
#mytable = soup.findAll(id="yfncsumtab")
#mysubtable = mytable.findAll('table')
#print mysubtable

#ForwardPEValue = soup.find(text=re.compile("Forward P/E")).findNext('td').text # Nahodit frazu "Forward P/E" i vydaet znachenie v sleduyshei yacheike

#ili po drugomu:
#MarketCap = soup.find(text=re.compile("Market Cap"))
#MarketCapTag = MarketCap.findNext('td').text

#record = {soup.find(text=re.compile("Forward P/E")):ForwardPEValue}
#scraperwiki.datastore.save([soup.find(text=re.compile("Forward P/E"))], record) 


#mytable = soup('table',limit =10)[9] #Otkryvaet 9-u po scetu tablicu na stranice
#tds = mytable.findAll('td')
#for td in tds:
#    print td
#print mytable.prettify()
#print mytable('tr',limit = 3)[2].prettify()


#for td in tds:
#    print td
#    record = { "td" : td.text }
    # save records to the datastore
#    scraperwiki.datastore.save(["td"], record) 