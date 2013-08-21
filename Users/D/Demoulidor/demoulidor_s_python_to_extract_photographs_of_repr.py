# Demoulidor´s Python to extract photographs of Representatives of Brazil
# Programa em linguagem Python para extrair fotografias dos Deputados Federais do Brasil
import scraperwiki
url = "http://www.camara.gov.br/internet/deputado/Dep_Lista_foto.asp?Legislatura=54&Partido=QQ&SX=QQ&Todos=None&UF=QQ&condic=QQ&forma=lista&nome=&ordem=nome&origem=None"
html = scraperwiki.scrape(url)
print html

import lxml.html
root = lxml.html.fromstring(html)


