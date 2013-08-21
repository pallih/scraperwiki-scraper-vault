import scraperwiki
import BeautifulSoup

from scraperwiki import datastore

# Very dumb, could be improved :)

#scrape page
html = scraperwiki.scrape('http://en.wikipedia.org/wiki/United_Kingdom_general_election,_2010')
page = BeautifulSoup.BeautifulSoup(html)

#find rows
for table in page.findAll('table'):
    for row in table.findAll('tr')[1:]: 
        col = row.contents[2]
        try:

            if "constituency" not in row.contents[3].contents[0]['href']:
                continue
            data = {'constituency': row.contents[3].contents[0].text}
            datastore.save(unique_keys=['constituency'], data=data)
            print row.contents
        except (IndexError, TypeError):
            continue




