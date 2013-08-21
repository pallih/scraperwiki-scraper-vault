# M1 - Datenextraktion V 0.1 - Phyton

import scraperwiki
import lxml.html

#Zusammensetzen des Projektlinks
projektnummer = '85457' # ausgewählte Nummer des Projektes, welches analysiert werden soll
projektsuchlink =  'http://cordis.europa.eu/newsearch/getDoc?doctype=PROJ&xslt-template=projects/xsl/projectdet_en.xslt&rcn=' # Teil den alle Suchen gemeinsam haben
projektlink = projektsuchlink + projektnummer #zusammensetzen des ganzen Projektlinks aus Suchlink und Projektnummer

# Zugriff auf die Seite des Projektes
html = scraperwiki.scrape(projektlink) # einführen des HTML Statements
root = lxml.html.fromstring(html) # HTML in ein XML Objekt umwandelt

# Auslesen der weiteren Teilnehmer
names = root.cssselect('div')
zaehler = True
zaehler2 = True
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
        #savestring = savestring.replace('<p>','')                      #Beschneiden des Strings um <p>        
    #print savestring                                       
        #if "Contract type: " in savestring:
            #savestring = savestring.replace('Contract type: ','')      #Beschneiden des Strings  
            #print savestring                                           #Ausgabe des Vertragstypen  




# Auslesen des Projektakronyms
#h1s = root.cssselect('p') 
#for h1 in h1s:
    #savestring = lxml.html.tostring(h1)                        #umwandeln des XMLs (in dem h1 zu finden ist) in einen String
    #savestring = savestring.replace('<p>','')                 #Beschneiden des Strings um <h1>        
    #savestring = savestring.replace('</p>','')                #Beschneiden des Strings um </h1> 
    #print savestring                                           #Ausgabe des gefundenen Projektakronyms
