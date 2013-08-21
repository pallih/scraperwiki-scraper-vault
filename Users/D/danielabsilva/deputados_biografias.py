import scraperwiki
import urllib
from lxml.html.soupparser import fromstring

def url_deputado():
    anos = range(41,42)
    for ano in anos:
        url_busca = "http://www.camara.gov.br/internet/deputado/DepNovos_Lista.asp?Legislatura=" +str(ano) + "&Partido=QQ&SX=QQ&Todos=None&UF=QQ&condic=QQ&forma=lista&nome=&ordem=nome&origem="
        print url_busca
        url_busca = urllib.urlopen(url_busca)
        html_busca = fromstring(url_busca)
        urls_deputados = html_busca.cssselect("#content a")
        for url in urls_deputados:
            dados(url.get("href"))

def dados(url_deputado):
    url_deputado = urllib
    html_deputado = fromstring(url_deputado)
    img = html_deputado.cssselect("*bioFoto")
    print img

url_deputado()
        
        
    