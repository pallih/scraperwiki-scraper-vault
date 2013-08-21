import scraperwiki
import BeautifulSoup

from scraperwiki import datastore

# Hello World Example #

help(scraperwiki.scrape)

#scrape page
html = scraperwiki.scrape('http://www.cumbria.gov.uk/schooldata/data/search.asp', {"Advanced": "Search", "Search": "Fuzzy", "search_Status":"ANY", "search_district":"ANY", "search_name":"", "search_town":"ANY", "search_type":"ANY", "page": 3})
print html
page = BeautifulSoup.BeautifulSoup(html)

#find rows
for table in page.findAll('table'):
    for row in table.findAll('tr')[1:]: 

        #save to datastore
        data = {'message' : row.td.string,}
        datastore.save(unique_keys=['message'], data=data)


