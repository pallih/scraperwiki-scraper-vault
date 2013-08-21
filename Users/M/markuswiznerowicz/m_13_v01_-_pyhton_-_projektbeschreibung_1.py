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

# Auslesen der Projektbeschreibung
ps = root.cssselect('p')
zaehler = True 
for p in ps:
    if  zaehler == True: 
        savestring = lxml.html.tostring(p)                          #umwandeln des XMLs (in dem h1 zu finden ist) in einen String
        savestring = savestring.replace('<p>','')                   #Beschneiden des Strings um <p>        
        savestring = savestring.replace('</p>','')                  #Beschneiden des Strings um </p> 
        savestring = savestring.replace('<br/>','')                 #Löschen der Breaktags <br/>  
        savestring = savestring.replace('<br>','')                  #Löschen der Breaktags <br>     
        zaehler = False                                             #zaheler auf False setzen, damit die Aktion nur einmal ausgeführt wird
        print savestring                                            #Ausgabe des gefundenen Projektakronyms



# Auslesen des Projektakronyms
#h1s = root.cssselect('p') 
#for h1 in h1s:
    #savestring = lxml.html.tostring(h1)                        #umwandeln des XMLs (in dem h1 zu finden ist) in einen String
    #savestring = savestring.replace('<p>','')                 #Beschneiden des Strings um <h1>        
    #savestring = savestring.replace('</p>','')                #Beschneiden des Strings um </h1> 
    #print savestring                                           #Ausgabe des gefundenen Projektakronyms
