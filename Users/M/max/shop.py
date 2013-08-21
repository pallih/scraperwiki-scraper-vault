import scraperwiki
import lxml.html
from bs4 import BeautifulSoup

for a in range(500):
    unterseite = "http://www.schum-euroshop.de/php/show_detail.php?shopid=" + str(a) #scrapt die Shopseiten von Schum
    html = scraperwiki.scrape(unterseite)
    soup = BeautifulSoup(html)
    Laendertext = soup.get_text()
    data = dict() #Um die Daten in die Datenbank zu schreiben, muss ich eine Art Array definieren
    data['url'] = unterseite
    data['text'] = Laendertext
    print(soup) #Testausgabe in die Console
    scraperwiki.sqlite.save(unique_keys=['url'], data=data) #Ein Eintrag des Arrays dient als "unique_key" für die Datenbank

