###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
from scraperwiki import datastore
# retrieve a page
#starting_url = 'http://www.taoiseach.gov.ie/eng/Taoiseach_and_Government/Government_Legislation_Programme/SECTION_A1.html'
#html = scraperwiki.scrape(starting_url)
#print html
#soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
#tds = soup.findAll('td') 
#for td in tds:
#    print td
#    record = { "td" : td.text }
    # save records to the datastore

#    data = {'url': url, 'title': title, 'purpose':purpose, 'dept':dept }
#    scraperwiki.datastore.save(['url'], data)


   ###############################################################################
# Basic scraper
###############################################################################



# retrieve a page


#def fullscrape():
starting_url = 'http://www.taoiseach.gov.ie/eng/Taoiseach_and_Government/Government_Legislation_Programme/SECTION_A1.html'
html = scraperwiki.scrape(starting_url)


soup = BeautifulSoup(html)
start=soup.find(text='next Session')

tds = soup.findAll('td')
#for t in soup.findAll('table'):
#    for tr in t.findAll('tr'):
#        print [td.contents for td in tr.findAll('td')]

for td in tds:
    record  = { "td" : td.text }
#save records to the datastore
    scraperwiki.sqlite.save(["td"], record)###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
from scraperwiki import datastore
# retrieve a page
#starting_url = 'http://www.taoiseach.gov.ie/eng/Taoiseach_and_Government/Government_Legislation_Programme/SECTION_A1.html'
#html = scraperwiki.scrape(starting_url)
#print html
#soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
#tds = soup.findAll('td') 
#for td in tds:
#    print td
#    record = { "td" : td.text }
    # save records to the datastore

#    data = {'url': url, 'title': title, 'purpose':purpose, 'dept':dept }
#    scraperwiki.datastore.save(['url'], data)


   ###############################################################################
# Basic scraper
###############################################################################



# retrieve a page


#def fullscrape():
starting_url = 'http://www.taoiseach.gov.ie/eng/Taoiseach_and_Government/Government_Legislation_Programme/SECTION_A1.html'
html = scraperwiki.scrape(starting_url)


soup = BeautifulSoup(html)
start=soup.find(text='next Session')

tds = soup.findAll('td')
#for t in soup.findAll('table'):
#    for tr in t.findAll('tr'):
#        print [td.contents for td in tr.findAll('td')]

for td in tds:
    record  = { "td" : td.text }
#save records to the datastore
    scraperwiki.sqlite.save(["td"], record)###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
from scraperwiki import datastore
# retrieve a page
#starting_url = 'http://www.taoiseach.gov.ie/eng/Taoiseach_and_Government/Government_Legislation_Programme/SECTION_A1.html'
#html = scraperwiki.scrape(starting_url)
#print html
#soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
#tds = soup.findAll('td') 
#for td in tds:
#    print td
#    record = { "td" : td.text }
    # save records to the datastore

#    data = {'url': url, 'title': title, 'purpose':purpose, 'dept':dept }
#    scraperwiki.datastore.save(['url'], data)


   ###############################################################################
# Basic scraper
###############################################################################



# retrieve a page


#def fullscrape():
starting_url = 'http://www.taoiseach.gov.ie/eng/Taoiseach_and_Government/Government_Legislation_Programme/SECTION_A1.html'
html = scraperwiki.scrape(starting_url)


soup = BeautifulSoup(html)
start=soup.find(text='next Session')

tds = soup.findAll('td')
#for t in soup.findAll('table'):
#    for tr in t.findAll('tr'):
#        print [td.contents for td in tr.findAll('td')]

for td in tds:
    record  = { "td" : td.text }
#save records to the datastore
    scraperwiki.sqlite.save(["td"], record)###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
from scraperwiki import datastore
# retrieve a page
#starting_url = 'http://www.taoiseach.gov.ie/eng/Taoiseach_and_Government/Government_Legislation_Programme/SECTION_A1.html'
#html = scraperwiki.scrape(starting_url)
#print html
#soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
#tds = soup.findAll('td') 
#for td in tds:
#    print td
#    record = { "td" : td.text }
    # save records to the datastore

#    data = {'url': url, 'title': title, 'purpose':purpose, 'dept':dept }
#    scraperwiki.datastore.save(['url'], data)


   ###############################################################################
# Basic scraper
###############################################################################



# retrieve a page


#def fullscrape():
starting_url = 'http://www.taoiseach.gov.ie/eng/Taoiseach_and_Government/Government_Legislation_Programme/SECTION_A1.html'
html = scraperwiki.scrape(starting_url)


soup = BeautifulSoup(html)
start=soup.find(text='next Session')

tds = soup.findAll('td')
#for t in soup.findAll('table'):
#    for tr in t.findAll('tr'):
#        print [td.contents for td in tr.findAll('td')]

for td in tds:
    record  = { "td" : td.text }
#save records to the datastore
    scraperwiki.sqlite.save(["td"], record)