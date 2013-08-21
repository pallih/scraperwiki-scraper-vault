# Blank Python
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

datescraped = datetime.date.today()
print datescraped

def scrapetickerpage(url, ticker):
    pagehtml = scraperwiki.scrape(url)
    tickersoup = BeautifulSoup(pagehtml)
    ForwardPEValue = tickersoup.find(text=re.compile("Forward P/E")).findNext('td').text
    record = {}
    record['Date scraped'] = datescraped
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


