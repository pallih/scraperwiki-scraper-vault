import scraperwiki
import lxml.html

ListadeNoticias = 'http://g1.globo.com/rio-de-janeiro/'
keywords = ["amor", "morte", "sexo", "crime", "zona sul"] # XXX: não usar acentos :/

def pegar_root_da_url(url):
    doc = lxml.html.parse(url)
    return doc.getroot()

def checar_palavra_chave(url, keywords, minimo=0):
    noticia = {'endereco': url, 'contagem': {}}
    root = pegar_root_da_url(url)
    resultado =  root.cssselect("#materia-letra")

    for elemento in resultado:
        for keyword in keywords:
            contagem = elemento.text_content().lower().count(keyword)
            if contagem > minimo:
                noticia['contagem'][keyword] = contagem

    if noticia['contagem'].keys():
        scraperwiki.sqlite.save(unique_keys=['endereco'], data=noticia)

def pegar_links(url):
    root = pegar_root_da_url(url)
    lista = []
    for elemento in root.cssselect('#destaques-regiao .chamadas a'):
        lista.append(elemento.get('href'))
    return lista

    
lista_de_noticias = pegar_links(ListadeNoticias)

for endereco in lista_de_noticias:
    checar_palavra_chave(endereco, keywords)import scraperwiki
import lxml.html

ListadeNoticias = 'http://g1.globo.com/rio-de-janeiro/'
keywords = ["amor", "morte", "sexo", "crime", "zona sul"] # XXX: não usar acentos :/

def pegar_root_da_url(url):
    doc = lxml.html.parse(url)
    return doc.getroot()

def checar_palavra_chave(url, keywords, minimo=0):
    noticia = {'endereco': url, 'contagem': {}}
    root = pegar_root_da_url(url)
    resultado =  root.cssselect("#materia-letra")

    for elemento in resultado:
        for keyword in keywords:
            contagem = elemento.text_content().lower().count(keyword)
            if contagem > minimo:
                noticia['contagem'][keyword] = contagem

    if noticia['contagem'].keys():
        scraperwiki.sqlite.save(unique_keys=['endereco'], data=noticia)

def pegar_links(url):
    root = pegar_root_da_url(url)
    lista = []
    for elemento in root.cssselect('#destaques-regiao .chamadas a'):
        lista.append(elemento.get('href'))
    return lista

    
lista_de_noticias = pegar_links(ListadeNoticias)

for endereco in lista_de_noticias:
    checar_palavra_chave(endereco, keywords)