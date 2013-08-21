# -*- coding: utf-8 -*-
import scraperwiki
from lxml import html as lxml_html
import urlparse
import re

import unidecode

ROOT = 'http://pacta.hn/'
URL_BASE = ROOT + 'web2.0/directorio?page='
DETAIL_URL = ROOT + 'web2.0/node/'

fixencoding = lambda s: s.decode('iso-8859-1', 'replace').encode('utf-8')

def slugify(str):
    str = unidecode.unidecode(str).lower()
    return re.sub(r'\W+','-',str)

def parseComercio(comercio_id):
    """ parsea una 'pagina de detalle' de un comercio """
    html = scraperwiki.scrape(DETAIL_URL + str(comercio_id))
    searchTree = lxml_html.fromstring(html)

    data = dict()

    data['id'] = comercio_id

    field_nombre = searchTree.xpath('//h2[@class="art-postheader"]/text()')[0].encode('utf-8','ignore').strip(' \t\n\r')
    data['nombre'] = field_nombre
    
    field_pais = searchTree.xpath('//div[@class="field field-type-text field-field-directorio-pais"]/div/div/text()')
    if field_pais:
        data['pais'] = field_pais[0].encode('utf-8','ignore').strip(' \t\n\r')
    else:
        data['pais'] = "-"

    field_estado = searchTree.xpath('//div[@class="field field-type-text field-field-directorio-estado"]/div/div/text()')
    if field_estado:
        data['estado'] = field_estado[0].encode('utf-8','ignore').strip(' \t\n\r')
    else:
        data['estado'] = "-"

    field_producto = searchTree.xpath('//div[@class="field field-type-text field-field-directorio-producto"]/div/div/text()')
    if field_producto:
        data['producto'] = field_producto[0].encode('utf-8','ignore').strip(' \t\n\r')
    else:
        data['producto'] = "-"

    field_contacto = searchTree.xpath('//div[@class="field field-type-text field-field-directorio-contacto"]/div/div/text()')
    if field_contacto:
        data['contacto'] = field_contacto[0].encode('utf-8','ignore').strip(' \t\n\r')
    else:
        data['contacto'] = "-"

    field_telefono = searchTree.xpath('//div[@class="field field-type-text field-field-directorio-telefono"]/div/div/text()')
    if field_telefono:
        data['telefono'] = field_telefono[0].encode('utf-8','ignore').strip(' \t\n\r')
    else:
        data['telefono'] = "-"

    field_datos = searchTree.xpath('//div[@class="field field-type-text field-field-directorio-datos"]/div/div/text()')
    if field_datos:
        data['datos'] = field_datos[0].encode('utf-8','ignore').strip(' \t\n\r')
    else:
        data['datos'] = "-"

    field_site = searchTree.xpath('//div[@class="field field-type-text field-field-directorio-site"]/div/div/text()')
    if field_site:
        data['site'] = field_site[0].encode('utf-8','ignore').strip(' \t\n\r')
    else:
        data['site'] = "-"

    print data
    scraperwiki.sqlite.save(unique_keys=['id'], data=data)

def runScraper():
    for page in range(0, 31):
        print "scrapeando página " + URL_BASE + str(page)
        html = scraperwiki.scrape(URL_BASE + str(page))
        searchTree = lxml_html.fromstring(html)
    
        for link in searchTree.cssselect('tr a[href^="/web2.0/node/"]'):
            url_parts = urlparse.urlparse(link.attrib['href'])
            path_parts = url_parts[2].rpartition('/')
            comercio_id = path_parts[2]
    
            parseComercio(comercio_id)

runScraper()
