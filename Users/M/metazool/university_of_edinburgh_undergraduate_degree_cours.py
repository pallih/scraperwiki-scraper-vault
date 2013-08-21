
# view-source:http://www.ed.ac.uk/studying/undergraduate/degrees?cw_xml=a-z.php

import scraperwiki
from BeautifulSoup import BeautifulSoup

source = 'http://www.ed.ac.uk/studying/undergraduate/degrees?cw_xml=a-z.php'

html = scraperwiki.scrape(source)
soup = BeautifulSoup(html)

items = soup.findAll('li')

for i in items:
    link = i.find('a')
    # look for links that match 'degree.php' - course detail template.
    if link is not None and link.has_key('href') and link['href'].rfind('degree.php') != -1:
        l = link['href']
        print l
        # pick out the course ID from the link 
        # e.g. http://www.ed.ac.uk/studying/undergraduate/degrees?id=GN42&cw_xml=degree.php

        id = l.rsplit('id=')[1].rsplit('&cw')[0]
        data = {'id':id,'link':l,'name':link.text}

        # here we should go and find the course detail, for now lets just save data
        scraperwiki.sqlite.save(['id'],data)        