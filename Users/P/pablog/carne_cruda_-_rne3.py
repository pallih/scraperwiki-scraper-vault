import scraperwiki
import urllib2
from lxml.html import fromstring
from lxml.html.clean import clean_html
from scraperwiki.sqlite import save

# Podcasts de Carne Cruda en Radio RNE 3

LAST_PAGE = 47

URL = 'http://www.rtve.es/alacarta/interno/contenttable.shtml?pbq=%d&modl=TOC&locale=es&pageSize=15&ctx=33932'
#URL2 = "http://www.rtve.es/podcast/radio-3/carne-cruda/index.shtml"
#URL3 = "http://www.rtve.es/podcast/radio-3/carne-cruda/pagina-%d.shtml"

headers = { 'User-Agent' : 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.3) Gecko/20091020 Ubuntu/9.10 (karmic) Firefox/3.6.0' }
podcasts_count = 0

def get_content(url):
    req = urllib2.Request(url, None, headers)
    html = urllib2.urlopen(req).read()
    html = clean_html(html)

    root = fromstring(html)
    return root.getroottree()


def parse_and_save(root):
    global podcasts_count
    links = root.xpath('//div[@class="ContentTabla"]/ul/li')[1:]
    
    for link in links:
        url = 'http://www.rtve.es' + link.xpath('span[@class="col_tit"]/a/@href')[0]
        titulo = link.xpath('span[@class="col_tit"]/a/text()')[0].encode('latin-1')

        # A algunos les falta el botón de descarga, pero el mp3 parece que sí está (ej.: pg 9)
        # http://www.rtve.es/alacarta/audios/carne-cruda/carne-cruda-paralisis-permanente-revive-07-03-12/1342911/
        try:
            url_mp3 = 'http://www.rtve.es' + link.xpath('span[@class="col_tip"]/a/@href')[0]
        except IndexError:
            print 'WARNING: Download not available:', url
            url_mp3 = None

        tipo = "".join(link.xpath('span[@class="col_tip"]/text()')).strip()
        duracion = link.xpath('span[@class="col_dur"]/text()')[0]
        popularidad = link.xpath('span[@class="col_pop"]/span/em/strong/span/text()')[0]
        fecha = link.xpath('span[@class="col_fec"]/text()')[0]
        desc_corta = link.xpath('div//span[@class="detalle"]/text()')[0].encode('latin-1')

        save([], {'titulo':titulo, 'url':url, 'url_mp3':url_mp3, 'tipo':tipo, 'duracion':duracion, 'popularidad':popularidad, 'fecha':fecha, 'descripcion_corta':desc_corta})
        print '%s: %s' %(fecha, titulo)
        podcasts_count = podcasts_count +1


for pg in range(1, LAST_PAGE+1):
    print 'Page', pg
    xmlroot = get_content(URL %pg)
    parse_and_save(xmlroot)

print 'FIN (%d podcasts)' %podcasts_count
import scraperwiki
import urllib2
from lxml.html import fromstring
from lxml.html.clean import clean_html
from scraperwiki.sqlite import save

# Podcasts de Carne Cruda en Radio RNE 3

LAST_PAGE = 47

URL = 'http://www.rtve.es/alacarta/interno/contenttable.shtml?pbq=%d&modl=TOC&locale=es&pageSize=15&ctx=33932'
#URL2 = "http://www.rtve.es/podcast/radio-3/carne-cruda/index.shtml"
#URL3 = "http://www.rtve.es/podcast/radio-3/carne-cruda/pagina-%d.shtml"

headers = { 'User-Agent' : 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.3) Gecko/20091020 Ubuntu/9.10 (karmic) Firefox/3.6.0' }
podcasts_count = 0

def get_content(url):
    req = urllib2.Request(url, None, headers)
    html = urllib2.urlopen(req).read()
    html = clean_html(html)

    root = fromstring(html)
    return root.getroottree()


def parse_and_save(root):
    global podcasts_count
    links = root.xpath('//div[@class="ContentTabla"]/ul/li')[1:]
    
    for link in links:
        url = 'http://www.rtve.es' + link.xpath('span[@class="col_tit"]/a/@href')[0]
        titulo = link.xpath('span[@class="col_tit"]/a/text()')[0].encode('latin-1')

        # A algunos les falta el botón de descarga, pero el mp3 parece que sí está (ej.: pg 9)
        # http://www.rtve.es/alacarta/audios/carne-cruda/carne-cruda-paralisis-permanente-revive-07-03-12/1342911/
        try:
            url_mp3 = 'http://www.rtve.es' + link.xpath('span[@class="col_tip"]/a/@href')[0]
        except IndexError:
            print 'WARNING: Download not available:', url
            url_mp3 = None

        tipo = "".join(link.xpath('span[@class="col_tip"]/text()')).strip()
        duracion = link.xpath('span[@class="col_dur"]/text()')[0]
        popularidad = link.xpath('span[@class="col_pop"]/span/em/strong/span/text()')[0]
        fecha = link.xpath('span[@class="col_fec"]/text()')[0]
        desc_corta = link.xpath('div//span[@class="detalle"]/text()')[0].encode('latin-1')

        save([], {'titulo':titulo, 'url':url, 'url_mp3':url_mp3, 'tipo':tipo, 'duracion':duracion, 'popularidad':popularidad, 'fecha':fecha, 'descripcion_corta':desc_corta})
        print '%s: %s' %(fecha, titulo)
        podcasts_count = podcasts_count +1


for pg in range(1, LAST_PAGE+1):
    print 'Page', pg
    xmlroot = get_content(URL %pg)
    parse_and_save(xmlroot)

print 'FIN (%d podcasts)' %podcasts_count
