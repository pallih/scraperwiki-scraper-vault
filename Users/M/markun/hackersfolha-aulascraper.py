from lxml.html import parse
import scraperwiki

def scrapeiaPagina(url):
    url = "http://tools.folha.com.br/print?url=" + url
    print url
    
    html = parse(url).getroot()
    
    data = {}
    
    data["titulo"]= html.cssselect("#articleNew h1")[0].text_content()
    data["dia"] = html.cssselect("#articleDate")[0].text_content()
    data["autor"] = html.cssselect("#articleBy")[0].text_content()
    data["textobruto"] = ""
    lista_paragrafos = html.cssselect("#articleNew p")
    
    for paragrafo in lista_paragrafos:
        pai_do_paragrafo = paragrafo.getparent()
        classe_do_pai_do_paragrafo = pai_do_paragrafo.get('id')
    
        if classe_do_pai_do_paragrafo != 'articleBy':
            data["textobruto"] = data["textobruto"] + paragrafo.text_content()
    
    data["veiculo"] = "Folha de São Paulo"
    
    #falta olho
    titulo = html.cssselect('title')[0].text_content()
    titulo_dividido = titulo.split('-')
    data['caderno'] = titulo_dividido[1].strip() #o item 1 eh o caderno
    
    data['urls_imagem'] = []
    imagens = html.cssselect('.articleGraphicImage img')
    
    for imagem in imagens:
        data['fotos'] += [foto.get("src")]
        data['urls_imagem'].append(imagem.get('src'))
    
    scraperwiki.sqlite.save(["titulo"], data)

html_l = parse("http://search.folha.com.br/search?q=hackers").getroot()

links = html_l.cssselect("#articleNew p a")
for l in links:
    if 'http://search.folha.com.br/' not in l.get('href'):
        try:
            scrapeiaPagina(l.get('href'))
        except:
            print 'resolvo depois:' + l.get('href')

