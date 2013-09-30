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

#Utilizamos o método cssselect para selecionar elementos na página
#o cssselect utiliza as regras de seleção de css
# use # para 'id'
# use . para 'class'
# não use nada para o elemento ex: div, td, p

tabela_subprefeitos = html.cssselect("#texto table")[1]
linhas = tabela_subprefeitos.cssselect("td[width='100%']")

# Criei uma lista com os elementos 'pais'. Os <tr>s em cima dos <td>s para facilitar a navegação.

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
    # Criar um dicionario para armazenar os valores que vamos salvar
    # Um dicionario é um conjunto de chave e valor. Ex: 'NOME' = 'PEDRO', 'IDADE', 26.
    data = {}

    # Utilizamos o método text_content() para extrair todo o texto dentro de um determinado pedaço de HTML.
    # Utilizamos o atributo .text para pegar apenas o texto que esta dentro daquela tag.

    data['nome'] = subprefeito.cssselect('td')[0].text_content()

    # Utilizamos o .getprevious() para selecionar o elemento imediatamente anterior ao nosso.
    # Utilizamos o .get('atributo') para pegar o valor de um atributo.

    data['foto'] = subprefeito.getprevious().cssselect('th img')[0].get('src')
    
    data['subprefeitura'] = subprefeito.getprevious().cssselect('th')[1].text

    # Utilizamos o .getnext() para pegar o elemento exatamente seguinte ao nosso.
    data['subprefeitura_link'] = subprefeito.getnext().cssselect('td a')[0].get('href')
    
    # Utilizamos o .strip() para remover quebras de linha e espaços desnecessarios no começo e no fim do texto.
    data['email'] = subprefeito.getnext().cssselect('td a')[1].text_content().strip()
        
    # Utilizamos o .tail para pegar o conteúdo de texto diretamente após um elemento. 
    # Ex: "<b>pedro</b> legal" o tail é = legal
    data['telefone'] = subprefeito.getnext().cssselect('td br')[1].tail.strip().strip('PABX: ')
         
    data['endereco'] = subprefeito.getnext().cssselect('td br')[3].tail
        
    # Utilizamos o if para testar condições. No caso especifico, um dos endereços estava fora do padrão html.
    if '3397-0500' in data['telefone']:
        data['endereco'] = subprefeito.getnext().cssselect('td strong')[0].tail

    # Removendo os caracteres excessivos.

    data['endereco'] = data['endereco'].strip()
                
    data['curriculo_link'] = subprefeito.getnext().cssselect('td a')[2].get('href')

    scraperwiki.sqlite.save(["email"], data)

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

#Utilizamos o método cssselect para selecionar elementos na página
#o cssselect utiliza as regras de seleção de css
# use # para 'id'
# use . para 'class'
# não use nada para o elemento ex: div, td, p

tabela_subprefeitos = html.cssselect("#texto table")[1]
linhas = tabela_subprefeitos.cssselect("td[width='100%']")

# Criei uma lista com os elementos 'pais'. Os <tr>s em cima dos <td>s para facilitar a navegação.

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
    # Criar um dicionario para armazenar os valores que vamos salvar
    # Um dicionario é um conjunto de chave e valor. Ex: 'NOME' = 'PEDRO', 'IDADE', 26.
    data = {}

    # Utilizamos o método text_content() para extrair todo o texto dentro de um determinado pedaço de HTML.
    # Utilizamos o atributo .text para pegar apenas o texto que esta dentro daquela tag.

    data['nome'] = subprefeito.cssselect('td')[0].text_content()

    # Utilizamos o .getprevious() para selecionar o elemento imediatamente anterior ao nosso.
    # Utilizamos o .get('atributo') para pegar o valor de um atributo.

    data['foto'] = subprefeito.getprevious().cssselect('th img')[0].get('src')
    
    data['subprefeitura'] = subprefeito.getprevious().cssselect('th')[1].text

    # Utilizamos o .getnext() para pegar o elemento exatamente seguinte ao nosso.
    data['subprefeitura_link'] = subprefeito.getnext().cssselect('td a')[0].get('href')
    
    # Utilizamos o .strip() para remover quebras de linha e espaços desnecessarios no começo e no fim do texto.
    data['email'] = subprefeito.getnext().cssselect('td a')[1].text_content().strip()
        
    # Utilizamos o .tail para pegar o conteúdo de texto diretamente após um elemento. 
    # Ex: "<b>pedro</b> legal" o tail é = legal
    data['telefone'] = subprefeito.getnext().cssselect('td br')[1].tail.strip().strip('PABX: ')
         
    data['endereco'] = subprefeito.getnext().cssselect('td br')[3].tail
        
    # Utilizamos o if para testar condições. No caso especifico, um dos endereços estava fora do padrão html.
    if '3397-0500' in data['telefone']:
        data['endereco'] = subprefeito.getnext().cssselect('td strong')[0].tail

    # Removendo os caracteres excessivos.

    data['endereco'] = data['endereco'].strip()
                
    data['curriculo_link'] = subprefeito.getnext().cssselect('td a')[2].get('href')

    scraperwiki.sqlite.save(["email"], data)

