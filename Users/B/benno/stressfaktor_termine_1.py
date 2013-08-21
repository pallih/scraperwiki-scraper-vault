#Blank Python
# -*- coding: iso-8859-15 -*-
import scraperwiki
import lxml.html
import datetime

html = scraperwiki.scrape("http://stressfaktor.squat.net/termine.php?display=7")
root = lxml.html.fromstring(html)

def createWochentag(element, tag, datum):
    veranstaltungen = []
    trow = element.cssselect("tr")
    #print "RRRRRRRRR", len(trow)
    for tr in trow[1:len(trow)]:
        if tr.attrib["bgcolor"] == u"#ffffff":
            #print "3. "
            veranstaltung = {}
            veranstaltung["tag"] = tag
            veranstaltung["datum"] = datum
            veranstaltung["zeit"] = tr.cssselect("td")[0].text_content().split(" ")[0]
            veranstaltung["ort"] = tr.cssselect("td")[1].cssselect("b")[0].text_content()
            art =  tr.cssselect("td")[1].cssselect("b")[0].tail
            veranstaltung["art"] = art[2:]
            veranstaltung["info"] = tr.cssselect("td")[1].getchildren()[0].cssselect("br")[0].tail
            veranstaltungen.append(veranstaltung)
    #span = element.cssselect("tr td span.text2")[1]
    #print "2. ", veranstaltungen
    #for ort in span.cssselect("b"):
    return veranstaltungen

def siteScrape():
    result = []
    #wochentage = [u"Montag", u"Dienstag", u"Mittwoch", u"Donnerstag", u"Freitag", u"Samstag", u"Sonntag"]
    tables = root.cssselect("table")
    for tab in tables:
        try:
            wochentag = tab.cssselect("tr td span.text2 b")[0].text.strip().split(",")[0]
            datum = tab.cssselect("tr td span.text2 b")[0].text.strip().split(",")[1]
            #print "1. ", wochentag, datum
            tag = createWochentag(tab, wochentag, datum)
            if not tag in result:
                result.append(tag)
        except:
            wochentag = u"nü"
        #if  wochentag in wochentage:

    print "Result: ", result
    writeData(result)

def writeData(result):
    scraperwiki.sqlite.execute("drop table if exists faktor_termine_berlin")
    scraperwiki.sqlite.execute("create table faktor_termine_berlin ( `tag` text, `ort` text, `zeit` text, `datum` text, `art` text, `info` text)")
    scraperwiki.sqlite.commit()
    for i in range(len(result)):
        for j in range(len(result[i])):
            ort = result[i][j]["ort"]
            info = result[i][j]["info"]
            tag = result[i][j]["tag"]
            datum = result[i][j]["datum"]
            zeit = result[i][j]["zeit"]
            art = result[i][j]["art"]
            data = {"info": info, "tag": tag, "ort": ort, "zeit": zeit, "datum": datum, "art": art}
            scraperwiki.sqlite.save(unique_keys=["tag", "info", "ort"], data=data, table_name="faktor_termine_berlin", verbose=6)

def main():
    siteScrape()

main()
