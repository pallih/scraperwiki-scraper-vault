import scraperwiki
import re
from BeautifulSoup import BeautifulSoup

## URL DE ORIGEM
url = 'http://www2.camara.sp.gov.br/Salarios/HTML/todos.html' #link de busca
html = scraperwiki.scrape(url) #pegando o html da página
soupObj = BeautifulSoup(html) #transformando num objeto do BeautifulSoup
tabela_principal = soupObj.findAll( "table", {"cellpadding":"0px"} ) #filtrando pelo tipo "tabela" com filtro de cellpadding
auxiliar = soupObj.findAll("th", {"bgcolor": "LightGrey"}) #Recuperando os "títulos"
titulos_pessoas = []#lista de títulos possíveis
#populando a lista de títulos e removendo os títulos do objeto Soup
for item in auxiliar:
    titulos_pessoas.append(item.text)
    item.extract()
auxiliar = soupObj.findAll("th")
for item in auxiliar:
    item.extract()
print tabela_principal.contents[0]


#lista = []
#contador = 1



