import scraperwiki
import lxml.html
from bs4 import BeautifulSoup

for a in range(21):
    b = a + 1
    unterseite = "http://www.bundeskanzlerin.de/Webs/BK/De/Aktuell/Reden/reden.html?gtp=74416_items%253D" + str(b) #klappert die Unterseiten ab, auf denen jeweils zehn Links zu Reden der Bundeskanzlerin sind - derzeit sind es 22 Unterseiten, das muss man von Hand checken.
    html = scraperwiki.scrape(unterseite)
    soup = BeautifulSoup(html)
    for link in soup.find_all('a'): #alle Links auf der Seite werden abgeklappert
        link = link.get('href') #Der aktuelle Link wird in der Variable "link" gespeichert
        if link is not None: #Test: Der Link sollte nicht leer sein
            if link.rfind('http') == -1: #Test: alle uns interessierenden Links sind relative Links, haben also kein "http" am Anfang
                    if link.rfind('Rede') > -1 and link.rfind('Reden') == -1: #Test: Alle uns interessierenden Links haben "Rede" in der URL, aber nicht "Reden" - das führt zurück zur Übersichsseite
                        link = "http://www.bundeskanzlerin.de/" + link #Den gefundenen Link zum absoluten Link machen
                        tml = scraperwiki.scrape(link) #Die Rede scrapen
                        oup = BeautifulSoup(tml)
                        Redentext = oup.get_text()
                        data = dict() #Um die Daten in die Datenbank zu schreiben, muss ich eine Art Array definieren
                        data['url'] = link
                        data['text'] = Redentext
                        print(Redentext) #Gibt den Text der Seite raus - das ist der Text der Rede plus noch überflüssigen HTML-Kram
                        scraperwiki.sqlite.save(unique_keys=['url'], data=data) #Ein Eintrag des Arrays dient als "unique_key" für die Datenbank


