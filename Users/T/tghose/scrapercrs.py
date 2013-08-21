# Get the links for all the pdfs from the CRS
import scraperwiki
import re
import urlparse
from BeautifulSoup import BeautifulSoup
def scrape_pdf_links(starting_url, homepage):
    html = scraperwiki.scrape(starting_url)
    soup = BeautifulSoup(html)
    results = soup.findAll('li')
    print results
    for result in results:
        #http://www.dhs.gov/xoig/assets/mgmtrpts/OIG_04-35_Sep04.pdf
        #print result.li        
        record = {}
        record['number'] = result.a['href']
        record['link'] = homepage + record['number']
        record['title'] = result.a.text
        record['date'] = result.contents[1]
        #print result.contents
        # search through the soup, and save everything after the </a> tag as d
        #print d
        #record['date'] = d
        #print record
        #record = {"a" : urlparse.urljoin(homepage, link['href'])
        scraperwiki.sqlite.save(["link"], record)
        


page = 'http://www.fas.org/sgp/crs/homesec/index.html'     
homepage = 'http://www.fas.org/sgp/crs/homesec/'
scrape_pdf_links(page, homepage)

