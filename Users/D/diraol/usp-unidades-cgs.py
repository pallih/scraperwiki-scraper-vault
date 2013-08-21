###############################################################################
# Basic scraper
# USP - UNIDADES DE ENSINO - Por Comissões de Graduação
# PÁGINA BASE DO JUPITERWEB
# http://sistemas2.usp.br/jupiterweb/jupColegiadoLista?tipo=D
###############################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup

#####################Coletando todas as unidades (CGs) (nome, código)#####################
cgs_url = 'http://sistemas2.usp.br/jupiterweb/jupColegiadoLista?tipo=D' #link de busca
html_cgs = scraperwiki.scrape(cgs_url) #pegando o html da página
cgsSoup = BeautifulSoup(html_cgs) #transformando num objeto do BeautifulSoup
cgs = cgsSoup.findAll( "span", {"class" : "txt_arial_8pt_gray"} ) #usar o BeautifulSoup para pegar a lista de cgs e seus códigos
lista = []
contador = 1

for cg in cgs:
    if contador % 2: #se for par retorna zero, se for ímpar retorna 1
        #caso ímpar (códgio_unidade)
        dados = {}
        codigoUnidade = int(cg.text)
        dados['codUnidade'] = codigoUnidade
        contador = 0
    else:
        #caso par (nome_unidade)
        nomeUnidade = cg.text
        dados['nomeUnidade'] = re.sub("&#034;",'"',nomeUnidade)
        lista.append(dados)
        contador = 1

#Colocando em ordem de código de unidade
lista = sorted(lista, key=lambda x: x['codUnidade'])
for item in lista:
    #Salvando a lista no datastore da lista das unidades
    scraperwiki.datastore.save(['codUnidade'], item)

