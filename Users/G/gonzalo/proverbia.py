#imports
import scraperwiki
import urlparse
import lxml.html           
#comentario
def parse_page(link, parse_pagination):
    starting_url = urlparse.urljoin(base_url, link)
    html = scraperwiki.scrape(starting_url)
    root = lxml.html.fromstring(html)
    autor = root.cssselect("h1")

    record = {}
    record['autor'] = autor[0].text
    #print autor[0].text

    for q in root.cssselect("div .q"):
        frase = q.cssselect("div .Frase blockquote")
        categoria = q.cssselect("div .Frase span.social_links a")
        record['categoria'] = categoria[0].text.replace("Frases Cortas de ", "")
        record['frase'] =  frase[0].text
        scraperwiki.sqlite.save(["frase"], record)
    
    if(parse_pagination):
        for pagination in root.cssselect("div .pagination ul li:not(.active) a"):
            if pagination.text.isdigit():
                parse_page(pagination.attrib.get("href"), False)

def parse_links(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    parse_page(root)

    lista_paginas = root.cssselect("div #paginas")
    try:
        for element, attribute, link, pos in lista_paginas [0] .iterlinks():
            html_link = scraperwiki.scrape(urlparse.urljoin(base_url, element.attrib.get('href')))
            root_link = lxml.html.fromstring(html_link)
            parse_page(root_link)
    except IndexError:
        print "Error en el link" + url

def parse_letras():
    for letra in range (122, 123):
        print "Procesando la letra: " + str(unichr(letra))
        starting_url = urlparse.urljoin(base_url, "frases-cortas-por-autores-"+str(unichr(letra))+".html")
        html = scraperwiki.scrape(starting_url)
        root = lxml.html.fromstring(html)
        for panel in root.cssselect("div .panel-autores"):
            for link in panel.cssselect("ul li a"):
                parse_page(link.attrib.get("href"), True)

base_url = "http://frasescortas.org/"
parse_letras()
#imports
import scraperwiki
import urlparse
import lxml.html           
#comentario
def parse_page(link, parse_pagination):
    starting_url = urlparse.urljoin(base_url, link)
    html = scraperwiki.scrape(starting_url)
    root = lxml.html.fromstring(html)
    autor = root.cssselect("h1")

    record = {}
    record['autor'] = autor[0].text
    #print autor[0].text

    for q in root.cssselect("div .q"):
        frase = q.cssselect("div .Frase blockquote")
        categoria = q.cssselect("div .Frase span.social_links a")
        record['categoria'] = categoria[0].text.replace("Frases Cortas de ", "")
        record['frase'] =  frase[0].text
        scraperwiki.sqlite.save(["frase"], record)
    
    if(parse_pagination):
        for pagination in root.cssselect("div .pagination ul li:not(.active) a"):
            if pagination.text.isdigit():
                parse_page(pagination.attrib.get("href"), False)

def parse_links(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    parse_page(root)

    lista_paginas = root.cssselect("div #paginas")
    try:
        for element, attribute, link, pos in lista_paginas [0] .iterlinks():
            html_link = scraperwiki.scrape(urlparse.urljoin(base_url, element.attrib.get('href')))
            root_link = lxml.html.fromstring(html_link)
            parse_page(root_link)
    except IndexError:
        print "Error en el link" + url

def parse_letras():
    for letra in range (122, 123):
        print "Procesando la letra: " + str(unichr(letra))
        starting_url = urlparse.urljoin(base_url, "frases-cortas-por-autores-"+str(unichr(letra))+".html")
        html = scraperwiki.scrape(starting_url)
        root = lxml.html.fromstring(html)
        for panel in root.cssselect("div .panel-autores"):
            for link in panel.cssselect("ul li a"):
                parse_page(link.attrib.get("href"), True)

base_url = "http://frasescortas.org/"
parse_letras()
