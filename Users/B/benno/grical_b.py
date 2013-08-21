#Blank Python
# -*- coding: iso-8859-15 -*-
import scraperwiki
import lxml.html
import datetime

html = scraperwiki.scrape("http://grical.org/s/?query=Berlin")
root = lxml.html.fromstring(html)
count_id = 12345

def getUid():
    global count_id
    count_id += 1
    return str(count_id)

def getData(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    details = {}
    adresse = plz = ort = u""
    #ort = "Berlin"
    try:
        data = root.cssselect("div.data")[1].text.split(",")
        #print data
        adresse = data[0].strip() + ", " + data[1].strip()
        try:
            plz_list = data[3].split(u"\xa0 \u2014 \xa0")
        except:
            try:
                plz_list = data[2].split(u"\xa0 \u2014 \xa0") 
            except:                
                plz_list = data[1].split(u"\xa0 \u2014 \xa0")
                adresse = data[0].strip() + ", " + data[1].strip().split()[0] + data[1].strip().split()[1]
                print "adresse : ", adresse
        try:
            plz = plz_list[1].replace("\n", "").strip()        
            ort = plz_list[2].replace("\n", "").strip()
        except:
            #ort = "Berlinkllklklklklklklklkl"
            if plz_list[0].replace("\n", "").strip()[:5].isdecimal():
                plz = plz_list[0].replace("\n", "").strip()[:5]
            #print "PLZZZ_XXXXXXXXXXXXXXXXXXX: ", plz
        if ort == u"" and len(data) > 3:
            ort_list = data[2].strip().split()
            #print "ZZZZZZZZZZZZZ : ", ort_list, len(ort_list)
            if len(ort_list) > 1:
                ort = ort_list[1]
                plz = ort_list[0]
            else:
                ort = ort_list[0]
        #print "hvkhvkhvgh ", ort
        #print "plz   ", plz
        if ort == u"":
            ort = "Berlin"
        details["adresse"] = adresse
        details["plz"] = plz
        details["ort"] = ort
    except:
        #raise
        #print "N.N.       !!!!!!!!!!!!!!!!!"
        if ort == u"":
            ort = "Berlin"
        details["adresse"] = adresse
        details["plz"] = plz
        details["ort"] = ort
    return details


def createEntity(element):
    entities = []
    event_mediums = element.cssselect("div.event_medium")
    for day in event_mediums:
        entity = {}
        entity["title"] = day.cssselect("div.title")[0].getchildren()[1].text_content()
        entity["url"] = "http://grical.org" + day.cssselect("div.title")[0].getchildren()[1].attrib["href"]
        date_list = day.cssselect("span.date a")
        tags = ""
        if len(date_list) > 1:
            date_bis = date_list[1].text
        else:
            date_bis = ""
        entity["datum"] = date_list[0].text
        entity["datum_bis"] = date_bis
        try:
            entity["deadlines"] = day.cssselect("span.deadlines a")[0].text.strip()
        except:
            entity["deadlines"] = ""
        try:
            entity["time"] = day.cssselect("span.time")[0].text
        except:
            entity["time"] = ""
        for el in day.cssselect("div.tags a"):
            tags = tags + el.text_content() + ", "
            entity["tags"] = tags
        details = getData(entity["url"])
        entity["adresse"] = details["adresse"]
        entity["plz"] = details["plz"]
        entity["ort"] = details["ort"]
        print "entity ", entity
        entities.append(entity)
    #print entities
    return entities

def siteScrape():
    result = []
    boxes = root.cssselect("div.daybox")
    for daybox in boxes:
        entity = createEntity(daybox)
        if not entity in result:
            result.append(entity)
    print "Result: ", result
    writeData(result)

def writeData(result):
    scraperwiki.sqlite.execute("drop table if exists grical_berlin")
    scraperwiki.sqlite.execute("create table grical_berlin ( `title` text, `datum` text, `datum_bis` text, `deadlines` text, `time` text, `adresse` text, `plz` text, `ort` text, `tags` text, `uid` text, `url` text)")
    scraperwiki.sqlite.commit()
    for i in range(len(result)):
        for j in range(len(result[i])):
            title = result[i][j]["title"]
            plz = result[i][j]["plz"]
            ort = result[i][j]["ort"]
            adresse = result[i][j]["adresse"]
            url = result[i][j]["url"]
            datum = result[i][j]["datum"]
            datum_bis = result[i][j]["datum_bis"]
            deadlines = result[i][j]["deadlines"]
            time = result[i][j]["time"]
            tags = result[i][j]["tags"]
            uid = getUid()
            data = {"title": title, "url": url, "datum": datum, "datum_bis": datum_bis, "deadlines": deadlines, "time": time, "adresse": adresse, "plz": plz, "ort": ort, "tags": tags, "uid": uid}
            scraperwiki.sqlite.save(unique_keys=["title", "url", "datum", "datum_bis", "deadlines", "time", "adresse", "plz", "ort", "tags", "uid"], data=data, table_name="grical_berlin", verbose=11)

def main():
    siteScrape()

main()
