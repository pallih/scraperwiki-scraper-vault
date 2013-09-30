import scraperwiki
import BeautifulSoup

from scraperwiki import datastore

#scrape page
html = scraperwiki.scrape('http://www.mapaction.org/map-catalogue/mapdetail/2704.html')
page = BeautifulSoup.BeautifulSoup(html)
#find rows that contain
print "HIIIIIII"
for row in page.find('table').findAll('tr','tagstable'):

        tag = row.find('td style="text-align:right;').string
       
        print tag
        data = {'Tag':tag
                
               }
        datastore.save(unique_keys=['tag'],data=data)


import scraperwiki
import BeautifulSoup

from scraperwiki import datastore

#scrape page
html = scraperwiki.scrape('http://www.mapaction.org/map-catalogue/mapdetail/2704.html')
page = BeautifulSoup.BeautifulSoup(html)
#find rows that contain
print "HIIIIIII"
for row in page.find('table').findAll('tr','tagstable'):

        tag = row.find('td style="text-align:right;').string
       
        print tag
        data = {'Tag':tag
                
               }
        datastore.save(unique_keys=['tag'],data=data)


