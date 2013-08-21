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



# scrape_table function: gets passed an individual page to scrape
def scrape_table_llistat(root):
    url_fitxes = root.findAll('a', {'class': 'title-link'})
    #print '--->url_fitxes', '\n', url_fitxes
    for url_fitxa in url_fitxes:
        #print url_fitxa.a['href']

        url = url_fitxa['href']
        size = url_fitxa.findNextSibling('span', {'class': 'time-vedeo'}).contents[0]
        #print '---> size: ', size
        scrape_table_curts(url, size)

url = 'http://www.filmsshort.com/genre/Gay-And-Lesbian-Films-1.html#13-minutes'

html = scraperwiki.scrape(url)
#print  '--->html:\n', html
    
soup = BeautifulSoup(html)
print '--->soup\n', soup