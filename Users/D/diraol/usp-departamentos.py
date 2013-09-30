##########################################################################################################
#                                                                                                        #
#                                                                                                        #
#                                            USP - Departamentos                                         #
#                                Informações coletadas do sistema JupiterWeb                             #
#                                                                                                        #
#                                                                                                        #
##########################################################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation
from operator import itemgetter, attrgetter

scraperwiki.sqlite.attach('usp-unidades-cgs')
keys = scraperwiki.sqlite.execute('select * from `usp-unidades-cgs`.swdata')['keys']
unidades = scraperwiki.sqlite.select('* from `usp-unidades-cgs`.swdata')
total_departamentos = 0
for unidade in unidades:
    #####################Coletando departamentos de uma unidade #####################
    codigoUnidade = unidade['codUnidade']
    nomeUnidade = unidade['nomeUnidade']
    ##link de busca
    starting_pagina_url = 'http://sistemas2.usp.br/jupiterweb/jupDepartamentoLista?codcg=' + codigoUnidade + '&tipo=D'
    ##pegando o html da página
    html_pagina = scraperwiki.scrape(starting_pagina_url)
    ##transformando num objeto do BeautifulSoup
    paginaSoup = BeautifulSoup(html_pagina)
    ##usar o BeautifulSoup para pegar a lista de docentes e seus códigos
    siglas = paginaSoup.findAll( "span", {"class" : "txt_arial_8pt_gray"} ) #pegando siglas
    nomes = paginaSoup.findAll( "a", {"class" : "link_gray"} ) #pegando nomes dos departamentos

    contador = 1
    total_departamentos_unidade = 0
    if siglas:
        #criar uma lista de professores com nome e número usp do docente
        for sigla, nome in zip(siglas, nomes):
                dados = {}
                dados['siglaDepartamento'] = sigla.text
                dados['nomeDepartamento'] = nome.text
                dados['codUnidade'] = codigoUnidade
                dados['nomUnidade'] = nomeUnidade
                total_departamentos_unidade += 1
                scraperwiki.sqlite.save(['siglaDepartamento'], dados)
    print "Unidade: " + nomeUnidade + " (" + codigoUnidade + ")"
    print "            Departamentos " + str(total_departamentos_unidade)
    total_departamentos += total_departamentos_unidade
print "Total de Departamentos na USP: " + str(total_departamentos)##########################################################################################################
#                                                                                                        #
#                                                                                                        #
#                                            USP - Departamentos                                         #
#                                Informações coletadas do sistema JupiterWeb                             #
#                                                                                                        #
#                                                                                                        #
##########################################################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation
from operator import itemgetter, attrgetter

scraperwiki.sqlite.attach('usp-unidades-cgs')
keys = scraperwiki.sqlite.execute('select * from `usp-unidades-cgs`.swdata')['keys']
unidades = scraperwiki.sqlite.select('* from `usp-unidades-cgs`.swdata')
total_departamentos = 0
for unidade in unidades:
    #####################Coletando departamentos de uma unidade #####################
    codigoUnidade = unidade['codUnidade']
    nomeUnidade = unidade['nomeUnidade']
    ##link de busca
    starting_pagina_url = 'http://sistemas2.usp.br/jupiterweb/jupDepartamentoLista?codcg=' + codigoUnidade + '&tipo=D'
    ##pegando o html da página
    html_pagina = scraperwiki.scrape(starting_pagina_url)
    ##transformando num objeto do BeautifulSoup
    paginaSoup = BeautifulSoup(html_pagina)
    ##usar o BeautifulSoup para pegar a lista de docentes e seus códigos
    siglas = paginaSoup.findAll( "span", {"class" : "txt_arial_8pt_gray"} ) #pegando siglas
    nomes = paginaSoup.findAll( "a", {"class" : "link_gray"} ) #pegando nomes dos departamentos

    contador = 1
    total_departamentos_unidade = 0
    if siglas:
        #criar uma lista de professores com nome e número usp do docente
        for sigla, nome in zip(siglas, nomes):
                dados = {}
                dados['siglaDepartamento'] = sigla.text
                dados['nomeDepartamento'] = nome.text
                dados['codUnidade'] = codigoUnidade
                dados['nomUnidade'] = nomeUnidade
                total_departamentos_unidade += 1
                scraperwiki.sqlite.save(['siglaDepartamento'], dados)
    print "Unidade: " + nomeUnidade + " (" + codigoUnidade + ")"
    print "            Departamentos " + str(total_departamentos_unidade)
    total_departamentos += total_departamentos_unidade
print "Total de Departamentos na USP: " + str(total_departamentos)