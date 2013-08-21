from lxml.html import parse
import scraperwiki

html = parse("http://tools.folha.com.br/print?url=http%3A%2F%2Fwww1.folha.uol.com.br%2Ftec%2F937953-mascara-do-anonymous-remete-a-figura-historica-do-seculo-17.shtml&site=emcimadahora").getroot()

data = {}

data["titulo"]= html.cssselect("#articleNew h1")[0].text_content()
data["dia"] = html.cssselect("#articleDate")[0].text_content()
data["autor"] = html.cssselect("#articleBy")[0].text_content()
data["textobruto"] = ""
for paragrafo in html.cssselect("#articleNew p"):
    data["textobruto"] = data["textobruto"] + paragrafo.text_content()[
#para não aparecer o autor, qestá no primeiro paragrafo, o melhor seria filtrar o #articlheBy, mas como não sabemos, mandamos listar a partir do segundo elemento (1o paragrafo propriamente dito), feito assim: for paragrafo in lista_paragrafos[1:]:
#outra função aplicavel seria o get.parent

#pai do parágrafo = get.parent, classe do pai do paragrafo = get(id)
    
data["veiculo"] = "Folha de São Paulo"

#falta olho
#falta caderno
#falta url da img


scraperwiki.sqlite.save(["titulo"], data)
