import scraperwiki
import urllib
from lxml.html import parse

# Blank Python



sessoes = ["sessoes-extraordinarias-anteriores", "sessoes-5a-anteriores", "sessoes-3a-anteriores"]
anos = ["2011", "2010", "2009", "2008"]

def raw_links(ano, sessao):
    base_url = "http://camarasjc.sp.tempsite.ws/clicknow/"
    count = 0
    while True:
        url = base_url + "interna.php?pag=" + sessao + "&ano=" + ano + "&ponto=" + str(count)
        html = parse(url).getroot()
        soup = html.cssselect("#sessoes")
        
        for l in soup:
            link = { 'url' : base_url + l.cssselect("a")[0].get('href'),
                     'titulo' : l.cssselect("a")[0].text.strip(),
                     'data' : l.cssselect("li")[0].text.strip(),
                     'pdf_url' : '',
                     'done' : 0 }
            scraperwiki.sqlite.save(['url'], link, table_name="rawlinks")
        count += 10

def pdf_url(url):
    html = parse(url).getroot()
    links = html.cssselect("#cont_miol a")
    for l in links:
        if '.pdf' or '.doc' in l.get('href'):
            return "http://camarasjc.sp.tempsite.ws" + l.get('href')

def rockndroll():
    data = scraperwiki.sqlite.select("* from rawlinks")
    for d in data:
        if d['done'] == 0:
            d['pdf_url'] = pdf_url(d['url'])
            if d['pdf_url']:
                d['done'] = 1
                scraperwiki.sqlite.save(['url'], d, table_name="rawlinks")

for sessao in sessoes:
    for ano in anos:
        print "Getting " + sessao + " de " + ano
        raw_links(ano, sessao)import scraperwiki
import urllib
from lxml.html import parse

# Blank Python



sessoes = ["sessoes-extraordinarias-anteriores", "sessoes-5a-anteriores", "sessoes-3a-anteriores"]
anos = ["2011", "2010", "2009", "2008"]

def raw_links(ano, sessao):
    base_url = "http://camarasjc.sp.tempsite.ws/clicknow/"
    count = 0
    while True:
        url = base_url + "interna.php?pag=" + sessao + "&ano=" + ano + "&ponto=" + str(count)
        html = parse(url).getroot()
        soup = html.cssselect("#sessoes")
        
        for l in soup:
            link = { 'url' : base_url + l.cssselect("a")[0].get('href'),
                     'titulo' : l.cssselect("a")[0].text.strip(),
                     'data' : l.cssselect("li")[0].text.strip(),
                     'pdf_url' : '',
                     'done' : 0 }
            scraperwiki.sqlite.save(['url'], link, table_name="rawlinks")
        count += 10

def pdf_url(url):
    html = parse(url).getroot()
    links = html.cssselect("#cont_miol a")
    for l in links:
        if '.pdf' or '.doc' in l.get('href'):
            return "http://camarasjc.sp.tempsite.ws" + l.get('href')

def rockndroll():
    data = scraperwiki.sqlite.select("* from rawlinks")
    for d in data:
        if d['done'] == 0:
            d['pdf_url'] = pdf_url(d['url'])
            if d['pdf_url']:
                d['done'] = 1
                scraperwiki.sqlite.save(['url'], d, table_name="rawlinks")

for sessao in sessoes:
    for ano in anos:
        print "Getting " + sessao + " de " + ano
        raw_links(ano, sessao)