import scraperwiki
from lxml.html import parse
import datetime
      
def clear(objeto, tipo="str"):
    if tipo == "[]":
        novo_objeto = []
        for i in objeto:
            if i:
                i = i.strip()
                novo_objeto.append(i)
        return novo_objeto
    elif tipo == "str":
        if objeto:
            return objeto.strip()

def crawl(data):
    url = "http://www.al.sp.gov.br/spl_consultas/consultaDetalhesProposicao.do?id=" + str(data['id']) + "&rowsPerPage=1000"
    soup = parse(url)
    data["last_scraped"] = datetime.datetime.now()
    data["documento"] = clear(soup.xpath('//font[text()=" Documento "]/following::font[@color="blue"]')[0].text_content())
    data["numero"] = clear(soup.xpath('//font[text()=" No\r\n\t\t\t\t\tLegislativo "]/following::font[@color="blue"]')[0].text_content())
    data["ementa"] = clear(soup.xpath('//font[text()="\r\n\t\t\t\t\tEmenta "]/following::font[@color="blue"]')[0].text_content())
    data["regime"] = clear(soup.xpath('//font[text()="\r\n\t\t\t\t\tRegime "]/following::font[@color="blue"]')[0].text_content())
    data["indexacao"] = ','.join(clear(soup.xpath(u'//font[text()=" Indexa\xe7\xe3o "]/following::font[@color="blue"]')[0].text_content().split(','), "[]"))
    data["autores"] = clear(soup.xpath('//font[text()=" Autor(es) "]/following::font[@color="blue"]')[0].text_content())
    data["apoiadores"] = clear(soup.xpath('//font[text()="\r\n\t\t\t\t\tApoiador(es) "]/following::font[@color="blue"]')[0].text_content())
    try:
        data["situacao_atual"] = clear(soup.xpath(u'//font[text()=" Situa\xe7\xe3o\r\n\t\t\t\t\t\tAtual "]/following::font')[0].text_content())
    except:
        data["situacao_atual"] = ''
    scraperwiki.sqlite.save(['id'], data)

def listaProposicoes(ano, tipo, armazenadas):
    url = "http://www.al.sp.gov.br/proposituras/lista.do?tipo=" + str(tipo) + "&ano=" + str(ano) + "&paginacao=5000"
    soup = parse(url)
    for link in soup.xpath('//td[@class="infL"]/a[@target="_top"]'):
        data = {}
        data["url"] = link.get('href')
        data["id"] = link.get('href').split("?id=")[1]
        data["ano"] = ano
        if data["id"] not in armazenadas:
            data = crawl(data)


    

#Inicio 1947
first_year = 1947
last_year = 2014
tipo = "1"
for ano in range(first_year, last_year):
    print "Capturando proposicoes de  " + str(ano)
    print "http://www.al.sp.gov.br/proposituras/lista.do?tipo=" + tipo + "&ano=" + str(ano) + "&paginacao=5000"
    armazenadas_dict = scraperwiki.sqlite.select("id from swdata where ano=="+str(ano))
    armazenadas = []
    for a in armazenadas_dict:
        armazenadas.append(a['id'])
    proposicoes = listaProposicoes(ano, tipo, armazenadas)
    
import scraperwiki
from lxml.html import parse
import datetime
      
def clear(objeto, tipo="str"):
    if tipo == "[]":
        novo_objeto = []
        for i in objeto:
            if i:
                i = i.strip()
                novo_objeto.append(i)
        return novo_objeto
    elif tipo == "str":
        if objeto:
            return objeto.strip()

def crawl(data):
    url = "http://www.al.sp.gov.br/spl_consultas/consultaDetalhesProposicao.do?id=" + str(data['id']) + "&rowsPerPage=1000"
    soup = parse(url)
    data["last_scraped"] = datetime.datetime.now()
    data["documento"] = clear(soup.xpath('//font[text()=" Documento "]/following::font[@color="blue"]')[0].text_content())
    data["numero"] = clear(soup.xpath('//font[text()=" No\r\n\t\t\t\t\tLegislativo "]/following::font[@color="blue"]')[0].text_content())
    data["ementa"] = clear(soup.xpath('//font[text()="\r\n\t\t\t\t\tEmenta "]/following::font[@color="blue"]')[0].text_content())
    data["regime"] = clear(soup.xpath('//font[text()="\r\n\t\t\t\t\tRegime "]/following::font[@color="blue"]')[0].text_content())
    data["indexacao"] = ','.join(clear(soup.xpath(u'//font[text()=" Indexa\xe7\xe3o "]/following::font[@color="blue"]')[0].text_content().split(','), "[]"))
    data["autores"] = clear(soup.xpath('//font[text()=" Autor(es) "]/following::font[@color="blue"]')[0].text_content())
    data["apoiadores"] = clear(soup.xpath('//font[text()="\r\n\t\t\t\t\tApoiador(es) "]/following::font[@color="blue"]')[0].text_content())
    try:
        data["situacao_atual"] = clear(soup.xpath(u'//font[text()=" Situa\xe7\xe3o\r\n\t\t\t\t\t\tAtual "]/following::font')[0].text_content())
    except:
        data["situacao_atual"] = ''
    scraperwiki.sqlite.save(['id'], data)

def listaProposicoes(ano, tipo, armazenadas):
    url = "http://www.al.sp.gov.br/proposituras/lista.do?tipo=" + str(tipo) + "&ano=" + str(ano) + "&paginacao=5000"
    soup = parse(url)
    for link in soup.xpath('//td[@class="infL"]/a[@target="_top"]'):
        data = {}
        data["url"] = link.get('href')
        data["id"] = link.get('href').split("?id=")[1]
        data["ano"] = ano
        if data["id"] not in armazenadas:
            data = crawl(data)


    

#Inicio 1947
first_year = 1947
last_year = 2014
tipo = "1"
for ano in range(first_year, last_year):
    print "Capturando proposicoes de  " + str(ano)
    print "http://www.al.sp.gov.br/proposituras/lista.do?tipo=" + tipo + "&ano=" + str(ano) + "&paginacao=5000"
    armazenadas_dict = scraperwiki.sqlite.select("id from swdata where ano=="+str(ano))
    armazenadas = []
    for a in armazenadas_dict:
        armazenadas.append(a['id'])
    proposicoes = listaProposicoes(ano, tipo, armazenadas)
    
