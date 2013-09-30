###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup

# retrieve a page
pesquisa_base = 'http://spce2010.tse.jus.br/spceweb.consulta.prestacaoconta2010/partidoServlet.do?acao=pesquisar&sqpartido=&sistema=null&tipoPesquisa=d&nrPartidoCompleto=&parcial=0&filtro=&entregaram=1&sgUf='
estados = [ 'BR', 'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO' ]

def getPartido(url, estado):
    html = scraperwiki.scrape(url + estado)
    soup = BeautifulSoup(html)
    # use BeautifulSoup to get all <td> tags
    soup = soup.find('tr', 'tituloTabelaFiltro').parent
    rows = soup.findAll('tr')
    rows.pop(0)
    for row in rows:
        cell = row.findAll('td')
        data = {}
        data['id'] = re.search("setSqComite\('([0-9]*)'", cell[0].a['onclick']).group(1)
        data['partido_estado'] = cell[0].a.string
        data['partido_partido'] = cell[1].a.string
        data['partido_descricao'] = cell[2].a.string
        #record = { "td" : td.text }
        # save records to the datastore
        scraperwiki.datastore.save(["id"], data) 

for estado in estados:
    getPartido(pesquisa_base, estado)
    print 'pegando ' + estado + '...'
    ###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup

# retrieve a page
pesquisa_base = 'http://spce2010.tse.jus.br/spceweb.consulta.prestacaoconta2010/partidoServlet.do?acao=pesquisar&sqpartido=&sistema=null&tipoPesquisa=d&nrPartidoCompleto=&parcial=0&filtro=&entregaram=1&sgUf='
estados = [ 'BR', 'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO' ]

def getPartido(url, estado):
    html = scraperwiki.scrape(url + estado)
    soup = BeautifulSoup(html)
    # use BeautifulSoup to get all <td> tags
    soup = soup.find('tr', 'tituloTabelaFiltro').parent
    rows = soup.findAll('tr')
    rows.pop(0)
    for row in rows:
        cell = row.findAll('td')
        data = {}
        data['id'] = re.search("setSqComite\('([0-9]*)'", cell[0].a['onclick']).group(1)
        data['partido_estado'] = cell[0].a.string
        data['partido_partido'] = cell[1].a.string
        data['partido_descricao'] = cell[2].a.string
        #record = { "td" : td.text }
        # save records to the datastore
        scraperwiki.datastore.save(["id"], data) 

for estado in estados:
    getPartido(pesquisa_base, estado)
    print 'pegando ' + estado + '...'
    