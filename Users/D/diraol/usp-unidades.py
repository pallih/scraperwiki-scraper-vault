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

#####################Coletando todas as unidades (nome, código)#####################
#Pegando a listagem das unidades por servidores temos todas as possibilidades (mais do que por docentes)
starting_unidades_url = 'http://sistemas3.usp.br/tycho/curriculoLattesListarUnidades?vinculo=SERVIDOR' #link de busca
html_unidades = scraperwiki.scrape(starting_unidades_url) #pegando o html da página
unidadesSoup = BeautifulSoup(html_unidades) #transformando num objeto do BeautifulSoup
unidades = unidadesSoup.findAll( "a", {"class" : "link_olive"} ) #usar o BeautifulSoup para pegar a lista de unidades e seus códigos
total_unidades = 0 #Contador do número de unidades
lista = []
for unidade in unidades:
    dados = {}
    codigoUnidade = int(re.split("codigoUnidade=(\d+)", str(unidade))[1]) #Pegando o código das unidade
    dados['codUnidade'] = codigoUnidade
    nomeUnidade = re.split(" \(", unidade.string)[0] #Pegando apenas o nome da unidade
    dados['nomeUnidade'] = re.sub("&#034;",'"',nomeUnidade)
    lista.append(dados)

#Colocando em ordem de código de unidade
lista = sorted(lista, key=lambda x: x['codUnidade'])
#lista = sorted(lista, key=lambda x: x['codUnidade'], reverse=True) #Tentativa de salvar a lista invertida, mas não deu certo
for item in lista:
    #Salvando a lista no datastore da lista das unidades
    scraperwiki.datastore.save(['codUnidade'], item)
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

#####################Coletando todas as unidades (nome, código)#####################
#Pegando a listagem das unidades por servidores temos todas as possibilidades (mais do que por docentes)
starting_unidades_url = 'http://sistemas3.usp.br/tycho/curriculoLattesListarUnidades?vinculo=SERVIDOR' #link de busca
html_unidades = scraperwiki.scrape(starting_unidades_url) #pegando o html da página
unidadesSoup = BeautifulSoup(html_unidades) #transformando num objeto do BeautifulSoup
unidades = unidadesSoup.findAll( "a", {"class" : "link_olive"} ) #usar o BeautifulSoup para pegar a lista de unidades e seus códigos
total_unidades = 0 #Contador do número de unidades
lista = []
for unidade in unidades:
    dados = {}
    codigoUnidade = int(re.split("codigoUnidade=(\d+)", str(unidade))[1]) #Pegando o código das unidade
    dados['codUnidade'] = codigoUnidade
    nomeUnidade = re.split(" \(", unidade.string)[0] #Pegando apenas o nome da unidade
    dados['nomeUnidade'] = re.sub("&#034;",'"',nomeUnidade)
    lista.append(dados)

#Colocando em ordem de código de unidade
lista = sorted(lista, key=lambda x: x['codUnidade'])
#lista = sorted(lista, key=lambda x: x['codUnidade'], reverse=True) #Tentativa de salvar a lista invertida, mas não deu certo
for item in lista:
    #Salvando a lista no datastore da lista das unidades
    scraperwiki.datastore.save(['codUnidade'], item)
