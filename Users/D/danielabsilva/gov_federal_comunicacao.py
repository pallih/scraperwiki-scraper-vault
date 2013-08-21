import scraperwiki

from lxml.html import parse
import scraperwiki
import re


html = parse("http://www2.planalto.gov.br/imprensa/contatos/contatos").getroot()
    
orgaos = html.cssselect(".tileItem")
for orgao in orgaos:
    nome = orgao.cssselect("h2")[0].text_content()
    itens = orgao.cssselect(".tileBody")[0]
    for item in itens:
        for linha in item.itertext():
            email = re.search("(.*@.*br)", linha)
            if email:
                print linha
            telefone = re.search("[0-9]", linha)
            if telefone:
                print linha

scraperwiki.sqlite.save_var('data_columns', [nome, email, telefone])


