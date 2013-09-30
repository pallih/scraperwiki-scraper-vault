###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
import re

# retrieve a page
starting_url = 'http://finance.yahoo.com/q/ks?s=GE+Key+Statistics'
html = scraperwiki.scrape(starting_url)
soup = BeautifulSoup(html)

#mytable = soup.findAll(id="yfncsumtab")
#mysubtable = mytable.findAll('table')
#print mysubtable

ForwardPEValue = soup.find(text=re.compile("Forward P/E")).findNext('td').text # Nahodit frazu "Forward P/E" i vydaet znachenie v sleduyshei yacheike

#ili po drugomu:
#MarketCap = soup.find(text=re.compile("Market Cap"))
#MarketCapTag = MarketCap.findNext('td').text

record = {soup.find(text=re.compile("Forward P/E")):ForwardPEValue}
scraperwiki.datastore.save([soup.find(text=re.compile("Forward P/E"))], record) 


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
    
###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
import re

# retrieve a page
starting_url = 'http://finance.yahoo.com/q/ks?s=GE+Key+Statistics'
html = scraperwiki.scrape(starting_url)
soup = BeautifulSoup(html)

#mytable = soup.findAll(id="yfncsumtab")
#mysubtable = mytable.findAll('table')
#print mysubtable

ForwardPEValue = soup.find(text=re.compile("Forward P/E")).findNext('td').text # Nahodit frazu "Forward P/E" i vydaet znachenie v sleduyshei yacheike

#ili po drugomu:
#MarketCap = soup.find(text=re.compile("Market Cap"))
#MarketCapTag = MarketCap.findNext('td').text

record = {soup.find(text=re.compile("Forward P/E")):ForwardPEValue}
scraperwiki.datastore.save([soup.find(text=re.compile("Forward P/E"))], record) 


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
    
