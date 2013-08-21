import scraperwiki
import urllib
from bs4 import BeautifulSoup as Soup

# stap 1: urls samenstellen


base_url = "http://evenementen.uitslagen.nl/2013/marathonrotterdam/details.php?s="
end_url = "&o=1&t=nl"

for num in range (1, 10):
    baseplusnr = base_url+str(num)
    url = baseplusnr+end_url
    
    
# stap 2: de urls openen

    soup = Soup(urllib.urlopen(url))

# stap 3: de 'niet gevonden' pagina's buiten beschouwing laten

    split = soup.find("b", style="color:red")
    if split is None:
        col = soup.findAll('td')

        
# stap 4: aanwijzen welke table data we willen hebben

        startnr = col[0].string.replace("Startnummer", "")
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

        
# stap 5: alle data verzamelen en opslaan

        data = {"NR":startnr, "Naam":naam, "Woonplaats":woonplaats, "Afstand":afstand, "Categorie":cat, "Totaal":totplaats, "Cat-plaats":catplaats,"Snelheid":snelh, "Bruto-tijd":brutot, "Netto-tijd":nett, "5KM":vijf, "10KM":tien, "15KM":vtien, "20KM":twintig,"HALF":half, "25KM":vtwintig,"30KM":dertig, "35KM":vdertig, "40KM":veertig}

        scraperwiki.sqlite.save(["NR"], data)

        
