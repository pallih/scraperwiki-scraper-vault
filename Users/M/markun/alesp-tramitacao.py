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

def scrape(id):
    url = "http://www.al.sp.gov.br/spl_consultas/consultaDetalhesProposicao.do?id=" + str(id) + "&rowsPerPage=1000"
    soup = parse(url)
    data = {}
    data["last_scraped"] = datetime.datetime.now()
    data["id"] = id
    data["documento"] = clear(soup.xpath('//font[text()=" Documento "]/following::font[@color="blue"]')[0].text_content())
    data["numero"] = clear(soup.xpath('//font[text()=" No\r\n\t\t\t\t\tLegislativo "]/following::font[@color="blue"]')[0].text_content())
    data["ementa"] = clear(soup.xpath('//font[text()="\r\n\t\t\t\t\tEmenta "]/following::font[@color="blue"]')[0].text_content())
    data["regime"] = clear(soup.xpath('//font[text()="\r\n\t\t\t\t\tRegime "]/following::font[@color="blue"]')[0].text_content())
    data["indexacao"] = clear(soup.xpath(u'//font[text()=" Indexa\xe7\xe3o "]/following::font[@color="blue"]')[0].text_content().split(','), "[]")
    data["autores"] = clear(soup.xpath('//font[text()=" Autor(es) "]/following::font[@color="blue"]')[0].text_content())
    data["apoiadores"] = clear(soup.xpath('//font[text()="\r\n\t\t\t\t\tApoiador(es) "]/following::font[@color="blue"]')[0].text_content())
    data["situacao_atual"] = clear(soup.xpath(u'//font[text()=" Situa\xe7\xe3o\r\n\t\t\t\t\t\tAtual "]/following::font')[0].text_content())
    
    data["pareceres"] = []
    pareceres = soup.xpath(u'//font/b[text()="Pareceres"]/../../../../tr[@valign="TOP"]')
    for p in pareceres:
        parecer = {}
        parecer["ordem"] = clear(p.xpath("./td[1]")[0].text_content(), 'str')
        parecer["numero"] = clear(p.xpath("./td[2]")[0].text_content(), 'str')
        parecer["resultado"] = clear(p.xpath("./td[3]")[0].text_content(), 'str')
        parecer["resumo"] = clear(p.xpath("./td[4]")[0].text_content(), 'str')
        parecer["relator"] = clear(p.xpath("./td[5]")[0].text_content(), 'str')
        parecer["comissao"] = clear(p.xpath("./td[6]")[0].text_content(), 'str')
        if p.xpath("./td[7]/a"):
            parecer["link"] = clear(p.xpath("./td[7]/a")[0].get("href"), 'str')
        elif p.xpath("./td[7]/img"):
            parecer["link"] = ''
        data["pareceres"].append(parecer)
    
    data["documentos"] = []
    documentos = soup.xpath(u'//font/b[text()="Documentos Acess\xf3rios\r\n\t\t\t\t"]/../../../../tr[@valign="TOP"]') 
    for d in documentos:
        documento = {}
        documento["ordem"] = clear(d.xpath("./td[1]")[0].text_content(), 'str')
        documento["publicacao"] = clear(d.xpath("./td[2]")[0].text_content(), 'str')
        documento["natureza"] = clear(d.xpath("./td[3]")[0].text_content(), 'str')
        documento["no_legislativo"] = clear(d.xpath("./td[4]")[0].text_content(), 'str')
        documento["ementa"] = clear(d.xpath("./td[5]")[0].text_content(), 'str')
        documento["autor"] = clear(d.xpath("./td[6]")[0].text_content(), 'str')
        if d.xpath("./td[7]/a"):
            documento["link"] = clear(d.xpath("./td[7]/a")[0].get("href"), 'str')
        elif d.xpath("./td[7]/img"):
            documento["link"] = ''
        data["documentos"].append(documento)
    data["tramitacoes"] = getTramitacao(id)
    scraperwiki.sqlite.save(['id'], data)
    return data

def getTramitacao(id):
    url = "http://www.al.sp.gov.br/spl_consultas/consultaDetalhesProposicao.do?id=" + str(id) + "&rowsPerPage=1000&act=detalheAndamento"
    soup = parse(url)   
    tramitacoes = []
    tramitacao = {}
    andamentos = soup.xpath(u'//font/b[text()="Andamento"]/../../../../tr[@valign="TOP"]')
    for a in andamentos:
        tramitacao["data"] = clear(a.xpath("./td[1]")[0].text_content(), 'str')
        tramitacao["descricao"] = clear(a.xpath("./td[2]")[0].text_content(), 'str')
        tramitacoes.append(tramitacao)
    return tramitacoes


def listaProposicoes(ano, tipo):
    url = "http://www.al.sp.gov.br/proposituras/lista.do?tipo=" + str(tipo) + "&ano=" + str(ano) + "&paginacao=5000"
    soup = parse(url)
    for link in soup.xpath('//td[@class="infL"]/a[@target="_top"]'):
        data = {}
        data["url"] = link.get('href')
        data["id"] = link.get('href').split("?id=")[1]
        scraperwiki.sqlite.save(['id'], data)

def rockandroll():
    lista = scraperwiki.sqlite.select("id from swdata where last_scraped IS Null")
    for item in lista:
        data = scrape(item['id'])

