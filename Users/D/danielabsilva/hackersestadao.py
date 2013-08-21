from lxml.html import parse, document_fromstring
from BeautifulSoup import UnicodeDammit
import scraperwiki
import urllib

def decode_html(html_string):
    converted = UnicodeDammit(html_string, isHTML=True)
    if not converted.unicode:
        raise UnicodeDecodeError(
            ', '.join(converted.triedEncodings))
    return document_fromstring(converted.unicode)

def paginacao():
    htmlpg = parse("http://www.estadao.com.br/busca/hacker").getroot()
    numpg = htmlpg.cssselect("#resultados-tabs ul.first li span")[0].text_content()
    pgfinal = int(numpg)/10.0
    if pgfinal.is_integer():
        return int(pgfinal)
    else:
        return int(pgfinal)+1

def listaMaterias():
    x = paginacao()
    for pg in range(1,x):
        print "Raspando pag " + str(pg) + " de " + str(x)
        html = parse("http://www.estadao.com.br/busca/includeBuscaEstadaoNovo/hacker/"+str(pg)).getroot()
        links = html.cssselect(".bb-md-resultados_tab h2 a")
        for link in links:
            linkruim = link.get("href").split("/")
            linkbom = "http://www.estadao.com.br/noticia_imp.php?req="+linkruim[len(linkruim)-1]
            baixaMateria(linkbom)

def baixaMateria(url):
    html_string = urllib.urlopen(url).read()
    try: 
        html = decode_html(html_string)
        materia(html,url)
    except:
        scraperwiki.sqlite.save(['url'], {'url' : url},table_name="erros")

def materia(html,url):
    titulo = html.cssselect(".bb-md-noticia h2")
    olho = html.cssselect(".bb-md-noticia h3")
    data = html.cssselect(".bb-md-noticia-fecha")
    autor = html.cssselect (".bb-md-noticia-autor")
    caderno = html.cssselect ("#logosub")
    textobruto = html.cssselect (".corpo")
    veiculo = "Estado de São Paulo"
    urlimg = html.cssselect (".corpo img")

    lista = {}
    lista['url']=url
    lista['titulo']=titulo[0].text_content()
    lista['olho']=olho[0].text_content()
    lista['data']=data[0].text_content()
    lista['autor']=autor[0].text_content().lstrip(" - ")
    lista['caderno']=caderno[0].text_content().lstrip("/")
    lista['texto bruto']=textobruto[0].text_content()
    try:
        lista['fotos']="http://estadao.com.bt/"+urlimg[0].get("src")
    except:
        lista['fotos']=""
    lista['veiculo']= veiculo
    
    scraperwiki.sqlite.save(['url'], lista)

    
    print titulo[0].text_content()
    print olho[0].text_content()
    print data[0].text_content()
    print autor[0].text_content().lstrip(" - ")
    print caderno[0].text_content().lstrip("/")
    print textobruto[0].text_content()
    #print urlimg[0].get("src")
    print veiculo

listaMaterias()

