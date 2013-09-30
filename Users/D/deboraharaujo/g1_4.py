import scraperwiki      # import, def, if, for, run são comandos para a máquina - pegar tutorial da linguagem Python
import lxml.html

ListadeNoticias = 'http://g1.globo.com/rio-de-janeiro/'
keywords = ["amor", "morte", "sexo", "crime", "zona sul"] # XXX: não usar acentos :/

def pegar_root_da_url(url):
    doc = lxml.html.parse(url)
    return doc.getroot()   #  getroot é tirar da "matrioska" maior

def checar_palavra_chave(url, keywords, minimo=0):
    noticia = {'endereco': url, 'contagem': {}}  # {} é dicionário
    root = pegar_root_da_url(url)
    resultado =  root.cssselect("#materia-letra")

    for elemento in resultado:
        for keyword in keywords:
            contagem = elemento.text_content().lower().count(keyword)
            if contagem > minimo:
                noticia['contagem'][keyword] = contagem   #  contagem de cada palavra-chave em cada notícia da ListadeNotícias (página escolhida)

    if noticia['contagem'].keys():
        scraperwiki.sqlite.save(unique_keys=['endereco'], data=noticia)

def pegar_links(url):
    root = pegar_root_da_url(url)
    lista = []
    for elemento in root.cssselect('#destaques-regiao .chamadas a'):
        lista.append(elemento.get('href'))
    return lista

    
lista_de_noticias = pegar_links(ListadeNoticias) # comando para o scraper pegar não apenas o número de vezes de cada palavra, mas também o link de cada matéria

for endereco in lista_de_noticias:
    checar_palavra_chave(endereco, keywords) #  organizar a tabela com as palavras de cada matéria aparecendo organizadas sem o link precisar aparecer mais de 1 vezimport scraperwiki      # import, def, if, for, run são comandos para a máquina - pegar tutorial da linguagem Python
import lxml.html

ListadeNoticias = 'http://g1.globo.com/rio-de-janeiro/'
keywords = ["amor", "morte", "sexo", "crime", "zona sul"] # XXX: não usar acentos :/

def pegar_root_da_url(url):
    doc = lxml.html.parse(url)
    return doc.getroot()   #  getroot é tirar da "matrioska" maior

def checar_palavra_chave(url, keywords, minimo=0):
    noticia = {'endereco': url, 'contagem': {}}  # {} é dicionário
    root = pegar_root_da_url(url)
    resultado =  root.cssselect("#materia-letra")

    for elemento in resultado:
        for keyword in keywords:
            contagem = elemento.text_content().lower().count(keyword)
            if contagem > minimo:
                noticia['contagem'][keyword] = contagem   #  contagem de cada palavra-chave em cada notícia da ListadeNotícias (página escolhida)

    if noticia['contagem'].keys():
        scraperwiki.sqlite.save(unique_keys=['endereco'], data=noticia)

def pegar_links(url):
    root = pegar_root_da_url(url)
    lista = []
    for elemento in root.cssselect('#destaques-regiao .chamadas a'):
        lista.append(elemento.get('href'))
    return lista

    
lista_de_noticias = pegar_links(ListadeNoticias) # comando para o scraper pegar não apenas o número de vezes de cada palavra, mas também o link de cada matéria

for endereco in lista_de_noticias:
    checar_palavra_chave(endereco, keywords) #  organizar a tabela com as palavras de cada matéria aparecendo organizadas sem o link precisar aparecer mais de 1 vez