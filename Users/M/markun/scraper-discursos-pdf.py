#-*- coding: utf-8 -*-
import scraperwiki
import urllib
import tempfile
import os
from lxml import etree, cssselect


# Blank Python
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


pdfurl = 'http://www.camara.gov.br/internet/plenario/notas/extraord/EM0811110900.pdf'
pdfdata = urllib.urlopen(pdfurl).read()
pdfxml = pdftoxml(pdfdata)
xml = etree.fromstring(pdfxml)

texto = css('text', xml)
discursos = []
discurso = {}

for linha in texto:
    if int(linha.get('left')) > 181: #ignora tudo que não for texto de discurso
        pass #print 'ignorando ' + str(linha.text)
        #print 'linha maior que 200'
    elif linha.getchildren(): #se for negrito, provavelmente nome de orador
        discursos.append(discurso)
        discurso = {}
        orador = linha.getchildren()[0]
        primeira_linha = linha.remove(orador)
        discurso['orador'] = orador.text
        if primeira_linha:
            discurso['texto'] = primeira_linha.text
        else:
            discurso['texto'] = ''
    else:
        if linha.text:
            if discurso.has_key('texto'):
                discurso['texto'] = discurso['texto'] + linha.text + " "


count = 0
for data in discursos:
    data['id'] = count
    scraperwiki.sqlite.save(['id'], data)
    count = count + 1