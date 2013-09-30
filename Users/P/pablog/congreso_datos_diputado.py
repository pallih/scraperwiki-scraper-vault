import urllib2
from lxml.html import fromstring
from lxml.html.clean import clean_html
import scraperwiki

headers = { 'User-Agent' : 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.3) Gecko/20091020 Ubuntu/9.10 (karmic) Firefox/3.6.0' }

def get_content(url):
    req = urllib2.Request(url, None, headers)
    html = urllib2.urlopen(req).read()
    html = clean_html(html)
    root = fromstring(html)
    return root.getroottree()


def parse_and_save(root, id):
    datos = {}

    datos['id'] = id

    # --- div datos_diputado ---

    datos['url_foto'] = 'http://www.congreso.es' + root.xpath('//div[@id="datos_diputado"]/p[@class="logo_grupo"][1]/img/@src')[0].encode('latin-1')
    datos['partido'] = root.xpath('//div[@id="datos_diputado"]/p[@class="nombre_grupo"]/text()')[0].encode('latin-1')

    gif = root.xpath('substring-after(//div[@id="datos_diputado"]/p[@class="pos_hemiciclo"]/img/@src,"_")') # '100_2310.gif'
    e = gif.split('100_')[1].split('.')[0] #3816

    if len(e) == 4:
        #http://www.congreso.es/wc/htdocs/web/img/hemiciclo/hemi_100_3816.gif
        datos['pos_sector'] = e[0]
        datos['pos_fila'] = e[1]
        datos['pos_butaca'] = e[2:4]
    elif len(e) == 1:
        #http://www.congreso.es/wc/htdocs/web/img/hemiciclo/hemi_100_3.gif
        datos['pos_sector'] = 6
        datos['pos_fila'] = 0
        datos['pos_butaca'] = e
    else:
        print len(e), e
        assert(False)

    # --- div datos_diputado ---
    datos['legislatura'] = root.xpath('//div[@id="curriculum"]/div[@class="principal"]/text()')[0].strip().encode('latin-1')
    datos['apellidos'] = root.xpath('substring-before(//div[@id="curriculum"]/div[@class="nombre_dip"]/text(),",")').strip().encode('latin-1')
    datos['nombre'] = root.xpath('substring-after(//div[@id="curriculum"]/div[@class="nombre_dip"]/text(),",")').strip().encode('latin-1')

    # Ciprià: http://www.congreso.es/portal/page/portal/Congreso/Congreso/Diputados/BusqForm?_piref73_1333155_73_1333154_1333154.next_page=/wc/fichaDiputado?idDiputado=329&idLegislatura=10
    # Aixalà: http://www.congreso.es/portal/page/portal/Congreso/Congreso/Diputados/BusqForm?_piref73_1333155_73_1333154_1333154.next_page=/wc/fichaDiputado?idDiputado=190&idLegislatura=10
    if 'Cipri' in datos['nombre']:
        datos['nombre'] = 'Cipria'
    if 'Solsona Aixal' in datos['apellidos']:
        datos['apellidos'] = 'Solsona Aixala'

    cargo = root.xpath('normalize-space(//div[@id="curriculum"]/div[@class="texto_dip"][1]/ul/li/div[@class="dip_rojo"][1]/text())')
    datos['cargo'] = cargo[:cargo.find(' ')].encode('latin-1')
    datos['circunscripcion'] = cargo[cargo.rfind(' ')+1:][:-1].encode('latin-1')

    if datos['cargo'] not in ('Diputado', 'Diputada'):
        print datos['cargo']
        assert(False)

    datos['grupo_parlamentario'] = root.xpath('//div[@id="curriculum"]/div[@class="texto_dip"][1]/ul/li/div[@class="dip_rojo"][2]/a/text()')[0].encode('latin-1')

    datos['nacimiento'] = root.xpath('normalize-space(//div[@id="curriculum"]/div[@class="texto_dip"][2]/ul/li[1]/text())')[10:-2].encode('latin-1')
    datos['cargos_anteriores'] = root.xpath('normalize-space(//div[@id="curriculum"]/div[@class="texto_dip"][2]/ul/li[2]/text())').encode('latin-1')[:-1]
    datos['estado_civil'] = root.xpath('normalize-space(//div[@id="curriculum"]/div[@class="texto_dip"][2]/ul/li[3]/text())').encode('latin-1')
    datos['curriculum'] = " ".join(root.xpath('//div[@id="curriculum"]/div[@class="texto_dip"][2]/ul/li[3]/text()')[1:]).replace('\n','').encode('latin-1')

    dec_txts = root.xpath('//div[@id="curriculum"]/div[@class="texto_dip"][2]/ul/li[@class="regact_dip"]/a/text()')
    dec_urls = root.xpath('//div[@id="curriculum"]/div[@class="texto_dip"][2]/ul/li[@class="regact_dip"]/a/@href')
    assert(len(dec_urls) == len(dec_txts))
    datos['declaracion_bienes_url'] = None
    datos['declaracion_actividades_url'] = None
    for url, txt in zip(dec_urls, dec_txts):
        url = 'http://www.congreso.es' + url
        if 'Actividades' in txt:
            datos['declaracion_actividades_url'] = url.encode('latin-1')
        elif 'Bienes' in txt:
            datos['declaracion_bienes_url'] = url.encode('latin-1')
        else:
            print txt
            print url
            assert(False)

    datos['email'] = None
    datos['web'] = None
    personal_urls = root.xpath('//div[@id="curriculum"]/div[@class="texto_dip"][2]/ul/li/div[@class="webperso_dip"]/div[@class="webperso_dip_parte"]/a/@href')
    for url in personal_urls:
        if url.startswith('mailto:'):
            datos['email'] = url.split(':')[1].encode('latin-1')
        elif url.startswith('http'):
            url = url.encode('latin-1')
            print 'http:', url
            if datos['web']:
                datos['web'] += '; ' + url
            else:
                datos['web'] = url
        else:
            if url.startswith('www.'):
                datos['web'] = 'http://' + url
            else:
                print url
                assert(False)

    datos['twitter'] = None
    datos['facebook_url'] = None
    datos['flickr_url'] = None
    datos['linkedin_url'] = None
    personal_urls = root.xpath('//div[@id="curriculum"]/div[@class="texto_dip"][2]/ul/li/div[@class="webperso_dip"]/div[@class="webperso_dip_imagen"]/a/@href')
    for url in personal_urls:
        if 'twitter.com/' in url:
            datos['twitter'] = url[url.rfind('/')+1:].encode('latin-1')
        elif 'facebook.com/' in url:
            datos['facebook_url'] = url.encode('latin-1')
        elif 'flickr.com/' in url:
            datos['flickr_url'] = url.encode('latin-1')
        elif 'linkedin.com/' in url:
            datos['linkedin_url'] = url.encode('latin-1')
        else:
            print url
            assert(False)

    """
    Twitter solo: http://www.congreso.es/portal/page/portal/Congreso/Congreso/Diputados/BusqForm?_piref73_1333155_73_1333154_1333154.next_page=/wc/fichaDiputado?idDiputado=191&idLegislatura=10
    Blog: http://www.congreso.es/portal/page/portal/Congreso/Congreso/Diputados/BusqForm?_piref73_1333155_73_1333154_1333154.next_page=/wc/fichaDiputado?idDiputado=246&idLegislatura=10
    Vimeo: http://www.congreso.es/portal/page/portal/Congreso/Congreso/Diputados/BusqForm?_piref73_1333155_73_1333154_1333154.next_page=/wc/fichaDiputado?idDiputado=282&idLegislatura=10
    Flickr: http://www.congreso.es/portal/page/portal/Congreso/Congreso/Diputados/BusqForm?_piref73_1333155_73_1333154_1333154.next_page=/wc/fichaDiputado?idDiputado=104&idLegislatura=10
    """

    datos['comisiones'] = "; ".join(root.xpath('//div[@id="curriculum"]/div[@class="listado_1"]/ul/li/a/text()')).encode('latin-1')

    print datos['apellidos'], datos['nombre']
    scraperwiki.sqlite.save(['id'], datos)


