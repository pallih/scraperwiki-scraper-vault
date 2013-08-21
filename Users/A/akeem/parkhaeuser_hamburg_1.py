import scraperwiki
import lxml.html

#definiere Datenquelle (url)
html = scraperwiki.scrape("http://www.hamburger-luft.de/daisywebservlet?action=start")

#Suche den Table Header
root = lxml.html.fromstring(html)
#Es handelt sich um eine Tabelle in einer Tabelle: daher suche table table und dann das erste tr
#der header ist der inhalt der ersten zelle
header = root.cssselect("table table tr")[0] 
colums = header.cssselect("th")


for tr in root.cssselect("table table tr"):
    tds = tr.cssselect("td")
       #ignoriere die ersten zeilen, in denen kein tr drin steht
    if not len(tds): continue

    #Zeitstempel
    time = tds[0].text_content()

    #mit dem enumeate befehl wird das tabellensystem druchgegangen, damit man die zeilen später den spalten zuordnen kann
    for i, cell in enumerate(tds[1:]):

        data = {"station": colums[i+1].text_content(),
                "time": time, 
                "staub": cell.text_content()
                }
        

        scraperwiki.sqlite.save(unique_keys=["station","time"], data=data)

