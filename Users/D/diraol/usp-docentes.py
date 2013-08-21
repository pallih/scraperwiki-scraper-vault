###############################################################################
#                                                                             #
#                                                                             #
#    ESTÁ É A VERSÃO QUE UTILIZA O SISTEMA TYCHO PARA CONSULTAR.              #
#                                                                             #
#                                                                             #
###############################################################################

sourcescraper = "usp-unidades" #listagem de todas as unidades da USP

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation
from operator import itemgetter, attrgetter

vinculo = "DOCENTE"
total_docentes = 0

scraperwiki.sqlite.attach('usp-unidades')
keys = scraperwiki.sqlite.execute('select * from `usp-unidades`.swdata')['keys']
unidades = scraperwiki.sqlite.select('* from `usp-unidades`.swdata')

for unidade in unidades:
    #####################Coletando docentes de uma unidade #####################
    codigoUnidade = unidade['codUnidade']
    nomeUnidade = unidade['nomeUnidade']
    total_docentes_unidade = 0
    ##link de busca
    starting_pagina_url = 'http://sistemas3.usp.br/tycho/curriculoLattesListarPessoas?codigoUnidade=' + codigoUnidade + '&tipoVinculo=' + vinculo
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
    if celulas:
        print celulas
        for celula in celulas:
            if aux:
                 celulas.remove(celula)
            else:
                aux = 1
        print celulas
        #criar uma lista de professores com nome e número usp do docente
        for celula in celulas:
            docente = {}
            if celula.a == None: #se o docente não tem um lattes coloca o número usp dele como "zero"
                docente['nusp'] = "0"
            else: #se o docente tem um lattes pega o número usp
                docente['nusp'] = str(re.split("codpes=(\d+)", str(celula.a))[1]) #Pegando o número USP do docente
            docente['nome'] = celula.text
            total_docentes_unidade += 1
            scraperwiki.datastore.save(['nome'], docente)
    print nomeUnidade + ' - ' + str(codigoUnidade) + ' (' + str(total_docentes_unidade) + ')'
    total_docentes += total_docentes_unidade
print 
print 'Total de Docentes: ' + str(total_docentes)
 