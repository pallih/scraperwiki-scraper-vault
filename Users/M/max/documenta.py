import scraperwiki
import lxml.html
from bs4 import BeautifulSoup

for a in range(500):
    b = a + 1
    unterseite = "http://alephino.documentaarchiv.de/alipac/LWHODLDGDKNCDDMLFXEY-05393/sysix?START=" + str(1 + (b-1)*10) #klappert die Suchergebnisseiten ab, auf denen jeweils zehn Links zu Künstlern der gesuchten documenta stehen - wieviele Unterseiten es gibt, ist egal, Hauptsache, die Schleife ist lang genug, um alle Unterseiten zu erfassen (der Rest der Schleife produziert einfach keine Daten). Achtung, die Seite produziert nach einiger Zeit einen Session-Timeout, dann auf der Datenbankseite neu suchen und den Link hier ersetzen!
    html = scraperwiki.scrape(unterseite)
    soup = BeautifulSoup(html)
    Linkzaehler = 0
    for link in soup.find_all('a'): #alle Links auf der Seite werden abgeklappert
        link = link.get('href') #Der aktuelle Link wird in der Variable "link" gespeichert
        if Linkzaehler == 0: #Es gibt auf jeder Seite zwei Links zum gleichen Datenbankeintrag.
            Linkzaehler = 1 #Leider sind diese Links nicht identisch. Deswegen muss ich zählen, um nur jeden zweiten Link zu scrapen
        else:
            Linkzaehler = 0 #"Linkzaehler" wird abwechselnd auf 1 und 0 gesetzt.
        if link is not None and Linkzaehler == 1: #Test: Der Link sollte nicht leer sein, nur jeder zweite Link wird gescrapt
            if link.rfind('http') > -1: #Test: alle uns interessierenden Links sind absolute Links, haben also ein "http" am Anfang
                    if link.rfind('BASE') > -1 and link.rfind('TIT') == -1: #Test: Alle uns interessierenden Links haben "BASE" in der URL, aber nicht "TIT" - letzteres führt zu leeren Zeilen in der Ergebnisdatenbank
                        tml = scraperwiki.scrape(link) #Den Datenbankeintrag des Künstlers scrapen
                        oup = BeautifulSoup(tml)
                        data = dict() #Um die Daten in die Ergebnisdatenbank zu schreiben, muss ich eine Art Array definieren
                        data['url'] = link
                        NAMEflag = 0 #Diese Flags sind nötig, weil immer in einer Tabellenzeile steht, welche Daten in der nächsten Tabellenzeile folgen.
                        GDflag = 0
                        GLflag = 0
                        WOHNflag = 0
                        SEXflag = 0
                        for td in oup.find_all('td'): #Über alle Tabelleneinträge im Datenbankeintrag des Künstlers iterieren
                            tag_text = td.string #Der Text des aktuellen Tabelleneintrags
                            hz = 0
                            if NAMEflag == 1:
                                for child in td.descendants: #Der Name steht innerhalb eines Links, also eines a-Tags
                                    Name = unicode(child.string) #Der a-Tag ist "Child" des td-Tags; dort müssen wir den Namen auslesen
                                    #print(Name)
                                    hz = hz + 1
                                    #print(hz)
                                    if hz == 2:
                                        #print('Name zu schreiben' + Name)  
                                        data['Name'] = Name
                                        #print('Name geschrieben')                            
                                NAMEflag = 0
                            if 'Name' in unicode(td.string):
                                #print('Name erkannt')
                                NAMEflag = 1
                                #hz = 0
                            if GDflag == 1:
                                data['Geburtsdaten'] = unicode(tag_text)
                                #print('Geburtsdaten geschrieben')
                                #print(tag_text)
                                GDflag = 0
                            if 'Geburtsdaten' in unicode(td.string): #Wenn in einer Tabellenzeile "Geburtsdaten" steht, stehen in der nächsten die Geburtsdaten
                                #print('Geburtsdaten erkannt')
                                GDflag = 1 #Das Flag zeigt an, dass in der nächsten Zeile die Geburtsdaten stehen - die wir speichern wollen.
                            if GLflag == 1:
                                data['Geburtsland'] = unicode(tag_text)
                                #print('Geburtsland geschrieben')
                                #print(tag_text)
                                GLflag = 0
                            if 'Geburtsland' in unicode(td.string):
                                #print('Geburtsland erkannt')
                                GLflag = 1
                            if WOHNflag == 1:
                                data['Wirkungsland'] = unicode(tag_text)
                                #print('Geschlecht geschrieben')
                                #print(tag_text)
                                WOHNflag = 0
                            if 'Wirkungsland' in unicode(td.string):
                                #print('Geschlecht erkannt')
                                WOHNflag = 1
                            if SEXflag == 1:
                                data['Geschlecht'] = unicode(tag_text)
                                #print('Geschlecht geschrieben')
                                #print(tag_text)
                                SEXflag = 0
                            if 'Geschlecht' in unicode(td.string):
                                #print('Geschlecht erkannt')
                                SEXflag = 1
                        scraperwiki.sqlite.save(unique_keys=['url'], data=data) #Ein Eintrag des Arrays dient als "unique_key" für die Datenbank


