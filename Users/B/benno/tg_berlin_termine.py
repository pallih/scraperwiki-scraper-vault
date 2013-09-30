#Blank Python
# -*- coding: iso-8859-15 -*-
import scraperwiki
import lxml.html
import datetime

html = scraperwiki.scrape("https://www.tg-berlin.de/alle-veranstaltungen/spielstaetten.html")
root = lxml.html.fromstring(html)
count_id = 12345

def getUid():
    global count_id
    count_id += 1
    return str(count_id)

def createEntity(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    infos = root.cssselect("div.sp_address p")[0]
    entity = {}
    entity["location"] = root.cssselect("h1.pagetitle")[0].text.strip()
    programm = []
    try:
        termine = root.cssselect("div.veranstaltungSingleView")
        #print termine
        for termin in termine:
            termin_data = {}
            termin_data["genre"] = termin.cssselect("div.tx_tgbveranstaltung_genre")[0].text.strip()
            termin_data["name"] = termin.cssselect("div.tx_tgbveranstaltung_werk h3")[0].text_content().strip()
            termin_data["datum"] = termin.cssselect("span.dateStart")[0].text.strip().split(",")[0][4:]
            termin_data["zeit"] = termin.cssselect("span.dateStart")[0].text.strip().split(",")[1].split()[0].strip()
            termin_data["preis"] = termin.cssselect("span.dateStart")[1].text.strip()[6:]
            #print "termine: ", termin_data
            programm.append(termin_data)
    except:
        raise
        print "keine termine"
    entity["termine"] = programm
    #print "entity: ", entity
    return entity

def siteScrape():
    result = []
    entity = {}
    locations = root.cssselect("div.spielstaette a")
    for loc in locations:
        try:
            url = "https://www.tg-berlin.de/" + loc.attrib["href"]
            entity = createEntity(url)
        except:
            raise
            #pass
        if not entity == {} and entity not in result:
            result.append(entity)
    print "Result: ", result
    writeData(result)

def writeData(result):
    scraperwiki.sqlite.execute("drop table if exists tg_berlin_termine")
    scraperwiki.sqlite.execute("create table tg_berlin_termine ( `name` text, `genre` text, `datum` text, `zeit` text, `preis` text, `location` text)")
    scraperwiki.sqlite.commit()
    for i in range(len(result)):
        location = result[i]["location"]
        for t in range(len(result[i]["termine"])):
            genre = result[i]["termine"][t]["genre"]
            name = result[i]["termine"][t]["name"]
            datum = result[i]["termine"][t]["datum"]
            zeit = result[i]["termine"][t]["zeit"]
            preis = result[i]["termine"][t]["preis"]           
            data = {"location": location, "genre": genre, "name": name, "datum": datum, "zeit": zeit, "preis": preis}
            #print data
            scraperwiki.sqlite.save(unique_keys=["location", "genre", "name", "datum", "zeit", "preis"], data=data, table_name="tg_berlin_termine", verbose=6)

def main():
    siteScrape()

main()
#Blank Python
# -*- coding: iso-8859-15 -*-
import scraperwiki
import lxml.html
import datetime

html = scraperwiki.scrape("https://www.tg-berlin.de/alle-veranstaltungen/spielstaetten.html")
root = lxml.html.fromstring(html)
count_id = 12345

def getUid():
    global count_id
    count_id += 1
    return str(count_id)

def createEntity(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    infos = root.cssselect("div.sp_address p")[0]
    entity = {}
    entity["location"] = root.cssselect("h1.pagetitle")[0].text.strip()
    programm = []
    try:
        termine = root.cssselect("div.veranstaltungSingleView")
        #print termine
        for termin in termine:
            termin_data = {}
            termin_data["genre"] = termin.cssselect("div.tx_tgbveranstaltung_genre")[0].text.strip()
            termin_data["name"] = termin.cssselect("div.tx_tgbveranstaltung_werk h3")[0].text_content().strip()
            termin_data["datum"] = termin.cssselect("span.dateStart")[0].text.strip().split(",")[0][4:]
            termin_data["zeit"] = termin.cssselect("span.dateStart")[0].text.strip().split(",")[1].split()[0].strip()
            termin_data["preis"] = termin.cssselect("span.dateStart")[1].text.strip()[6:]
            #print "termine: ", termin_data
            programm.append(termin_data)
    except:
        raise
        print "keine termine"
    entity["termine"] = programm
    #print "entity: ", entity
    return entity

def siteScrape():
    result = []
    entity = {}
    locations = root.cssselect("div.spielstaette a")
    for loc in locations:
        try:
            url = "https://www.tg-berlin.de/" + loc.attrib["href"]
            entity = createEntity(url)
        except:
            raise
            #pass
        if not entity == {} and entity not in result:
            result.append(entity)
    print "Result: ", result
    writeData(result)

def writeData(result):
    scraperwiki.sqlite.execute("drop table if exists tg_berlin_termine")
    scraperwiki.sqlite.execute("create table tg_berlin_termine ( `name` text, `genre` text, `datum` text, `zeit` text, `preis` text, `location` text)")
    scraperwiki.sqlite.commit()
    for i in range(len(result)):
        location = result[i]["location"]
        for t in range(len(result[i]["termine"])):
            genre = result[i]["termine"][t]["genre"]
            name = result[i]["termine"][t]["name"]
            datum = result[i]["termine"][t]["datum"]
            zeit = result[i]["termine"][t]["zeit"]
            preis = result[i]["termine"][t]["preis"]           
            data = {"location": location, "genre": genre, "name": name, "datum": datum, "zeit": zeit, "preis": preis}
            #print data
            scraperwiki.sqlite.save(unique_keys=["location", "genre", "name", "datum", "zeit", "preis"], data=data, table_name="tg_berlin_termine", verbose=6)

def main():
    siteScrape()

main()
