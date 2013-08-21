###############################################################################
# Schooloscope
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

# retrieve a page
base_url = 'http://schooloscope.com'
starting_url = '/results'
html = scraperwiki.scrape(base_url + starting_url)
#print html
soup = BeautifulSoup(html)

categoryLinks = []
schools = []
tryAgains = []

def parseListOfSchools( link ):
    html = scraperwiki.scrape(base_url + link)
        
    soup = BeautifulSoup(html)
    establishments = soup.findAll('td', { 'class' : 'establishment' })
    for e in establishments:
        links = e.findAll('a')
        for link in links:
            if link.get('href') != None:
                #print link['href']
                schools.append(link['href'])
                record = { "school" : base_url + link['href']  }
                # save records to the datastore
                scraperwiki.datastore.save(["school"], record) 
    return 0

# the first page just lists the areas in which schools can be found
trs = soup.findAll('tr') 
for tr in trs:
    #print tr
    th = tr.find('th')
    #print th.text
    tds = tr.findAll('td')
    for td in tds:
        link = td.find('a')
        #print link['href']
        categoryLinks.append(link['href'])
        #print td.text
        
        
#process each of the areas
#TODO this only does the newest inspection reports, and there may be schools which are now closed
#     and only appear in older reports
for link in categoryLinks:
    #print link
    try:
        parseListOfSchools(link)
    except HtmlError:
        tryAgains.append( link )

#there may be some links which fail, so I'd like to try these again
for link in tryAgains:
    #print link;
    try:
        parseListOfSchools(link)
        #successfully completed, so remove from try again list
        tryAgains.remove(link)
    except HtmlError:
        print link + " failed"
