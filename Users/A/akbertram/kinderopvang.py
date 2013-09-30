###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
import re
import urlparse

from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'http://www.landelijkregisterkinderopvang.nl/pp/zoeken/AlleOkoTypenZoekResultaten.jsf?currentPage=0&okonaam=&inschrijfnummer=&straat=&postcode=&woonplaats=Den+Haag'
html = scraperwiki.scrape(url=starting_url, user_agent="'User-agent', 'Mozilla/5.0 (Windows NT 6.1; rv:15.0) Gecko/20120716 Firefox/15.0a2'" )
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
detailLinks = soup.findAll('a', href=re.compile('GegevensOKO')) 
for detailLink in detailLinks:
        
    detailUrl = 'http://www.landelijkregisterkinderopvang.nl' + detailLink['href']
    detailHtml = scraperwiki.scrape(detailUrl)
    detailSoup = BeautifulSoup(detailHtml)
    detailUrlParsed = urlparse.urlparse(detailUrl)
    detailParams = urlparse.parse_qs(detailUrlParsed.query)
    id = int(detailParams['selectedResultId'][0])

    record = { 'id': id }
    rows = detailSoup.findAll('div', { 'class': 'row' } )
    for row in rows:
        left = row.find('div', { 'class':'row-left' }  )
        right = row.find('div', { 'class':'row-right' } )
        if left != None and right != None:
            leftSpan =left.find('span', text=re.compile('\w|\d'))
            rightSpan = right.find('span', text=re.compile('\w|\d'))
            if leftSpan != None and rightSpan != None:
                key = leftSpan.string.strip()
                value = rightSpan.string.strip()
                if len(key) > 0 and len(value) > 0:
                    print key + '=' + value
                    record[key] = value


    # save records to the datastore
    scraperwiki.datastore.save(['id'], record) 
    ###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
import re
import urlparse

from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'http://www.landelijkregisterkinderopvang.nl/pp/zoeken/AlleOkoTypenZoekResultaten.jsf?currentPage=0&okonaam=&inschrijfnummer=&straat=&postcode=&woonplaats=Den+Haag'
html = scraperwiki.scrape(url=starting_url, user_agent="'User-agent', 'Mozilla/5.0 (Windows NT 6.1; rv:15.0) Gecko/20120716 Firefox/15.0a2'" )
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
detailLinks = soup.findAll('a', href=re.compile('GegevensOKO')) 
for detailLink in detailLinks:
        
    detailUrl = 'http://www.landelijkregisterkinderopvang.nl' + detailLink['href']
    detailHtml = scraperwiki.scrape(detailUrl)
    detailSoup = BeautifulSoup(detailHtml)
    detailUrlParsed = urlparse.urlparse(detailUrl)
    detailParams = urlparse.parse_qs(detailUrlParsed.query)
    id = int(detailParams['selectedResultId'][0])

    record = { 'id': id }
    rows = detailSoup.findAll('div', { 'class': 'row' } )
    for row in rows:
        left = row.find('div', { 'class':'row-left' }  )
        right = row.find('div', { 'class':'row-right' } )
        if left != None and right != None:
            leftSpan =left.find('span', text=re.compile('\w|\d'))
            rightSpan = right.find('span', text=re.compile('\w|\d'))
            if leftSpan != None and rightSpan != None:
                key = leftSpan.string.strip()
                value = rightSpan.string.strip()
                if len(key) > 0 and len(value) > 0:
                    print key + '=' + value
                    record[key] = value


    # save records to the datastore
    scraperwiki.datastore.save(['id'], record) 
    