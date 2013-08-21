######################################
# M1 - Datenextraktion V 0.1 - Phyton#
######################################

### Import von Modulen
import scraperwiki                                             
import lxml.html 

### Set up des Datenspeichers
record = {}
 
### Linkvariablen

Linkteil1 = 'http://cordis.europa.eu/newsearch/index.cfm?ENGINE_ID=CORDIS_ENGINE_ID&Summary=quick&combo_orderby=all&nPage='
Linkteil2 = '&all_words=ict&page=resultListGET&combo_resultperpage=10&form_id=simple_search&SEARCH_TYPE_ID=CORDIS_SEARCH_ID&useraction=simple_search&REF_PROGRAMMEACRONYM=FP7-ICT&REF_Collection=EN_PROJ'
Seite = 1

### Maximale Projektanzahl

Suchlink = Linkteil1 + "1" + Linkteil2
html = scraperwiki.scrape(Suchlink)
root = lxml.html.fromstring(html)                              # HTML in ein XML Objekt zur weiteren Bearbeitung umwandelt
zaehler = 1

divs = root.cssselect('div')              # Benennen des gesuchten Statements (das Akronym befindet sich in einem h1-Block)
for div in divs:
    savestring = lxml.html.tostring(div)                        # Umwandeln des XMLs (in dem h1 zu finden ist) in einen String
    if '<div class="resultSummary">' in savestring:
        if zaehler == 5:
            range2 = savestring.split('of ')
            hilfsstring = range2[1]
            range2 = hilfsstring.split(' ')
            projektanzahl = int (range2[0])
            projektanzahlgeteilt = projektanzahl / 10
            rest = projektanzahl - projektanzahlgeteilt*10
            if rest == 0:
                durchlauf = projektanzahlgeteilt + 1
            else:
                durchlauf = projektanzahlgeteilt + 2
        else:
            zaehler = zaehler +1

### Auslesen der einzelnen Projekt IDs

zaehlnr = 1

def idlesen(Link):
    global zaehlnr
    html = scraperwiki.scrape(Suchlink)
    root = lxml.html.fromstring(html)  
    divs = root.cssselect('div') 
    zaehler = 1
    for div in divs:
        savestring = lxml.html.tostring(div)
        if '<div class="resultItem">' in savestring:
            if zaehler == 4:
                range = savestring.split('reference=')
                print savestring
                hilfsstring = range[1]
                range = hilfsstring.split('&amp')
                record ['PrNr'] =  str(zaehlnr)
                record ['Projektnummer'] = range[0]
                print range [0]
                zaehlnr = zaehlnr + 1 
                scraperwiki.sqlite.save(['PrNr'], record) 
            else:
                zaehler = zaehler +1 

### Link erzeugen und alle Projekt IDs auslesen

for i in range(1,durchlauf): 
    Suchlink = Linkteil1 + str(i) + Linkteil2
    idlesen(Suchlink)


    
