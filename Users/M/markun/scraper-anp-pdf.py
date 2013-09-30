#-*- coding: utf-8 -*-
import scraperwiki
import urllib
import tempfile
import os
from lxml import etree, cssselect

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
    
    texto = css('text[font=2]', xml)
    discursos = []
    discurso = {}
    
    last_line = texto[0].get('top')
    
    raw_data = { 'municipio' : '', 'bairro' : '', 'empresa' : '', 'endereco' : '', 'data' : '', 'tipo' : '' , 'bandeira' : ''}
    data = raw_data
    
    '''<text top="160" left="29" width="68" height="13" font="2">ARARUAMA</text>
    <text top="160" left="170" width="51" height="13" font="2">CENTRO</text>
    <text top="160" left="352" width="136" height="13" font="2">AUTO POSTO 151 LTDA</text>
    <text top="160" left="1123" width="59" height="13" font="2">AUTUADO</text>
    <text top="160" left="1012" width="60" height="13" font="2">02/04/2008</text>
    <text top="160" left="582" width="144" height="13" font="2">AV JOHN KENNEDY 220,-</text>
    <text top="161" left="881" width="88" height="13" font="2">CBPI                  </text>'''
    
    
    for number, linha in enumerate(texto):
        left = int(linha.get('left'))
        if left == 29:
            data['municipio'] += linha.text + ' '
        elif left == 170:
            data['bairro'] += linha.text + ' '
        elif left == 352:
            data['empresa'] += linha.text + ' '
        elif left == 582:
            data['endereco'] += linha.text + ' '
        elif left == 881 :
            data['bandeira'] += linha.text + ' '
        elif left == 1012:
            data['data'] += linha.text + ' '
        elif left == 1118 or 1123:
            data['tipo'] += linha.text + ' '
            if texto[number+1].get('left') != '1112':
                for d in data:
                    d.strip()
                data['id'] = data['empresa'].lower() + '_' + data['data'] + '_' + data['bairro'].lower()
                scraperwiki.sqlite.save(['id'], data)
                data = { 'municipio' : '', 'bairro' : '', 'empresa' : '', 'endereco' : '', 'data' : '', 'tipo' : '' , 'bandeira' : ''}


scraper_pdf('http://www.anp.gov.br/?dw=47445')#-*- coding: utf-8 -*-
import scraperwiki
import urllib
import tempfile
import os
from lxml import etree, cssselect

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
    
    texto = css('text[font=2]', xml)
    discursos = []
    discurso = {}
    
    last_line = texto[0].get('top')
    
    raw_data = { 'municipio' : '', 'bairro' : '', 'empresa' : '', 'endereco' : '', 'data' : '', 'tipo' : '' , 'bandeira' : ''}
    data = raw_data
    
    '''<text top="160" left="29" width="68" height="13" font="2">ARARUAMA</text>
    <text top="160" left="170" width="51" height="13" font="2">CENTRO</text>
    <text top="160" left="352" width="136" height="13" font="2">AUTO POSTO 151 LTDA</text>
    <text top="160" left="1123" width="59" height="13" font="2">AUTUADO</text>
    <text top="160" left="1012" width="60" height="13" font="2">02/04/2008</text>
    <text top="160" left="582" width="144" height="13" font="2">AV JOHN KENNEDY 220,-</text>
    <text top="161" left="881" width="88" height="13" font="2">CBPI                  </text>'''
    
    
    for number, linha in enumerate(texto):
        left = int(linha.get('left'))
        if left == 29:
            data['municipio'] += linha.text + ' '
        elif left == 170:
            data['bairro'] += linha.text + ' '
        elif left == 352:
            data['empresa'] += linha.text + ' '
        elif left == 582:
            data['endereco'] += linha.text + ' '
        elif left == 881 :
            data['bandeira'] += linha.text + ' '
        elif left == 1012:
            data['data'] += linha.text + ' '
        elif left == 1118 or 1123:
            data['tipo'] += linha.text + ' '
            if texto[number+1].get('left') != '1112':
                for d in data:
                    d.strip()
                data['id'] = data['empresa'].lower() + '_' + data['data'] + '_' + data['bairro'].lower()
                scraperwiki.sqlite.save(['id'], data)
                data = { 'municipio' : '', 'bairro' : '', 'empresa' : '', 'endereco' : '', 'data' : '', 'tipo' : '' , 'bandeira' : ''}


scraper_pdf('http://www.anp.gov.br/?dw=47445')