###############################################################################
# Structurae link scraper
# For licensing reasons only scrapes the structure name and url, no other data is collected
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

# retrieve a page
base_url = 'http://en.structurae.de'
alpha_url = base_url + '/structures/alpha/index.cfm?let='
min_url = '&min='
data_url = base_url + '/structures/data/index.cfm?id='

alphaCategories = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

alphaPages = []

def dealWithStructureLinks(structureLinks):
    for link in structureLinks:
        href = link.get('href')
        name = link.text.replace("&nbsp;", "")
        if href is not None:
            key = href.replace("/structures/data/index.cfm?id=", "")
            record = { "key" : key, "name" : name, "link" : base_url + href }
            # save records to the datastore
            scraperwiki.datastore.save(["key"], record) 

# go through all the category pages looking for the rest of the pages
for cat in alphaCategories:
    starting_url = alpha_url + cat
    html = scraperwiki.scrape(starting_url)
    soup = BeautifulSoup(html)

    links = soup.findAll('a', {'class':'nextprev1'})
    for link in links:
        href = link.get('href')
        if href is not None:
            alphaPages.append(base_url + '/structures/alpha/' + href)          
    #the category page also contains the first 100 structures  
    structureLinks = soup.findAll('a', {'class' : 'listableleft'})
    dealWithStructureLinks(structureLinks)
    
#now go through each of the paged results and get the structures
for page in alphaPages:
    html = scraperwiki.scrape(page)
    soup = BeautifulSoup(html)
    structureLinks = soup.findAll('a', {'class' : 'listableleft'})
    dealWithStructureLinks(structureLinks)
    
    