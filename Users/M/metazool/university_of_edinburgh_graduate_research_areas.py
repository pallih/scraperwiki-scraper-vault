# http://www.ed.ac.uk/studying/postgraduate/finder/subjectarea.php?taught=N
# also taught=Y

import scraperwiki
from BeautifulSoup import BeautifulSoup
 
baseurl = 'http://www.ed.ac.uk/studying/postgraduate/finder/'
source = baseurl + 'subjectarea.php?taught='
taught = ['Y','N']


for t in taught:
    html = scraperwiki.scrape(source+t)
    soup = BeautifulSoup(html)

    items = soup.findAll('li')

    for i in items:
        link = i.find('a')
        # look for links that match 'details.php' - subject area detail template.
        if link is not None and link.has_key('href') and link['href'].rfind('details.php') != -1:
            l = link['href']
            print l
            # pick out the subject ID from the link 
        
            id = l.rsplit('id=')[1].rsplit('">')[0]
            data = {'id':id,'link':baseurl+l,'name':link.text,'taught':t}

            # here we should go and find the course detail, for now lets just save data
            scraperwiki.sqlite.save(['id'],data)        # http://www.ed.ac.uk/studying/postgraduate/finder/subjectarea.php?taught=N
# also taught=Y

import scraperwiki
from BeautifulSoup import BeautifulSoup
 
baseurl = 'http://www.ed.ac.uk/studying/postgraduate/finder/'
source = baseurl + 'subjectarea.php?taught='
taught = ['Y','N']


for t in taught:
    html = scraperwiki.scrape(source+t)
    soup = BeautifulSoup(html)

    items = soup.findAll('li')

    for i in items:
        link = i.find('a')
        # look for links that match 'details.php' - subject area detail template.
        if link is not None and link.has_key('href') and link['href'].rfind('details.php') != -1:
            l = link['href']
            print l
            # pick out the subject ID from the link 
        
            id = l.rsplit('id=')[1].rsplit('">')[0]
            data = {'id':id,'link':baseurl+l,'name':link.text,'taught':t}

            # here we should go and find the course detail, for now lets just save data
            scraperwiki.sqlite.save(['id'],data)        