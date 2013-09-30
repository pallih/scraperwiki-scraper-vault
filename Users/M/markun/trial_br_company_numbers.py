###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
import urllib
import re
from BeautifulSoup import BeautifulSoup

# retrieve a page
#scraperwiki isn't loading the page properly; made a local mirror
starting_url = 'http://www.cvm.gov.br/asp/cvmwww/fundos/fidcadingl.asp'

#mirror done with 'wget --mirror http://www.cvm.gov.br/asp/cvmwww/fundos/fidcadingl.asp'
starting_url = 'http://mirrors.thacker.com.br/www.cvm.gov.br/asp/cvmwww/fundos/fidcadingl.asp'

def getCompanies(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html, fromEncoding='iso-8859-')
    rows = soup.table.findAll('a')
    for link in rows:
        clink = re.search('\?(.*)', link['href'])
        #clink = url + '?' + clink.group(1)
        #mirror '%3f' instead of '?'
        clink = url + '%3f' + clink.group(1)
        id = re.search('cdcvm=([0-9]*)', link['href'])
        id = id.group(1)
        getCompanyData(clink, id)

def getCompanyData(url, id):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html, fromEncoding='iso-8859-')
    rows = soup.findAll('tr') 
    data = {}
    data['id'] = id
    for row in rows:
        cell = row.findAll('td')
        data[cell[0].b.text.lower()] = cell[2].font.string
        # save records to the datastore
    scraperwiki.datastore.save(["id"], data)

companies = getCompanies(starting_url)###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
import urllib
import re
from BeautifulSoup import BeautifulSoup

# retrieve a page
#scraperwiki isn't loading the page properly; made a local mirror
starting_url = 'http://www.cvm.gov.br/asp/cvmwww/fundos/fidcadingl.asp'

#mirror done with 'wget --mirror http://www.cvm.gov.br/asp/cvmwww/fundos/fidcadingl.asp'
starting_url = 'http://mirrors.thacker.com.br/www.cvm.gov.br/asp/cvmwww/fundos/fidcadingl.asp'

def getCompanies(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html, fromEncoding='iso-8859-')
    rows = soup.table.findAll('a')
    for link in rows:
        clink = re.search('\?(.*)', link['href'])
        #clink = url + '?' + clink.group(1)
        #mirror '%3f' instead of '?'
        clink = url + '%3f' + clink.group(1)
        id = re.search('cdcvm=([0-9]*)', link['href'])
        id = id.group(1)
        getCompanyData(clink, id)

def getCompanyData(url, id):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html, fromEncoding='iso-8859-')
    rows = soup.findAll('tr') 
    data = {}
    data['id'] = id
    for row in rows:
        cell = row.findAll('td')
        data[cell[0].b.text.lower()] = cell[2].font.string
        # save records to the datastore
    scraperwiki.datastore.save(["id"], data)

companies = getCompanies(starting_url)