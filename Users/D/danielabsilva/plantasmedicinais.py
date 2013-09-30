# -*- coding: utf-8 -*-
import scraperwiki
import urllib
from lxml.html import parse

url_base = "http://ci-67.ciagri.usp.br/pm/"

def parsehome():
    html = parse(url_base).getroot()
    cods = html.cssselect("option")
    for cod in cods:
        try:
            parsepg(cod.get("value"))
        except:
            print "error no " + cod.get("value")

def parsepg(cod):
    url = url_base + "ver_1pl.asp?f_cod=" + cod
    html = parse(url).getroot()
    data = {}
    data["id"] = cod
    keys = []
    tabela = html.cssselect("table")[3]
    for tr in tabela.cssselect("tr"):
        key = tr.cssselect("td")[0].text_content().strip()
        if key == "":
            data["informacoes_adicionais"] = tr.cssselect("td")[1].text_content()
        elif key == "Nome popular":
            data["nome_popular"] = tr.cssselect("td")[1].text_content()
        elif key == u'Nome cient\xedfico':
            data["nome_cientifico"] = tr.cssselect("td")[1].text_content()
        elif key == "Fotos ampliadas":
            data["imgs"] = []
            imgs = tr.cssselect("td a")
            for img in imgs:
                data["imgs"].append(img.get("href"))
        elif key == u'Fam\xedlia':
            data["familia"] = tr.cssselect("td")[1].text_content()
        elif key == 'Parte usada':
            data["parte_usada"] = tr.cssselect("td")[1].text_content()
        elif key == u'Propriedades terap\xeauticas':
            data["propriedades_terapeuticas"] = tr.cssselect("td")[1].text_content()
        elif key == u'Princ\xedpios ativos':
            data["principios_ativos"] = tr.cssselect("td")[1].text_content()
        elif key == u'Indica\xe7\xf5es terap\xeauticas':
            data["indicacoes_terapeuticas"] = tr.cssselect("td")[1].text_content()
        elif key == u'Sinon\xedmia popular':
            data["sinonimia_popular"] = tr.cssselect("td")[1].text_content()
        elif key == u'Sinon\xedmia cient\xedfica':
            data["sinonimia_cientifica"] = tr.cssselect("td")[1].text_content()
        else:
            keys.append(key)
    scraperwiki.sqlite.save(["id"], data)
         

parsehome()
# -*- coding: utf-8 -*-
import scraperwiki
import urllib
from lxml.html import parse

url_base = "http://ci-67.ciagri.usp.br/pm/"

def parsehome():
    html = parse(url_base).getroot()
    cods = html.cssselect("option")
    for cod in cods:
        try:
            parsepg(cod.get("value"))
        except:
            print "error no " + cod.get("value")

def parsepg(cod):
    url = url_base + "ver_1pl.asp?f_cod=" + cod
    html = parse(url).getroot()
    data = {}
    data["id"] = cod
    keys = []
    tabela = html.cssselect("table")[3]
    for tr in tabela.cssselect("tr"):
        key = tr.cssselect("td")[0].text_content().strip()
        if key == "":
            data["informacoes_adicionais"] = tr.cssselect("td")[1].text_content()
        elif key == "Nome popular":
            data["nome_popular"] = tr.cssselect("td")[1].text_content()
        elif key == u'Nome cient\xedfico':
            data["nome_cientifico"] = tr.cssselect("td")[1].text_content()
        elif key == "Fotos ampliadas":
            data["imgs"] = []
            imgs = tr.cssselect("td a")
            for img in imgs:
                data["imgs"].append(img.get("href"))
        elif key == u'Fam\xedlia':
            data["familia"] = tr.cssselect("td")[1].text_content()
        elif key == 'Parte usada':
            data["parte_usada"] = tr.cssselect("td")[1].text_content()
        elif key == u'Propriedades terap\xeauticas':
            data["propriedades_terapeuticas"] = tr.cssselect("td")[1].text_content()
        elif key == u'Princ\xedpios ativos':
            data["principios_ativos"] = tr.cssselect("td")[1].text_content()
        elif key == u'Indica\xe7\xf5es terap\xeauticas':
            data["indicacoes_terapeuticas"] = tr.cssselect("td")[1].text_content()
        elif key == u'Sinon\xedmia popular':
            data["sinonimia_popular"] = tr.cssselect("td")[1].text_content()
        elif key == u'Sinon\xedmia cient\xedfica':
            data["sinonimia_cientifica"] = tr.cssselect("td")[1].text_content()
        else:
            keys.append(key)
    scraperwiki.sqlite.save(["id"], data)
         

parsehome()
