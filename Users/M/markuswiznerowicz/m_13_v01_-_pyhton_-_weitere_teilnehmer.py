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
