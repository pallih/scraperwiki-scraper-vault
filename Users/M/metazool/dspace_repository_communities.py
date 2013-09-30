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
            # NB unique_keys should be a list
        scraperwiki.sqlite.save(unique_keys=['url'], data={'name':a.text,'url':link})


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
            # NB unique_keys should be a list
        scraperwiki.sqlite.save(unique_keys=['url'], data={'name':a.text,'url':link})


