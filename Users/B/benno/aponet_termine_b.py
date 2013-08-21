#Blank Python
# -*- coding: iso-8859-15 -*-
import scraperwiki
import lxml.html
import datetime
count_id = 12345

def getUid():
    global count_id
    count_id += 1
    return str(count_id)

def createEntity(element):
    infos = element.cssselect("p.adress")[0]
    entity = {}
    entity["location"] = element.cssselect("h2")[0].text.strip()
    entity["oeffnungszeiten"] = element.cssselect("p")[1].text_content().strip()
    try:
        entity["adresse"] = infos.text.strip()
    except:
        entity["adresse"] = ""
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
    try:
        telefon = element.cssselect("p.contact")[0]
        entity["telefon"] = telefon.text[5:].strip()
    except:
        entity["telefon"] = ""
    #print "entity: ", entity
    return entity

def siteScrape():
    dat = datetime.date.today()
    datum = dat.strftime("%d.%m.%Y")
    url = "http://www.aponet.de/service/notdienstapotheke-finden/suchergebnis/" + datum + "/10117.html"
    print "url: ", url
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    result = []
    entity = {}
    locations = root.cssselect("div.box_adress")
    for loc in locations:
        try:
            entity = createEntity(loc)
        except:
            raise
            #pass
        if not entity == {} and entity not in result:
            result.append(entity)
    print "Result: ", result
    writeData(result)

def writeData(result):
    scraperwiki.sqlite.execute("drop table if exists aponet_termine_berlin")
    scraperwiki.sqlite.execute("create table aponet_termine_berlin ( `location` text, `oeffnungszeiten` text, `adresse` text, `plz` text, `ort` text,`telefon` text)")
    scraperwiki.sqlite.commit()
    for i in range(len(result)):
        location = result[i]["location"]
        oeffnungszeiten = result[i]["oeffnungszeiten"]
        plz = result[i]["plz"]
        ort = result[i]["ort"]
        adresse = result[i]["adresse"]
        telefon = result[i]["telefon"]
        uid = getUid()
        data = {"adresse": adresse, "location": location, "plz": plz, "ort": ort, "telefon": telefon, "oeffnungszeiten": oeffnungszeiten}
        #print data
        scraperwiki.sqlite.save(unique_keys=["location", "plz", "ort", "adresse"], data=data, table_name="aponet_termine_berlin", verbose=6)

def main():
    siteScrape()

main()
