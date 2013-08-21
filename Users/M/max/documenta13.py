import scraperwiki
import lxml.html
from bs4 import BeautifulSoup


unterseite = "http://d13.documenta.de/de/teilnehmer/antoni-cumella/"
html = scraperwiki.scrape(unterseite)
soup = BeautifulSoup(html)
for link in soup.find_all('a'): #alle Links auf der Seite werden abgeklappert
    link = link.get('href') #Der aktuelle Link wird in der Variable "link" gespeichert
    print(link)
    if link is not None: #Test: Der Link sollte nicht leer sein, nur jeder zweite Link wird gescrapt
        if link.rfind('teilnehmer') > -1 and link.rfind('tx_') == -1: #Test: alle uns interessierenden Links sind absolute Links, haben also ein "http" am Anfang
            #if link.rfind('BASE') > -1 and link.rfind('TIT') == -1: #Test: Alle uns interessierenden Links haben "BASE" in der URL, aber nicht "TIT" - letzteres führt zu leeren Zeilen in der Ergebnisdatenbank
            link = "http://d13.documenta.de/" + link
            tml = scraperwiki.scrape(link) #Den Datenbankeintrag des Künstlers scrapen
            oup = BeautifulSoup(tml)
            text = oup.get_text()
            print(text)
            data = dict() #Um die Daten in die Ergebnisdatenbank zu schreiben, muss ich eine Art Array definieren
            data['url'] = link
            data['text'] = text
            scraperwiki.sqlite.save(unique_keys=['url'], data=data) #Ein Eintrag des Arrays dient als "unique_key" für die Datenbank


