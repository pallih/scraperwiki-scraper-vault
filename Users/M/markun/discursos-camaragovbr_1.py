# -*- coding: utf-8 -*-                                                                                                                                               
###############################################################################                                                                                       
# Basic scraper                                                                                                                                                       
###############################################################################                                                                                       

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup

#defaults
base_url = 'http://www.camara.gov.br/internet/sitaqweb/resultadoPesquisaDiscursos.asp?'
dtInicio = '&dtInicio=' + '01/01/1966'
dtFim = '&dtFim=' + '01/01/1969'
CurrentPage = '&CurrentPage='
PageSize = '&PageSize=' + '250'
options = 'txIndexacao=&BasePesq=plenario&txOrador=&txPartido=&txUF=&txSessao=&listaTipoSessao=&listaTipoInterv=&inFalaPres=&listaTipoFala=&listaFaseSessao=&txAparteante=&listaEtapa=&CampoOrdenacao=dtSessao&TipoOrdenacao=DESC&txTexto=&txSumario='
page_number = '1'

                                                                                                                                                     
def scrape_discursos(url='', page=0):
    
    id_data = 0
    html = unicode(scraperwiki.scrape(url), 'utf-8', 'ignore')
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
            data['discurso'] = cell[3].string
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
            data['id'] = str(page) + '-' + str(id_data)
            id_data = id_data + 1
            try:
                scraperwiki.sqlite.save(['id'], data) # save the records one by one
            except UnicodeDecodeError:
                print 'Erro no discurso do ' + data['orador'] + ' de ' + data['data']


def scrape_num():
    first_page = 1
    url = base_url + options + dtInicio + dtFim + PageSize + CurrentPage + str(first_page)
    html = unicode(scraperwiki.scrape(url), 'utf-8', 'ignore')
    soup = BeautifulSoup(html, fromEncoding='utf-8')  
    link = soup.find(text=unicode('Última Página', 'utf-8', 'ignore'))
    print link
    link = link.parent['href']
    teste = re.search('CurrentPage=([0-9]*)&', link)
    paginas = int(teste.group(1))
    paginas = paginas + 1
    return paginas

paginas = scraperwiki.sqlite.get_var('paginas', scrape_num())
scraperwiki.sqlite.save_var('paginas', paginas)

last_page = scraperwiki.sqlite.get_var('last_page', 1)

for page in range(last_page, paginas):
    print "Scrapeando pagina " + str(page)
    url = base_url + options + dtInicio + dtFim + PageSize + CurrentPage + str(page)
    scrape_discursos(url, page)
    scraperwiki.sqlite.save_var('last_page', page)
