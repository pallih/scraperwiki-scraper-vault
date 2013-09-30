#-*- coding: utf-8 -*-
import scraperwiki
import urllib
import tempfile
import os
from lxml import etree, cssselect
import re

def css(selector, xml):
    return cssselect.CSSSelector(selector)(xml)

def pdftoxml(pdfdata):
    """converts pdf file to xml file"""
    pdffout = tempfile.NamedTemporaryFile(suffix='.pdf')
    pdffout.write(pdfdata)
    pdffout.flush()

    xmlin = tempfile.NamedTemporaryFile(mode='r', suffix='.xml')
    tmpxml = xmlin.name # "temph.xml"
    cmd = '/usr/bin/pdftohtml -xml -nodrm -zoom 1.5 -enc UTF-8 -noframes "%s" "%s"' % (pdffout.name, os.path.splitext(tmpxml)[0])
    cmd = cmd + " >/dev/null 2>&1" # can't turn off output, so throw away even stderr yeuch
    os.system(cmd)

    pdffout.close()
    #xmlfin = open(tmpxml)
    xmldata = xmlin.read()
    xmlin.close()
    return xmldata


def scraper_pdf(pdfurl):
    pdfdata = urllib.urlopen(pdfurl).read()
    pdfxml = pdftoxml(pdfdata)
    xml = etree.fromstring(pdfxml)

    texto = css('page text', xml)
    
    discursos = []
    discurso = {}
    
    last_line = texto[0].get('top')
    
    raw_data = { 'municipio' : '', 'bairro' : '', 'empresa' : '', 'endereco' : '', 'data' : '', 'tipo' : '' , 'bandeira' : ''}
    data = raw_data
    
    '''<text top="172" left="65" width="4" height="13" font="3"><b>-</b></text>
        <text top="193" left="35" width="89" height="17" font="5"><b>APARECIDA</b></text>
        <text top="240" left="437" width="63" height="13" font="3"><b>ITAGUAÇU</b></text>
        <text top="240" left="34" width="214" height="13" font="3"><b>ROD PRESIDENTE DUTRA,S/N-KM 75</b></text>
        <text top="216" left="34" width="345" height="13" font="3"><b>POSTO E RESTAURANTE ARCO IRIS DE APARECIDA LTDA.</b></text>
        <text top="262" left="35" width="50" height="13" font="2">BRANCA</text>
        <text top="217" left="620" width="192" height="13" font="2">Posto Revendedor de Combustíveis</text>
        <text top="312" left="34" width="60" height="13" font="2">01/09/2011</text>

        <text top="309" left="359" width="434" height="13" font="2">Comercializar/Armazenar Gasolina fora das especificações - percentual de Etanol</text>
        <text top="312" left="151" width="88" height="13" font="2">Auto de Infração</text>
        <text top="332" left="359" width="359" height="13" font="2">Interdição - Gasolina fora das especificações - percentual de Etanol</text>
        <text top="334" left="151" width="97" height="13" font="2">Auto de Interdição</text>'''
    

    for number, linha in enumerate(texto):
        left = int(linha.get('left'))
        font = int(linha.get('font'))
        try:
            next_line = texto[number+1]
        except IndexError:
            next_line = linha
        if left ==35 and font==5:
            data['municipio'] = linha.findtext("b")
        elif left == 437:
            data['bairro'] = linha.findtext("b")
        elif left == 34 and next_line.get('left') == '35':
            data['empresa'] = linha.findtext("b")
        elif left == 34 and next_line.get('left') == '34':
            data['endereco'] = re.sub(",-$", "", linha.findtext("b"))
        elif left == 35 and font == 2 :
            data['bandeira'] = linha.text + ' '
        elif left == 359 and font == 2:
            if next_line.get('left') == '151' and next_line.get('width') == '88' and data['endereco'] != '':
                data['tipo'] = linha.text
                for d in data:
                    d.strip()
                data['id'] = re.sub(" |,|\.|:|-", "", data['empresa'].lower() + '_' + data['endereco'].lower())
                scraperwiki.sqlite.save(['id'], data)
                data = { 'municipio' : '', 'bairro' : '', 'empresa' : '', 'endereco' : '', 'data' : '', 'tipo' : '' , 'bandeira' : ''}


scraper_pdf("http://www.anp.gov.br/?dw=59011") # Minas Gerais
scraper_pdf("http://www.anp.gov.br/?dw=59028") # Espírito Santo
scraper_pdf("http://www.anp.gov.br/?dw=59019") # Rio de Janeiro
scraper_pdf("http://www.anp.gov.br/?dw=59026") #São Paulo#-*- coding: utf-8 -*-
import scraperwiki
import urllib
import tempfile
import os
from lxml import etree, cssselect
import re

