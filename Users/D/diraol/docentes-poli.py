###############################################################################
#                                                                             #
#                                                                             #
#                                                                             #
#                                                                             #
#    ESTÁ É A VERSÃO QUE UTILIZA O SISTEMA TYCHO PARA CONSULTAR.              #
#    COMO O SISTEMA FOI RETIRADO DO AR ELA PAROU DE FUNCIONAR,                #
#    ENTÃO SERÁ FEITA UMA NOVA VERSÃO UTILIZANDO O JUPITERWEB                 #
#                                                                             #
#                                                                             #
#                                                                             #
#                                                                             #
###############################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup

#####################Coletando docentes de uma unidade #####################
vinculo = "DOCENTE"
##link de busca
starting_pagina_url = 'http://sistemas3.usp.br/tycho/curriculoLattesListarPessoas?codigoUnidade=3&tipoVinculo=DOCENTE'
##pegando o html da página
html_pagina = scraperwiki.scrape(starting_pagina_url)
##transformando num objeto do BeautifulSoup
paginaSoup = BeautifulSoup(html_pagina)
##usar o BeautifulSoup para pegar a lista de docentes e seus códigos
tabela = paginaSoup.find( "table", {"class" : "table_list"} ) #pegando a tabela que contém a lista de docentes
celulas = tabela.findAll("td") #pegando cada linha da tabela
celulas.remove(celulas[0]) #removendo linha de cabeçalho
celulas.remove(celulas[0]) #removendo linha de cabeçalho

#removendo as células da coluna "atualização"
aux = 0
for celula in celulas:
    if aux:
         celulas.remove(celula)
    else:
        aux = 1
#criar uma lista de professores com nome e número usp do docente
total_docentes = 1 #variável incremental para escrever algum número usp para os docentes cujo nusp não foi encontrado
for celula in celulas:
    docente = {}
    if (celula.a): #se o docente tem um lattes pega o número usp
        docente['idusp'] = re.search("codpub=(\w+)", celula.a['href']).group(1) #Pegando o número USP do docente
    else:
        docente['idusp'] = 0
    total_docentes += 1
    docente['contador'] = total_docentes
    docente['nome'] = celula.text
    scraperwiki.sqlite.save(['contador'], docente)###############################################################################
#                                                                             #
#                                                                             #
#                                                                             #
#                                                                             #
#    ESTÁ É A VERSÃO QUE UTILIZA O SISTEMA TYCHO PARA CONSULTAR.              #
#    COMO O SISTEMA FOI RETIRADO DO AR ELA PAROU DE FUNCIONAR,                #
#    ENTÃO SERÁ FEITA UMA NOVA VERSÃO UTILIZANDO O JUPITERWEB                 #
#                                                                             #
#                                                                             #
#                                                                             #
#                                                                             #
###############################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup

#####################Coletando docentes de uma unidade #####################
vinculo = "DOCENTE"
##link de busca
starting_pagina_url = 'http://sistemas3.usp.br/tycho/curriculoLattesListarPessoas?codigoUnidade=3&tipoVinculo=DOCENTE'
##pegando o html da página
html_pagina = scraperwiki.scrape(starting_pagina_url)
##transformando num objeto do BeautifulSoup
paginaSoup = BeautifulSoup(html_pagina)
##usar o BeautifulSoup para pegar a lista de docentes e seus códigos
tabela = paginaSoup.find( "table", {"class" : "table_list"} ) #pegando a tabela que contém a lista de docentes
celulas = tabela.findAll("td") #pegando cada linha da tabela
celulas.remove(celulas[0]) #removendo linha de cabeçalho
celulas.remove(celulas[0]) #removendo linha de cabeçalho

#removendo as células da coluna "atualização"
aux = 0
for celula in celulas:
    if aux:
         celulas.remove(celula)
    else:
        aux = 1
#criar uma lista de professores com nome e número usp do docente
total_docentes = 1 #variável incremental para escrever algum número usp para os docentes cujo nusp não foi encontrado
for celula in celulas:
    docente = {}
    if (celula.a): #se o docente tem um lattes pega o número usp
        docente['idusp'] = re.search("codpub=(\w+)", celula.a['href']).group(1) #Pegando o número USP do docente
    else:
        docente['idusp'] = 0
    total_docentes += 1
    docente['contador'] = total_docentes
    docente['nome'] = celula.text
    scraperwiki.sqlite.save(['contador'], docente)