listaProposicoes(2011, 1)
rockandroll()import scraperwiki
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

def scrape(id):
    url = "http://www.al.sp.gov.br/spl_consultas/consultaDetalhesProposicao.do?id=" + str(id) + "&rowsPerPage=1000"
    soup = parse(url)
    data = {}
    data["last_scraped"] = datetime.datetime.now()
    data["id"] = id
    data["documento"] = clear(soup.xpath('//font[text()=" Documento "]/following::font[@color="blue"]')[0].text_content())
    data["numero"] = clear(soup.xpath('//font[text()=" No\r\n\t\t\t\t\tLegislativo "]/following::font[@color="blue"]')[0].text_content())
    data["ementa"] = clear(soup.xpath('//font[text()="\r\n\t\t\t\t\tEmenta "]/following::font[@color="blue"]')[0].text_content())
    data["regime"] = clear(soup.xpath('//font[text()="\r\n\t\t\t\t\tRegime "]/following::font[@color="blue"]')[0].text_content())
    data["indexacao"] = clear(soup.xpath(u'//font[text()=" Indexa\xe7\xe3o "]/following::font[@color="blue"]')[0].text_content().split(','), "[]")
    data["autores"] = clear(soup.xpath('//font[text()=" Autor(es) "]/following::font[@color="blue"]')[0].text_content())
    data["apoiadores"] = clear(soup.xpath('//font[text()="\r\n\t\t\t\t\tApoiador(es) "]/following::font[@color="blue"]')[0].text_content())
    data["situacao_atual"] = clear(soup.xpath(u'//font[text()=" Situa\xe7\xe3o\r\n\t\t\t\t\t\tAtual "]/following::font')[0].text_content())
    
    data["pareceres"] = []
    pareceres = soup.xpath(u'//font/b[text()="Pareceres"]/../../../../tr[@valign="TOP"]')
    for p in pareceres:
        parecer = {}
        parecer["ordem"] = clear(p.xpath("./td[1]")[0].text_content(), 'str')
        parecer["numero"] = clear(p.xpath("./td[2]")[0].text_content(), 'str')
        parecer["resultado"] = clear(p.xpath("./td[3]")[0].text_content(), 'str')
        parecer["resumo"] = clear(p.xpath("./td[4]")[0].text_content(), 'str')
        parecer["relator"] = clear(p.xpath("./td[5]")[0].text_content(), 'str')
        parecer["comissao"] = clear(p.xpath("./td[6]")[0].text_content(), 'str')
        if p.xpath("./td[7]/a"):
            parecer["link"] = clear(p.xpath("./td[7]/a")[0].get("href"), 'str')
        elif p.xpath("./td[7]/img"):
            parecer["link"] = ''
        data["pareceres"].append(parecer)
    
    data["documentos"] = []
    documentos = soup.xpath(u'//font/b[text()="Documentos Acess\xf3rios\r\n\t\t\t\t"]/../../../../tr[@valign="TOP"]') 
    for d in documentos:
        documento = {}
        documento["ordem"] = clear(d.xpath("./td[1]")[0].text_content(), 'str')
        documento["publicacao"] = clear(d.xpath("./td[2]")[0].text_content(), 'str')
        documento["natureza"] = clear(d.xpath("./td[3]")[0].text_content(), 'str')
        documento["no_legislativo"] = clear(d.xpath("./td[4]")[0].text_content(), 'str')
        documento["ementa"] = clear(d.xpath("./td[5]")[0].text_content(), 'str')
        documento["autor"] = clear(d.xpath("./td[6]")[0].text_content(), 'str')
        if d.xpath("./td[7]/a"):
            documento["link"] = clear(d.xpath("./td[7]/a")[0].get("href"), 'str')
        elif d.xpath("./td[7]/img"):
            documento["link"] = ''
        data["documentos"].append(documento)
    data["tramitacoes"] = getTramitacao(id)
    scraperwiki.sqlite.save(['id'], data)
    return data

def getTramitacao(id):
    url = "http://www.al.sp.gov.br/spl_consultas/consultaDetalhesProposicao.do?id=" + str(id) + "&rowsPerPage=1000&act=detalheAndamento"
    soup = parse(url)   
    tramitacoes = []
    tramitacao = {}
    andamentos = soup.xpath(u'//font/b[text()="Andamento"]/../../../../tr[@valign="TOP"]')
    for a in andamentos:
        tramitacao["data"] = clear(a.xpath("./td[1]")[0].text_content(), 'str')
        tramitacao["descricao"] = clear(a.xpath("./td[2]")[0].text_content(), 'str')
        tramitacoes.append(tramitacao)
    return tramitacoes


def listaProposicoes(ano, tipo):
    url = "http://www.al.sp.gov.br/proposituras/lista.do?tipo=" + str(tipo) + "&ano=" + str(ano) + "&paginacao=5000"
    soup = parse(url)
    for link in soup.xpath('//td[@class="infL"]/a[@target="_top"]'):
        data = {}
        data["url"] = link.get('href')
        data["id"] = link.get('href').split("?id=")[1]
        scraperwiki.sqlite.save(['id'], data)

def rockandroll():
    lista = scraperwiki.sqlite.select("id from swdata where last_scraped IS Null")
    for item in lista:
        data = scrape(item['id'])

listaProposicoes(2011, 1)
rockandroll()