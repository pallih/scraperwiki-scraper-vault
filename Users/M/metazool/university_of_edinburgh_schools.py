# http://www.ed.ac.uk/schools-departments/colleges-schools

import scraperwiki
from BeautifulSoup import BeautifulSoup

source = 'http://www.ed.ac.uk/schools-departments/colleges-schools'

colleges = ['mvm','hss','se']

html = scraperwiki.scrape(source)
soup = BeautifulSoup(html)

items = soup.findAll('li')

for i in items:

    # schools <li> items are marked with college class 
    college = None
    try:
        college = i['class']
    except:
        continue
    if college not in colleges:
        continue

    # okay, this is a school
    link = i.find('a')
    # look for links that match 'degree.php' - course detail template.
    if link is not None and link.has_key('href'):
        l = link['href']
        print l
        data = {'college':i['class'],'name':link.text,'link':l}
      
        scraperwiki.sqlite.save(['link'],data)        