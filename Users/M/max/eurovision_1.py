import scraperwiki
import lxml.html
from bs4 import BeautifulSoup

for a in range(56):
    b = a + 1956
    unterseite = "http://www.eurovision.de/geschichte/geschichte383_jahr-" + str(b) + ".html" #scrapt die einzelnen Jahresseiten der Eurovisionsseite
    html = scraperwiki.scrape(unterseite)
    soup = BeautifulSoup(html)
    Laendertext = soup.get_text()
    data = dict() #Um die Daten in die Datenbank zu schreiben, muss ich eine Art Array definieren
    data['url'] = unterseite
    data['Jahr'] = str(b)
    data['text'] = Laendertext
    data['Gewinner'] = soup.find("h2") #das Gewinnerland des jeweiligen Jahres steht auf der Seite nach dem ersten <h2>-tag
    print(soup.find("h2")) #Testausgabe in die Console
    scraperwiki.sqlite.save(unique_keys=['url'], data=data) #Ein Eintrag des Arrays dient als "unique_key" für die Datenbank

