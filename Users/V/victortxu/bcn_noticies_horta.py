import scraperwiki
import time
import re
from BeautifulSoup import BeautifulSoup

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


def ara():
    '''return a UNIX style timestamp representing now'''
    return int(time.time())


def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    #print  '--->html:\n', html
    
    soup = BeautifulSoup(html)
    print '--->soup\n', soup
    
   for url_llistat_cat in soup.select("#noticies"):
        print '--->url_llistat_cat:\n',url_llistat_cat
        #for llistat_li in url_llistat_cat.findAll('li'):
            #print llistat_li.a['href']
            #scrape_table_llistat(llistat_li.a['href'])

        
base_url = 'http://w110.bcn.cat/portal/site/Horta-Guinardo'

#starting_url = urlparse.urljoin(base_url, 'page/1/')
scrape_and_look_for_next_link(base_url)import scraperwiki
import time
import re
from BeautifulSoup import BeautifulSoup

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


def ara():
    '''return a UNIX style timestamp representing now'''
    return int(time.time())


def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    #print  '--->html:\n', html
    
    soup = BeautifulSoup(html)
    print '--->soup\n', soup
    
   for url_llistat_cat in soup.select("#noticies"):
        print '--->url_llistat_cat:\n',url_llistat_cat
        #for llistat_li in url_llistat_cat.findAll('li'):
            #print llistat_li.a['href']
            #scrape_table_llistat(llistat_li.a['href'])

        
base_url = 'http://w110.bcn.cat/portal/site/Horta-Guinardo'

#starting_url = urlparse.urljoin(base_url, 'page/1/')
scrape_and_look_for_next_link(base_url)