import scraperwiki
import lxml.html
from bs4 import BeautifulSoup


unterseite = "https://en.wikipedia.org/wiki/Category:Olympic_gold_medalists"
html = scraperwiki.scrape(unterseite, user_agent='Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')
soup = BeautifulSoup(html)
for link in soup.find_all('a'): #alle Links auf der Seite werden abgeklappert
    link = link.get('href') #Der aktuelle Link wird in der Variable "link" gespeichert
    print(link)
    if link is not None: #Test: Der Link sollte nicht leer sein, nur jeder zweite Link wird gescrapt
        if link.rfind('for') > -1: #Test: alle uns interessierenden Links haben "for" im Linktext
            link = "https://en.wikipedia.org/" + link
            tml = scraperwiki.scrape(link) #Den Datenbankeintrag des Künstlers scrapen
            oup = BeautifulSoup(tml)
            text = oup.get_text()
            print(text)
            data = dict() #Um die Daten in die Ergebnisdatenbank zu schreiben, muss ich eine Art Array definieren
            data['url'] = link
            data['text'] = text
            scraperwiki.sqlite.save(unique_keys=['url'], data=data) #Ein Eintrag des Arrays dient als "unique_key" für die Datenbank


