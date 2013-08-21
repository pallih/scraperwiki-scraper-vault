###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
import mechanize
import re
import urlparse
from BeautifulSoup import BeautifulSoup

# Global variables
starting_url = 'http://www.landelijkregisterkinderopvang.nl/pp/zoeken/AlleOkoTypenZoekResultaten.jsf?currentPage=0&naam=&straat=&postcode=&woonplaats=&verantwoordelijkeGemeente=406&zoekHistorischeNaam=false'

def scrape_KODetails(rHTML, KO_ID):
    detailSoup = BeautifulSoup(rHTML)

    record = { 'id': KO_ID }
    rows = detailSoup.findAll('div', { 'class': re.compile('row.*') } )
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
    scraperwiki.sqlite.save(['id'], record)


def scrape_resultset(resulturl):

    # Open website via mechanize due to 302 redirect issues
    r = br.open(resulturl)
    
    # retrieve a page
    html = r.read()
    soup = BeautifulSoup(html)

    # use BeautifulSoup to get all <td> tags
    detailLinks = soup.findAll('a', href=re.compile('GegevensOKO'))
    for detailLink in detailLinks:
        detailUrl = 'http://www.landelijkregisterkinderopvang.nl' + detailLink['href']
        detailUrlParsed = urlparse.urlparse(detailUrl)
        detailParams = urlparse.parse_qs(detailUrlParsed.query)
        id = int(detailParams['selectedResultId'][0])
        detailHtml = br.open(detailUrl).read()
        scrape_KODetails(detailHtml, id)

    next_link = soup.findAll('li', { 'class' : 'volgende' } )
    if next_link:
        nextlnk = next_link[0].find('a')
        print nextlnk['href']
        next_url = urlparse.urljoin('http://www.landelijkregisterkinderopvang.nl', nextlnk['href'])
        scrape_resultset(next_url)

# Browser
# -------
# Make use of Mechanize as we need to be logged on to see the data
br = mechanize.Browser()

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; rv:15.0) Gecko/20120716 Firefox/15.0a2')]

scrape_resultset(starting_url)

