import scraperwiki
html = scraperwiki.scrape('http://www.transportcafe.co.uk/cafelist.html')
#print html

from BeautifulSoup import BeautifulSoup
soup = BeautifulSoup(html) # turn our HTML into a BeautifulSoup object
ahref = soup.findAll('a') # get all the <a> tags, ie links - however, quite a few entries are not links​​​
for a in ahref:
    print a # the full HTML tag
    print a.text # just the text inside the HTML tag

#this bit saves the data in the scraperwiki datastore​​
for a in ahref:
     record = { "a" : a.text } # column name and value
     scraperwiki.datastore.save(["a"], record) # save the records one by one

#we now need to follow those links and store the location information​​
    

import scraperwiki
html = scraperwiki.scrape('http://www.transportcafe.co.uk/cafelist.html')
#print html

from BeautifulSoup import BeautifulSoup
soup = BeautifulSoup(html) # turn our HTML into a BeautifulSoup object
ahref = soup.findAll('a') # get all the <a> tags, ie links - however, quite a few entries are not links​​​
for a in ahref:
    print a # the full HTML tag
    print a.text # just the text inside the HTML tag

#this bit saves the data in the scraperwiki datastore​​
for a in ahref:
     record = { "a" : a.text } # column name and value
     scraperwiki.datastore.save(["a"], record) # save the records one by one

#we now need to follow those links and store the location information​​
    

import scraperwiki
html = scraperwiki.scrape('http://www.transportcafe.co.uk/cafelist.html')
#print html

from BeautifulSoup import BeautifulSoup
soup = BeautifulSoup(html) # turn our HTML into a BeautifulSoup object
ahref = soup.findAll('a') # get all the <a> tags, ie links - however, quite a few entries are not links​​​
for a in ahref:
    print a # the full HTML tag
    print a.text # just the text inside the HTML tag

#this bit saves the data in the scraperwiki datastore​​
for a in ahref:
     record = { "a" : a.text } # column name and value
     scraperwiki.datastore.save(["a"], record) # save the records one by one

#we now need to follow those links and store the location information​​
    

