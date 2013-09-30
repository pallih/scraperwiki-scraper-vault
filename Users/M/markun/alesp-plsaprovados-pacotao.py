import scraperwiki
from lxml.html import parse
import datetime
import urlparse

def scrape(currentPage=0):
    try:
        lista_dict = scraperwiki.sqlite.select("id from swdata")
    except:    
        lista_dict = []
    lista = []
    for l in lista_dict:
        lista.append(l['id'])

    
    print "Loading url... "
    base_url = "http://www.al.sp.gov.br/spl_consultas/consultaProposicoesAction.do?"
    args = "direction=acima&lastPage=0&currentPage=" + str(currentPage)+ "&act=detalhe&idDocumento=&rowsPerPage=500&currentPageDetalhe=1&tpDocumento=&method=search&text=&natureId=18&legislativeNumber=&legislativeYear=&natureIdMainDoc=&anoDeExercicio=&legislativeNumberMainDoc=&legislativeYearMainDoc=&strInitialDate=&strFinalDate=&author=&supporter=&politicalPartyId=&tipoDocumento=&stageId=&strVotedInitialDate=&strVotedFinalDate=&approved=&rejected=&advancedSearch=#inicio"
    soup = parse(base_url+args).getroot()
    lastPage = soup.xpath("//input[@name='lastPage']")[0].get("value")
    
    print "Scraping... " + str(currentPage) + " of " + str(lastPage)
    for l in soup.cssselect("tr")[4:-25]:
        data = {}
        data["data"] = l.cssselect("td")[0].text_content().strip()
        data["descricao"] = l.cssselect("td font a")[0].text_content().strip()
        data["titulo"] = l.cssselect("td font b")[0].text_content().strip() 
        data["autor"] = l.cssselect("td")[2].text_content().strip()
        data["etapa"] = l.cssselect("td")[3].text_content().strip()
        data["url"] = l.cssselect("td font a")[0].get("href")
        data["id"] =  urlparse.parse_qs(urlparse.urlparse(data["url"]).query)["idDocumento"][0] #diferente por tipo de doc
        scraperwiki.sqlite.save(["id"],data)
    if currentPage > int(lastPage):
        pass
    else:
        scrape(int(currentPage)+1)


scrape()import scraperwiki
from lxml.html import parse
import datetime
import urlparse

def scrape(currentPage=0):
    try:
        lista_dict = scraperwiki.sqlite.select("id from swdata")
    except:    
        lista_dict = []
    lista = []
    for l in lista_dict:
        lista.append(l['id'])

    
    print "Loading url... "
    base_url = "http://www.al.sp.gov.br/spl_consultas/consultaProposicoesAction.do?"
    args = "direction=acima&lastPage=0&currentPage=" + str(currentPage)+ "&act=detalhe&idDocumento=&rowsPerPage=500&currentPageDetalhe=1&tpDocumento=&method=search&text=&natureId=18&legislativeNumber=&legislativeYear=&natureIdMainDoc=&anoDeExercicio=&legislativeNumberMainDoc=&legislativeYearMainDoc=&strInitialDate=&strFinalDate=&author=&supporter=&politicalPartyId=&tipoDocumento=&stageId=&strVotedInitialDate=&strVotedFinalDate=&approved=&rejected=&advancedSearch=#inicio"
    soup = parse(base_url+args).getroot()
    lastPage = soup.xpath("//input[@name='lastPage']")[0].get("value")
    
    print "Scraping... " + str(currentPage) + " of " + str(lastPage)
    for l in soup.cssselect("tr")[4:-25]:
        data = {}
        data["data"] = l.cssselect("td")[0].text_content().strip()
        data["descricao"] = l.cssselect("td font a")[0].text_content().strip()
        data["titulo"] = l.cssselect("td font b")[0].text_content().strip() 
        data["autor"] = l.cssselect("td")[2].text_content().strip()
        data["etapa"] = l.cssselect("td")[3].text_content().strip()
        data["url"] = l.cssselect("td font a")[0].get("href")
        data["id"] =  urlparse.parse_qs(urlparse.urlparse(data["url"]).query)["idDocumento"][0] #diferente por tipo de doc
        scraperwiki.sqlite.save(["id"],data)
    if currentPage > int(lastPage):
        pass
    else:
        scrape(int(currentPage)+1)


scrape()