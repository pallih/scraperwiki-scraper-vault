import scraperwiki
from lxml.html import parse
import datetime

def dataNorma(proposicao_id):
    print "Data norma... " + proposicao_id
    url = "http://www.al.sp.gov.br/spl_consultas/consultaDetalhesProposicao.do?id=" + str(proposicao_id)
    print url
    soup = parse(url).getroot()
    pl_url = "http://www.al.sp.gov.br/legislacao/norma.do?" + soup.xpath("//font[text()=' Norma ']/following::a")[0].get('href').split("?")[1]
    print pl_url
    soup = parse(pl_url).getroot()
    data_norma = soup.xpath('//td/p')[0].text_content().split("de")[1].strip()
    return data_norma

def scrape(currentPage=0):
    lista_dict = scraperwiki.sqlite.select("id from swdata")
    lista = []
    for l in lista_dict:
        lista.append(l['id'])

    print "Loading url... "
    base_url = "http://www.al.sp.gov.br/spl_consultas/consultaProposicoesAction.do?"
    args = "direction=acima&lastPage=0&currentPage=" + str(currentPage)+ "&act=detalhe&idDocumento=&rowsPerPage=1000&currentPageDetalhe=1&tpDocumento=&method=search&text=&natureId=&legislativeNumber=&legislativeYear=&natureIdMainDoc=&anoDeExercicio=&legislativeNumberMainDoc=&legislativeYearMainDoc=&strInitialDate=&strFinalDate=&author=&supporter=&politicalPartyId=&tipoDocumento=&stageId=Transformado+em+Norma&strVotedInitialDate=&strVotedFinalDate=&approved=&rejected=&advancedSearch=#inicio"
    soup = parse(base_url+args).getroot()
    lastPage = soup.xpath("//input[@name='lastPage']")[0].get("value")
    print "Scraping... " + str(currentPage) + " of " + str(lastPage)
    for l in soup.cssselect("tr")[4:-25]:
        data = {}
        data["data"] = l.cssselect("td")[0].text_content().strip()
        data["ementa"] = l.cssselect("td font a")[0].text_content().strip()
        data["projeto"] = l.cssselect("td font b")[0].text_content().strip() 
        data["autor"] = l.cssselect("td")[2].text_content().strip()
        data["etapa"] = l.cssselect("td")[3].text_content().strip()
        data["url"] = l.cssselect("td font a")[0].get("href")
        data["id"] = data["url"].split("id=")[1]
        if data["id"] not in lista:
            try:
                data["norma"] = dataNorma(data["id"])
                dataIni =  datetime.datetime.strptime(data['data'],"%d/%m/%Y")
                dataFim =  datetime.datetime.strptime(data['norma'],"%d/%m/%Y")
                tempo =  dataFim - dataIni
                data['tempo'] = tempo.days
                scraperwiki.sqlite.save(["id"],data)
            except:
                print "error on " + data["url"]
    if currentPage > int(lastPage):
        pass
    else:
        scrape(int(currentPage)+1)


scrape()import scraperwiki
from lxml.html import parse
import datetime

def dataNorma(proposicao_id):
    print "Data norma... " + proposicao_id
    url = "http://www.al.sp.gov.br/spl_consultas/consultaDetalhesProposicao.do?id=" + str(proposicao_id)
    print url
    soup = parse(url).getroot()
    pl_url = "http://www.al.sp.gov.br/legislacao/norma.do?" + soup.xpath("//font[text()=' Norma ']/following::a")[0].get('href').split("?")[1]
    print pl_url
    soup = parse(pl_url).getroot()
    data_norma = soup.xpath('//td/p')[0].text_content().split("de")[1].strip()
    return data_norma

def scrape(currentPage=0):
    lista_dict = scraperwiki.sqlite.select("id from swdata")
    lista = []
    for l in lista_dict:
        lista.append(l['id'])

    print "Loading url... "
    base_url = "http://www.al.sp.gov.br/spl_consultas/consultaProposicoesAction.do?"
    args = "direction=acima&lastPage=0&currentPage=" + str(currentPage)+ "&act=detalhe&idDocumento=&rowsPerPage=1000&currentPageDetalhe=1&tpDocumento=&method=search&text=&natureId=&legislativeNumber=&legislativeYear=&natureIdMainDoc=&anoDeExercicio=&legislativeNumberMainDoc=&legislativeYearMainDoc=&strInitialDate=&strFinalDate=&author=&supporter=&politicalPartyId=&tipoDocumento=&stageId=Transformado+em+Norma&strVotedInitialDate=&strVotedFinalDate=&approved=&rejected=&advancedSearch=#inicio"
    soup = parse(base_url+args).getroot()
    lastPage = soup.xpath("//input[@name='lastPage']")[0].get("value")
    print "Scraping... " + str(currentPage) + " of " + str(lastPage)
    for l in soup.cssselect("tr")[4:-25]:
        data = {}
        data["data"] = l.cssselect("td")[0].text_content().strip()
        data["ementa"] = l.cssselect("td font a")[0].text_content().strip()
        data["projeto"] = l.cssselect("td font b")[0].text_content().strip() 
        data["autor"] = l.cssselect("td")[2].text_content().strip()
        data["etapa"] = l.cssselect("td")[3].text_content().strip()
        data["url"] = l.cssselect("td font a")[0].get("href")
        data["id"] = data["url"].split("id=")[1]
        if data["id"] not in lista:
            try:
                data["norma"] = dataNorma(data["id"])
                dataIni =  datetime.datetime.strptime(data['data'],"%d/%m/%Y")
                dataFim =  datetime.datetime.strptime(data['norma'],"%d/%m/%Y")
                tempo =  dataFim - dataIni
                data['tempo'] = tempo.days
                scraperwiki.sqlite.save(["id"],data)
            except:
                print "error on " + data["url"]
    if currentPage > int(lastPage):
        pass
    else:
        scrape(int(currentPage)+1)


scrape()