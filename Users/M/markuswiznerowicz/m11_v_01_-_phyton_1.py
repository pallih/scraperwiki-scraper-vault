######################################
# M1 - Datenextraktion V 0.1 - Phyton#
######################################

import scraperwiki                                             # Import des scraperwiki Moduls
import lxml.html                                               # Import des HTML zu XML Moduls

### Zusammensetzen des Projektlinks 
projektnummer = '85460'                                        # ausgewählte Nummer des Projektes, welches analysiert werden soll
projektsuchlink =  'http://cordis.europa.eu/newsearch/getDoc?doctype=PROJ&xslt-template=projects/xsl/projectdet_en.xslt&rcn='                                                                                                    # Linkelement, das alle Suchen gemeinsam haben.
projektlink = projektsuchlink + projektnummer                  # Zusammensetzen des ganzen Projektlinks aus Suchlink und Projektnummer

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
    print savestring                                           # Ausgabe des gefundenen Projektakronyms
    
### Auslesen des ausgeschriebenen Titels 
h2s = root.cssselect('h2')                                     # Benennen des gesuchten Statements (h2-Block)
zaehler = True                                                 # Hilfsvariabel zum exkulsiven Auslesen des ersten Arguments
for h2 in h2s:
     if  zaehler == True:                                      # Hilfsvariable
        savestring = lxml.html.tostring(h2)                    # Umwandeln des XMLs (in dem h2 zu finden ist) in einen String
        savestring = savestring.replace('<h2>','')             # Beschneiden des Strings um <h2>        
        savestring = savestring.replace('</h2>','')            # Beschneiden des Strings um </h2>
        zaehler = False                                        # Setzen der Hilfsvariable auf False => dadruch kann die Bedingung nicht mehr erfüllt werden
        print savestring                                       # Ausgabe des gesamten Titels des Projektes

### Auslesen der Projektzuordnung
h2s = root.cssselect('h2')                                     # Benennen des gesuchten Statements (h2-Block)
for h2 in h2s:
    savestring = lxml.html.tostring(h2)                        # Umwandeln des XMLs (in dem h2 zu finden ist) in einen String
    if  'Subjects' in savestring:                              # Suchen im String nach "Subjects", denn dahinter stehen die Zuordnungen
        savestring = savestring.replace('<h2>','')             # Beschneiden des Strings um <h2>        
        savestring = savestring.replace('</h2>','')            # Beschneiden des Strings um </h2>
        savestring = savestring.replace('Subjects','')         # Beschneiden des Strings um </Subjects>
        print savestring                                       # Ausgabe des gesamten HTML-Statements


### Auslesen von Projektstart und Projektende, Projektreference, Projektstatus, Kosten, Anteil der Kosten getragen durch die EU
### Projektnummer, Letzes Update der Projektinformationen 

bs = root.cssselect('b')                                              # Benennen des gesuchten Statements (b-Block)

for b in bs:                                     
        savestring = lxml.html.tostring(b)                            # Umwandeln des XMLs (in dem b zu finden ist) in einen String
        savestring = savestring.replace('<b>','')                     # Beschneiden des Strings um <b>        
        savestring = savestring.replace('</b>','')                    # Beschneiden des Strings um </b>
        if "From " in savestring:
            savestring = savestring.replace('From ','') 
            print savestring                                          # Ausgabe des Projektstarts   
        if "to " in savestring:
            savestring = savestring.replace('to ','') 
            print savestring                                          # Ausgabe des Projektendes  
        if "Project reference: " in savestring:
            savestring = savestring.replace('Project reference: ','') 
            print savestring                                          # Ausgabe der Projektreferenz  
        if "Status: " in savestring:
            savestring = savestring.replace('Status: ','') 
            print savestring                                          # Ausgabe des Projektstatus  
        if "Total cost: EUR " in savestring:
            savestring = savestring.replace('Total cost: EUR ','') 
            savestring = savestring.replace(' ','') 
            print savestring                                          # Ausgabe der Projektkosten  
        if "EU contribution: " in savestring:
            savestring = savestring.replace('EU contribution: EUR ','') 
            savestring = savestring.replace(' ','')  
            print savestring                                          # Ausgabe des EU-Anteils an den Projektkosten 
        if "Record number: " in savestring:
            savestring = savestring.replace('Record number: ','') 
            savestring = savestring.replace(' /','') 
            print savestring                                          # Ausgabe der Nummer des Projektes
        if "Last updated on (QVD): " in savestring:
            savestring = savestring.replace('Last updated on (QVD): ','') 
            savestring = savestring.replace(' /','') 
            print savestring                                          # Ausgabe des letzen Update-Datums    



