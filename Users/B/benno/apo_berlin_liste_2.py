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

def createEntity(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    infos = root.cssselect("address.vcard")[0]
    entity = {}
    entity["detail_url"] = url
    entity["location"] = root.cssselect("h2")[0].text.strip()
    try:
        entity["adresse"] = infos.cssselect("span.street-address")[0].text.strip()
    except:
        entity["adresse"] = ""
    try:
        plz = infos.cssselect("span.postal-code")[0].text.strip()
        if plz.isdigit():
            entity["plz"] = plz
        else:
            entity["plz"] = ""
    except:
        entity["plz"] = ""
    try:
        entity["ort"] = infos.cssselect("span.locality")[0].text.strip()
    except:
        entity["ort"] = ""
    try:
        entity["telefon"] = infos.cssselect("span.tel")[0].text.strip().replace("\s", "")
    except:
        entity["telefon"] = ""
    try:
        entity["url"] = infos.cssselect("a.url")[0].attrib["href"]
    except:
        entity["url"] = ""
    try:
        entity["latitude"] = root.cssselect("span.latitude")[0].text.strip()
    except:
        entity["latitude"] = ""
    try:
        entity["longitude"] = root.cssselect("span.longitude")[0].text.strip()
    except:
        entity["longitude"] = ""

    #print "entity: ", entity
    return entity

def siteScrape():
    result = []
    url_parent_list = ["http://www.med-kolleg.de/apotheke/Berlin/Berlin.html"]
    url_list = []
    entity = {}
    b = 20
    e = 40
    while e < 860:
        url_parent_list.append("http://www.med-kolleg.de/apotheke/Berlin/Berlin/" + str(b) + "/" + str(e) + ".html")
        b += 20
        e += 20
    print "len(parents... ", len(url_parent_list), url_parent_list
    for el in url_parent_list:
        html = scraperwiki.scrape(el)
        root = lxml.html.fromstring(html)
        locations = root.cssselect("span.adr")
        for loc in locations:
            try:
                url = "http://www.med-kolleg.de" + loc.cssselect("a.url")[0].attrib["href"]
                url_list.append(url)
            except:
                raise
                pass
    for loc in url_list:
        #print "loc   :   ", loc
        entity = createEntity(loc)
        if not entity == {} and entity not in result:
            result.append(entity)
    print "Result: ", result
    writeData(result)

def writeData(result):
    scraperwiki.sqlite.execute("drop table if exists apo_berlin_liste")
    scraperwiki.sqlite.execute("create table apo_berlin_liste ( `location` text, `adresse` text, `plz` text, `ort` text, `telefon` text, `longitude` text, `latitude` text, `detail_url` text, `url` text, `uid` text)")
    scraperwiki.sqlite.commit()
    for i in range(len(result)):
        location = result[i]["location"]
        plz = result[i]["plz"]
        ort = result[i]["ort"]
        adresse = result[i]["adresse"]
        telefon = result[i]["telefon"]
        detail_url = result[i]["detail_url"]
        url = result[i]["url"]
        longitude = result[i]["longitude"]
        latitude = result[i]["latitude"]
        uid = getUid()
        data = {"adresse": adresse, "location": location, "plz": plz, "ort": ort, "telefon": telefon, "detail_url": detail_url, "url": url, "longitude": longitude, "latitude": latitude, "uid": uid}
        #print data
        scraperwiki.sqlite.save(unique_keys=["location", "plz", "ort", "uid", "adresse"], data=data, table_name="apo_berlin_liste", verbose=10)

def main():
    siteScrape()

main()
