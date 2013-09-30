import scraperwiki
import lxml.html
from bs4 import BeautifulSoup
import urlparse
import re

url = "http://www.thepotteries.org/art/"

def scrapeLinks(link):
    webpage = urlparse.urljoin("http://www.thepotteries.org/art/",str(link.get('href')))
    print webpage


    scraperwiki.sqlite.save(unique_keys=[],data={'webpage':webpage})
    """if webpage:
        webPageScrape = scraperwiki.scrape(webpage)
    
        soup2 = BeautifulSoup(webPageScrape)
        details = soup.find_all('p')
        print details[6]"""


html = scraperwiki.scrape(url)
soup = BeautifulSoup(html)
for link in soup.find_all('a'):
    if link:
    #print(link.get('href'))
        scrapeLinks(link)

import scraperwiki
import lxml.html
from bs4 import BeautifulSoup
import urlparse
import re

url = "http://www.thepotteries.org/art/"

def scrapeLinks(link):
    webpage = urlparse.urljoin("http://www.thepotteries.org/art/",str(link.get('href')))
    print webpage


    scraperwiki.sqlite.save(unique_keys=[],data={'webpage':webpage})
    """if webpage:
        webPageScrape = scraperwiki.scrape(webpage)
    
        soup2 = BeautifulSoup(webPageScrape)
        details = soup.find_all('p')
        print details[6]"""


html = scraperwiki.scrape(url)
soup = BeautifulSoup(html)
for link in soup.find_all('a'):
    if link:
    #print(link.get('href'))
        scrapeLinks(link)