# Auslesen der Projektbeschreibung, des Acronyms , der Subprogramm area und des Vertragstypens
ps = root.cssselect('p')
zaehler = True 
for p in ps:
        savestring = lxml.html.tostring(p)                             #umwandeln des XMLs (in dem h1 zu finden ist) in einen String
        savestring = savestring.replace('<p>','')                      #Beschneiden des Strings um <p>        
        savestring = savestring.replace('</p>','')                     #Beschneiden des Strings um </p> 
        savestring = savestring.replace('<br/>','')                    #Löschen der Breaktags <br/>  
        savestring = savestring.replace('<br>','')                     #Löschen der Breaktags <br>  
        savestring = savestring.replace('</b>','')                     #Löschen des Tags </b>  
        savestring = savestring.replace('<b>','')                      #Löschen des Tags <b>
        if  zaehler == True:  
            print savestring                   
            zaehler = False                                               #zaheler auf False setzen, damit die Aktion nur einmal ausgeführt wird
        if "Programme acronym" in savestring:
            savestring = savestring.replace('</a>','')                 #Löschen des Tags </a> 
            range = savestring.split('>')                              #Teilen des Strings an dem ">" Zeichen
            print range[1]                                             #Ausgabe des hinteren Teilsstrings => der Projektzuordnung
        if "Subprogramme area: " in savestring:
            savestring = savestring.replace('Subprogramme area: ','')  #Beschneiden des Strings 
            print savestring                                           #Ausgabe des Subprogramm Bereiches                                                   
        if "Contract type: " in savestring:
            savestring = savestring.replace('Contract type: ','')      #Beschneiden des Strings  
            print savestring                                           #Ausgabe des Vertragstypen  

# Auslesen des Projektleiters
names = root.cssselect('div')
zaehler = True
for name in names:
    savestring = lxml.html.tostring(name)                                           #umwandeln des XMLs (in dem h1 zu finden ist) in einen String
    if '<div class="projcoord" id="coord">' in savestring and zaehler == True:
        zaehler = False
    elif '<div class="projcoord" id="coord">'in savestring and zaehler == False:
               range = savestring.split('<div class="name">')                              #Teilen des Strings an dem ">" Zeichen
               hilfsstring = range[1]
               range = hilfsstring .split('<') 
               print range[0] 
               range = savestring.split('<div class="country">')                              #Teilen des Strings an dem ">" Zeichen
               hilfsstring = range[1]
               range = hilfsstring .split('<') 
               print range[0]
               savestring = savestring.replace('Administrative contact: ','') 
               range = savestring.split('<div class="optional item-content">')                              #Teilen des Strings an dem ">" Zeichen
               hilfsstring = range[1]
               range = hilfsstring .split('<') 
               print range[0]

# Auslesen der weiteren Teilnehmer
names = root.cssselect('div')
zaehler = True
for name in names:
    savestring = lxml.html.tostring(name)                                              #umwandeln des XMLs (in dem h1 zu finden ist) in einen String
    if '<div class="main">' in savestring and zaehler == False:
            
            if '<div class="projcoord" id="coord">' in savestring:                    #Auslesen des verantwortlichen Institues für das Projekt
                zaehler = False      
            elif '<h2>' in savestring:                                      #Auslesen des verantwortlichen Institues für das Projekt
                zaehler = False
            else:
                if 'class="participant"' in savestring: 
                    range = savestring.split('<div class="name">')                              #Teilen des Strings an dem ">" Zeichen
                    hilfsstring = range[1]
                    range = hilfsstring .split('<') 
                    print range[0] 
                    range = savestring.split('<div class="country">')                              #Teilen des Strings an dem ">" Zeichen
                    hilfsstring = range[1]
                    range = hilfsstring .split('<') 
                    print range[0]    
                    savestring = savestring.replace('Administrative contact: ','') 
                    range = savestring.split('<div class="optional item-content">')                              #Teilen des Strings an dem ">" Zeichen
                    hilfsstring = range[1]
                    range = hilfsstring .split('<') 
                    print range[0]            
                
 
        #print savestring
    if '<div class="name">' in savestring and zaehler == True: 
        zaehler = False 

#for p in ps:
#     record = { "p" : lxml.html.tostring(p) } # column name and value
#     scraperwiki.sqlite.save(["p"], record) # save the records one by one