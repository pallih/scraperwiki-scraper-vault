import scraperwiki
from lxml.html import parse
import urllib
import time
import md5
import csv

def getPagina(soup, cnpj):
    print "Espera 3 segundos..."
    #time.sleep(3)
    lista = soup.cssselect("div .resultado")
    results = []
    for l in lista:
        data = {}
        data['link'] = "http://www.jusbrasil.com.br" + l.cssselect("h2 a")[0].get("href")
        data['cnpj'] = cnpj
        data['resumo'] = l.cssselect(".snippet")[0].text_content()
        data['titulo'] = l.cssselect("h2 a")[0].get("title")
        data['fonte'] = l.cssselect(".fonte")[0].text.split(" - ")[0]
        data['data'] = l.cssselect(".fonte")[0].text.split(" - ")[1]
        id = data['link']+data['cnpj']+data['resumo']
        data['id'] = md5.new(id.encode("utf-8")).hexdigest()
        results.append(data)
    for r in results:
        scraperwiki.sqlite.save(["id"], data)

def getMovements(cnpj):
    try:
        cnpj_l = urllib.quote_plus(cnpj)
        url = 'http://www.jusbrasil.com.br/diarios/busca?q=' + cnpj_l + '&s=diarios&o=data'
        soup = parse(url).getroot()
    except "IOError: Error reading file":
        error = { "link" : url }
        scraperwiki.sqlite.save(["link"], error, table_name="error")
    
    print "Salvando cnpj " + cnpj
    getPagina(soup, cnpj)

    #tem paginacao?
    links = soup.cssselect("#paginador .linkGreen.page")
    for l in links:
        try:
            url = 'http://www.jusbrasil.com.br/diarios/busca' + l.get("href")
            soupp = parse(url).getroot()
            getPagina(soupp, cnpj)
        except:
            error = { "link" : url }
            scraperwiki.sqlite.save(["link"], error, table_name="error")
        


def getCsv(url):
    csvfile = scraperwiki.scrape(url)
    cnpjs = csv.reader(csvfile.splitlines())
    for cnpj in cnpjs:
        mov = getMovements(cnpj[0])

url = "https://docs.google.com/spreadsheet/pub?key=0ArwVSoc8z4afdE52Q0Y5UzFpa2c5MFZ2XzRvVjhDTFE&single=true&gid=2&output=csv"    
getCsv(url)


import scraperwiki
from lxml.html import parse
import urllib
import time
import md5
import csv

def getPagina(soup, cnpj):
    print "Espera 3 segundos..."
    #time.sleep(3)
    lista = soup.cssselect("div .resultado")
    results = []
    for l in lista:
        data = {}
        data['link'] = "http://www.jusbrasil.com.br" + l.cssselect("h2 a")[0].get("href")
        data['cnpj'] = cnpj
        data['resumo'] = l.cssselect(".snippet")[0].text_content()
        data['titulo'] = l.cssselect("h2 a")[0].get("title")
        data['fonte'] = l.cssselect(".fonte")[0].text.split(" - ")[0]
        data['data'] = l.cssselect(".fonte")[0].text.split(" - ")[1]
        id = data['link']+data['cnpj']+data['resumo']
        data['id'] = md5.new(id.encode("utf-8")).hexdigest()
        results.append(data)
    for r in results:
        scraperwiki.sqlite.save(["id"], data)

def getMovements(cnpj):
    try:
        cnpj_l = urllib.quote_plus(cnpj)
        url = 'http://www.jusbrasil.com.br/diarios/busca?q=' + cnpj_l + '&s=diarios&o=data'
        soup = parse(url).getroot()
    except "IOError: Error reading file":
        error = { "link" : url }
        scraperwiki.sqlite.save(["link"], error, table_name="error")
    
    print "Salvando cnpj " + cnpj
    getPagina(soup, cnpj)

    #tem paginacao?
    links = soup.cssselect("#paginador .linkGreen.page")
    for l in links:
        try:
            url = 'http://www.jusbrasil.com.br/diarios/busca' + l.get("href")
            soupp = parse(url).getroot()
            getPagina(soupp, cnpj)
        except:
            error = { "link" : url }
            scraperwiki.sqlite.save(["link"], error, table_name="error")
        


def getCsv(url):
    csvfile = scraperwiki.scrape(url)
    cnpjs = csv.reader(csvfile.splitlines())
    for cnpj in cnpjs:
        mov = getMovements(cnpj[0])

url = "https://docs.google.com/spreadsheet/pub?key=0ArwVSoc8z4afdE52Q0Y5UzFpa2c5MFZ2XzRvVjhDTFE&single=true&gid=2&output=csv"    
getCsv(url)


