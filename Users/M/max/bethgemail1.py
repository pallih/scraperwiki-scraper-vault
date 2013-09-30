import scraperwiki
import lxml.html
from bs4 import BeautifulSoup

#bethge = "file:///C:/test/bethgetest.htm"
html = scraperwiki.scrape()
soup = BeautifulSoup(html)
print(soup)
for link in soup.find_all('a'): #alle Links auf der Seite werden abgeklappert
    link = link.get('href') #Der aktuelle Link wird in der Variable "link" gespeichert
    if link is not None: #Test: Der Link sollte nicht leer sein
        if link.rfind('pdf') == -1: #Test: PDFs wollen wir nicht scrapen
            print(link)
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

#bethge = "file:///C:/test/bethgetest.htm"
html = scraperwiki.scrape()
soup = BeautifulSoup(html)
print(soup)
for link in soup.find_all('a'): #alle Links auf der Seite werden abgeklappert
    link = link.get('href') #Der aktuelle Link wird in der Variable "link" gespeichert
    if link is not None: #Test: Der Link sollte nicht leer sein
        if link.rfind('pdf') == -1: #Test: PDFs wollen wir nicht scrapen
            print(link)
            link = "http://www.eurovision.de/" + link #Den gefundenen Link zum absoluten Link machen
            tml = scraperwiki.scrape(link) #Die Rede scrapen
            oup = BeautifulSoup(tml)
            Laendertext = oup.get_text()
            data = dict() #Um die Daten in die Datenbank zu schreiben, muss ich eine Art Array definieren
            data['url'] = link
            data['text'] = Laendertext
            print(Laendertext) #Gibt den Text der Seite raus - das ist der Text der Rede plus noch Ã¼berflÃ¼ssigen HTML-Kram
            scraperwiki.sqlite.save(unique_keys=['url'], data=data) #Ein Eintrag des Arrays dient als "unique_key" fÃ¼r die Datenbank
