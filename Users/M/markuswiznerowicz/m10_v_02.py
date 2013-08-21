######################################
# M1 - Datenextraktion V 0.3 - Phyton#
######################################

### Import von Modulen
import scraperwiki                                             
import lxml.html 
 
### Set up des Datenspeichers
record = {}

### Zusammensetzen des Projektlinks 
projektnummer = '85457'                                        # ausgewählte Nummer des Projektes, welches analysiert werden soll
projektsuchlink =  'http://cordis.europa.eu/newsearch/getDoc?doctype=PROJ&xslt-template=projects/xsl/projectdet_en.xslt&rcn='                                                                                                   # Linkelement, das alle Suchen gemeinsam haben.
projektlink = projektsuchlink + projektnummer                  # Zusammensetzen des ganzen Projektlinks aus Suchlink und Projektnummer
record ['nr'] = projektnummer                                  # Speichern der Nr des Projektes

### Zugriff auf die Seite des Projektes 
html = scraperwiki.scrape(projektlink)                         # Übergeben des Links an die scraperwiki
root = lxml.html.fromstring(html)                              # HTML in ein XML Objekt zur weiteren Bearbeitung umwandelt



### Auslesen des Projektakronyms 
h1s = root.cssselect('h1')                                     # Benennen des gesuchten Statements (das Akronym befindet sich in einem h1-Block)
for h1 in h1s:
    savestring = lxml.html.tostring(h1)                        # Umwandeln des XMLs (in dem h1 zu finden ist) in einen String
    savestring = savestring.replace('<h1>','')                 # Beschneiden des Strings um <h1>        
    savestring = savestring.replace('</h1>','')                # Beschneiden des Strings um </h1> 
    savestring = savestring.replace(' ','')                    # Beschneiden des Strings um Leerzeichen                                          
    record ['Akronym'] = savestring                            # Speichern des gefundenen Projektakronyms im Array
    
### Auslesen des ausgeschriebenen Titels 
h2s = root.cssselect('h2')                                     # Benennen des gesuchten Statements (h2-Block)
Hilfsbool= True                                                # Hilfsvariabel zum exkulsiven Auslesen des ersten Arguments
for h2 in h2s:
     if  Hilfsbool== True:                                     # Hilfsvariable
        savestring = lxml.html.tostring(h2)                    # Umwandeln des XMLs (in dem h2 zu finden ist) in einen String
        savestring = savestring.replace('<h2>','')             # Beschneiden des Strings um <h2>        
        savestring = savestring.replace('</h2>','')            # Beschneiden des Strings um </h2>
        Hilfsbool= False                                       # Setzen der Hilfsvariable auf False => dadruch kann die Bedingung nicht mehr erfüllt werden
        record ['Titel'] = savestring                          # Speichern des gesamten Titels des Projektes im Array

### Auslesen der Projektzuordnung
h2s = root.cssselect('h2')                                     # Benennen des gesuchten Statements (h2-Block)
for h2 in h2s:
    savestring = lxml.html.tostring(h2)                        # Umwandeln des XMLs (in dem h2 zu finden ist) in einen String
    if  'Subjects' in savestring:                              # Suchen im String nach "Subjects", denn dahinter stehen die Zuordnungen
        savestring = savestring.replace('<h2>','')             # Beschneiden des Strings um <h2>        
        savestring = savestring.replace('</h2>','')            # Beschneiden des Strings um </h2>
        savestring = savestring.replace('Subjects','')         # Beschneiden des Strings um </Subjects>
        record ['Zuordnung'] = savestring                      # Speichern der Projektzuordnung im Array


### Auslesen von Projektstart und Projektende, Projektreference, Projektstatus, Kosten, Anteil der Kosten getragen durch die EU
### Projektnummer, Letzes Update der Projektinformationen 

bs = root.cssselect('b')                                              # Benennen des gesuchten Statements (b-Block)

