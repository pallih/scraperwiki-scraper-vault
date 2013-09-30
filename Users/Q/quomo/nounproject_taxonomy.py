import scraperwiki
import lxml.html
import itertools

base_url = 'http://thenounproject.com'
start_url = 'http://thenounproject.com/categories/'

scrape = scraperwiki.scrape(start_url)

root = lxml.html.fromstring(scrape)

links = []
#get the link to the next category
for el in root.cssselect("div.category>a:first-child"): #for now only want toplevel categories, but we could grab all image links, too.
    aLink = el.attrib['href']
    links.append(aLink)

for el in root.cssselect("section#categories div div a h3"):
    categoryName = el.text.strip()

    #for le in el.cssselect("span:first-child"): #get the number and the category
    #    catAmount = le.text.replace('( ', '')
    #    catAmount = catAmount.replace(' )', '')    
        
    #    catNums.append(catAmount)


datData = []

#follow the category links to the subcategories
for link in links[0:]: #only have range for testing output
    #follow link and scrape it
    current = base_url.strip() + link.strip()


    subScrape = scraperwiki.scrape(current)
    print '... Gathering: ', current
    subRoot = lxml.html.fromstring(subScrape)
    print 'we have: ', subRoot
    
    #parse it
    print 'scraping the innards...'    
    categoryName = subRoot.cssselect("div.content-container>h2")[0].text

    for el in subRoot.cssselect("li.category"): #need to get >h3>a, then get the count...loops and loops
        myGuy = el.cssselect("h3>a")

        subCount = 0 
        for le in el.cssselect("ul.icons>li.icon"): 
            
            subCount += 1
        
        datData.append({
            "category" : categoryName,
            "subcategory" : myGuy[0].text,
            "total": subCount,
            "url" : current
        
        })    
        


#print "datData = ", datData
    
print 'all set, cabat'

scraperwiki.sqlite.save(unique_keys=["subcategory"], data=datData, table_name="nptaxonomy")


import scraperwiki
import lxml.html
import itertools

base_url = 'http://thenounproject.com'
start_url = 'http://thenounproject.com/categories/'

scrape = scraperwiki.scrape(start_url)

root = lxml.html.fromstring(scrape)

links = []
#get the link to the next category
for el in root.cssselect("div.category>a:first-child"): #for now only want toplevel categories, but we could grab all image links, too.
    aLink = el.attrib['href']
    links.append(aLink)

for el in root.cssselect("section#categories div div a h3"):
    categoryName = el.text.strip()

    #for le in el.cssselect("span:first-child"): #get the number and the category
    #    catAmount = le.text.replace('( ', '')
    #    catAmount = catAmount.replace(' )', '')    
        
    #    catNums.append(catAmount)


datData = []

#follow the category links to the subcategories
for link in links[0:]: #only have range for testing output
    #follow link and scrape it
    current = base_url.strip() + link.strip()


    subScrape = scraperwiki.scrape(current)
    print '... Gathering: ', current
    subRoot = lxml.html.fromstring(subScrape)
    print 'we have: ', subRoot
    
    #parse it
    print 'scraping the innards...'    
    categoryName = subRoot.cssselect("div.content-container>h2")[0].text

    for el in subRoot.cssselect("li.category"): #need to get >h3>a, then get the count...loops and loops
        myGuy = el.cssselect("h3>a")

        subCount = 0 
        for le in el.cssselect("ul.icons>li.icon"): 
            
            subCount += 1
        
        datData.append({
            "category" : categoryName,
            "subcategory" : myGuy[0].text,
            "total": subCount,
            "url" : current
        
        })    
        


#print "datData = ", datData
    
print 'all set, cabat'

scraperwiki.sqlite.save(unique_keys=["subcategory"], data=datData, table_name="nptaxonomy")


import scraperwiki
import lxml.html
import itertools

base_url = 'http://thenounproject.com'
start_url = 'http://thenounproject.com/categories/'

scrape = scraperwiki.scrape(start_url)

root = lxml.html.fromstring(scrape)

links = []
#get the link to the next category
for el in root.cssselect("div.category>a:first-child"): #for now only want toplevel categories, but we could grab all image links, too.
    aLink = el.attrib['href']
    links.append(aLink)

for el in root.cssselect("section#categories div div a h3"):
    categoryName = el.text.strip()

    #for le in el.cssselect("span:first-child"): #get the number and the category
    #    catAmount = le.text.replace('( ', '')
    #    catAmount = catAmount.replace(' )', '')    
        
    #    catNums.append(catAmount)


datData = []

#follow the category links to the subcategories
for link in links[0:]: #only have range for testing output
    #follow link and scrape it
    current = base_url.strip() + link.strip()


    subScrape = scraperwiki.scrape(current)
    print '... Gathering: ', current
    subRoot = lxml.html.fromstring(subScrape)
    print 'we have: ', subRoot
    
    #parse it
    print 'scraping the innards...'    
    categoryName = subRoot.cssselect("div.content-container>h2")[0].text

    for el in subRoot.cssselect("li.category"): #need to get >h3>a, then get the count...loops and loops
        myGuy = el.cssselect("h3>a")

        subCount = 0 
        for le in el.cssselect("ul.icons>li.icon"): 
            
            subCount += 1
        
        datData.append({
            "category" : categoryName,
            "subcategory" : myGuy[0].text,
            "total": subCount,
            "url" : current
        
        })    
        


#print "datData = ", datData
    
print 'all set, cabat'

scraperwiki.sqlite.save(unique_keys=["subcategory"], data=datData, table_name="nptaxonomy")


import scraperwiki
import lxml.html
import itertools

base_url = 'http://thenounproject.com'
start_url = 'http://thenounproject.com/categories/'

scrape = scraperwiki.scrape(start_url)

root = lxml.html.fromstring(scrape)

links = []
#get the link to the next category
for el in root.cssselect("div.category>a:first-child"): #for now only want toplevel categories, but we could grab all image links, too.
    aLink = el.attrib['href']
    links.append(aLink)

for el in root.cssselect("section#categories div div a h3"):
    categoryName = el.text.strip()

    #for le in el.cssselect("span:first-child"): #get the number and the category
    #    catAmount = le.text.replace('( ', '')
    #    catAmount = catAmount.replace(' )', '')    
        
    #    catNums.append(catAmount)


datData = []

#follow the category links to the subcategories
for link in links[0:]: #only have range for testing output
    #follow link and scrape it
    current = base_url.strip() + link.strip()


    subScrape = scraperwiki.scrape(current)
    print '... Gathering: ', current
    subRoot = lxml.html.fromstring(subScrape)
    print 'we have: ', subRoot
    
    #parse it
    print 'scraping the innards...'    
    categoryName = subRoot.cssselect("div.content-container>h2")[0].text

    for el in subRoot.cssselect("li.category"): #need to get >h3>a, then get the count...loops and loops
        myGuy = el.cssselect("h3>a")

        subCount = 0 
        for le in el.cssselect("ul.icons>li.icon"): 
            
            subCount += 1
        
        datData.append({
            "category" : categoryName,
            "subcategory" : myGuy[0].text,
            "total": subCount,
            "url" : current
        
        })    
        


#print "datData = ", datData
    
print 'all set, cabat'

scraperwiki.sqlite.save(unique_keys=["subcategory"], data=datData, table_name="nptaxonomy")


