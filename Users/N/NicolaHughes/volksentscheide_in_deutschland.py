import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://www.mehr-demokratie.de/volkentscheide-in-deutschland.html")
root = lxml.html.fromstring(html)
for tr in root.cssselect("table[class='contenttable contenttable-0'] tr"):
    tds = tr.cssselect("td")
    tds = [td.text_content().encode('utf-8').replace("&quot;", "") for td in tds]
    if len(tds)>1:
        data = {'Nr' : tds[0],'Datum VE' : tds[1],'Land' : tds[2],'Gegenstand' : tds[3],'Initiatoren' : tds[4],'Unterstuetzer' : tds[5],'Ergfolg-formal' : tds[6], 'Ergfolg-faktisch' : tds[6], 'Nachgeschichte' : tds[6], 'Abstimmungs-beteiligung' : tds[6], 'Fuer VB' : tds[6], 'Fuer VB in prozent der Wahl-berechtigten' : tds[6]}
        print data
        scraperwiki.sqlite.save(['Nr', 'Datum VE', 'Gegenstand'], data)