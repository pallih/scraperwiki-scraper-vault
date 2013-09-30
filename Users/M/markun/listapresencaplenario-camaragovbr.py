# -*- coding: <iso-8859-1> -*-
###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup, Comment

#dados da sessão
numLegislatura = 54
numSessao = 2

# retrieve a page
starting_url = 'http://www.camara.gov.br/internet/votacao/mostraPresenca.asp?numLegislatura=54&codCasa=1&numSessaoLegislativa=1&indTipoSessaoLegislativa=O&numSessao=2&indTipoSessao=E&tipo=1'
html = scraperwiki.scrape(starting_url)
#print html
soup = BeautifulSoup(html)


#id arbitrario
id = 0

#data da sessão
data = soup.find("strong", text=re.compile("../../...."))
print data

listagem = soup.find("table", "Cor")
listagem = listagem.findAll("tr")
for row in listagem:
    if (row.find("th", { "colspan" : "3" })) :
        estado = row.find("strong").text
    if (row.find(text=re.compile("NOME"))) :
        data = {}
        nome = row.find(text=re.compile("NOME"))
        partido = row.find(text=re.compile("PARTIDO"))
        bloco = row.find(text=re.compile("BLOCO"))
        data['nome'] = nome.nextSibling
        data['partido'] = partido.nextSibling
        data['bloco'] = bloco.nextSibling
        data['estado'] = estado
        data['id'] = str(numLegislatura) + '-' + str(numSessao) + '-' + str(id)
        id = id + 1
        scraperwiki.datastore.save(['id'], data) # save the records one by one# -*- coding: <iso-8859-1> -*-
###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup, Comment

#dados da sessão
numLegislatura = 54
numSessao = 2

# retrieve a page
starting_url = 'http://www.camara.gov.br/internet/votacao/mostraPresenca.asp?numLegislatura=54&codCasa=1&numSessaoLegislativa=1&indTipoSessaoLegislativa=O&numSessao=2&indTipoSessao=E&tipo=1'
html = scraperwiki.scrape(starting_url)
#print html
soup = BeautifulSoup(html)


#id arbitrario
id = 0

#data da sessão
data = soup.find("strong", text=re.compile("../../...."))
print data

listagem = soup.find("table", "Cor")
listagem = listagem.findAll("tr")
for row in listagem:
    if (row.find("th", { "colspan" : "3" })) :
        estado = row.find("strong").text
    if (row.find(text=re.compile("NOME"))) :
        data = {}
        nome = row.find(text=re.compile("NOME"))
        partido = row.find(text=re.compile("PARTIDO"))
        bloco = row.find(text=re.compile("BLOCO"))
        data['nome'] = nome.nextSibling
        data['partido'] = partido.nextSibling
        data['bloco'] = bloco.nextSibling
        data['estado'] = estado
        data['id'] = str(numLegislatura) + '-' + str(numSessao) + '-' + str(id)
        id = id + 1
        scraperwiki.datastore.save(['id'], data) # save the records one by one