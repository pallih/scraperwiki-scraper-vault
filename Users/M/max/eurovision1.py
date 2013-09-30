import scraperwiki
import lxml.html
from bs4 import BeautifulSoup

unterseite = "http://www.eurovision.de/laender/index.html"
html = scraperwiki.scrape(unterseite)
soup = BeautifulSoup(html)
for link in soup.find_all('a'): #alle Links auf der Seite werden abgeklappert
    link = link.get('href') #Der aktuelle Link wird in der Variable "link" gespeichert
    if link is not None: #Test: Der Link sollte nicht leer sein
        if link.rfind('laender') > -1 and link.rfind('index') == -1: #Test: Alle uns interessierenden Links haben "laender" in der URL, aber nicht "index"
            link = "http://www.eurovision.de/" + link #Den gefundenen Link zum absoluten Link machen
            tml = scraperwiki.scrape(link) #Die Rede scrapen
            oup = BeautifulSoup(tml)
            Laendertext = oup.get_text()
            data = dict() #Um die Daten in die Datenbank zu schreiben, muss ich eine Art Array definieren
            data['url'] = link
            data['text'] = Laendertext
            print(Laendertext) #Gibt den Text der Seite raus - das ist der Text der Rede plus noch Ã¼berflÃ¼ssigen HTML-Kram
            scraperwiki.sqlite.save(unique_keys=['url'], data=data) #Ein Eintrag des Arrays dient als "unique_key" fÃ¼r die Datenbank
import scraperwiki
import lxml.html
from bs4 import BeautifulSoup

unterseite = "http://www.eurovision.de/laender/index.html"
html = scraperwiki.scrape(unterseite)
soup = BeautifulSoup(html)
for link in soup.find_all('a'): #alle Links auf der Seite werden abgeklappert
    link = link.get('href') #Der aktuelle Link wird in der Variable "link" gespeichert
    if link is not None: #Test: Der Link sollte nicht leer sein
        if link.rfind('laender') > -1 and link.rfind('index') == -1: #Test: Alle uns interessierenden Links haben "laender" in der URL, aber nicht "index"
            link = "http://www.eurovision.de/" + link #Den gefundenen Link zum absoluten Link machen
            tml = scraperwiki.scrape(link) #Die Rede scrapen
            oup = BeautifulSoup(tml)
            Laendertext = oup.get_text()
            data = dict() #Um die Daten in die Datenbank zu schreiben, muss ich eine Art Array definieren
            data['url'] = link
            data['text'] = Laendertext
            print(Laendertext) #Gibt den Text der Seite raus - das ist der Text der Rede plus noch Ã¼berflÃ¼ssigen HTML-Kram
            scraperwiki.sqlite.save(unique_keys=['url'], data=data) #Ein Eintrag des Arrays dient als "unique_key" fÃ¼r die Datenbank
