import scraperwiki

from lxml.html import parse
import scraperwiki
import re


html = parse("http://www.aenoticias.pr.gov.br/modules/conteudo/conteudo.php?conteudo=80").getroot()
meio = html.cssselect("#conteudo")
linkfim = meio[0].cssselect("#conteudo-funcoes")
meio[0].remove(linkfim[0])
count = 0
orgaos = meio[0].cssselect("a")
for orgao in orgaos:
    data = {}
    data["nome"] = orgao.text_content()
    try:
        data["url"] = orgao.get("href")
    except:
        data["url"] = "sem url"
    if orgao.getparent().tag == "h5":
        data["telefone"] = orgao.getparent().tail
    else:
        data["telefone"]=orgao.tail
    data["id"] = count
    scraperwiki.sqlite.save(['id'],data)
    count = count + 1








    