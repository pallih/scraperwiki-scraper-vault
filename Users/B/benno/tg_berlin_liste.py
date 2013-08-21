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
    try:
        #print infos.getchildren()[0].tail
        get_adresse = infos.getchildren()[0].tail.strip().split()
    except:
        get_adresse = ["", ""]
    #print "getaddadadada", get_adresse
    plz = get_adresse[0]
    if plz.isdigit():
        entity["plz"] = plz
    else:
        entity["plz"] = ""
    try:
        entity["ort"] = get_adresse[1]
    except:
        entity["ort"] = ""
    entity["location"] = root.cssselect("h1.pagetitle")[0].text.strip()
    try:
        entity["adresse"] = infos.text.strip()
    except:
        entity["adresse"] = ""
    try:
        telefon = root.cssselect("div.sp_phone")[0]
        entity["telefon"] = telefon.text_content().strip()[8:]
    except:
        entity["telefon"] = ""
    try:
        url = root.cssselect("div.sp_www a")[0]
        entity["url"] = url.text.split()[1].strip()
    except:
        entity["url"] = ""
    #print "entityUrl: ", entity["telefon"]
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
            #raise
            pass
        if not entity == {} and entity not in result:
            result.append(entity)
    print "Result: ", result
    writeData(result)

def writeData(result):
    scraperwiki.sqlite.execute("drop table if exists tg_berlin")
    scraperwiki.sqlite.execute("create table tg_berlin ( `location` text, `adresse` text, `plz` text, `ort` text,`telefon` text, `url` text, `uid` text)")
    scraperwiki.sqlite.commit()
    for i in range(len(result)):
        location = result[i]["location"]
        plz = result[i]["plz"]
        ort = result[i]["ort"]
        adresse = result[i]["adresse"]
        telefon = result[i]["telefon"]
        url = result[i]["url"]
        uid = getUid()
        data = {"adresse": adresse, "location": location, "plz": plz, "ort": ort, "telefon": telefon, "url": url, "uid": uid}
        #print data
        scraperwiki.sqlite.save(unique_keys=["location", "plz", "ort", "uid", "adresse"], data=data, table_name="tg_berlin", verbose=7)

def main():
    siteScrape()

main()
