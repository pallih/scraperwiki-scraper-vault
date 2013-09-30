# Scraper 01 - Obter as CPIs em aberto na câmara municipal de São Paulo.
# URL que será raspada: http://www1.camara.sp.gov.br/cpi_joomla.asp
# URL principal (de onde a url acima é chamada através de um iframe): http://www.camara.sp.gov.br/index.php?option=com_wrapper&view=wrapper&Itemid=38
# Dados que serão raspados:
#     - Título da CPI
#     - url para detalhes da CPI

# PARA FAZER (02/02/12):
# - Implementar leitura de detalhes da cpi, como texto, data início e data término.

#scraperwiki - armazena as informacoes de uma variavel dicionario no scraperwiki
#lxml - para scrapear as paginas

import scraperwiki
from lxml.html import parse

# parse() -> método html para transformar o html da página em um objeto que o Python entende.
# .getroot() -> obtém a raiz do objeto

html = parse("http://www1.camara.sp.gov.br/cpi_joomla.asp").getroot()

# O método cssselect para selecionar elementos na página (utiliza as regras de seleção de css)
# use # para 'id'
# use . para 'class'
# não use nada para o elemento ex: div, td, p

linhas = html.cssselect("tr")

for linha in linhas:
    # Criar um dicionario para armazenar os valores que vamos salvar - chave/valor
    data = {}

    # nome da CPI
    data['nome'] = linha.cssselect('td')[1].text_content()

    # url de detalhe da CPI, utilizada também como id único
    data['urlDetalhe'] = linha.cssselect('td a')[0].get('href')

    # url completa para acessar a página de detalhe da CPI
    data['urlCompleta'] = 'http://www1.camara.sp.gov.br/%s' % data['urlDetalhe']

    # print data['urlCompleta']
    scraperwiki.sqlite.save(["urlDetalhe"], data)
# Scraper 01 - Obter as CPIs em aberto na câmara municipal de São Paulo.
# URL que será raspada: http://www1.camara.sp.gov.br/cpi_joomla.asp
# URL principal (de onde a url acima é chamada através de um iframe): http://www.camara.sp.gov.br/index.php?option=com_wrapper&view=wrapper&Itemid=38
# Dados que serão raspados:
#     - Título da CPI
#     - url para detalhes da CPI

# PARA FAZER (02/02/12):
# - Implementar leitura de detalhes da cpi, como texto, data início e data término.

#scraperwiki - armazena as informacoes de uma variavel dicionario no scraperwiki
#lxml - para scrapear as paginas

import scraperwiki
from lxml.html import parse

# parse() -> método html para transformar o html da página em um objeto que o Python entende.
# .getroot() -> obtém a raiz do objeto

html = parse("http://www1.camara.sp.gov.br/cpi_joomla.asp").getroot()

# O método cssselect para selecionar elementos na página (utiliza as regras de seleção de css)
# use # para 'id'
# use . para 'class'
# não use nada para o elemento ex: div, td, p

linhas = html.cssselect("tr")

for linha in linhas:
    # Criar um dicionario para armazenar os valores que vamos salvar - chave/valor
    data = {}

    # nome da CPI
    data['nome'] = linha.cssselect('td')[1].text_content()

    # url de detalhe da CPI, utilizada também como id único
    data['urlDetalhe'] = linha.cssselect('td a')[0].get('href')

    # url completa para acessar a página de detalhe da CPI
    data['urlCompleta'] = 'http://www1.camara.sp.gov.br/%s' % data['urlDetalhe']

    # print data['urlCompleta']
    scraperwiki.sqlite.save(["urlDetalhe"], data)
