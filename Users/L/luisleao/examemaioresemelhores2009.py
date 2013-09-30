# -*- coding: utf-8 -*-  

###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
import re


# retrieve a page
# http://exame.abril.com.br/negocios/melhores-e-maiores/empresas/ficha/[1..1874]/2009

base_url = 'http://exame.abril.com.br/negocios/melhores-e-maiores/empresas/ficha/%s/2009'
page = scraperwiki.metadata.get('page', default=1)


#def encodeutf8(value):
#    rawfromiso = value.encode('iso-8859-1')
#    return unicode(rawfromiso, 'utf-8')

#def unicode2utf8(value):
#    u = unicode(value, "ISO-8859-1")
#    return u.encode("UTF-8")

def scrape(url):
    data = {}
    text = BeautifulSoup(scraperwiki.scrape(url))
    text = text.find('div','box_empresa')

    data['razao_social'] = text.find('div', 'nome_empresa').text

    for dado in text.findAll('p'):
        if dado.find("span","name") and dado.find("span","value"):
            nome = dado.find("span","name").text.lower().replace(":", "").replace(" ", "").replace(u"ç", u"c")
            valor = dado.find("span","value").text
            data[nome] = valor
            #print "%s: %s" % (nome, valor)

    scraperwiki.datastore.save(["cnpj"], data)
    print "%s: %s" % (data['cnpj'], data['razao_social'])


for i in range(page, 1874):
    scrape(base_url % i)
    if i == 1874: #reiniciar a contagem
        i = 1
    scraperwiki.metadata.save("page", i)


# -*- coding: utf-8 -*-  

###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
import re


# retrieve a page
# http://exame.abril.com.br/negocios/melhores-e-maiores/empresas/ficha/[1..1874]/2009

base_url = 'http://exame.abril.com.br/negocios/melhores-e-maiores/empresas/ficha/%s/2009'
page = scraperwiki.metadata.get('page', default=1)


#def encodeutf8(value):
#    rawfromiso = value.encode('iso-8859-1')
#    return unicode(rawfromiso, 'utf-8')

#def unicode2utf8(value):
#    u = unicode(value, "ISO-8859-1")
#    return u.encode("UTF-8")

def scrape(url):
    data = {}
    text = BeautifulSoup(scraperwiki.scrape(url))
    text = text.find('div','box_empresa')

    data['razao_social'] = text.find('div', 'nome_empresa').text

    for dado in text.findAll('p'):
        if dado.find("span","name") and dado.find("span","value"):
            nome = dado.find("span","name").text.lower().replace(":", "").replace(" ", "").replace(u"ç", u"c")
            valor = dado.find("span","value").text
            data[nome] = valor
            #print "%s: %s" % (nome, valor)

    scraperwiki.datastore.save(["cnpj"], data)
    print "%s: %s" % (data['cnpj'], data['razao_social'])


for i in range(page, 1874):
    scrape(base_url % i)
    if i == 1874: #reiniciar a contagem
        i = 1
    scraperwiki.metadata.save("page", i)