def css(selector, xml):
    return cssselect.CSSSelector(selector)(xml)

def pdftoxml(pdfdata):
    """converts pdf file to xml file"""
    pdffout = tempfile.NamedTemporaryFile(suffix='.pdf')
    pdffout.write(pdfdata)
    pdffout.flush()

    xmlin = tempfile.NamedTemporaryFile(mode='r', suffix='.xml')
    tmpxml = xmlin.name # "temph.xml"
    cmd = '/usr/bin/pdftohtml -xml -nodrm -zoom 1.5 -enc UTF-8 -noframes "%s" "%s"' % (pdffout.name, os.path.splitext(tmpxml)[0])
    cmd = cmd + " >/dev/null 2>&1" # can't turn off output, so throw away even stderr yeuch
    os.system(cmd)

    pdffout.close()
    #xmlfin = open(tmpxml)
    xmldata = xmlin.read()
    xmlin.close()
    return xmldata


def scraper_pdf(pdfurl):
    pdfdata = urllib.urlopen(pdfurl).read()
    pdfxml = pdftoxml(pdfdata)
    xml = etree.fromstring(pdfxml)

    texto = css('page text', xml)
    
    discursos = []
    discurso = {}
    
    last_line = texto[0].get('top')
    
    raw_data = { 'municipio' : '', 'bairro' : '', 'empresa' : '', 'endereco' : '', 'data' : '', 'tipo' : '' , 'bandeira' : ''}
    data = raw_data
    
    '''<text top="172" left="65" width="4" height="13" font="3"><b>-</b></text>
        <text top="193" left="35" width="89" height="17" font="5"><b>APARECIDA</b></text>
        <text top="240" left="437" width="63" height="13" font="3"><b>ITAGUAÇU</b></text>
        <text top="240" left="34" width="214" height="13" font="3"><b>ROD PRESIDENTE DUTRA,S/N-KM 75</b></text>
        <text top="216" left="34" width="345" height="13" font="3"><b>POSTO E RESTAURANTE ARCO IRIS DE APARECIDA LTDA.</b></text>
        <text top="262" left="35" width="50" height="13" font="2">BRANCA</text>
        <text top="217" left="620" width="192" height="13" font="2">Posto Revendedor de Combustíveis</text>
        <text top="312" left="34" width="60" height="13" font="2">01/09/2011</text>

        <text top="309" left="359" width="434" height="13" font="2">Comercializar/Armazenar Gasolina fora das especificações - percentual de Etanol</text>
        <text top="312" left="151" width="88" height="13" font="2">Auto de Infração</text>
        <text top="332" left="359" width="359" height="13" font="2">Interdição - Gasolina fora das especificações - percentual de Etanol</text>
        <text top="334" left="151" width="97" height="13" font="2">Auto de Interdição</text>'''
    

    for number, linha in enumerate(texto):
        left = int(linha.get('left'))
        font = int(linha.get('font'))
        try:
            next_line = texto[number+1]
        except IndexError:
            next_line = linha
        if left ==35 and font==5:
            data['municipio'] = linha.findtext("b")
        elif left == 437:
            data['bairro'] = linha.findtext("b")
        elif left == 34 and next_line.get('left') == '35':
            data['empresa'] = linha.findtext("b")
        elif left == 34 and next_line.get('left') == '34':
            data['endereco'] = re.sub(",-$", "", linha.findtext("b"))
        elif left == 35 and font == 2 :
            data['bandeira'] = linha.text + ' '
        elif left == 359 and font == 2:
            if next_line.get('left') == '151' and next_line.get('width') == '88' and data['endereco'] != '':
                data['tipo'] = linha.text
                for d in data:
                    d.strip()
                data['id'] = re.sub(" |,|\.|:|-", "", data['empresa'].lower() + '_' + data['endereco'].lower())
                scraperwiki.sqlite.save(['id'], data)
                data = { 'municipio' : '', 'bairro' : '', 'empresa' : '', 'endereco' : '', 'data' : '', 'tipo' : '' , 'bandeira' : ''}


scraper_pdf("http://www.anp.gov.br/?dw=59011") # Minas Gerais
scraper_pdf("http://www.anp.gov.br/?dw=59028") # Espírito Santo
scraper_pdf("http://www.anp.gov.br/?dw=59019") # Rio de Janeiro
scraper_pdf("http://www.anp.gov.br/?dw=59026") #São Paulo