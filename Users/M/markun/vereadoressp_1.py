from lxml.html import parse
import scraperwiki
import re

def listaVereadores():
    html = parse("http://www1.camara.sp.gov.br/vereadores_joomla.asp").getroot()
    
    links = html.cssselect("a")
    for link in links:
        vereador(link.get("href"))

def vereador(vereadordavez):

    html = parse("http://www1.camara.sp.gov.br/"+vereadordavez).getroot()
    
    nome = html.cssselect("#nome_vereador")
    foto = html.cssselect("#Table2 img")
    
    lista = {}
    
    lista['nome']=nome[0].text_content()
    lista['foto']="http://www1.camara.sp.gov.br/"+foto[0].get("src")
    lista['id'] = re.search('.*vereador=([0-9]*)', vereadordavez).groups()[0]
    
    scraperwiki.sqlite.save(['nome'], lista)
    
    print nome[0].text_content()
    print foto[0].get("src")

listaVereadores()

from lxml.html import parse
import scraperwiki
import re

def listaVereadores():
    html = parse("http://www1.camara.sp.gov.br/vereadores_joomla.asp").getroot()
    
    links = html.cssselect("a")
    for link in links:
        vereador(link.get("href"))

def vereador(vereadordavez):

    html = parse("http://www1.camara.sp.gov.br/"+vereadordavez).getroot()
    
    nome = html.cssselect("#nome_vereador")
    foto = html.cssselect("#Table2 img")
    
    lista = {}
    
    lista['nome']=nome[0].text_content()
    lista['foto']="http://www1.camara.sp.gov.br/"+foto[0].get("src")
    lista['id'] = re.search('.*vereador=([0-9]*)', vereadordavez).groups()[0]
    
    scraperwiki.sqlite.save(['nome'], lista)
    
    print nome[0].text_content()
    print foto[0].get("src")

listaVereadores()

