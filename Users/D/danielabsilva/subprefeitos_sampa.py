import scraperwiki 
from lxml.html import parse

html = parse("http://www.prefeitura.sp.gov.br/cidade/secretarias/subprefeituras/subprefeituras/subprefeitos/index.php?p=21778").getroot()

tabela_subprefeitos = html.cssselect("#texto table")[1]
linhas = tabela_subprefeitos.cssselect("td[width='100%']")

for elemento in linhas:
    print linhas.text_content()



