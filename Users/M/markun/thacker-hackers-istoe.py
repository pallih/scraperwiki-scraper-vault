import scraperwiki
import urllib
from lxml.html import parse, document_fromstring
from BeautifulSoup import UnicodeDammit
import re

def decode_html(html_string):
    converted = UnicodeDammit(html_string, isHTML=True)
    if not converted.unicode:
        raise UnicodeDecodeError(
            ', '.join(converted.triedEncodings))
    return converted.unicode

def listaLinks():
    baseurl ="http://www.istoe.com.br/busca/paginar/"
    termo = 'hacker'
    options = "/?filter=N"
    last_page = 6
    data = []

    for paginar in range(1,last_page+1):
        url = baseurl + str(paginar) + "/" + termo + options
        
        doc = parse(url).getroot()
        
        links = doc.cssselect("#listaNoticias dl dt a")
        

        for l in links:
            link = {}
            link['title'] = l.text_content()
            link['href'] = "http://www.istoe.com.br"+l.get('href')
            scraperwiki.sqlite.save(['href'], link, table_name="links")
            data.append(link)

    return data

def montaLista():
    links = scraperwiki.sqlite.select('href from links')
    data = []
    for l in links:
        data.append(l['href'])
    return data

def scrapePaginas():
    urls = montaLista()
    for url in urls:
        tag_soup = urllib.urlopen(url).read()
        doc = document_fromstring(decode_html(tag_soup))
     
        data = {}
        data['titulo'] = doc.cssselect('#materiaTopo h2')[0].text_content().strip()
        data['olho'] = ''
        data['autor'] = doc.cssselect('#materiaTopo span')[0].text_content().strip()
        data['url'] = url
        data['texto_bruto'] = doc.cssselect('#divCompleta')[0].text_content().strip()
        dia = doc.cssselect('#info .subInfo')[0].text_content()
        dia = re.search("([0-9]{2}\.[A-z]{3}\.[0-9]{2} - [0-9]{2}:[0-9]{2})", dia).groups()[0]
        data['data'] = dia
        data['veiculo'] = 'ISTOE'
        
        if doc.cssselect(".tituloVermelho"):
            data['caderno'] = doc.cssselect(".tituloVermelho")[0].text_content().strip()
        else:
            data['caderno'] = '-'
        data['fotos'] = []
        scraperwiki.sqlite.save(['url'], data, table_name='materias')
        print data

scrapePaginas()import scraperwiki
import urllib
from lxml.html import parse, document_fromstring
from BeautifulSoup import UnicodeDammit
import re

def decode_html(html_string):
    converted = UnicodeDammit(html_string, isHTML=True)
    if not converted.unicode:
        raise UnicodeDecodeError(
            ', '.join(converted.triedEncodings))
    return converted.unicode

def listaLinks():
    baseurl ="http://www.istoe.com.br/busca/paginar/"
    termo = 'hacker'
    options = "/?filter=N"
    last_page = 6
    data = []

    for paginar in range(1,last_page+1):
        url = baseurl + str(paginar) + "/" + termo + options
        
        doc = parse(url).getroot()
        
        links = doc.cssselect("#listaNoticias dl dt a")
        

        for l in links:
            link = {}
            link['title'] = l.text_content()
            link['href'] = "http://www.istoe.com.br"+l.get('href')
            scraperwiki.sqlite.save(['href'], link, table_name="links")
            data.append(link)

    return data

def montaLista():
    links = scraperwiki.sqlite.select('href from links')
    data = []
    for l in links:
        data.append(l['href'])
    return data

def scrapePaginas():
    urls = montaLista()
    for url in urls:
        tag_soup = urllib.urlopen(url).read()
        doc = document_fromstring(decode_html(tag_soup))
     
        data = {}
        data['titulo'] = doc.cssselect('#materiaTopo h2')[0].text_content().strip()
        data['olho'] = ''
        data['autor'] = doc.cssselect('#materiaTopo span')[0].text_content().strip()
        data['url'] = url
        data['texto_bruto'] = doc.cssselect('#divCompleta')[0].text_content().strip()
        dia = doc.cssselect('#info .subInfo')[0].text_content()
        dia = re.search("([0-9]{2}\.[A-z]{3}\.[0-9]{2} - [0-9]{2}:[0-9]{2})", dia).groups()[0]
        data['data'] = dia
        data['veiculo'] = 'ISTOE'
        
        if doc.cssselect(".tituloVermelho"):
            data['caderno'] = doc.cssselect(".tituloVermelho")[0].text_content().strip()
        else:
            data['caderno'] = '-'
        data['fotos'] = []
        scraperwiki.sqlite.save(['url'], data, table_name='materias')
        print data

scrapePaginas()