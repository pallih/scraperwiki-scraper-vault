import scraperwiki
import time
import re
from BeautifulSoup import BeautifulSoup
import urlparse


def scrape_table_llistat(root):
    html = scraperwiki.scrape(root)
    #print  '--->html:\n', html
    
    soup = BeautifulSoup(html)
    #print '--->soup\n', soup
    
    for url_fitxa in soup.findAll('div', {'class': 'filmlisttext'}):
        url = url_fitxa.find('div', {'class': 'filmlisttitle'}).a['href']
        #print '--->url\n', url

        notes = url_fitxa.find('div', {'class': 'filmlistdetail'}).text
        #print '--->notes\n', notes

        plot = url_fitxa.find('div', {'class': 'excerpt'}).text
        #print '--->plot\n', plot

        
        if not (url == "http://www.twitter.com/shortoftheweek"  or url == "http://www.shortoftheweek.com/submit/" ):     # CORRECT!  
            #print '--->url\n', url
            scrape_table_curts(url, notes, plot)
        
        #url = url_fitxa['href']
        #size = url_fitxa.findNextSibling('span', {'class': 'time-vedeo'}).contents[0]
        #print '---> size: ', size
        #scrape_table_curts(url, size)









def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print  '--->html:\n', html
    
    soup = BeautifulSoup(html)
    print '--->soup\n', soup

    for url_fitxa in soup.findAll('a', {'class': 'justicia'}):
        print '--->url_fitxa:\n',url_fitxa['href']

    pag_next = soup.findAll('a', {'class': 'siguiente'})
    print '--->pag_next:\n', pag_next['href']
    url_pag_next = base_url + '/ca/signos_distintivos/' + pag_next['href']
    scrape_and_look_for_next_link(url_pag_next)

    

        
base_url = 'http://www.oepm.es'
query_inicial = '/ca/signos_distintivos/resultados.html?denominacion=Contenga&texto=barcelona'

url_inicial = base_url + query_inicial
#url_inicial = urlparse.urljoin(base_url, query_inicial)

scrape_and_look_for_next_link(url_inicial)



