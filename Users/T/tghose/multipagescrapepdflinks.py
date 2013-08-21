# Scrape multiple pages of reports
# Get the links for all the pdfs
import scraperwiki
import re
import urlparse
import mechanize
from BeautifulSoup import BeautifulSoup
def scrape_pdf_links(starting_url, homepage):
    html = scraperwiki.scrape(starting_url)
    soup = BeautifulSoup(html)
    links = soup.findAll(href=re.compile('pdf$'))
    for link in links:
        # links look like this:
        #http://www.gao.gov/new.items/d1190r.pdf
        record = {"a" : link['href'])}
        scraperwiki.datastore.save(["a"], record)
        print record


page = 'http://gao.gov/docsearch/app_processform.php'     
homepage = 'http://gao.gov'
scrape_pdf_links(page, homepage)

# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
#next link looks like: http://gao.gov/docsearch/app_processform.php?app_id=docdblite_agency&page=2


