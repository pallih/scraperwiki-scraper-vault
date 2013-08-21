import scraperwiki
import BeautifulSoup

from scraperwiki import datastore

# Hello World Example #

#scrape page
html = scraperwiki.scrape('http://scraperwiki.com/hello_world.html')
page = BeautifulSoup.BeautifulSoup(html)

#find rows
for table in page.findAll('table'):
    for row in table.findAll('tr')[1:]: 

        #save to datastore
        data = {'message' : row.td.string,}
        datastore.save(unique_keys=['message'], data=data)


