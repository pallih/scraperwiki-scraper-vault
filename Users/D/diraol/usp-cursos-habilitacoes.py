##########################################################################################################
#                                                                                                        #
#                                                                                                        #
#                                       USP - Cursos e Habilitação                                       #
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
total_cursos = 0

for unidade in unidades:
##########################################################################################################
#                                                                                                        #
#                              Código que vai rodar para cada Unidade                                    #
#                                                                                                        #
##########################################################################################################
    codigoUnidade = unidade['codUnidade']
    nomeUnidade = unidade['nomeUnidade']
    print "-" + nomeUnidade + " (" + codigoUnidade + ")"
    total_cursos_unidade = 0
    ###################################################################
    #                                                                 #
    #            Começando a coletar os cursos/habilitações           #
    #                 pelos cursos "novos" (atuais)                   #
    #                                                                 #
    ###################################################################
    starting_pagina_url = 'http://sistemas2.usp.br/jupiterweb/jupCursoLista?codcg=' + codigoUnidade + '&tipo=N'       #link de busca
    html_pagina = scraperwiki.scrape(starting_pagina_url)                                                  #pegando o html da página
    paginaSoup = BeautifulSoup(html_pagina)                                               #transformando num objeto do BeautifulSoup
    unidade = paginaSoup.findAll( "a", {"class" : "link_gray"} )                             #pegar a lista de cursos e seus códigos
    periodos = paginaSoup.findAll( "span", {"class" : "txt_arial_8pt_gray"})
                                                                        #Retirando link para a página de cursos antigos, caso exista
    for curso in unidade:
        tipoCurso = re.split("tipo=(\w)", str(curso))[1]
        if tipoCurso == "V":
            unidade.remove(curso)
    #criar uma lista de cursos/habilitações com os respectivos códigos
    for curso, periodo in zip(unidade, periodos):
        dados = {}
        dados['codcur'] = re.split("codcur=(\d+)", str(curso))[1]
        dados['codhab'] = re.split("codhab=(\d+)", str(curso))[1]
        dados['nome'] = curso.text
        dados['periodo'] = periodo.text
        dados['unidade'] = nomeUnidade
        dados['codunidade'] = codigoUnidade
        dados['Status'] = "N"
        total_cursos_unidade += 1
        scraperwiki.sqlite.save(['codcur', 'codhab'], dados)
    print "---Cursos/Habilitações Novos: " + str(total_cursos_unidade)
    total_cursos += total_cursos_unidade

    ###################################################################
    #                                                                 #
    #                   Coletando os cursos/habilitações              #
    #                         dos cursos "antigos"                    #
    #                                                                 #
    ###################################################################
    starting_pagina_url = 'http://sistemas2.usp.br/jupiterweb/jupCursoLista?codcg=' + codigoUnidade + '&tipo=V'       #link de busca
    html_pagina = scraperwiki.scrape(starting_pagina_url)                                                  #pegando o html da página
    paginaSoup = BeautifulSoup(html_pagina)                                               #transformando num objeto do BeautifulSoup
    unidade = paginaSoup.findAll( "span", {"class" : "txt_arial_8pt_gray"} )                 #pegar a lista de cursos e seus códigos
                                                                  #criar uma lista de cursos/habilitações com os respectivos códigos
    if unidade:
        contador = 1
        for valor in unidade:
            if contador == 1:
                dados = {}
                dados['codcur'] = re.split("codcur=(\d+)", str(valor))[1]
                dados['codhab'] = re.split("codhab=(\d+)", str(valor))[1]
                contador = 2
            elif contador == 2:
                curso = valor.text
                contador = 3
            elif contador == 3:
                dados['nome'] = curso + " - " + valor.text
                contador = 4
            elif contador == 4:
                dados['periodo'] = valor.text
                dados['unidade'] = nomeUnidade
                dados['codunidade'] = codigoUnidade
                dados['Status'] = "V"
                total_cursos_unidade += 1
                scraperwiki.sqlite.save(['codcur', 'codhab'], dados)
                contador = 1
        print "---Cursos/Habilitações Antigos: " + str(total_cursos_unidade)
        total_cursos += total_cursos_unidade

print "Total de Cursos na USP: " + str(total_cursos)