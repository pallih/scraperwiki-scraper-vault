import scraperwiki
import urllib
from bs4 import BeautifulSoup as Soup


# de koppeling maken tussen de urls en deze scraper

scraperwiki.sqlite.attach("maro_urls")
 
scrapings = scraperwiki.sqlite.select("* from `maro_urls`.swdata")

# de url weergeven

for scraping in scrapings:
    url = scraping["url"]
    print url

# de code uit de originele scraper

    soup = Soup(urllib.urlopen(url)) #open de pagina

#onderscheid maken tussen pagina's met data en lege pagina's. Als we dat niet doen, loopt de scraper vast op de eerste de beste pagina die niet aan de zoekvraag voldoet, oftewel de eerste lege pagina (id=2) 
#"Niet gevonden" onderscheidt zich door tag-style rood
#None zijn de pagina's die niet aan de tag-style rood voldoen, en dus bevatten ze wel data

#onderstaande coderegels zijn niet meer nodig, want alle gescrapete urls bevatten data als het goed is

#    split = soup.find("b", style="color:red")
#    if split is None:    

    col = soup.findAll('td') #alle td tags vinden
       
#aangeven welke td-cellen we willen hebben 

    startnr = col[0].string.replace("Startnummer", "")#.strip() #is deze strip nog nodig? nee dus
    naam = col[4].string
    woonplaats = col[6].string
    afstand = col[8].string
    cat = col[10].string
    totplaats = col[12].string 
    catplaats = col[14].string
    snelh = col[16].string
    brutot = col[18].string
    nett = col[20].string
    
    vijf = col[24].string
    tien = col[26].string
    vtien = col[28].string
    twintig = col[30].string
    half = col[32].string
    vtwintig = col[34].string
    dertig = col[36].string
    vdertig = col[38].string
    veertig = col[40].string

    data = {"url":url, "NR":startnr, "Naam":naam, "Woonplaats":woonplaats, "Afstand":afstand, "Categorie":cat, "Totaal":totplaats, "Cat-plaats":catplaats,"Snelheid":snelh, "Bruto-tijd":brutot, "Netto-tijd":nett, "5KM":vijf, "10KM":tien, "15KM":vtien, "20KM":twintig,"HALF":half, "25KM":vtwintig,"30KM":dertig, "35KM":vdertig, "40KM":veertig} #definieren wat ik wil opslaan in de database

    scraperwiki.sqlite.save(["NR"], data) #opslaan in de database


    

    import scraperwiki
import urllib
from bs4 import BeautifulSoup as Soup


# de koppeling maken tussen de urls en deze scraper

scraperwiki.sqlite.attach("maro_urls")
 
scrapings = scraperwiki.sqlite.select("* from `maro_urls`.swdata")

# de url weergeven

for scraping in scrapings:
    url = scraping["url"]
    print url

# de code uit de originele scraper

    soup = Soup(urllib.urlopen(url)) #open de pagina

#onderscheid maken tussen pagina's met data en lege pagina's. Als we dat niet doen, loopt de scraper vast op de eerste de beste pagina die niet aan de zoekvraag voldoet, oftewel de eerste lege pagina (id=2) 
#"Niet gevonden" onderscheidt zich door tag-style rood
#None zijn de pagina's die niet aan de tag-style rood voldoen, en dus bevatten ze wel data

#onderstaande coderegels zijn niet meer nodig, want alle gescrapete urls bevatten data als het goed is

#    split = soup.find("b", style="color:red")
#    if split is None:    

    col = soup.findAll('td') #alle td tags vinden
       
#aangeven welke td-cellen we willen hebben 

    startnr = col[0].string.replace("Startnummer", "")#.strip() #is deze strip nog nodig? nee dus
    naam = col[4].string
    woonplaats = col[6].string
    afstand = col[8].string
    cat = col[10].string
    totplaats = col[12].string 
    catplaats = col[14].string
    snelh = col[16].string
    brutot = col[18].string
    nett = col[20].string
    
    vijf = col[24].string
    tien = col[26].string
    vtien = col[28].string
    twintig = col[30].string
    half = col[32].string
    vtwintig = col[34].string
    dertig = col[36].string
    vdertig = col[38].string
    veertig = col[40].string

    data = {"url":url, "NR":startnr, "Naam":naam, "Woonplaats":woonplaats, "Afstand":afstand, "Categorie":cat, "Totaal":totplaats, "Cat-plaats":catplaats,"Snelheid":snelh, "Bruto-tijd":brutot, "Netto-tijd":nett, "5KM":vijf, "10KM":tien, "15KM":vtien, "20KM":twintig,"HALF":half, "25KM":vtwintig,"30KM":dertig, "35KM":vdertig, "40KM":veertig} #definieren wat ik wil opslaan in de database

    scraperwiki.sqlite.save(["NR"], data) #opslaan in de database


    

    