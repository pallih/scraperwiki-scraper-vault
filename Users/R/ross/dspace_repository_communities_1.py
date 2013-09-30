# Blank Python
import scraperwiki
from BeautifulSoup import BeautifulSoup

# retrieve a page
url = 'http://datashare.is.ed.ac.uk/community-list'

html = scraperwiki.scrape(url)
soup = BeautifulSoup(html)

links = soup.findAll('a')

for a in links:
    link = a['href']
    if link.rfind('handle') != -1:
        print link, '-', a.text
        scraperwiki.sqlite.save(['url'], data={'name':a.text,'url':link}, table_name='ds')
        print 'saved'
        print scraperwiki.sqlite.select('count(*) from ds')


# Blank Python
import scraperwiki
from BeautifulSoup import BeautifulSoup

# retrieve a page
url = 'http://datashare.is.ed.ac.uk/community-list'

html = scraperwiki.scrape(url)
soup = BeautifulSoup(html)

links = soup.findAll('a')

for a in links:
    link = a['href']
    if link.rfind('handle') != -1:
        print link, '-', a.text
        scraperwiki.sqlite.save(['url'], data={'name':a.text,'url':link}, table_name='ds')
        print 'saved'
        print scraperwiki.sqlite.select('count(*) from ds')


# Blank Python
import scraperwiki
from BeautifulSoup import BeautifulSoup

# retrieve a page
url = 'http://datashare.is.ed.ac.uk/community-list'

html = scraperwiki.scrape(url)
soup = BeautifulSoup(html)

links = soup.findAll('a')

for a in links:
    link = a['href']
    if link.rfind('handle') != -1:
        print link, '-', a.text
        scraperwiki.sqlite.save(['url'], data={'name':a.text,'url':link}, table_name='ds')
        print 'saved'
        print scraperwiki.sqlite.select('count(*) from ds')


# Blank Python
import scraperwiki
from BeautifulSoup import BeautifulSoup

# retrieve a page
url = 'http://datashare.is.ed.ac.uk/community-list'

html = scraperwiki.scrape(url)
soup = BeautifulSoup(html)

links = soup.findAll('a')

for a in links:
    link = a['href']
    if link.rfind('handle') != -1:
        print link, '-', a.text
        scraperwiki.sqlite.save(['url'], data={'name':a.text,'url':link}, table_name='ds')
        print 'saved'
        print scraperwiki.sqlite.select('count(*) from ds')


