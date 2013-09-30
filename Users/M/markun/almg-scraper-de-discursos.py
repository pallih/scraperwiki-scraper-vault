import scraperwiki
from lxml.html import parse
import urllib

html = urllib.urlopen("http://www.almg.gov.br/consulte/pronunciamentos/index.html?pagina=1&advanced=advanced&run=1&aba=js_pesquisaAvancada&txtPalavras=copa&tp=100&ordem=2")
soup = parse(html).getroot()

numero_de_paginas = int(soup.cssselect(".paginas-contagem")[0].text_content().split("/")[1].strip())

print numero_de_paginas

def pegaLinks(numero_da_pagina):
    html = urllib.urlopen("http://www.almg.gov.br/consulte/pronunciamentos/index.html?pagina="+ str(numero_da_pagina) +"&advanced=advanced&run=1&aba=js_pesquisaAvancada&txtPalavras=copa&tp=100&ordem=2")
    soup = parse(html).getroot()

    discursos = []
    for d in soup.cssselect("#busca-acervo li"):
        if d.cssselect("a.read-more"):
            discurso = pegaInformacao(d.cssselect("a.read-more")[0].get("href"))
            discursos.append(discurso)
            print d.cssselect("a.read-more")[0].get("href")
    return discursos

def pegaInformacao(d):
    html = urllib.urlopen("http://www.almg.gov.br" + d)
    soup = parse(html).getroot()
    discurso = {}
    discurso['url'] = "http://www.almg.gov.br" + d
    discurso['autor'] = soup.xpath("//strong[text()='Autor:']")[0].text_content().strip("Autor:").strip()
    discurso['data'] = soup.xpath("//strong[text()='Data:']")[0].text_content().strip()
    if soup.xpath("//strong[text()='Partido:']/.."):
        discurso['partido'] =  soup.xpath("//strong[text()='Partido:']/..")[0].text_content().strip("Partido:").strip()
    discurso['assunto'] = soup.xpath("//strong[text()='Assunto:']/..")[0].text_content().strip("Assunto:").strip()
    discurso['resumo'] = soup.xpath("//strong[text()='Resumo:']/..")[0].text_content().strip("Resumo:").strip()
    discurso['integra'] = soup.cssselect("#js_tabTexto")[0].text_content()
    scraperwiki.sqlite.save(['url'], discurso)
    return discurso

for pagina in range(1,numero_de_paginas+1):
    discursos = pegaLinks(pagina)
import scraperwiki
from lxml.html import parse
import urllib

html = urllib.urlopen("http://www.almg.gov.br/consulte/pronunciamentos/index.html?pagina=1&advanced=advanced&run=1&aba=js_pesquisaAvancada&txtPalavras=copa&tp=100&ordem=2")
soup = parse(html).getroot()

numero_de_paginas = int(soup.cssselect(".paginas-contagem")[0].text_content().split("/")[1].strip())

print numero_de_paginas

def pegaLinks(numero_da_pagina):
    html = urllib.urlopen("http://www.almg.gov.br/consulte/pronunciamentos/index.html?pagina="+ str(numero_da_pagina) +"&advanced=advanced&run=1&aba=js_pesquisaAvancada&txtPalavras=copa&tp=100&ordem=2")
    soup = parse(html).getroot()

    discursos = []
    for d in soup.cssselect("#busca-acervo li"):
        if d.cssselect("a.read-more"):
            discurso = pegaInformacao(d.cssselect("a.read-more")[0].get("href"))
            discursos.append(discurso)
            print d.cssselect("a.read-more")[0].get("href")
    return discursos

def pegaInformacao(d):
    html = urllib.urlopen("http://www.almg.gov.br" + d)
    soup = parse(html).getroot()
    discurso = {}
    discurso['url'] = "http://www.almg.gov.br" + d
    discurso['autor'] = soup.xpath("//strong[text()='Autor:']")[0].text_content().strip("Autor:").strip()
    discurso['data'] = soup.xpath("//strong[text()='Data:']")[0].text_content().strip()
    if soup.xpath("//strong[text()='Partido:']/.."):
        discurso['partido'] =  soup.xpath("//strong[text()='Partido:']/..")[0].text_content().strip("Partido:").strip()
    discurso['assunto'] = soup.xpath("//strong[text()='Assunto:']/..")[0].text_content().strip("Assunto:").strip()
    discurso['resumo'] = soup.xpath("//strong[text()='Resumo:']/..")[0].text_content().strip("Resumo:").strip()
    discurso['integra'] = soup.cssselect("#js_tabTexto")[0].text_content()
    scraperwiki.sqlite.save(['url'], discurso)
    return discurso

for pagina in range(1,numero_de_paginas+1):
    discursos = pegaLinks(pagina)
