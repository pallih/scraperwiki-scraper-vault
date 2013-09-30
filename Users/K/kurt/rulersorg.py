import scraperwiki
from urllib2 import urlopen
import datetime

rulerslines = []

def extract(year,month):
    url = "http://rulers.org/" + year + "-" + month + ".html"
    try:
        webpage = urlopen(url)
    except:
        print "Fehler beim Oeffnen von " + url
    else:
        for line in webpage.readlines():
            if line.startswith("<H3>"):
                day_text = line[len("<H3>"):-len("</H3> ")] #Tag aus Überschrift extrahieren
                continue
            if line.startswith("<B>"): #alle Texteinträge
                text = line.replace("<B>","").replace("</B>","").replace("<I>","").replace("</I>","").replace("<BR>","") #B- und I-Tags entfernen
                # bei neuem Text diesen ausgeben (später per E-Mail)
                if text.decode("ISO-8859-1") not in existing_texts_list:
                    #print "=== !NEU! ==="
                    #print day_text + "-" + month + "-" + year + ": " + text
                    rulerslines.append(day_text + "-" + month + "-" + year + ": " + text)
                # Daten speichern
                data = {
                    'year' : year,
                    'month' : month,
                    'day' : day_text,
                    'text' : text.decode("ISO-8859-1")
                }
                scraperwiki.sqlite.save(unique_keys=['text'], data=data)


# diesen und letzten Monat ermitteln
today = datetime.date.today()

year = today.strftime('%Y')
month = today.strftime('%m') #zweistellig, wird auch so in URL benötigt

first = datetime.date(day=1, month=today.month, year=today.year)
lastmonth = first - datetime.timedelta(days=1)
month_lastmonth = lastmonth.strftime("%m") # letzter Monat
year_lastmonth = lastmonth.strftime("%Y") # Jahr des letzten Monats 


# vorhandene Einträge (nur die Texte) aus Datenbank auslesen, um später die neuen erkennen zu können
existing_texts_list = []

try:
    existing_texts = scraperwiki.sqlite.execute("select text from swdata")
except:
    pass # Datenbank leer, Liste bleibt leer
else:
    for existing_text_data in existing_texts['data']: # Liste mit schon vorhandenen texts füllen, geht sicher schöner
        for etd in existing_text_data:
            existing_texts_list.append(etd)


#Daten extrahieren und vergleichen
extract(year_lastmonth,month_lastmonth) # für *letzten* Monat
extract(year,month) # für *diesen* Monat


if rulerslines:
    print "=== !NEU! ==="
    print rulerslines
import scraperwiki
from urllib2 import urlopen
import datetime

rulerslines = []

def extract(year,month):
    url = "http://rulers.org/" + year + "-" + month + ".html"
    try:
        webpage = urlopen(url)
    except:
        print "Fehler beim Oeffnen von " + url
    else:
        for line in webpage.readlines():
            if line.startswith("<H3>"):
                day_text = line[len("<H3>"):-len("</H3> ")] #Tag aus Überschrift extrahieren
                continue
            if line.startswith("<B>"): #alle Texteinträge
                text = line.replace("<B>","").replace("</B>","").replace("<I>","").replace("</I>","").replace("<BR>","") #B- und I-Tags entfernen
                # bei neuem Text diesen ausgeben (später per E-Mail)
                if text.decode("ISO-8859-1") not in existing_texts_list:
                    #print "=== !NEU! ==="
                    #print day_text + "-" + month + "-" + year + ": " + text
                    rulerslines.append(day_text + "-" + month + "-" + year + ": " + text)
                # Daten speichern
                data = {
                    'year' : year,
                    'month' : month,
                    'day' : day_text,
                    'text' : text.decode("ISO-8859-1")
                }
                scraperwiki.sqlite.save(unique_keys=['text'], data=data)


# diesen und letzten Monat ermitteln
today = datetime.date.today()

year = today.strftime('%Y')
month = today.strftime('%m') #zweistellig, wird auch so in URL benötigt

first = datetime.date(day=1, month=today.month, year=today.year)
lastmonth = first - datetime.timedelta(days=1)
month_lastmonth = lastmonth.strftime("%m") # letzter Monat
year_lastmonth = lastmonth.strftime("%Y") # Jahr des letzten Monats 


# vorhandene Einträge (nur die Texte) aus Datenbank auslesen, um später die neuen erkennen zu können
existing_texts_list = []

try:
    existing_texts = scraperwiki.sqlite.execute("select text from swdata")
except:
    pass # Datenbank leer, Liste bleibt leer
else:
    for existing_text_data in existing_texts['data']: # Liste mit schon vorhandenen texts füllen, geht sicher schöner
        for etd in existing_text_data:
            existing_texts_list.append(etd)


#Daten extrahieren und vergleichen
extract(year_lastmonth,month_lastmonth) # für *letzten* Monat
extract(year,month) # für *diesen* Monat


if rulerslines:
    print "=== !NEU! ==="
    print rulerslines
