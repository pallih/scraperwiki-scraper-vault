#Blank Python
# -*- coding: iso-8859-15 -*-
import scraperwiki
import lxml.html
import datetime
from string import maketrans

html = scraperwiki.scrape("http://stressfaktor.squat.net/adressen.php")
root = lxml.html.fromstring(html)
count_id = 12345

def getUid(location, plz):
    #global count_id
    #count_id += 1
    identi = (plz + location).lower()
    #print identi
    #intab = u"abcdefghij -()!.,\\xfkroz\'\xf\'"
    #outtab = "0123456789012345678901234"
    #trantab = maketrans(intab, outtab)
    new_identi = identi.replace(" ", "")
    print new_identi
    return new_identi

def createEntity(element, location):
    span = element.cssselect("span.text2")[0]
    entity = {}
    try:
        get_adresse = span.getchildren()[1].tail.split(",")
    except:
        get_adresse = ["", "kein ort"]
    #print "getaddadadada", get_adresse
    try:
        get_ovm_info = span.getchildren()[2].tail
    except:
        get_ovm_info = u""
    if  get_ovm_info == None:
        get_ovm_info = u""
    plz = get_adresse[1].split()[0] 
    if plz.isdigit():
        entity["plz"] = plz
    else:
        entity["plz"] = ""
    try:
        entity["ort"] = get_adresse[1].split()[1]
    except:
        entity["ort"] = "Berlin"
    entity["location"] = location
    entity["adresse"] = get_adresse[0]
    entity["ovm_info"] = get_ovm_info.strip()
    info = element.cssselect("span.text2")[1].text
    if info == None :
        #print "ATTENTION:  da sind noch \r\n 's drinne evtl entfernen!!!!!?????!!!!???"
        info = element.cssselect("span.text2")[1].text_content()
    try:
        for child in element.cssselect("span.text2")[1].getchildren():
            info = info + u"" + child.tail + u""
    except:
        #print "EXCEPT"
        if  info == None:
            info = ""
    #print info
    entity["info"] = info
    #print entity
    return entity

def siteScrape():
    result = []
    entity = {}
    tables = root.cssselect("table")
    for tab in tables:
        try:
            orte = tab.cssselect("span.text2 b a")[0].text_content().strip()
        except:
            try:
                orte = tab.cssselect("span.text2 b")[0].text_content().strip()
            except:
                orte = u""
        if not orte == u"":
            #print "orte ", orte
            entity = createEntity(tab, orte)
        if not entity == {} and entity not in result:
            result.append(entity)
    #print "Result: ", result
    writeData(result)

def writeData(result):
    scraperwiki.sqlite.execute("drop table if exists faktor_adressen_berlin")
    scraperwiki.sqlite.execute("create table faktor_adressen_berlin ( `location` text, `adresse` text, `plz` text, `ort` text, `ovm_info` text, `info` text, `uid` text)")
    scraperwiki.sqlite.commit()
    for i in range(len(result)):
        location = result[i]["location"]
        plz = result[i]["plz"]
        ort = result[i]["ort"]
        adresse = result[i]["adresse"]
        ovm_info = result[i]["ovm_info"]
        info = result[i]["info"]
        uid = getUid(location, plz)
        data = {"info": info, "adresse": adresse, "location": location, "plz": plz, "ort": ort, "ovm_info": ovm_info, "uid": uid}
        #print data
        scraperwiki.sqlite.save(unique_keys=["ovm_info", "info", "ort", "uid", "adresse"], data=data, table_name="faktor_adressen_berlin", verbose=7)

def main():
    siteScrape()

main()
