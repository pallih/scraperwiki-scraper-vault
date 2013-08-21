###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup

# retrieve a page
#pesquisa_base = 'http://spce2010.tse.jus.br/spceweb.consulta.prestacaoconta2010/candidatoServlet.do?#acao=pesquisar&sqCandidato=&sistema=null&candidatura=0&parcial=0&filtro=&entregaram=1&sgUe='

pesquisa_base = 'http://www.doingbusiness.org/rankings'

estados = [ 'BR', 'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO' ]

def getCandidato(url, estado):
#    html = scraperwiki.scrape(url + estado)
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    # use BeautifulSoup to get all <td> tags
#    soup = soup.find('tr', 'tituloTabelaFiltro').parent
    soup = soup.find('class="RankingDataHeader"')
#    rows = soup.findAll('tr')

    rows = soup.findAll('tr')

    rows.pop(0)
    for row in rows:
        cell = row.findAll('td')
        data = {}
#        data['id'] = re.search("setSqCandidato\('([0-9]*)'", cell[0].a['onclick']).group(1)
        data['Country'] = cell[0].a.string
#        data['candidato_numero'] = cell[0].a.string
        data['Field01'] = cell[1].a.string
#        data['candidato_nome'] = cell[1].a.string
        data['Field02'] = cell[2].a.string
#        data['candidato_estado'] = cell[2].string
#        data['candidato_estado'] = estado

        data['Field03'] = cell[2].a.string
        data['Field04'] = cell[2].a.string
        data['Field05'] = cell[2].a.string
        data['Field06'] = cell[2].a.string
        data['Field07'] = cell[2].a.string
        data['Field08'] = cell[2].a.string
        data['Field09'] = cell[2].a.string
        data['Field10'] = cell[2].a.string

        #record = { "td" : td.text }
        # save records to the datastore
#        scraperwiki.datastore.save(["id"], data) 

#for estado in estados:
#    getCandidato(pesquisa_base, estado)
#    print 'pegando ' + estado + '...'
 
    getCandidato(pesquisa_base,)
    print data   