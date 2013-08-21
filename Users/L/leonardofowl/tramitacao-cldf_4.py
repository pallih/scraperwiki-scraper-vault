# -*- coding: utf-8 -*-  


# link que devera ser acionado
# http://www.cl.df.gov.br/Legislacao/consultaProposicao-[1..9]![1..9999]![2011]!visualizar.action

# constante da url (usar o %s para substituir)
starting_url = 'http://www.cl.df.gov.br/Legislacao/consultaProposicao-%s!%s!%s!visualizar.action'

#Tipos de proposicoes
#1- Projeto de Lei 
#8- Projeto de Lei Complementar 
#9- Proposta de Emenda à Lei Orgânica 
#6- Projeto de Decreto Legislativo 
#5- Projeto de Resolução 
#2- Indicação 
#4- Moção 
#7- Recurso 
#3- Requerimento



###############################################################################
import scraperwiki
import urllib
import re
from BeautifulSoup import BeautifulSoup


#converte acentuacao em unescape para unicode
import copy, re

hexentityMassage = copy.copy(BeautifulSoup.MARKUP_MASSAGE)
hexentityMassage = [(re.compile('&#x([^;]+);'), 
    lambda m: '&#%d' % int(m.group(1), 16))]

def convert(html):
    return BeautifulSoup(html,
        convertEntities=BeautifulSoup.HTML_ENTITIES,
        markupMassage=hexentityMassage)


###############################################################################







###############################################################################
#funcao para scrapear os dados
###############################################################################
def scrape(tipoprop, numprop, anoprop):

    url = starting_url % (tipoprop, numprop, anoprop)
    html = urllib.urlopen(url).read()

    #soup = BeautifulSoup(html)
    soup = convert(html)
    #usar o BeautifulSoup para pegar os dados do projeto


    if not soup.find("span", { "class" : "actionMessage" }) is None:
        print "NAO RETORNOU REGISTRO"
        return False

    #carregar as linhas (td's) da primeira tabela
    linhas = soup.findAll("td", { "class" : "linha" }) #text='Proposição:')

    data = {
        "chave" : "%s-%s-%s" % (anoprop, tipoprop, numprop),
        "tipoprop": tipoprop,
        "numprop": numprop,
        "anoprop": anoprop,
    
        "proposicao": linhas[0].text,
        "ementa": linhas[1].text,
        "leitura": linhas[2].text,
        "situacao": linhas[3].text,
        "localizacao": linhas[4].text,
        "autoria": linhas[5].text
    }
    
    #incluir historicos (table da ultima td com class linha)
    historicos = linhas[6].findAll("tr")
    for index, historico in enumerate(historicos):
        items = historico.findAll("td")
    
        historico_item = items[0].text
        historico_data = items[1].text
        historico_local = items[2].text
        historico_texto = items[3].text
    
        if index == 0:
            data["historicos"] = historico_item
    
        data["historico_%s_data" % historico_item] = historico_data
        data["historico_%s_local" % historico_item] = historico_local
        data["historico_%s_texto" % historico_item] = historico_texto
    
    print data
    scraperwiki.sqlite.save(unique_keys=["chave"], data=data)
    return True


###############################################################################
# percorrer tipos de proposicoes e numeros
###############################################################################

#TODO: melhorar o esquema de percorrer os itens (salvar de onde parou)

#for tipoprop in range(9):
#    for numprop in range(999):
#        if not scrape(tipoprop+1, numprop+1, "2011"):
#            break;


for numprop in range(999):
     if not scrape("2", numprop+1, "2011"):
         break;


#scrape("1", "9999", "2011")
#scrape("1", "2", "2011")
# range(3,10) - para determinar o inicio e fim do range

