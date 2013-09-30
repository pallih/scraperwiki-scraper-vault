# Get the links for all the pdfs
import scraperwiki
import re
import urlparse
from BeautifulSoup import BeautifulSoup
def scrape_pdf_links(starting_url, homepage):
    html = scraperwiki.scrape(starting_url)
    soup = BeautifulSoup(html)
    links = soup.findAll(href=re.compile('pdf$'))
    for link in links:
        #http://www.dhs.gov/xoig/assets/mgmtrpts/OIG_04-35_Sep04.pdf
        arel = urlparse.urljoin(homepage, link['href'])
        #record = {"a" : urlparse.urljoin(homepage, link['href'])}
        #scraperwiki.datastore.save(["a"], record)
        #print record
        print arel


page = 'http://www.fas.org/sgp/crs/homesec/index.html'     
homepage = 'http://www.fas.org/sgp/crs/homesec/'
scrape_pdf_links(page, homepage)
# Get the links for all the pdfs
import scraperwiki
import re
import urlparse
from BeautifulSoup import BeautifulSoup
def scrape_pdf_links(starting_url, homepage):
    html = scraperwiki.scrape(starting_url)
    soup = BeautifulSoup(html)
    links = soup.findAll(href=re.compile('pdf$'))
    for link in links:
        #http://www.dhs.gov/xoig/assets/mgmtrpts/OIG_04-35_Sep04.pdf
        arel = urlparse.urljoin(homepage, link['href'])
        #record = {"a" : urlparse.urljoin(homepage, link['href'])}
        #scraperwiki.datastore.save(["a"], record)
        #print record
        print arel


page = 'http://www.fas.org/sgp/crs/homesec/index.html'     
homepage = 'http://www.fas.org/sgp/crs/homesec/'
scrape_pdf_links(page, homepage)