scraperwiki.sqlite.attach("congreso_listado_de_diputados")
sql = scraperwiki.sqlite.select("id, url from congreso_listado_de_diputados.swdata")

for s in sql:
    url = s['url']
    id = s['id']
    print id, url
    xmlroot = get_content(url)
    parse_and_save(xmlroot, id)
    
print 'FIN'

import urllib2
from lxml.html import fromstring
from lxml.html.clean import clean_html
import scraperwiki

headers = { 'User-Agent' : 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.3) Gecko/20091020 Ubuntu/9.10 (karmic) Firefox/3.6.0' }

def get_content(url):
    req = urllib2.Request(url, None, headers)
    html = urllib2.urlopen(req).read()
    html = clean_html(html)
    root = fromstring(html)
    return root.getroottree()


def parse_and_save(root, id):
    datos = {}

    datos['id'] = id

    # --- div datos_diputado ---

    datos['url_foto'] = 'http://www.congreso.es' + root.xpath('//div[@id="datos_diputado"]/p[@class="logo_grupo"][1]/img/@src')[0].encode('latin-1')
    datos['partido'] = root.xpath('//div[@id="datos_diputado"]/p[@class="nombre_grupo"]/text()')[0].encode('latin-1')

    gif = root.xpath('substring-after(//div[@id="datos_diputado"]/p[@class="pos_hemiciclo"]/img/@src,"_")') # '100_2310.gif'
    e = gif.split('100_')[1].split('.')[0] #3816

    if len(e) == 4:
        #http://www.congreso.es/wc/htdocs/web/img/hemiciclo/hemi_100_3816.gif
        datos['pos_sector'] = e[0]
        datos['pos_fila'] = e[1]
        datos['pos_butaca'] = e[2:4]
    elif len(e) == 1:
        #http://www.congreso.es/wc/htdocs/web/img/hemiciclo/hemi_100_3.gif
        datos['pos_sector'] = 6
        datos['pos_fila'] = 0
        datos['pos_butaca'] = e
    else:
        print len(e), e
        assert(False)

    # --- div datos_diputado ---
    datos['legislatura'] = root.xpath('//div[@id="curriculum"]/div[@class="principal"]/text()')[0].strip().encode('latin-1')
    datos['apellidos'] = root.xpath('substring-before(//div[@id="curriculum"]/div[@class="nombre_dip"]/text(),",")').strip().encode('latin-1')
    datos['nombre'] = root.xpath('substring-after(//div[@id="curriculum"]/div[@class="nombre_dip"]/text(),",")').strip().encode('latin-1')

    # Ciprià: http://www.congreso.es/portal/page/portal/Congreso/Congreso/Diputados/BusqForm?_piref73_1333155_73_1333154_1333154.next_page=/wc/fichaDiputado?idDiputado=329&idLegislatura=10
    # Aixalà: http://www.congreso.es/portal/page/portal/Congreso/Congreso/Diputados/BusqForm?_piref73_1333155_73_1333154_1333154.next_page=/wc/fichaDiputado?idDiputado=190&idLegislatura=10
    if 'Cipri' in datos['nombre']:
        datos['nombre'] = 'Cipria'
    if 'Solsona Aixal' in datos['apellidos']:
        datos['apellidos'] = 'Solsona Aixala'

    cargo = root.xpath('normalize-space(//div[@id="curriculum"]/div[@class="texto_dip"][1]/ul/li/div[@class="dip_rojo"][1]/text())')
    datos['cargo'] = cargo[:cargo.find(' ')].encode('latin-1')
    datos['circunscripcion'] = cargo[cargo.rfind(' ')+1:][:-1].encode('latin-1')

    if datos['cargo'] not in ('Diputado', 'Diputada'):
        print datos['cargo']
        assert(False)

    datos['grupo_parlamentario'] = root.xpath('//div[@id="curriculum"]/div[@class="texto_dip"][1]/ul/li/div[@class="dip_rojo"][2]/a/text()')[0].encode('latin-1')

    datos['nacimiento'] = root.xpath('normalize-space(//div[@id="curriculum"]/div[@class="texto_dip"][2]/ul/li[1]/text())')[10:-2].encode('latin-1')
    datos['cargos_anteriores'] = root.xpath('normalize-space(//div[@id="curriculum"]/div[@class="texto_dip"][2]/ul/li[2]/text())').encode('latin-1')[:-1]
    datos['estado_civil'] = root.xpath('normalize-space(//div[@id="curriculum"]/div[@class="texto_dip"][2]/ul/li[3]/text())').encode('latin-1')
    datos['curriculum'] = " ".join(root.xpath('//div[@id="curriculum"]/div[@class="texto_dip"][2]/ul/li[3]/text()')[1:]).replace('\n','').encode('latin-1')

    dec_txts = root.xpath('//div[@id="curriculum"]/div[@class="texto_dip"][2]/ul/li[@class="regact_dip"]/a/text()')
    dec_urls = root.xpath('//div[@id="curriculum"]/div[@class="texto_dip"][2]/ul/li[@class="regact_dip"]/a/@href')
    assert(len(dec_urls) == len(dec_txts))
    datos['declaracion_bienes_url'] = None
    datos['declaracion_actividades_url'] = None
    for url, txt in zip(dec_urls, dec_txts):
        url = 'http://www.congreso.es' + url
        if 'Actividades' in txt:
            datos['declaracion_actividades_url'] = url.encode('latin-1')
        elif 'Bienes' in txt:
            datos['declaracion_bienes_url'] = url.encode('latin-1')
        else:
            print txt
            print url
            assert(False)

    datos['email'] = None
    datos['web'] = None
    personal_urls = root.xpath('//div[@id="curriculum"]/div[@class="texto_dip"][2]/ul/li/div[@class="webperso_dip"]/div[@class="webperso_dip_parte"]/a/@href')
    for url in personal_urls:
        if url.startswith('mailto:'):
            datos['email'] = url.split(':')[1].encode('latin-1')
        elif url.startswith('http'):
            url = url.encode('latin-1')
            print 'http:', url
            if datos['web']:
                datos['web'] += '; ' + url
            else:
                datos['web'] = url
        else:
            if url.startswith('www.'):
                datos['web'] = 'http://' + url
            else:
                print url
                assert(False)

    datos['twitter'] = None
    datos['facebook_url'] = None
    datos['flickr_url'] = None
    datos['linkedin_url'] = None
    personal_urls = root.xpath('//div[@id="curriculum"]/div[@class="texto_dip"][2]/ul/li/div[@class="webperso_dip"]/div[@class="webperso_dip_imagen"]/a/@href')
    for url in personal_urls:
        if 'twitter.com/' in url:
            datos['twitter'] = url[url.rfind('/')+1:].encode('latin-1')
        elif 'facebook.com/' in url:
            datos['facebook_url'] = url.encode('latin-1')
        elif 'flickr.com/' in url:
            datos['flickr_url'] = url.encode('latin-1')
        elif 'linkedin.com/' in url:
            datos['linkedin_url'] = url.encode('latin-1')
        else:
            print url
            assert(False)

    """
    Twitter solo: http://www.congreso.es/portal/page/portal/Congreso/Congreso/Diputados/BusqForm?_piref73_1333155_73_1333154_1333154.next_page=/wc/fichaDiputado?idDiputado=191&idLegislatura=10
    Blog: http://www.congreso.es/portal/page/portal/Congreso/Congreso/Diputados/BusqForm?_piref73_1333155_73_1333154_1333154.next_page=/wc/fichaDiputado?idDiputado=246&idLegislatura=10
    Vimeo: http://www.congreso.es/portal/page/portal/Congreso/Congreso/Diputados/BusqForm?_piref73_1333155_73_1333154_1333154.next_page=/wc/fichaDiputado?idDiputado=282&idLegislatura=10
    Flickr: http://www.congreso.es/portal/page/portal/Congreso/Congreso/Diputados/BusqForm?_piref73_1333155_73_1333154_1333154.next_page=/wc/fichaDiputado?idDiputado=104&idLegislatura=10
    """

    datos['comisiones'] = "; ".join(root.xpath('//div[@id="curriculum"]/div[@class="listado_1"]/ul/li/a/text()')).encode('latin-1')

    print datos['apellidos'], datos['nombre']
    scraperwiki.sqlite.save(['id'], datos)


scraperwiki.sqlite.attach("congreso_listado_de_diputados")
sql = scraperwiki.sqlite.select("id, url from congreso_listado_de_diputados.swdata")

for s in sql:
    url = s['url']
    id = s['id']
    print id, url
    xmlroot = get_content(url)
    parse_and_save(xmlroot, id)
    
print 'FIN'

