import scraperwiki
import time
import re
from BeautifulSoup import BeautifulSoup
import lxml.html

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


def ara():
    '''return a UNIX style timestamp representing now'''
    return int(time.time())


def scrape_table_curts(url):    
    #print '--->url', '\n', url

    htmlFitxa = scraperwiki.scrape(url)
    #print '--->htmFitxa', '\n', htmlFitxa

    soupFitxa = BeautifulSoup(htmlFitxa)
    #print '--->soupFitxa', '\n', soupFitxa

    rootFitxa = lxml.html.fromstring(htmlFitxa)
    #print '--->rootFitxa', '\n', rootFitxa

    
    try:
        data = {}
    
        data['url_fitxa'] = url

        centre = soupFitxa.find('div', {'class': 'centre-detail-container'}).h2.contents[0]
        print '--->centre', '\n', centre
        data['centre'] = centre
      
        #taula = htmlFitxa.find('table', {'class': 'centre-info'})
        taula = rootFitxa.cssselect('table.centre-info')
        print '--->taula', '\n', taula
        print(etree.tostring(taula, pretty_print=True))
        #soupTaula = lxml.html.tostring(taula)
        #print '--->soupTaula', '\n', soupTaula

        #for fila in 
        

        #scraperwiki.sqlite.save(['centres_csic'], data, table_name="curts")
      
    except Exception: 
        print '---> error :', url, ara()
        error = {}
        error['url_fitxa'] = url
        error['id'] = ara()



        #scraperwiki.sqlite.save(['url_fitxa'], error, table_name="error")
        pass




def scrape_table_llistat(root):
    url_fitxes = root.findAll('td', {'class': 'col-1'})
    print '--->url_fitxes', '\n', url_fitxes
    for url_fitxa in url_fitxes:
        #print url_fitxa.a['href']

        url = url_fitxa.a['href']

        scrape_table_curts(url)


def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    #print  '--->html:\n', html
    
    soup = BeautifulSoup(html)
    #print '--->soup\n', soup
    
    scrape_table_llistat(soup)

    try:
        next_link = soup.find('div', {'class': 'page-links'}).find('a', {'class': 'next'})['href']
        #print '--->next_link', '\n', next_link

        scrape_and_look_for_next_link(next_link)
    
    except Exception:

        print '<<<< END next_link >>>>'
        

base_url = 'http://www.csic.es/web/guest/centros-de-investigacion1'
#starting_url = urlparse.urljoin(base_url, 'page/1/')
scrape_and_look_for_next_link(base_url)
import scraperwiki
import time
import re
from BeautifulSoup import BeautifulSoup
import lxml.html

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


def ara():
    '''return a UNIX style timestamp representing now'''
    return int(time.time())


def scrape_table_curts(url):    
    #print '--->url', '\n', url

    htmlFitxa = scraperwiki.scrape(url)
    #print '--->htmFitxa', '\n', htmlFitxa

    soupFitxa = BeautifulSoup(htmlFitxa)
    #print '--->soupFitxa', '\n', soupFitxa

    rootFitxa = lxml.html.fromstring(htmlFitxa)
    #print '--->rootFitxa', '\n', rootFitxa

    
    try:
        data = {}
    
        data['url_fitxa'] = url

        centre = soupFitxa.find('div', {'class': 'centre-detail-container'}).h2.contents[0]
        print '--->centre', '\n', centre
        data['centre'] = centre
      
        #taula = htmlFitxa.find('table', {'class': 'centre-info'})
        taula = rootFitxa.cssselect('table.centre-info')
        print '--->taula', '\n', taula
        print(etree.tostring(taula, pretty_print=True))
        #soupTaula = lxml.html.tostring(taula)
        #print '--->soupTaula', '\n', soupTaula

        #for fila in 
        

        #scraperwiki.sqlite.save(['centres_csic'], data, table_name="curts")
      
    except Exception: 
        print '---> error :', url, ara()
        error = {}
        error['url_fitxa'] = url
        error['id'] = ara()



        #scraperwiki.sqlite.save(['url_fitxa'], error, table_name="error")
        pass




def scrape_table_llistat(root):
    url_fitxes = root.findAll('td', {'class': 'col-1'})
    print '--->url_fitxes', '\n', url_fitxes
    for url_fitxa in url_fitxes:
        #print url_fitxa.a['href']

        url = url_fitxa.a['href']

        scrape_table_curts(url)


def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    #print  '--->html:\n', html
    
    soup = BeautifulSoup(html)
    #print '--->soup\n', soup
    
    scrape_table_llistat(soup)

    try:
        next_link = soup.find('div', {'class': 'page-links'}).find('a', {'class': 'next'})['href']
        #print '--->next_link', '\n', next_link

        scrape_and_look_for_next_link(next_link)
    
    except Exception:

        print '<<<< END next_link >>>>'
        

base_url = 'http://www.csic.es/web/guest/centros-de-investigacion1'
#starting_url = urlparse.urljoin(base_url, 'page/1/')
scrape_and_look_for_next_link(base_url)
