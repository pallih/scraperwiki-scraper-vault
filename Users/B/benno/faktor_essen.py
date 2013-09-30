#Blank Python
# -*- coding: iso-8859-15 -*-
import scraperwiki
import lxml.html
import datetime

html = scraperwiki.scrape("http://stressfaktor.squat.net/vokue.php?day=all")
root = lxml.html.fromstring(html)

def createWochentag(element, tag):
    veranstaltungen = []
    span = element.cssselect("span.text2")[1]
    for ort in span.cssselect("a"):
        veranstaltung = {}
        veranstaltung["tag"] = tag
        veranstaltung["ort"] = ort.text.strip()
        zeit = ort.getparent().tail
        veranstaltung["info"] = zeit[1:].strip()
        veranstaltungen.append(veranstaltung)
    return veranstaltungen

def siteScrape():
    result = []
    wochentage = [u"Montag", u"Dienstag", u"Mittwoch", u"Donnerstag", u"Freitag", u"Samstag", u"Sonntag"]
    tables = root.cssselect("table")
    for tab in tables:
        try:
            wochentag = tab.cssselect("tr td span b")[0].text.strip()
        except:
            wochentag = u"nü"
        if  wochentag in wochentage:
            tag = createWochentag(tab, wochentag)
            if not tag in result:
                result.append(tag)
    #print "Result: ", result
    writeData(result)

def writeData(result):
    scraperwiki.sqlite.execute("drop table if exists faktor_essen_berlin")
    scraperwiki.sqlite.execute("create table faktor_essen_berlin ( `tag` text, `ort` text, `info` text)")
    scraperwiki.sqlite.commit()
    for i in range(len(result)):
        for j in range(len(result[i])):
            ort = result[i][j]["ort"]
            info = result[i][j]["info"]
            tag = result[i][j]["tag"]
            programm = {"info": info, "tag": tag, "ort": ort}
            scraperwiki.sqlite.save(unique_keys=["tag", "info", "ort"], data=programm, table_name="faktor_essen_berlin", verbose=3)

def main():
    siteScrape()

main()
#Blank Python
# -*- coding: iso-8859-15 -*-
import scraperwiki
import lxml.html
import datetime

html = scraperwiki.scrape("http://stressfaktor.squat.net/vokue.php?day=all")
root = lxml.html.fromstring(html)

def createWochentag(element, tag):
    veranstaltungen = []
    span = element.cssselect("span.text2")[1]
    for ort in span.cssselect("a"):
        veranstaltung = {}
        veranstaltung["tag"] = tag
        veranstaltung["ort"] = ort.text.strip()
        zeit = ort.getparent().tail
        veranstaltung["info"] = zeit[1:].strip()
        veranstaltungen.append(veranstaltung)
    return veranstaltungen

def siteScrape():
    result = []
    wochentage = [u"Montag", u"Dienstag", u"Mittwoch", u"Donnerstag", u"Freitag", u"Samstag", u"Sonntag"]
    tables = root.cssselect("table")
    for tab in tables:
        try:
            wochentag = tab.cssselect("tr td span b")[0].text.strip()
        except:
            wochentag = u"nü"
        if  wochentag in wochentage:
            tag = createWochentag(tab, wochentag)
            if not tag in result:
                result.append(tag)
    #print "Result: ", result
    writeData(result)

def writeData(result):
    scraperwiki.sqlite.execute("drop table if exists faktor_essen_berlin")
    scraperwiki.sqlite.execute("create table faktor_essen_berlin ( `tag` text, `ort` text, `info` text)")
    scraperwiki.sqlite.commit()
    for i in range(len(result)):
        for j in range(len(result[i])):
            ort = result[i][j]["ort"]
            info = result[i][j]["info"]
            tag = result[i][j]["tag"]
            programm = {"info": info, "tag": tag, "ort": ort}
            scraperwiki.sqlite.save(unique_keys=["tag", "info", "ort"], data=programm, table_name="faktor_essen_berlin", verbose=3)

def main():
    siteScrape()

main()
