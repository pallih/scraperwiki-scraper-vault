import scraperwiki

# Blank Python

# -*- coding: UTF-8 -*-
import urllib
from BeautifulSoup import BeautifulSoup, SoupStrainer
from time import time

anos = ['2011'] #'2010','2009','2008','2007']

#lista tirada de http://www.ibge.gov.br/home/geociencias/areaterritorial/principal.shtm

ufs = [
    '21', #Maranhão
    '22', #Piauí
    '23', #Ceará
    '24', #Rio Grande do Norte
    '25', #Paraíba
    '26', #Pernambuco
    '27', #Alagoas
    '28', #Sergipe
    '29', #Bahia

]

aufs = [
    '35', #São Paulo
    '11', #Rondônia
    '12', #Acre
    '13', #Amazonas
    '14', #Roraima
    '15', #Pará
    '16', #Amapá
    '17', #Tocantins
    '21', #Maranhão
    '22', #Piauí
    '23', #Ceará
    '24', #Rio Grande do Norte
    '25', #Paraíba
    '26', #Pernambuco
    '27', #Alagoas
    '28', #Sergipe
    '29', #Bahia
    '31', #Minas Gerais
    '32', #Espírito Santo
    '33', #Rio de Janeiro
    '41', #Paraná
    '42', #Santa Catarina
    '43', #Rio Grande do Sul
    '50', #Mato Grosso do Sul
    '51', #Mato Grosso
    '52', #Goiás
    '53', #Distrito Federal
]

url = "https://www.fnde.gov.br/siope/dadosInformadosMunicipio.do"

##def url_final(uf,munic,ano):
  ##  return url_parte1 + ano + url_parte2 + uf + url_parte3 + munic + url_parte4


#cronômetro
##t0 = time()

#saida = open('saida.txt', 'w')

def lista_municipios(uf):
    municipios = []
    url = "https://www.fnde.gov.br/siope/relatorioRREOMunicipal2009.do"
    page = urllib.urlopen(url, urllib.urlencode({'cod_uf': uf}))
    soup = BeautifulSoup(page.read())
    a = soup.find('select', {"name": 'municipios'})

    for i in a.findAll('option'):
        municipios.append(i['value'])

    return municipios

##contador_municipios_ok = 0
##contador_municipios_pulados = 0
##total_municipios_feitos = 0

for uf in ufs:
    municipios = lista_municipios(uf)

    for municipio in municipios:
    ##    total_municipios_feitos += 1
        retorno = {}
        retorno['uf'] = uf
        retorno['municipio'] = municipio
        for ano in anos:
            parametros = {'acao': 'pesquisar',
                          'pag': 'result',
                          'periodos': 1,
                          'anos': ano,
                          'cod_uf': uf,
                          'municipios': municipio,
                          'admin': 3,
                          'planilhas': 125,
                          'descricaoItem': 'Consolidado+de+Despesa',
                          'descricaodoItem': 'Consolidado+de+Receita',
                          'nivel': ''}

            #monta a url conforme os parâmetros especificados e estabelece a conexão com o servidor
            pagina = urllib.urlopen(url, urllib.urlencode(parametros))

            #joga fora todos os elementos da página que não as linhas de uma tabela - tr (table row)
            linhas = BeautifulSoup(pagina.read(), parseOnlyThese=SoupStrainer('tr'))
            

            try:
                #realiza a busca pelo texto determinado
                linha_alvo = linhas.find(text='DESPESA TOTAL (Inclui Inativos)').parent.parent.parent

                #uma vez com a linha alvo, é só filtrar as colunas (td) certas
                colunas = linha_alvo.findAll('td')
                #atualizada = colunas[2].findChild().text
                retorno['pago' + '_' + ano] = colunas[4].findChild().text
  ##              contador_municipios_ok += 1


                #saida.write("%s;%s;%s;%s\n" % (ano, uf, municipio, pago))
            #Se a operação de busca da linha alvo falhar (porque o município não existe, por exemplo),
            #a condição abaixo é executada
            except AttributeError:
                retorno['pago' + '_' + ano] = 0
                #contador_municipios_pulados += 1
                #saida.write("%s;%s;%s;---\n" % (ano, uf, municipio))

        scraperwiki.sqlite.save(['municipio'], retorno)
        ##if (total_municipios_feitos % 10) == 0:
          ##  print total_municipios_feitos

##t1 = time()

#saida.write('\n\nTempo de execução: %.1fs' %(t1-t0))
##print '\n\nTempo de execução: %.1fs' %(t1-t0)
#saida.close()
import scraperwiki

