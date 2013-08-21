from re import compile, findall
from urlparse import urljoin

from scraperwiki import scrape

try:
    #replace scrape with caching version
    from local import scrape
except ImportError:
    print 'on server'

DOMAIN = 'http://www.catholic-hierarchy.org'
BISHOP_INDEX = 'http://www.catholic-hierarchy.org/bishop/ll.html'
CONTINENT_INDEX = 'http://www.catholic-hierarchy.org/diocese/qview.html'

def remove_dups(lst):
    for item in list(lst):
        while lst.count(item) > 1:
            lst.remove(item)
    return lst

def re_scrape(url, regex, name=''):
    page = scrape(url)
    items = regex.findall(page)
    items = remove_dups(items)
    print items
    print len(items), name
    return items
    

bish_links = re_scrape(BISHOP_INDEX, compile(r'<a href="(ll\w+\d*.html)">'), name='bishop index pages')
cont_links = re_scrape(CONTINENT_INDEX, compile(r'<a href="(qview\w+\d*.html)">'), name='continent index pages')

bish_urls = [urljoin(DOMAIN+'/bishop/', rel) for rel in bish_links][:2]
cont_urls = [urljoin(DOMAIN+'/diocese/', rel) for rel in cont_links][:2]

#print bish_urls
#print cont_urls

class CatholicUnit(object):
    def __repr__(self):
        return str(self.data)

def parse_bishops(page):
    return page.rsplit('</ul>', 1)[0].split('<li><a href="b')[1:]

"""<li><a href="batoyebi.html">Bishop Ayo-Maria <b>Atoyebi</b></a>, O.P., 
Bishop of <a href="/diocese/dilor.html">Ilorin</a>, <a href="/country/ng.html">Nigeria</a>"""

class Bishop(CatholicUnit):
    def __init__(self, html):
        """
        extract attrs from html
        """
        self.diocese = findall('<a href="/diocese/(d\w+.html)">([^<]+)</a>', html)
        self.country = ''#todo
        self.data = dict(ds)
        
        
def parse_dioceses(page):
    return page.rsplit('</ul><p>', 1)[0].split('<li><b>')[1:]
    
"""<li><b><a href="drimo.html">Rimouski</a></b>: <a href="dbaie.html">Baie-Comeau</a>, <a href="dgasp.html">Gaspe</a><br>"""

class Diocese(CatholicUnit):
    """
    extract attrs from html
    except the html contains many diocese
    """
    def __init__(self, html):
        ds = findall('<a href="(d\w+.html)">([^<]+)</a>', html)
        self.data = dict(ds)

bishops = []
dioceses = []
for i, url in enumerate(bish_urls):
    page = scrape(url)
    #print (findall(r'<title>([^<]*)</title>', page) or [None])[0]
    bishops.extend([Bishop(html) for html in parse_bishops(page)])
print len(bishops), 'bishops, eg', bishops[3:5]

for i, url in enumerate(cont_urls):
    page = scrape(url)
    #print (findall(r'<title>([^<]*)</title>', page) or [None])[0]
    dioceses.extend([Diocese(html) for html in parse_dioceses(page)])
print len(dioceses), 'dioceses, eg', dioceses[3:5]
