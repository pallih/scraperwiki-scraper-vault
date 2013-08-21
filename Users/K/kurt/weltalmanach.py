# -*- coding: utf_8 -*-

from bs4 import BeautifulSoup
from urllib2 import urlopen
import scraperwiki

url = 'http://www.weltalmanach.de/'
webseite = urlopen(url)
soup = BeautifulSoup(webseite)
items = soup.find_all('div', 'item')

#emaillibrary = scraperwiki.utils.swimport("general-emails-on-scrapers")
#subjectline, headerlines, bodylines, footerlines = emaillibrary.EmailMessageParts("onlyexceptions")

almanachlines = [] # hier werden neue Einträge gesammelt

existing_key_list = []


# vorhandene Einträge (nur die Keys) aus Datenbank auslesen, um später die neuen erkennen zu können

try:
    existing_keys = scraperwiki.sqlite.execute("select key from swdata")
except:
    pass # Datenbank leer, Liste bleibt leer
else:
    for existing_key_data in existing_keys['data']: # Liste mit schon vorhandenen keys füllen, geht sicher schöner
        for ekd in existing_key_data:
            existing_key_list.append(ekd)       


# Scrapen, ggf. E-Mail-Text vorbereiten, Daten speichern

for item in items:
    month = item.find_all('div', 'month')
    if len(month) == 0: # erstes Item ohne Monat = Ende der gesuchten Items erreicht
        break
    month_string = month[0].string
    year = item.find_all('div', 'year')
    year_string = year[0].string
    day = item.find_all('div', 'day')
    day_string = day[0].string
    infos = item.find_all('div', 'info')
    infosH2 = infos[0].find_all('h2')    
    thema_string = infosH2[0].string
    infosP = infos[0].find_all('p')
    text_string = infosP[0].string    
    
    key = year_string + "-" + month_string + "-" + day_string + "-" + thema_string.replace(" ", "_")
    
    # bei neuem Eintrag diesen in E-Mail-Text speichern
    if key not in existing_key_list:
        almanachlines.append("Datum: " + year_string + "-" + month_string + "-" + day_string)
        almanachlines.append("Thema: " + thema_string.encode('ascii', 'replace'))
        almanachlines.append("Aenderung: " + text_string.encode('ascii', 'replace'))
        almanachlines.append("")
    
    # Daten des Eintrags speichern
    data = {
        'key' : key,
        'day' : day_string,
        'month' : month_string,
        'year' : year_string,
        'thema' : thema_string.encode("utf-8"),
        'text' : text_string.encode("utf-8")
    }
    scraperwiki.sqlite.save(unique_keys=['key'], data=data)


if almanachlines:
    print "=== !NEU! ==="
    print almanachlines

# am Ende E-Mail ausgeben
#subjectline += " und Aenderungen im Weltalmanach"
#if bodylines or almanachlines:
#    if not bodylines:
#        headerlines, footerlines = [ ], [ ]   # kill off cruft surrounding no message
#    print "\n".join([subjectline] + almanachlines + headerlines + bodylines + footerlines)

