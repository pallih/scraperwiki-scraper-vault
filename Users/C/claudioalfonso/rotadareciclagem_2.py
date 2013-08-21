# -*- coding: utf-8 -*-
import scraperwiki
import lxml
from lxml.html import parse
from lxml.etree import parse as xmlparse
from lxml.cssselect import CSSSelector

# Mapa

def get_mapa():
    base_url = "http://www.rotadareciclagem.com.br/site.html?method=carregaEntidades&"
    
    options = "latMax=27.293068543847625&lngMax=84.66230031250007&latMin=-50.46827383595759&lngMin=-161.851566875&zoomAtual=14"
    #options = "latMax=-15.76194355063211&lngMax=-47.86326041431886&latMin=-15.80281903113728&lngMin=-47.98362851353151&zoomAtual=14"
    
    
    a = xmlparse(base_url+options).getroot()
    markers = a.findall('marker')
    
    for m in markers:
        data = {}
        data['lat'] = m.get('lat')
        data['lng'] = m.get('lng')
        data['id'] = m.get('id')
        data['type'] =  m.get('prefixo')
        data['nome'] = m.text
        scraperwiki.sqlite.save(['id'], data)

def loadrecord(data):
    url = "http://www.rotadareciclagem.com.br/" + data['type'] + "/" + str(data['id'])
    soup = parse(url).getroot()
    
    #Ficha
    info = soup.cssselect('#infoEntidade')
    lista = info[0].cssselect('span')
    
    for l in lista:
        tipo = l.getprevious()
        if tipo.__class__ == lxml.html.LabelElement:
            tipo = tipo.text_content()
        if tipo == u"Endereço:":
            data['endereco'] = l.text_content()
        elif tipo == "Complemento:":
            data['complemento'] = l.text_content()
        elif tipo == "Bairro:":
            data['bairro'] = l.text_content()
        elif tipo == "Cep:":    
            data['cep'] = l.text_content()
        elif tipo == "Cidade:":
            data['cidade'] = l.text_content()
        elif tipo == " Estado:":
            data['estado'] = l.text_content()
    
    #Materiais
    data['recebe'] = []
    recebe = info[0].cssselect('span[style="margin-top: 12px"]')
    for r in recebe:
        data['recebe'].append(r.text_content())

    #to String
    data['recebe'] = ', '.join(data['recebe'])
    
    #Info de contato
    contato = soup.cssselect('fieldset[title="Outros locais onde reciclar embalagens longa vida"]')
    if len(contato) == 2:
        lista = contato[1].cssselect('span')
        for l in lista:
            tipo = l.getprevious()
            if tipo.__class__ == lxml.html.LabelElement:
                tipo = tipo.text_content()
            if tipo == "Email:":
                data['email'] = l.cssselect('b')[0].text_content()
            elif tipo == "Telefone:":
                data['telefone'] = l.cssselect('b')[0].text_content()
    
    data['completed'] = 5
    scraperwiki.sqlite.save(['id'], data)

def rockandroll():
    lista = scraperwiki.sqlite.select("* from swdata")
    for l in lista:
        if l['completed'] != 5  and int(l['id']) > 0:
            loadrecord(l)

rockandroll()