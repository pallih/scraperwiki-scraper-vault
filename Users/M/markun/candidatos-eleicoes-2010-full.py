###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
import re
import urllib
import csv
from BeautifulSoup import BeautifulSoup

# retrieve a page
pesquisa_base = 'http://spce2010.tse.jus.br/spceweb.consulta.prestacaoconta2010/candidatoServlet.do?acao=pesquisar&sqCandidato=&sistema=null&candidatura=0&parcial=0&filtro=&entregaram=1&sgUe='
receitas_base = 'http://spce2010.tse.jus.br/spceweb.consulta.receitasdespesas2010/exportaReceitaCsvCandidato.action?sqCandidato='
#doacoes_base = 'http://spce2010.tse.jus.br/spceweb.consulta.receitasdespesas2010/exportaReceitaCsvCandidato.action?sqCandidato=20000000311&sgUe=AL'

estados = [ 'BR', 'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO' ]

def getReceitas(id, estado):
    arquivo = urllib.urlopen(receitas_base + id + '&sgUe=' + estado)
    lines = arquivo.readlines()
    if (lines):
        clist = list(csv.reader(lines, delimiter=';'))
        clist.pop(0)
        header = ['doador', 'cpf_cnpj', 'data', 'recibo_eleitoral', 'valor', 'especie', 'candidato_nome', 'candidato_numero', 'candidatura', 'partido', 'uf']
        result = [ dict(zip(header, row))  for row in clist ]
        return result


def getCandidatos(estado):
    html = scraperwiki.scrape(pesquisa_base + estado)
    soup = BeautifulSoup(html)
    # use BeautifulSoup to get all <td> tags
    soup = soup.find('tr', 'tituloTabelaFiltro').parent
    rows = soup.findAll('tr')
    rows.pop(0)
    candidatos = []
    for row in rows:
        cell = row.findAll('td')
        candidato = re.search("setSqCandidato\('([0-9]*)'", cell[0].a['onclick']).group(1)
        candidatos.append(candidato)
        #data['candidato_numero'] = cell[0].a.string
        #data['candidato_nome'] = cell[1].a.string
        #data['candidato_estado'] = estado
        return candidatos
        

def scrapeEverything(estado):
        candidatos = getCandidatos(estado)
        for candidato in candidatos:
            receitas = getReceitas(candidato, estado)
        if (receitas):
            scraperwiki.datastore.save(['recibo_eleitoral'], receitas)

def saveRecords(result, id):
        for k in result.keys():
            if data.has_key(k): continue
            else: data[k] = detalhes[k]


for estado in estados:
    scrapeEverything("AL")
    print 'pegando ' + estado + '...'
    ###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
import re
import urllib
import csv
from BeautifulSoup import BeautifulSoup

# retrieve a page
pesquisa_base = 'http://spce2010.tse.jus.br/spceweb.consulta.prestacaoconta2010/candidatoServlet.do?acao=pesquisar&sqCandidato=&sistema=null&candidatura=0&parcial=0&filtro=&entregaram=1&sgUe='
receitas_base = 'http://spce2010.tse.jus.br/spceweb.consulta.receitasdespesas2010/exportaReceitaCsvCandidato.action?sqCandidato='
#doacoes_base = 'http://spce2010.tse.jus.br/spceweb.consulta.receitasdespesas2010/exportaReceitaCsvCandidato.action?sqCandidato=20000000311&sgUe=AL'

estados = [ 'BR', 'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO' ]

def getReceitas(id, estado):
    arquivo = urllib.urlopen(receitas_base + id + '&sgUe=' + estado)
    lines = arquivo.readlines()
    if (lines):
        clist = list(csv.reader(lines, delimiter=';'))
        clist.pop(0)
        header = ['doador', 'cpf_cnpj', 'data', 'recibo_eleitoral', 'valor', 'especie', 'candidato_nome', 'candidato_numero', 'candidatura', 'partido', 'uf']
        result = [ dict(zip(header, row))  for row in clist ]
        return result


def getCandidatos(estado):
    html = scraperwiki.scrape(pesquisa_base + estado)
    soup = BeautifulSoup(html)
    # use BeautifulSoup to get all <td> tags
    soup = soup.find('tr', 'tituloTabelaFiltro').parent
    rows = soup.findAll('tr')
    rows.pop(0)
    candidatos = []
    for row in rows:
        cell = row.findAll('td')
        candidato = re.search("setSqCandidato\('([0-9]*)'", cell[0].a['onclick']).group(1)
        candidatos.append(candidato)
        #data['candidato_numero'] = cell[0].a.string
        #data['candidato_nome'] = cell[1].a.string
        #data['candidato_estado'] = estado
        return candidatos
        

def scrapeEverything(estado):
        candidatos = getCandidatos(estado)
        for candidato in candidatos:
            receitas = getReceitas(candidato, estado)
        if (receitas):
            scraperwiki.datastore.save(['recibo_eleitoral'], receitas)

def saveRecords(result, id):
        for k in result.keys():
            if data.has_key(k): continue
            else: data[k] = detalhes[k]


for estado in estados:
    scrapeEverything("AL")
    print 'pegando ' + estado + '...'
    