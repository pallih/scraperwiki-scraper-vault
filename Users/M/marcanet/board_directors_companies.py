import scraperwiki
import BeautifulSoup 
# Board directors

def telefonica():
    company = "telefonica"
    url = "http://www.telefonica.com/en/shareholders_investors/html/gcorp/compcomision.shtml"
    try:   
        html = scraperwiki.scrape(url)
        soup = BeautifulSoup.BeautifulSoup(html)
        tableBoard = soup.find('table', {"class": "tabla_generica"})
        trDirectors = tableBoard.findAll("tr")
        for d in trDirectors:
            nameDirector = d.findAll("td")[0].getText()[4:]
            position = d.findAll("td")[1].getText()
            if nameDirector !="":
                id = company+"_"+nameDirector.replace(" ","-")
                data = {"id":id,"company":company,"name":nameDirector,"position":position,"Condition":""}
                scraperwiki.sqlite.save(unique_keys=['id'],data=data)
    except:
        print "Error scrapping in "+company
        pass

def repsolBoard():
    company = "repsol"
    url = "http://www.repsol.com/es_en/corporacion/accionistas-inversores/gobierno-corporativo/consejo-de-administracion/"
    try:    
        html = scraperwiki.scrape(url)
        soup = BeautifulSoup.BeautifulSoup(html)
        divBoard = soup.find('div', {"class": "col_cent1004"})
        divDirectors = divBoard.findAll("div",{"class": "tripleColumnaBC"})[1:]
        for d in divDirectors:
            try:
                nameDirector = d.find("h4").getText()
                if nameDirector!="":
                    position = str(d).split('</h4>')[1].split('<br />')[0].split(">")[-1].replace("&nbsp;"," ").rstrip()
                    id = company+"_"+nameDirector.replace(" ","-")
                    data = {"id":id,"company":company,"name":nameDirector,"position":position,"Condition":""}
                    scraperwiki.sqlite.save(unique_keys=['id'],data=data)
            except:
                pass
    except:
        print "Error scrapping in "+company
        pass

def gasNatural():
    company = "gas_natural"
    url = "http://www.gasnaturalfenosa.com/en/home/shareholders+and+investors/corporate+governance/government+agencies/1285338473580/board+of+directors.html"
    try:
        html = scraperwiki.scrape(url)
        soup = BeautifulSoup.BeautifulSoup(html)
        tableBoard = soup.find('table', {"class": "tablaDeDatos"}).find("tbody")
        trDirectors = tableBoard.findAll("tr")
        for d in trDirectors:
            try:
                position = ""
                nameDirector = ""
                if str(d.find("th")).find("<br />")!=-1 and str(d.find("th")).split("<br />")>0:
                    position = str(d.find("th")).split("<br />")[0].split(">")[-1][:-1] 
                    nameDirector = str(d.find("th")).split("<br />")[1][:-5].strip().title()
                else:
                    nameDirector = d.find("th").getText()
                    position = d.findAll("td")[0].getText()
                    if position.find("(")!=-1:
                        position = position[:-3]

                if nameDirector.find(",")!=-1:
                    nameDirector = nameDirector.split(",")[1]+" "+nameDirector.split(",")[0]
                    nameDirector = nameDirector.rstrip().strip().title()
                if position != "" and nameDirector != "":
                    id = company+"_"+nameDirector.replace(" ","-")
                    data = {"id":id,"company":company,"name":nameDirector,"position":position,"Condition":""}
                    scraperwiki.sqlite.save(unique_keys=['id'],data=data)
            except:
                pass
    except:
        print "Error scrapping in "+company
        pass

def bankinter():
    company = "bankinter"
    url = "https://webcorporativa.bankinter.com/www2/corporativa/en/gobierno_corporativo/consejo_administracion/miembros_consejo"
    try:
        html = scraperwiki.scrape(url)
        soup = BeautifulSoup.BeautifulSoup(html)
        divBoard = soup.find('div', {"class": "caj_contenido_01"}).find("tbody")
        print divBoard.getText()
        trDirectors = divBoard.findAll("tr")
        print "adasd"
        for d in trDirectors:
            print trDirectors.getText()
    except:
        print "Error scrapping in "+company
        pass

# list companies to scrap
#repsolBoard()
#telefonica()
#gasNatural()
bankinter()

'''
List done ibex35:
TELEFONICA
GAS NATURAL
REPSOL YPF

List to do ibex35:

ABENGOA CL.B -> http://www.abengoabioenergy.com/web/en/acerca_de/consejo_de_administracion/
ABERTIS -> http://www.abertis.com/board-of-directors-and-committees/var/lang/en/idm/474
ACCIONA -> http://www.acciona.com/shareholders--investors/corporate-governance/governance-and-executive-boards/board-of-directors
ACERINOX -> http://www.acerinox.es/Inversores/Gobierno_corporativo/Organos_de_Gobierno_de_la_Sociedad/Consejo_de_Administracion/?__setlocale=en
ACS -> http://www.grupoacs.com/index.php/en/c/aboutacs_organization_managementbodies_boardofdirectors
AMADEUS -> http://www.investors.amadeus.com/english/corporate_governance/composition_board/
ARCELORMITTAL -> http://www.arcelormittal.com/corp/who-we-are/leadership/board-of-directors
BANKINTER -> https://webcorporativa.bankinter.com/www2/corporativa/en/gobierno_corporativo/consejo_administracion/miembros_consejo
BME ->http://www.bolsasymercados.es/aspx/inf_legal/consejo.aspx?id=ing&tipo=consejo
BBVA ->
CAIXABANK ->
DIA ->
ENAGAS ->
ENDESA ->
FCC ->
FERROVIAL ->
GRIFOLS ->
IAG (IBERIA) ->
IBERDROLA ->
INDITEX ->
INDRA ->
JAZZTEL ->
MAPFRE ->
MEDIASET ->
OHL ->
POPULAR ->
REE ->
SABADELL ->
SACYR ->
SANTANDER ->
TECNICAS REUNIDAS ->
VISCOFAN ->

Mercado continuo
funespana-> http://accionistas.funespana.es/index.php?opc=11
'''