for b in bs:                                     
        savestring = lxml.html.tostring(b)                            # Umwandeln des XMLs (in dem b zu finden ist) in einen String
        savestring = savestring.replace('<b>','')                     # Beschneiden des Strings um <b>        
        savestring = savestring.replace('</b>','')                    # Beschneiden des Strings um </b>
        if "From " in savestring:                                     
            savestring = savestring.replace('From ','')               
            record ['Von'] = savestring                               # Speichern des Projektstarts im Array
        if "to " in savestring:                                       
            savestring = savestring.replace('to ','')                 
            record ['Bis'] = savestring                               # Speichern des Projektendes im Array
        if "Project reference: " in savestring:                       
            savestring = savestring.replace('Project reference: ','') 
            record ['Referenz'] = savestring                          # Speichern der Projektreferenz im Array
        if "Status: " in savestring:                                  
            savestring = savestring.replace('Status: ','')            
            record ['Status'] = savestring                            # Speichern des Projektstatus im Array
        if "Total cost: EUR " in savestring:
            savestring = savestring.replace('Total cost: EUR ','') 
            savestring = savestring.replace(' ','') 
            record ['Gesamtkosten'] = savestring                      # Speichern der Projektgesamtkosten im Array
        if "EU contribution: " in savestring:
            savestring = savestring.replace('EU contribution: EUR ','') 
            savestring = savestring.replace(' ','')  
            record ['Eu Anteil'] = savestring                         # Speichern des EU Anteiles im Array
        if "Record number: " in savestring:
            savestring = savestring.replace('Record number: ','') 
            savestring = savestring.replace(' /','') 
            record ['RNr'] = savestring                               # Speichern der Record Nr im Array
        if "Last updated on (QVD): " in savestring:
            savestring = savestring.replace('Last updated on (QVD): ','') 
            savestring = savestring.replace(' /','') 
            record ['Lastupdate'] = savestring                        # Speichern des letzen Update-Datums im Array

# Auslesen der Projektbeschreibung, des Akronyms , der Subprogramm area und des Vertragstypens
ps = root.cssselect('p')
Hilfsbool= True 
for p in ps:
        savestring = lxml.html.tostring(p)                             # Umwandeln des XMLs (in dem p zu finden ist) in einen String
        savestring = savestring.replace('<p>','')                      # Beschneiden des Strings um <p>        
        savestring = savestring.replace('</p>','')                     # Beschneiden des Strings um </p> 
        savestring = savestring.replace('<br/>','')                    # Löschen der Breaktags <br/>  
        savestring = savestring.replace('<br>','')                     # Löschen der Breaktags <br>  
        savestring = savestring.replace('</b>','')                     # Löschen des Tags </b>  
        savestring = savestring.replace('<b>','')                      # Löschen des Tags <b>
        if  Hilfsbool== True:       
            record ['Beschreibung'] = savestring                       # Speichern der Beschreibung im Array
            Hilfsbool= False                                           # Hilfsbool auf False setzen, damit die Aktion nur einmal ausgeführt wird
        if "Programme acronym" in savestring:
            savestring = savestring.replace('</a>','')                 # Löschen des Tags </a> 
            range = savestring.split('>')                              # Teilen des Strings an dem ">" Zeichen
            record ['PAkronym'] = range[1]                             # Speichern der Projektzuordnung im Array
        if "Subprogramme area: " in savestring:
            savestring = savestring.replace('Subprogramme area: ','')  # Beschneiden des Strings 
            record ['Subprogramme'] = savestring                       # Speichern des Subprogrammes im Array
        if "Contract type: " in savestring:
            savestring = savestring.replace('Contract type: ','')      # Beschneiden des Strings  
            record ['Contract type'] = savestring                      # Speichern des Vertragstypen im Array  

