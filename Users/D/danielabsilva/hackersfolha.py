from lxml.html import parse
import scraperwiki
import urllib

def paginacao():
    htmlpg = parse("http://search.folha.com.br/search?q=hacker").getroot()
    resultado = htmlpg.cssselect("h2.localSearchTarja span")[0].text_content()
    numpg = resultado.split(" de ")[1].replace(".","").strip(")")
    pgfinal = int(numpg)/25.0
    if pgfinal.is_integer():
        return int(pgfinal)
    else:
        return int(pgfinal)+1

def listaMaterias():
    x = paginacao()
    for pg in range(1,x):
        print "Raspando pag " + str(pg) + " de " + str(x)
        htmlbusca = parse("http://search.folha.com.br/search?q=hacker&sr="+str(pg)).getroot()
        links = htmlbusca.cssselect("#articleNew p a")
        for link in links:
            linkruim = link.get("href")
            linkbom = "http://tools.folha.com.br/print?url="+linkruim
            if '/especial/' in linkbom:
                print 'pulei o especial da Folha'
            else:
                try: 
                    materia(linkbom)
                except:
                    scraperwiki.sqlite.save(['url'], {'url' : linkbom},table_name="erros")
                    print "erro em " + linkbom

def materia(url):
    html = parse(url).getroot()
    lista = {}
    lista["titulo"]= html.cssselect("#articleNew h1")[0].text_content()
    lista["dia"] = html.cssselect("#articleDate")[0].text_content()
    lista["autor"] = html.cssselect("#articleBy")[0].text_content()
    titulo = html.cssselect('title')[0].text_content()
    titulo_dividido = titulo.split('-')
    lista['caderno'] = titulo_dividido[1].strip()
    lista["texto bruto"] = ""
    lista_paragrafos = html.cssselect("#articleNew p")
    for paragrafo in lista_paragrafos:
        pai_do_paragrafo = paragrafo.getparent()
        classe_do_pai_do_paragrafo = pai_do_paragrafo.get('id')
        if classe_do_pai_do_paragrafo != 'articleBy':
            lista["texto bruto"] = lista["texto bruto"] + paragrafo.text_content()
    lista["veiculo"] = "Folha de São Paulo"
    lista["fotos"] = []
    fotos = html.cssselect(".articleGraphicImage img")
    for foto in fotos:
        lista["fotos"].append(foto.get("src"))
    lista["olho"] = "não tem"

    scraperwiki.sqlite.save(["titulo"], lista)

listaMaterias()from lxml.html import parse
import scraperwiki
import urllib

def paginacao():
    htmlpg = parse("http://search.folha.com.br/search?q=hacker").getroot()
    resultado = htmlpg.cssselect("h2.localSearchTarja span")[0].text_content()
    numpg = resultado.split(" de ")[1].replace(".","").strip(")")
    pgfinal = int(numpg)/25.0
    if pgfinal.is_integer():
        return int(pgfinal)
    else:
        return int(pgfinal)+1

def listaMaterias():
    x = paginacao()
    for pg in range(1,x):
        print "Raspando pag " + str(pg) + " de " + str(x)
        htmlbusca = parse("http://search.folha.com.br/search?q=hacker&sr="+str(pg)).getroot()
        links = htmlbusca.cssselect("#articleNew p a")
        for link in links:
            linkruim = link.get("href")
            linkbom = "http://tools.folha.com.br/print?url="+linkruim
            if '/especial/' in linkbom:
                print 'pulei o especial da Folha'
            else:
                try: 
                    materia(linkbom)
                except:
                    scraperwiki.sqlite.save(['url'], {'url' : linkbom},table_name="erros")
                    print "erro em " + linkbom

def materia(url):
    html = parse(url).getroot()
    lista = {}
    lista["titulo"]= html.cssselect("#articleNew h1")[0].text_content()
    lista["dia"] = html.cssselect("#articleDate")[0].text_content()
    lista["autor"] = html.cssselect("#articleBy")[0].text_content()
    titulo = html.cssselect('title')[0].text_content()
    titulo_dividido = titulo.split('-')
    lista['caderno'] = titulo_dividido[1].strip()
    lista["texto bruto"] = ""
    lista_paragrafos = html.cssselect("#articleNew p")
    for paragrafo in lista_paragrafos:
        pai_do_paragrafo = paragrafo.getparent()
        classe_do_pai_do_paragrafo = pai_do_paragrafo.get('id')
        if classe_do_pai_do_paragrafo != 'articleBy':
            lista["texto bruto"] = lista["texto bruto"] + paragrafo.text_content()
    lista["veiculo"] = "Folha de São Paulo"
    lista["fotos"] = []
    fotos = html.cssselect(".articleGraphicImage img")
    for foto in fotos:
        lista["fotos"].append(foto.get("src"))
    lista["olho"] = "não tem"

    scraperwiki.sqlite.save(["titulo"], lista)

listaMaterias()