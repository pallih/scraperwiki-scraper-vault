# -*- coding: utf-8 -*-

# Scraping 101 - Página de Subprefeitos
# Essa é a página que queremos scrapear:
# http://www.prefeitura.sp.gov.br/cidade/secretarias/subprefeituras/subprefeituras/subprefeitos/index.php?p=21778
# Queremos obter as seguintes informações de cada subprefeito:
# * Nome
# * Link da Foto
# * Subprefeitura
# * Link pra página da subprefeitura
# * Email
# * Telefone
# * Endereço da praça de atendimento
# * Link para o curriculo


#importanto as bibliotecas que vamos utilizar
#scraperwiki - armazena as informacoes de uma variavel dicionario no scraperwiki
#lxml - para scrapear as paginas

import scraperwiki 
from lxml.html import parse

# Utilizaremos a função parse() do método html para transformar o html da página em um objeto que o Python entenda.
# Vamos guardar a raiz desse objeto na variavel 'html' usando o metodo .getroot()

html = parse("http://www.prefeitura.sp.gov.br/cidade/secretarias/subprefeituras/subprefeituras/subprefeitos/index.php?p=21778").getroot()

# utilizamos o cssselect para selecionar elementos da pagina
# o cssselect utiliza as regras da seleção css
# use # para 'id'
# use . para 'class'
# nao use nada para o elemento ex: div, ts, p

tabela_subprefeitos = html.cssselect("#texto table")[1]
linhas = tabela_subprefeitos.cssselect("td[width='100%']")
linhas.pop(0)

# criar uma lista com os elementos 'pais'. Os <tr>s 
linhas_subprefeitos = []
for linha in linhas:
    linhas_subprefeitos.append(linha.getparent())

#Exemplo de HTML de um subprefeito
# <tr>
#   <th width="25%" style="text-align: center;" rowspan="3"><img width="95" height="108" src="http://www.prefeitura.sp.gov.br/cidade/secretarias/upload/subprefeituras/secretaria/Fotos%20subprefeitos/Aricanduva_Jorge%20Augusto%20leme.jpg" alt=""></th>
#   <th colspan="2" style="text-align: left;">Aricanduva / Vila Formosa</th>
# </tr>
#
# <tr>
#  <td width="100%" colspan="2" style="text-align: left;"><strong>Jorge Augusto Leme</strong></td>
# </tr>
#
# <tr>
#  <td colspan="2" style="text-align: left;">
#     <p><a href="http://vilaprudente.prefeitura.sp.gov.br/">http://vilaprudente.prefeitura.sp.gov.br</a><br>
#     <a href="mailto:vilaprudentegabineteexp@prefeitura.sp.gov.br">vilaprudentegabineteexp@prefeitura.sp.gov.br</a><br>
#      PABX: 3397-0800<br>
#     <strong>Praça de Atendimento</strong><br>
#     Avenida do Oratório, 172 - CEP 03220-000<br>
#     <a href="http://www.prefeitura.sp.gov.br/cidade/secretarias/subprefeituras/vila_prudente/organizacao/index.php?p=379">Curriculo</a></p>
#  </td>
# </tr>


for subprefeito in linhas_subprefeitos:
    
# criar um dicionario (conjunto de chave e valor) para armazenar os valores que vamos salvar
# dicionario sempre um conjunto de chave e valor ex:"nome" = 'henrique', 'idade', 23
    
    data = {}

    #utilizamos o text_content() para extrair tododo o texto dentro de um determinado pedaço de html
    #utilizamos o atributo .text para pegar apenas o texto que esta dentro daquela tag
    #utilizamos o .get('atributo') para pegar o valor de um atributo    
    
    data['nome'] = subprefeito.cssselect('td')[0].text_content
    
    data['foto'] = subprefeito.getprevious().cssselect('th img')[0].get('src')
    
    data['subprefeitura'] = subprefeito.getprevious().cssselect('th')[1].text
    
    #utilizagetmos o getnext() para pegar o elemento exatamente seguinte ao nosso
    data['subprefeitura_link'] = subprefeito.getnext().cssselect('td a')[0].get('href')
    
    #utilizamos o .strip() para remover quebras de linha e espaços desnecessarios no começo e no fim do texto    
    data['email'] = subprefeito.getnext().cssselect('td a')[1].text_content().strip()
   
    #utilizar o .tail para pegar o conteúdo de texto deretamente após um elemento. ex: "<b>henrique</b> legal" o tail é legal
    data['telefone'] = subprefeito.getnext().cssselect('td br')[1].tail.strip().strip('PABX: ')
    
    data['endereco'] = subprefeito.getnext().cssselect('td br')[3].tail
    
    #utilizamos o if para testar condições.
    if '3397-0500' in data['telefone']:
        data['endereco'] = subprefeito.getnext().cssselect('td strong')[0].tail 

    data['endereco'].strip()
    
    data['curriculo_link'] = subprefeito.getnext().cssselect('td a')[2].get('href')


    curriculo = parse(data['curriculo_link']).getroot()
    curriculo.cssselect["#texto_p")[2].text_content()
    print curriculo

    # scraperwiki.sqlite.save(["email"], data)
    
    



