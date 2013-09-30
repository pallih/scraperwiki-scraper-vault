print "Idea taken from:santarem-candidatoseleicoes2008-br"

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup #for processing HTML (others are XML, all)

# html = scraperwiki.scrape("http://unstats.un.org/unsd/demographic/products/socind/education.htm")

baseweblink = 'http://en.rsf.org/spip.php?page=classement&id_rubrique=1034'

# baseweblink = 'http://spce2010.tse.jus.br/spceweb.consulta.prestacaoconta2010/candidatoServlet.do?acao=pesquisar&sqCandidato=&

# sistema=null&candidatura=0&parcial=0&filtro=&entregaram=1&sgUe='

# arraylist_1 = [ 'BR','RR']

arraylist_1 = ['']

# print html


def getValues(url, onevalue):
    html = scraperwiki.scrape(url + onevalue)
    soup = BeautifulSoup(html)
    # use BeautifulSoup to get all <td> tags
#    soup = soup.find('tr', 'tituloTabelaFiltro').parent
#    soup = soup.find('tr', 'row_first').parent
#    rows = soup.findAll('tr')
    rows = soup.findAll('tr class=','row_first')
#    rows.pop(0)
    for row in rows:
        cell = row.findAll('td')
        data = {}
#        data['id'] = re.search("setSqCandidato\('([0-9]*)'", cell[0].a['onclick']).group(1)
        data['candidato_numero'] = cell[0].a.string
        data['candidato_nome'] = cell[1].a.string
#        data['candidato_estado'] = cell[2].string
#        data['candidato_estado'] = estado
        #record = { "td" : td.text }
        # save records to the datastore
        scraperwiki.datastore.save(["id"], data)

for onevalue in arraylist_1:
#    getValues(baseweblink, onevalue)
    getValues(baseweblink, onevalue)
    print 'fixedstring ' + onevalue + '...'

print "Idea taken from:santarem-candidatoseleicoes2008-br"

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup #for processing HTML (others are XML, all)

# html = scraperwiki.scrape("http://unstats.un.org/unsd/demographic/products/socind/education.htm")

baseweblink = 'http://en.rsf.org/spip.php?page=classement&id_rubrique=1034'

# baseweblink = 'http://spce2010.tse.jus.br/spceweb.consulta.prestacaoconta2010/candidatoServlet.do?acao=pesquisar&sqCandidato=&

# sistema=null&candidatura=0&parcial=0&filtro=&entregaram=1&sgUe='

# arraylist_1 = [ 'BR','RR']

arraylist_1 = ['']

# print html


def getValues(url, onevalue):
    html = scraperwiki.scrape(url + onevalue)
    soup = BeautifulSoup(html)
    # use BeautifulSoup to get all <td> tags
#    soup = soup.find('tr', 'tituloTabelaFiltro').parent
#    soup = soup.find('tr', 'row_first').parent
#    rows = soup.findAll('tr')
    rows = soup.findAll('tr class=','row_first')
#    rows.pop(0)
    for row in rows:
        cell = row.findAll('td')
        data = {}
#        data['id'] = re.search("setSqCandidato\('([0-9]*)'", cell[0].a['onclick']).group(1)
        data['candidato_numero'] = cell[0].a.string
        data['candidato_nome'] = cell[1].a.string
#        data['candidato_estado'] = cell[2].string
#        data['candidato_estado'] = estado
        #record = { "td" : td.text }
        # save records to the datastore
        scraperwiki.datastore.save(["id"], data)

for onevalue in arraylist_1:
#    getValues(baseweblink, onevalue)
    getValues(baseweblink, onevalue)
    print 'fixedstring ' + onevalue + '...'

