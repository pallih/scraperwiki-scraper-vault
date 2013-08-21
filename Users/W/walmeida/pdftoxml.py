#Script em Python para extrair dados dos pdfs
import scraperwiki
import urllib2
import lxml.etree

scraperwiki.sqlite.attach("linkinteiroteor")
data = scraperwiki.sqlite.select('* from linkinteiroteor.swdata limit 1')

for item in data:
    url = "http://www.camara.gov.br/proposicoesWeb/prop_mostrarintegra?codteor=466841"
    #url = item['urlPdf']
    print url
    pdfdata = urllib2.urlopen(url).read()
    xmldata = scraperwiki.pdftoxml(pdfdata)
    print len(xmldata)
    print "XmlData: ", xmldata