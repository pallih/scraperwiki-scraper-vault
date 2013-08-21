import scraperwiki

from lxml.html import parse
import scraperwiki
import re


html = parse("http://www2.planalto.gov.br/imprensa/contatos/contatos").getroot()
    
orgaos = html.cssselect(".tileItem")
for orgao in orgaos:
    nome = orgao.cssselect("h2")[0].text_content()
    itens = orgao.cssselect(".tileBody")[0]
    count = 0
    for item in itens:
        data = { 'body' : nome }
        for linha in item.itertext():
            email = re.search("(.*@.*br)", linha)
            if email:
                data['email'] = linha.strip('Geral:')
            telefone = re.search("[0-9]", linha)
            if telefone:
                data['telefone'] = linha
            if not telefone and not email:
                data['outros'] = linha
            data['id'] = nome + str(count)
            scraperwiki.sqlite.save(['id'],data)
            count = count + 1

