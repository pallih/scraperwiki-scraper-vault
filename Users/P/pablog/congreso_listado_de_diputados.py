import scraperwiki
import urllib2
from lxml.html import fromstring
from lxml.html.clean import clean_html
from scraperwiki.sqlite import save

START_URL = 'http://www.congreso.es/portal/page/portal/Congreso/Congreso/Diputados?_piref73_1333056_73_1333049_1333049.next_page=/wc/menuAbecedarioInicio&tipoBusqueda=completo&idLegislatura=10'
headers = { 'User-Agent' : 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.3) Gecko/20091020 Ubuntu/9.10 (karmic) Firefox/3.6.0' }


def get_content(url):
    req = urllib2.Request(url, None, headers)
    html = urllib2.urlopen(req).read()
    html = clean_html(html)

    root = fromstring(html)
    return root.getroottree()


def parse_and_save(root):
    urls = root.xpath('//div[@class="listado_1"]/ul/li/a/@href')
    names = root.xpath('//div[@class="listado_1"]/ul/li/a/text()')
    assert(len(urls)==25)
    assert(len(names)==25)
    
    for url, nombre in zip(urls, names):
        url = 'http://www.congreso.es' + url
        nombre = nombre.encode('latin-1')
        id = url.split('idDiputado=')[1].split('&')[0]
        save(['id'], {'id':int(id), 'nombre':nombre, 'url':url})
        print nombre

    nsiguiente = root.xpath('count(//div[@class="paginacion"][1]/ul/a)')
    if nsiguiente == 2:
        return root.xpath('//div[@class="paginacion"][1]/ul/a[2]/@href')[0]
    elif nsiguiente == 1:
        if 'Siguiente' in root.xpath('//div[@class="paginacion"][1]/ul/a/text()')[0]:
            return root.xpath('//div[@class="paginacion"][1]/ul/a/@href')[0]
        else:
            print 'No hay más URLs'
            return None


pg = 1
nexturl = START_URL
while nexturl:
    print 'Page', pg
    xmlroot = get_content(nexturl)
    nexturl = parse_and_save(xmlroot)
    pg = pg+1

print 'FIN (%d páginas)' %pg
