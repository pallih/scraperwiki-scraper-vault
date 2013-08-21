# -*- coding: utf-8 -*-                                                                                                                                               
###############################################################################                                                                                       
# Basic scraper                                                                                                                                                       
###############################################################################                                                                                       

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup


#Configure aqui as opcoes
data_inicio = ''
data_fim = ''
orador = ''
texto = 'desarmamento'
page_size = 10


#defaults
base_url = 'http://www.camara.gov.br/internet/sitaqweb/'
options = 'resultadoPesquisaDiscursos.asp?txIndexacao=&BasePesq=plenario&txPartido=&txUF=&txSessao=&listaTipoSessao=&listaTipoInterv=&inFalaPres=&listaTipoFala=&listaFaseSessao=&txAparteante=&listaEtapa=&CampoOrdenacao=dtSessao&TipoOrdenacao=ASC&txSumario='
op_dtInicio = '' + data_inicio 
op_dtFim = '' + data_fim
op_txOrador = '&txOrador=' + orador
op_txTexto = '&txTexto=' + texto
op_PageSize = '&PageSize=' + str(page_size)
op_CurrentPage = '&CurrentPage='
full_url = base_url + options + op_dtInicio + op_dtFim + op_txOrador + op_txTexto + op_PageSize + op_CurrentPage

                                                                                                                                                    
def scrape_discursos(url, page):
    
    id_data = 0

    html = unicode(scraperwiki.scrape(url + str(page)), 'utf-8', 'ignore')
    soup = BeautifulSoup(html, fromEncoding='utf-8')  
    discursos = soup.find("tbody")
    discurso = discursos.findAll("tr")
    for row in discurso:
        if (row.find("td", { "align" : "center" })):
            data = {}
            cell = row.findAll("td")
            data['data'] = cell[0].string
            data['sessao'] = cell[1].string
            data['fase'] = cell[2].string
            try:
                data['discurso_url'] = base_url + cell[3].a['href']
                print data['discurso_url']
                data['discurso'] = getDiscurso(data['discurso_url'])
            except:
                data['discurso_url'] = ''
                data['discurso'] = ''

            #   data['sumario'] = cell[4].string
            orad = re.search('(.*), (.*)-([A-z]*)', cell[5].string)
            if (orad):
                data['orador'] = orad.group(1)
                data['partido'] = orad.group(2)
                data['estado'] = orad.group(3)
            else:    
                data['orador'] = cell[5].string
                data['partido'] = '-'
                data['estado'] = '-'
            data['hora'] = cell[6].string
            data['publicacao'] = cell[7].string
        elif (row.find("td", "Sumario")):
            data['sumario'] = row.td.string
            data['id'] = str(id_data)
            id_data = id_data + 1
            try:
                scraperwiki.datastore.save(['id'], data) # save the records one by one
                page = page + 1
                scraperwiki.sqlite.save_var('last_page', page)
            except UnicodeDecodeError:
                print 'Erro no discurso do ' + data['orador'] + ' de ' + data['data']
    try:
        scrape_discursos(full_url + page)
    except:
        print 'completo'

    def getDiscurso(url):
        html = unicode(scraperwiki.scrape(url), 'utf-8', 'ignore')
        soup = BeautifulSoup(html, fromEncoding='utf-8')
        soup = soup.find('div', { 'id' : 'content' })
        soup = soup.find('p', { 'align' : 'justify' })
        return soup.renderContents()

last_page = scraperwiki.sqlite.get_var('last_page', 1)
scrape_discursos(full_url, last_page)