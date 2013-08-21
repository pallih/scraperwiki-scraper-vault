##########################################################################################################
#                                                                                                        #
#                                                                                                        #
#                                            USP - Disciplinas                                           #
#                                Informações coletadas do sistema JupiterWeb                             #
#                                                                                                        #
#                                                                                                        #
##########################################################################################################

sourcescraper = "usp-departamentos" #listagem de todos os departamentos da USP de unidades que possuem Comissão de Graduação

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation
from operator import itemgetter, attrgetter

keys = getKeys(sourcescraper)
departamentos = getData(sourcescraper)
total_disciplinas = 0
for departamento in departamentos:
    #####################Coletando disciplinas de um departamento #####################
    codigoUnidade = departamento.get(keys[2])
    print codigoUnidade
    siglaDepartamento = departamento.get(keys[1])
    print siglaDepartamento
    nomeDepartamento = departamento.get(keys[3])
    ##link de busca
    starting_pagina_url = 'http://sistemas2.usp.br/jupiterweb/jupDisciplinaLista?codcg=' + codigoUnidade + '&pfxdisval=' + siglaDepartamento + '&tipo=D'
    ##pegando o html da página
    html_pagina = scraperwiki.scrape(starting_pagina_url)
    ##transformando num objeto do BeautifulSoup
    paginaSoup = BeautifulSoup(html_pagina)
    ##usar o BeautifulSoup para pegar a lista de docentes e seus códigos
    celulas = paginaSoup.findAll( "span", {"class" : "txt_arial_8pt_gray"}) #pegando codigos das disciplinas
    #nao mudamos nada(Sheila)
###############################################################################################################################################################
    #Cada linha da tabela possui 4 colunas (Sigla, Nome, Ativação e Desativação). A lista vem com essas 4 informações, então devemos tratá-las uma por vez
    coluna = 0
    contador = 1
    lista = []
    total_disciplinas_departamento = 0
    if celulas:
        for celula in celulas:
            if coluna == 0: #Sigla da Disciplina
                dados = {}
                dados['codUnidade'] = codigoUnidade
                dados['siglaDepartamento'] = siglaDepartamento
                dados['codDisciplina'] = celula.text
                coluna += 1
            elif coluna == 1: #Nome da Disciplina
                dados['nomeDisciplina'] = celula.text
                coluna += 1
            elif coluna == 2: #Ativação
                dados['dtaAtivacao'] = celula.text
                coluna += 1
            elif coluna == 3: #Destaviação
                if celula.text:
                    dados['dataDesAtivacao'] = celula.text
                else:
                    dados['dataDesAtivacao'] = ""
                print dados
                total_disciplinas_departamento += 1
                scraperwiki.datastore.save(['codDisciplina'], dados)
                coluna = 0


    #print "Unidade: " + nomeUnidade + " (" + codigoUnidade + ")"
    #print "            Departamentos " + str(total_departamentos_unidade)
    #total_departamentos += total_departamentos_unidade
#print "Total de Departamentos na USP: " + str(total_departamentos)