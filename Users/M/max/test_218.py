import scraperwiki
html = scraperwiki.scrape("http://www.bundeskanzlerin.de/Webs/BK/De/Aktuell/Reden/reden.html")
import lxml.html
from bs4 import BeautifulSoup

soup = BeautifulSoup(html)

#scraped alle von einer Seite verlinkten Reden, in diesem Fall die zehn neuesten

for link in soup.find_all('a'): #alle Links auf der Seite werden abgeklappert
    link = link.get('href') #Der Link wird in der Variable "link" gespeichert
    if link is not None: #Test: Der Link sollte nicht leer sein
        if link.rfind('http') == -1: #Test: alle uns interessierenden Links sind relative Links, haben also kein "http" am Anfang
            if link.rfind('Rede') > -1 and link.rfind('Reden') == -1: #Test: Alle uns interessierenden Links haben "Rede" in der URL, aber nicht "Reden" - das führt zurück zur Übersichsseite
                link = "http://www.bundeskanzlerin.de/" + link #Den gefundenen Link zum absoluten Link machen
                tml = scraperwiki.scrape(link) #Die Rede scrapen
                oup = BeautifulSoup(tml)
                print(oup.get_text()) #Gibt den Text der Seite raus - das ist der Text der Rede plus noch überflüssigen HTML-Kram


import scraperwiki
html = scraperwiki.scrape("http://www.bundeskanzlerin.de/Webs/BK/De/Aktuell/Reden/reden.html")
import lxml.html
from bs4 import BeautifulSoup

soup = BeautifulSoup(html)

#scraped alle von einer Seite verlinkten Reden, in diesem Fall die zehn neuesten

for link in soup.find_all('a'): #alle Links auf der Seite werden abgeklappert
    link = link.get('href') #Der Link wird in der Variable "link" gespeichert
    if link is not None: #Test: Der Link sollte nicht leer sein
        if link.rfind('http') == -1: #Test: alle uns interessierenden Links sind relative Links, haben also kein "http" am Anfang
            if link.rfind('Rede') > -1 and link.rfind('Reden') == -1: #Test: Alle uns interessierenden Links haben "Rede" in der URL, aber nicht "Reden" - das führt zurück zur Übersichsseite
                link = "http://www.bundeskanzlerin.de/" + link #Den gefundenen Link zum absoluten Link machen
                tml = scraperwiki.scrape(link) #Die Rede scrapen
                oup = BeautifulSoup(tml)
                print(oup.get_text()) #Gibt den Text der Seite raus - das ist der Text der Rede plus noch überflüssigen HTML-Kram


