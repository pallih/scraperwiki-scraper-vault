###############################################################################
# Waitrose scraper
# http://www.localstore.co.uk/stores/83005/costa/
###############################################################################

from pyparsing import Literal, quotedString, removeQuotes, delimitedList






import scraperwiki,re
from BeautifulSoup import BeautifulSoup

record = {}

starting_url = 'http://www.whistles.co.uk/pws/StoreFinder.ice?country=GB&countryRegion=&findStore=findStore&page=Stores&store='
html = scraperwiki.scrape(starting_url)
soup = BeautifulSoup(html)
print soup
matches = soup.findAll(text=re.compile('storeData'))
print matches

for match in matches:
    
    tds = match.split(",")
    print tds
            
    for td in tds:
                
        matched = td.split(':')
        #print matched
       
    
        if (matched[0].strip()=='region'):
             record['region'] = matched[1].strip()
        if (matched[0].strip()=='lon'):
             record['lon'] = matched[1].strip()
        if (matched[0].strip()=='lat'):
             record['lat'] = matched[1].strip()
        if (matched[0].strip()=='name'):
             record['name'] = matched[1].strip()
             scraperwiki.sqlite.save(['name'], record)


