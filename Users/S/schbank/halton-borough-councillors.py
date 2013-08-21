## Halton Borough Councillors ##

import scraperwiki
import BeautifulSoup
import re
from scraperwiki import datastore

#scrape page
html = scraperwiki.scrape('http://councillors.halton.gov.uk/mgMemberIndex.asp?VW=TABLE&PIC=1&FN=WARD')
page = BeautifulSoup.BeautifulSoup(html)

#get councillors
for row in page.find('div', {'class' : 'mgContent'}).find('table').findAll('tr')[1:]:
    cells = row.findAll('td')[1:]
    councillor_name = cells[0].find('a').string.title()
    councillor_link = 'http://councillors.halton.gov.uk/' + cells[0].find('a')['href']
    political_party = cells[1].string.title()
    ward = cells[2].string.title()
    
    data = {'councillor_name' : councillor_name,
            'councillor_link' : councillor_link,
            'political_party' : political_party,
            'ward' : ward,
            }
    datastore.save(unique_keys=['councillor_name', 'councillor_link'], data=data)


