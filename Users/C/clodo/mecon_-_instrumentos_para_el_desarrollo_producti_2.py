# -*- coding: utf-8 -*-
import scraperwiki
from lxml import html as lxml_html
import urlparse
import re

import unidecode

ROOT = 'http://www.instrumentos.mecon.gov.ar/'
URL_BASE = ROOT + 'resultados.php?cantidad=9999&t='
DETAIL_URL = ROOT + 'mensajes-ver-mensajes.php?order=fecha%%20desc&cantidad=3&id_prog='

fixencoding = lambda s: s.decode('iso-8859-1', 'replace').encode('utf-8')

def slugify(str):
    str = unidecode.unidecode(str).lower()
    return re.sub(r'\W+','-',str)

def parseInstrumento(instrumento_id):
    """ parsea una 'pagina de detalle' de un instrumento """
    html = scraperwiki.scrape(DETAIL_URL + str(instrumento_id))
    searchTree = lxml_html.fromstring(html)

    data = dict()

    data['id'] = instrumento_id

    field_titulo = searchTree.xpath('//span[@class="titulo_tabla"]/text()')[0].encode('utf-8','ignore').strip(' \t\n\r')
    data['titulo'] = field_titulo

    for field in searchTree.xpath('//span[@class="Estilo3"]/strong'):
        parent = field.getparent()

        field_key = slugify(re.sub(r':$', '', re.sub('[ \t\r\n]+', ' ', field.text).strip(' \t\n\r')))
        field.drop_tree()

        if(field_key == 'web' and parent.xpath('a/@href')):
            field_value = parent.xpath('a/@href')[0]
        else:
            # field_value = re.sub(r'^[^a-z0-9A-Z]+', '', parent.text_content()).encode('utf-8','ignore').strip(' \t\n\r')
            field_value = re.sub('[ \t\r\n]+', ' ', re.sub(r'^[^a-z0-9A-Z]+', '', parent.text_content())).encode('utf-8','ignore').strip(' \t\n\r')

        data[field_key] = field_value

    print data
    scraperwiki.sqlite.save(unique_keys=['id'], data=data)

def runScraper(tipo):
    html = scraperwiki.scrape(URL_BASE + str(tipo))
    searchTree = lxml_html.fromstring(html)
    
    for link in searchTree.cssselect('a[href^="mensajes-ver-mensajes.php"]'):
        instrumento_id = urlparse.parse_qs(urlparse.urlparse(link.attrib['href']).query)['id_prog'][0]
        # instrumento_html = scraperwiki.scrape(ROOT + 'mensajes-ver-mensajes.php?id_prog=%s&order=fecha%%20desc&cantidad=3' % instrumento_id)
        parseInstrumento(instrumento_id)
    

# para los nacionales
runScraper(1)
# para los provinciales
# runScraper(2)
# -*- coding: utf-8 -*-
import scraperwiki
from lxml import html as lxml_html
import urlparse
import re

import unidecode

ROOT = 'http://www.instrumentos.mecon.gov.ar/'
URL_BASE = ROOT + 'resultados.php?cantidad=9999&t='
DETAIL_URL = ROOT + 'mensajes-ver-mensajes.php?order=fecha%%20desc&cantidad=3&id_prog='

fixencoding = lambda s: s.decode('iso-8859-1', 'replace').encode('utf-8')

def slugify(str):
    str = unidecode.unidecode(str).lower()
    return re.sub(r'\W+','-',str)

def parseInstrumento(instrumento_id):
    """ parsea una 'pagina de detalle' de un instrumento """
    html = scraperwiki.scrape(DETAIL_URL + str(instrumento_id))
    searchTree = lxml_html.fromstring(html)

    data = dict()

    data['id'] = instrumento_id

    field_titulo = searchTree.xpath('//span[@class="titulo_tabla"]/text()')[0].encode('utf-8','ignore').strip(' \t\n\r')
    data['titulo'] = field_titulo

    for field in searchTree.xpath('//span[@class="Estilo3"]/strong'):
        parent = field.getparent()

        field_key = slugify(re.sub(r':$', '', re.sub('[ \t\r\n]+', ' ', field.text).strip(' \t\n\r')))
        field.drop_tree()

        if(field_key == 'web' and parent.xpath('a/@href')):
            field_value = parent.xpath('a/@href')[0]
        else:
            # field_value = re.sub(r'^[^a-z0-9A-Z]+', '', parent.text_content()).encode('utf-8','ignore').strip(' \t\n\r')
            field_value = re.sub('[ \t\r\n]+', ' ', re.sub(r'^[^a-z0-9A-Z]+', '', parent.text_content())).encode('utf-8','ignore').strip(' \t\n\r')

        data[field_key] = field_value

    print data
    scraperwiki.sqlite.save(unique_keys=['id'], data=data)

def runScraper(tipo):
    html = scraperwiki.scrape(URL_BASE + str(tipo))
    searchTree = lxml_html.fromstring(html)
    
    for link in searchTree.cssselect('a[href^="mensajes-ver-mensajes.php"]'):
        instrumento_id = urlparse.parse_qs(urlparse.urlparse(link.attrib['href']).query)['id_prog'][0]
        # instrumento_html = scraperwiki.scrape(ROOT + 'mensajes-ver-mensajes.php?id_prog=%s&order=fecha%%20desc&cantidad=3' % instrumento_id)
        parseInstrumento(instrumento_id)
    

# para los nacionales
runScraper(1)
# para los provinciales
# runScraper(2)