# Blank Python

# -*- coding: UTF-8 -*-
import urllib
from BeautifulSoup import BeautifulSoup, SoupStrainer
from time import time

anos = ['2011'] #'2010','2009','2008','2007']

#lista tirada de http://www.ibge.gov.br/home/geociencias/areaterritorial/principal.shtm

ufs = [
    '21', #Maranhão
    '22', #Piauí
    '23', #Ceará
    '24', #Rio Grande do Norte
    '25', #Paraíba
    '26', #Pernambuco
    '27', #Alagoas
    '28', #Sergipe
    '29', #Bahia

]

aufs = [
    '35', #São Paulo
    '11', #Rondônia
    '12', #Acre
    '13', #Amazonas
    '14', #Roraima
    '15', #Pará
    '16', #Amapá
    '17', #Tocantins
    '21', #Maranhão
    '22', #Piauí
    '23', #Ceará
    '24', #Rio Grande do Norte
    '25', #Paraíba
    '26', #Pernambuco
    '27', #Alagoas
    '28', #Sergipe
    '29', #Bahia
    '31', #Minas Gerais
    '32', #Espírito Santo
    '33', #Rio de Janeiro
    '41', #Paraná
    '42', #Santa Catarina
    '43', #Rio Grande do Sul
    '50', #Mato Grosso do Sul
    '51', #Mato Grosso
    '52', #Goiás
    '53', #Distrito Federal
]

url = "https://www.fnde.gov.br/siope/dadosInformadosMunicipio.do"

##def url_final(uf,munic,ano):
  ##  return url_parte1 + ano + url_parte2 + uf + url_parte3 + munic + url_parte4


#cronômetro
##t0 = time()

#saida = open('saida.txt', 'w')

def lista_municipios(uf):
    municipios = []
    url = "https://www.fnde.gov.br/siope/relatorioRREOMunicipal2009.do"
    page = urllib.urlopen(url, urllib.urlencode({'cod_uf': uf}))
    soup = BeautifulSoup(page.read())
    a = soup.find('select', {"name": 'municipios'})

    for i in a.findAll('option'):
        municipios.append(i['value'])

    return municipios

##contador_municipios_ok = 0
##contador_municipios_pulados = 0
##total_municipios_feitos = 0

for uf in ufs:
    municipios = lista_municipios(uf)

    for municipio in municipios:
    ##    total_municipios_feitos += 1
        retorno = {}
        retorno['uf'] = uf
        retorno['municipio'] = municipio
        for ano in anos:
            parametros = {'acao': 'pesquisar',
                          'pag': 'result',
                          'periodos': 1,
                          'anos': ano,
                          'cod_uf': uf,
                          'municipios': municipio,
                          'admin': 3,
                          'planilhas': 125,
                          'descricaoItem': 'Consolidado+de+Despesa',
                          'descricaodoItem': 'Consolidado+de+Receita',
                          'nivel': ''}

            #monta a url conforme os parâmetros especificados e estabelece a conexão com o servidor
            pagina = urllib.urlopen(url, urllib.urlencode(parametros))

            #joga fora todos os elementos da página que não as linhas de uma tabela - tr (table row)
            linhas = BeautifulSoup(pagina.read(), parseOnlyThese=SoupStrainer('tr'))
            

            try:
                #realiza a busca pelo texto determinado
                linha_alvo = linhas.find(text='DESPESA TOTAL (Inclui Inativos)').parent.parent.parent

                #uma vez com a linha alvo, é só filtrar as colunas (td) certas
                colunas = linha_alvo.findAll('td')
                #atualizada = colunas[2].findChild().text
                retorno['pago' + '_' + ano] = colunas[4].findChild().text
  ##              contador_municipios_ok += 1


                #saida.write("%s;%s;%s;%s\n" % (ano, uf, municipio, pago))
            #Se a operação de busca da linha alvo falhar (porque o município não existe, por exemplo),
            #a condição abaixo é executada
            except AttributeError:
                retorno['pago' + '_' + ano] = 0
                #contador_municipios_pulados += 1
                #saida.write("%s;%s;%s;---\n" % (ano, uf, municipio))

        scraperwiki.sqlite.save(['municipio'], retorno)
        ##if (total_municipios_feitos % 10) == 0:
          ##  print total_municipios_feitos

##t1 = time()

#saida.write('\n\nTempo de execução: %.1fs' %(t1-t0))
##print '\n\nTempo de execução: %.1fs' %(t1-t0)
#saida.close()
