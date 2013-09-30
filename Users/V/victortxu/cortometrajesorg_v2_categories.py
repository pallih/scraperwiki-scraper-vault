import scraperwiki
#import urlparse
import lxml.html
import re
from BeautifulSoup import BeautifulSoup
import random
import time

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


def ara():
    '''return a UNIX style timestamp representing now'''
    return int(time.time())

    


# scrape_table function: gets passed an individual page to scrape
def scrape_table_llistat(root):
    url_fitxes = root.findAll('div', {'class': 'post-text'})
    print '--->> url_fitxes \n', url_fitxes
    
    for url_fitxa in url_fitxes:
        try:
            data = {}
        
            category = url_fitxa.find('div', {'class': 'post-meta'}).find('a', rel = 'tag').contents[0]
            #print category
            title = url_fitxa.h2.a.contents[0]
            url = url_fitxa.h2.a['href']
            print '--->> url_fitxa \n', title, '---', url
            data['url_fitxa'] = url
            data['title'] = title
            data['category'] = category
            data['id'] = ara()
            scraperwiki.sqlite.save(['id'], data, table_name="categories")

        except Exception:
            print '---> error \n', Exception, url 
            error = {}
            error['id'] = ara()
            error['url_fitxa'] = url
            error['exception'] = Exception
            scraperwiki.sqlite.save(['id'], error, table_name="error")
            pass
        
        
      


def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    #print html
    #root = lxml.html.fromstring(html)
    #print root
    #scrape_table_llistat(root)
    #print tostring(root, pretty_print=True)
    #next_link = root.find_rel_links('next')
    
    scrape_table_llistat(soup)
    next_link = soup.find('link', rel = 'next')['href']
    #print next_link
    if next_link:
        #next_url = urlparse.urljoin(base_url, next_link)
        #print next_url
        scrape_and_look_for_next_link(next_link)


base_url = 'http://cortometrajes.org/cortometrajes/page/26/'
#starting_url = urlparse.urljoin(base_url, 'page/1/')
scrape_and_look_for_next_link(base_url)import scraperwiki
#import urlparse
import lxml.html
import re
from BeautifulSoup import BeautifulSoup
import random
import time

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


def ara():
    '''return a UNIX style timestamp representing now'''
    return int(time.time())

    


# scrape_table function: gets passed an individual page to scrape
def scrape_table_llistat(root):
    url_fitxes = root.findAll('div', {'class': 'post-text'})
    print '--->> url_fitxes \n', url_fitxes
    
    for url_fitxa in url_fitxes:
        try:
            data = {}
        
            category = url_fitxa.find('div', {'class': 'post-meta'}).find('a', rel = 'tag').contents[0]
            #print category
            title = url_fitxa.h2.a.contents[0]
            url = url_fitxa.h2.a['href']
            print '--->> url_fitxa \n', title, '---', url
            data['url_fitxa'] = url
            data['title'] = title
            data['category'] = category
            data['id'] = ara()
            scraperwiki.sqlite.save(['id'], data, table_name="categories")

        except Exception:
            print '---> error \n', Exception, url 
            error = {}
            error['id'] = ara()
            error['url_fitxa'] = url
            error['exception'] = Exception
            scraperwiki.sqlite.save(['id'], error, table_name="error")
            pass
        
        
      


def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    #print html
    #root = lxml.html.fromstring(html)
    #print root
    #scrape_table_llistat(root)
    #print tostring(root, pretty_print=True)
    #next_link = root.find_rel_links('next')
    
    scrape_table_llistat(soup)
    next_link = soup.find('link', rel = 'next')['href']
    #print next_link
    if next_link:
        #next_url = urlparse.urljoin(base_url, next_link)
        #print next_url
        scrape_and_look_for_next_link(next_link)


base_url = 'http://cortometrajes.org/cortometrajes/page/26/'
#starting_url = urlparse.urljoin(base_url, 'page/1/')
scrape_and_look_for_next_link(base_url)