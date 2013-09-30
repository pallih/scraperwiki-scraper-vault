import urllib
import scraperwiki
import urllib2
import codecs
from lxml.html import parse, document_fromstring, etree
from BeautifulSoup import UnicodeDammit

def decode_html(html_string):
    converted = UnicodeDammit(html_string, isHTML=True)
    if not converted.unicode:
        raise UnicodeDecodeError(
            ', '.join(converted.triedEncodings))
    return converted.unicode

def scrape(url):
    headers = { 'User-Agent' : 'Mozilla/5.0' }
    req = urllib2.Request(url, None, headers)
    html = urllib2.urlopen(req).read()
    return html

def listaLinks():
    baseurl ="http://www.google.com/custom?num=100&hl=pt-BR&client=pub-6775984018762070&cof=FORID:11%3BAH:left%3BS:http://revistaepoca.globo.com/%3BCX:Revista%2520Epoca%3BL:http://revistaepoca.globo.com/Portal/editoraglobo/estaticos/revepoca/imgv3/logo_revista.gif%3BLH:100%3BLP:1%3BVLC:%23551a8b%3BDIV:%23cccccc%3B&rurl=http://revistaepoca.globo.com/Revista/Epoca/0,,RS0-15210,00.html%3Fcx%3D012582155851081905792%253A8a57uo50lru%26cof%3DFORID%253A11%26q%3Dhacker%26sa.x%3D41%26sa.y%3D7%26google_rsg%3D__9xGX2I38T15Pq5WTOlDUD887r74%3D&cx=012582155851081905792:8a57uo50lru&ad=w9&adkw=AELymgUxg01ARUw0HoEds-qfPmyRTJ7TCXBkzqRu-MrBqAkOUEL09nzyebnuXGZ9fo6aXk6Ev4LPGbdK_uqI1gBBjHSGrgbAlOFqGPn5OQjWdCom31bB33g&boostcse=0&ei=nosbTqa5BbOCsgLN59GwCA"
    
    options = "&q=hacker&start=0&sa=N&as_qdr=m6"
    
    html = scrape(baseurl + options)
    
    doc = parse(baseurl+options).getroot()
    
    links = doc.cssselect(".r a")
    
    data = []
    for l in links:
        link = {}
        link['title'] = l.text_content()
        link['href'] = l.get('href')
        scraperwiki.sqlite.save(['href'], link, table_name="links")
        data.append(link)
    return data

def montaLista():
    links = scraperwiki.sqlite.select('href from links')
    data = []
    for l in links:
        if l['href'].find('EMI') > 0: #ignora coisas que nao sejam noticias
            data.append(l['href'])
    return data

urls = montaLista()
for url in urls:
    tag_soup = urllib.urlopen(url.replace('EMI','ERT')).read()
    doc = document_fromstring(decode_html(tag_soup))
   
    lista_fotos = doc.cssselect('.foto')
    fotos = []
    base_foto = 'http://revistaepoca.globo.com'
    for f in lista_fotos:
        fotos.append(base_foto + f.get('src'))
    
    data = {}
    data['titulo'] = doc.cssselect('.materiaTitulo')[0].text_content().strip()
    data['olho'] = doc.cssselect('.materiaSubtitulo')[0].text_content().strip()
    data['autor'] = doc.cssselect('.materiaCredito')[0].text_content().strip()
    data['url'] = url
    data['texto_bruto'] = doc.cssselect('#materiaContainer')[0].text_content().strip()
    data['data'] = doc.cssselect('.materiaData')[0].text_content()
    data['veiculo'] = 'EPOCA'
    data['caderno'] = doc.xpath("//meta[@name='editoria']")[0].get('content').strip()
    data['fotos'] = fotos
    scraperwiki.sqlite.save(['url'], data, table_name='materias')
    print dataimport urllib
import scraperwiki
import urllib2
import codecs
from lxml.html import parse, document_fromstring, etree
from BeautifulSoup import UnicodeDammit

def decode_html(html_string):
    converted = UnicodeDammit(html_string, isHTML=True)
    if not converted.unicode:
        raise UnicodeDecodeError(
            ', '.join(converted.triedEncodings))
    return converted.unicode

def scrape(url):
    headers = { 'User-Agent' : 'Mozilla/5.0' }
    req = urllib2.Request(url, None, headers)
    html = urllib2.urlopen(req).read()
    return html

def listaLinks():
    baseurl ="http://www.google.com/custom?num=100&hl=pt-BR&client=pub-6775984018762070&cof=FORID:11%3BAH:left%3BS:http://revistaepoca.globo.com/%3BCX:Revista%2520Epoca%3BL:http://revistaepoca.globo.com/Portal/editoraglobo/estaticos/revepoca/imgv3/logo_revista.gif%3BLH:100%3BLP:1%3BVLC:%23551a8b%3BDIV:%23cccccc%3B&rurl=http://revistaepoca.globo.com/Revista/Epoca/0,,RS0-15210,00.html%3Fcx%3D012582155851081905792%253A8a57uo50lru%26cof%3DFORID%253A11%26q%3Dhacker%26sa.x%3D41%26sa.y%3D7%26google_rsg%3D__9xGX2I38T15Pq5WTOlDUD887r74%3D&cx=012582155851081905792:8a57uo50lru&ad=w9&adkw=AELymgUxg01ARUw0HoEds-qfPmyRTJ7TCXBkzqRu-MrBqAkOUEL09nzyebnuXGZ9fo6aXk6Ev4LPGbdK_uqI1gBBjHSGrgbAlOFqGPn5OQjWdCom31bB33g&boostcse=0&ei=nosbTqa5BbOCsgLN59GwCA"
    
    options = "&q=hacker&start=0&sa=N&as_qdr=m6"
    
    html = scrape(baseurl + options)
    
    doc = parse(baseurl+options).getroot()
    
    links = doc.cssselect(".r a")
    
    data = []
    for l in links:
        link = {}
        link['title'] = l.text_content()
        link['href'] = l.get('href')
        scraperwiki.sqlite.save(['href'], link, table_name="links")
        data.append(link)
    return data

def montaLista():
    links = scraperwiki.sqlite.select('href from links')
    data = []
    for l in links:
        if l['href'].find('EMI') > 0: #ignora coisas que nao sejam noticias
            data.append(l['href'])
    return data

urls = montaLista()
for url in urls:
    tag_soup = urllib.urlopen(url.replace('EMI','ERT')).read()
    doc = document_fromstring(decode_html(tag_soup))
   
    lista_fotos = doc.cssselect('.foto')
    fotos = []
    base_foto = 'http://revistaepoca.globo.com'
    for f in lista_fotos:
        fotos.append(base_foto + f.get('src'))
    
    data = {}
    data['titulo'] = doc.cssselect('.materiaTitulo')[0].text_content().strip()
    data['olho'] = doc.cssselect('.materiaSubtitulo')[0].text_content().strip()
    data['autor'] = doc.cssselect('.materiaCredito')[0].text_content().strip()
    data['url'] = url
    data['texto_bruto'] = doc.cssselect('#materiaContainer')[0].text_content().strip()
    data['data'] = doc.cssselect('.materiaData')[0].text_content()
    data['veiculo'] = 'EPOCA'
    data['caderno'] = doc.xpath("//meta[@name='editoria']")[0].get('content').strip()
    data['fotos'] = fotos
    scraperwiki.sqlite.save(['url'], data, table_name='materias')
    print data