from BeautifulSoup import BeautifulSoup
import scraperwiki
import string
import re
import urllib
from xml.dom import minidom

for i in range(1,1000):
    html = scraperwiki.scrape('http://www.ocean30.us/idx/prop-list.html?page=%s' % i)
    soup = BeautifulSoup(html)
    tds = soup.findAll('a', href=re.compile('details.html')) # get all the <td> tags
    for td in tds:
            if td:
                link = td['href']
                if link:
                    dapper = "http://open.dapper.net/RunDapp?dappName=CommunitiesFlorida&v=1&applyToUrl=%s" % link
                    #dom = minidom.parse(urllib.urlopen(dapper))
                    #print dom
                    #scraperwiki.datastore.save
                    try:
                        html = scraperwiki.scrape(dapper)
                        scraperwiki.datastore.save(link, html)
                    except:
                        pass
from BeautifulSoup import BeautifulSoup
import scraperwiki
import string
import re
import urllib
from xml.dom import minidom

for i in range(1,1000):
    html = scraperwiki.scrape('http://www.ocean30.us/idx/prop-list.html?page=%s' % i)
    soup = BeautifulSoup(html)
    tds = soup.findAll('a', href=re.compile('details.html')) # get all the <td> tags
    for td in tds:
            if td:
                link = td['href']
                if link:
                    dapper = "http://open.dapper.net/RunDapp?dappName=CommunitiesFlorida&v=1&applyToUrl=%s" % link
                    #dom = minidom.parse(urllib.urlopen(dapper))
                    #print dom
                    #scraperwiki.datastore.save
                    try:
                        html = scraperwiki.scrape(dapper)
                        scraperwiki.datastore.save(link, html)
                    except:
                        pass