# Auslesen des Projektleiters
names = root.cssselect('div')
Hilfsbool= True
for name in names:
    savestring = lxml.html.tostring(name)                                                  # umwandeln des XMLs (in dem name zu finden ist) in einen String
    if '<div class="projcoord" id="coord">' in savestring and Hilfsbool== True:            # Überspringen des ersten Auftauchens der "projcoord"
        Hilfsbool= False
    elif '<div class="projcoord" id="coord">'in savestring and Hilfsbool== False:          # im zweiten Block mit Infos wird dieser Teil ausgeführt 
               range = savestring.split('<div class="name">')                              # Teilen des Savestrings bevor das leitende Institut auftaucht 
               hilfsstring = range[1]                                                      # Hilfsstring an dessen Anfang das Insitut steht
               range = hilfsstring .split('<')                                             # Spalten des Hilfsstrings (nach der gesuchen Information)
               record ['L Institut'] = range[0]                                            # Speichern des Institus im Array
               range = savestring.split('<div class="country">')                           # Teilen des Savestrings bevor das leitende Land auftaucht 
               hilfsstring = range[1]                                                      # Hilfsstring an dessen Anfang das Land steht
               range = hilfsstring .split('<')                                             # Spalten des Hilfsstrings (nach der gesuchen Information)
               record ['L Land'] = range[0]                                                # Speichern des Land im Array
               savestring = savestring.replace('Administrative contact: ','')              # Beschneiden des savestring um den Ausdruck in ()
               range = savestring.split('<div class="optional item-content">')             # Teilen des Savestrings bevor die leitende Person auftaucht 
               hilfsstring = range[1]                                                      # Hilfsstring an dessen Anfang die leitende Person steht   
               range = hilfsstring .split('<')                                             # Spalten des Hilfsstrings (nach der gesuchen Information)
               record ['L Ansprech'] = range[0]                                            # Speichern der leitenden Person im Array

# Auslesen der weiteren Teilnehmer
divs = root.cssselect('div')
Hilfsbool= True                                                                            # Hilfsvariabel 
zaehlvariabel = 1                                                                          # Zaehlvariabel zum Speichern der Teilnehmer 
for div in divs:
    savestring = lxml.html.tostring(div)                                                   # Umwandeln des XMLs (in dem div steht) in einen String
    if '<div class="main">' in savestring and Hilfsbool== False:            
            if '<div class="projcoord" id="coord">' in savestring:                         # Umgehen des Projektoridinationsblocks
                Hilfsbool= False      
            elif '<h2>' in savestring:                                                     # Umgehen des H2-Blocks
                Hilfsbool= False
            else:
                if 'class="participant"' in savestring:                                    # Code der auf die Teilnehmer anzuwenden ist
                    range = savestring.split('<div class="name">')                         # Teilen des Savestrings bevor das teilnehmende Institut auftaucht
                    hilfsstring = range[1]                                                 # Hilfsstring an dessen Anfang das Insitut steht
                    range = hilfsstring .split('<')                                        # Spalten des Hilfsstrings (nach der gesuchen Information)
                    Teilnehmerinstitut = "ti" + str(zaehlvariabel)                         # Erzeugen einer Spaltenbezeichnung an Hand der Teilnehmernummer
                    record [Teilnehmerinstitut] = range[0]                                 # Speichern des Teilnehmerinstitutes im Array
                    range = savestring.split('<div class="country">')                      # Teilen des Savestrings bevor das teilnehmende Land auftaucht
                    hilfsstring = range[1]                                                 # Hilfsstring an dessen Anfang das Land steht
                    range = hilfsstring .split('<')                                        # Spalten des Hilfsstrings (nach der gesuchen Information)
                    Teilnehmerland = "tl" + str(zaehlvariabel)                             # Erzeugen einer Spaltenbezeichnung an Hand der Teilnehmernummer
                    record [Teilnehmerland] = range[0]                                     # Speichern des Teilnehmerlandes im Array
                    savestring = savestring.replace('Administrative contact: ','')         # Beschneiden des savestring um den Ausdruck in ()
                    range = savestring.split('<div class="optional item-content">')        # Teilen des Savestrings bevor dar teilnehmende Leiter auftaucht
                    hilfsstring = range[1]                                                 # Hilfsstring an dessen Anfang der Leiter steht
                    range = hilfsstring .split('<')                                        # Spalten des Hilfsstrings (nach der gesuchen Information)
                    Teilnehmername = "tn" + str(zaehlvariabel)                             # Erzeugen einer Spaltenbezeichnung an Hand der Teilnehmernummer
                    record [Teilnehmername] = range[0]                                     # Speichern des Teilnehmerleiters im Array
                    zaehlvariabel = zaehlvariabel +1                                       # Erhöhen der Zählvaraibel


    if '<div class="name">' in savestring and Hilfsbool== True:                            # Umgehen des ersten Textblocks
        Hilfsbool= False 

print record                                                                               # Ausgabe des gesamten Records (zu Kontrolle)
scraperwiki.sqlite.save(['nr'], record)                                                    # save the records one by one