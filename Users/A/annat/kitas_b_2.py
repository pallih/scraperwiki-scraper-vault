#Blank Python
# -*- coding: iso-8859-15 -*-
import scraperwiki
import lxml.html
import datetime
import time

def createEntity(table_details, einrichtung_name, id):
    einrichtung = [{"name": einrichtung_name, "id": id}]
    details = {}
    for tr in table_details.cssselect("tr"):
        attrib = tr.cssselect("td")[0].text_content().strip()
        details[attrib] = tr.cssselect("td")[1].text_content().strip()
        #print details
    einrichtung[0]["details"] = details
    #print einrichtung
    return einrichtung

def siteScrape(id):
    url = "http://www.berlin.de/sen/familie/kindertagesbetreuung/kita_verzeichnis/anwendung/kitaDetails.aspx?ID=" + str(id)
    #print url
    try:
        html = scraperwiki.scrape(url)
    except:
        return""
    root = lxml.html.fromstring(html)
    einrichtung_name = u""
    try:
        #print root.cssselect("table#TabelleKitaDetails")[0]
        einrichtung_name = root.cssselect("span#lblEinrichtung")[0].text_content()
        table_details = root.cssselect("table#TabelleKitaDetails")[0]
        #print einrichtung_name
        if not einrichtung_name == "":
            return createEntity(table_details, einrichtung_name, id)
        else:
            return ""
    except:
        print "Einrichtung_name failed!"
        return ""

def writeData(result):
    scraperwiki.sqlite.execute("drop table if exists kitas_berlin")
    scraperwiki.sqlite.execute("create table kitas_berlin ( `kita` text, `adresse` text, `telefon` text, `traegerart` text, `internet` text, `email` text, `uid` text)")
    scraperwiki.sqlite.commit()
    for i in range(len(result)):
            einrichtung = result[i][0]["name"]
            uid = result[i][0]["id"]
            adresseAll = result[i][0]["details"]['Adresse']
            addrSplit = adresseAll.split(" ")
            
            addr = " ".join(addrSplit[0:-4])
            plz = addrSplit[-2]
            ort = addrSplit[-1]
            hausNr = list(addrSplit[-4])
            
            
            while hausNr[0] == "0":
                hausNr.remove("0")
                
            hausNr = "".join(hausNr)
            adresse = addr + " " + hausNr

            print adresse
            try:
                traegerart = result[i][0]["details"][u'Tr\xe4gerart']
            except:
                traegerart = ""
            try:
                telefon = result[i][0]["details"]['Telefon']
            except:
                telefon = ""

            
            try:
                internet = result[i][0]["details"]['Internet']
            except:
                internet = ""
            try:
                email = result[i][0]["details"]['Email']
            except:
                email = ""
                
            #for k in range(len(result[i][0]["details"])):
                #print "details!!! ", result[i][0]["details"].items()
            #print id, internet, email, einrichtung, adresse, traegerart, telefon
            data = {"kita": einrichtung, "adresse": adresse, "plz" : plz, "ort" : ort,  "telefon": telefon, "traegerart": traegerart, "internet": internet, "email": email, "uid": uid}
            scraperwiki.sqlite.save(unique_keys=["kita", "adresse", "telefon", "traegerart", "internet", "email", "uid"], data=data, table_name="kitas_berlin", verbose=7)

def main():
    result = []
    for id in range(2146): #12209-10063 = 2146
        print id
        identi = 10063 + id
        #print identi
        objekt = siteScrape(identi)
        #print objekt
        if  objekt:
            result.append(objekt)
            time.sleep(3)
        #print "result:", result
    writeData(result)
main()
#Blank Python
# -*- coding: iso-8859-15 -*-
import scraperwiki
import lxml.html
import datetime
import time

def createEntity(table_details, einrichtung_name, id):
    einrichtung = [{"name": einrichtung_name, "id": id}]
    details = {}
    for tr in table_details.cssselect("tr"):
        attrib = tr.cssselect("td")[0].text_content().strip()
        details[attrib] = tr.cssselect("td")[1].text_content().strip()
        #print details
    einrichtung[0]["details"] = details
    #print einrichtung
    return einrichtung

def siteScrape(id):
    url = "http://www.berlin.de/sen/familie/kindertagesbetreuung/kita_verzeichnis/anwendung/kitaDetails.aspx?ID=" + str(id)
    #print url
    try:
        html = scraperwiki.scrape(url)
    except:
        return""
    root = lxml.html.fromstring(html)
    einrichtung_name = u""
    try:
        #print root.cssselect("table#TabelleKitaDetails")[0]
        einrichtung_name = root.cssselect("span#lblEinrichtung")[0].text_content()
        table_details = root.cssselect("table#TabelleKitaDetails")[0]
        #print einrichtung_name
        if not einrichtung_name == "":
            return createEntity(table_details, einrichtung_name, id)
        else:
            return ""
    except:
        print "Einrichtung_name failed!"
        return ""

def writeData(result):
    scraperwiki.sqlite.execute("drop table if exists kitas_berlin")
    scraperwiki.sqlite.execute("create table kitas_berlin ( `kita` text, `adresse` text, `telefon` text, `traegerart` text, `internet` text, `email` text, `uid` text)")
    scraperwiki.sqlite.commit()
    for i in range(len(result)):
            einrichtung = result[i][0]["name"]
            uid = result[i][0]["id"]
            adresseAll = result[i][0]["details"]['Adresse']
            addrSplit = adresseAll.split(" ")
            
            addr = " ".join(addrSplit[0:-4])
            plz = addrSplit[-2]
            ort = addrSplit[-1]
            hausNr = list(addrSplit[-4])
            
            
            while hausNr[0] == "0":
                hausNr.remove("0")
                
            hausNr = "".join(hausNr)
            adresse = addr + " " + hausNr

            print adresse
            try:
                traegerart = result[i][0]["details"][u'Tr\xe4gerart']
            except:
                traegerart = ""
            try:
                telefon = result[i][0]["details"]['Telefon']
            except:
                telefon = ""

            
            try:
                internet = result[i][0]["details"]['Internet']
            except:
                internet = ""
            try:
                email = result[i][0]["details"]['Email']
            except:
                email = ""
                
            #for k in range(len(result[i][0]["details"])):
                #print "details!!! ", result[i][0]["details"].items()
            #print id, internet, email, einrichtung, adresse, traegerart, telefon
            data = {"kita": einrichtung, "adresse": adresse, "plz" : plz, "ort" : ort,  "telefon": telefon, "traegerart": traegerart, "internet": internet, "email": email, "uid": uid}
            scraperwiki.sqlite.save(unique_keys=["kita", "adresse", "telefon", "traegerart", "internet", "email", "uid"], data=data, table_name="kitas_berlin", verbose=7)

def main():
    result = []
    for id in range(2146): #12209-10063 = 2146
        print id
        identi = 10063 + id
        #print identi
        objekt = siteScrape(identi)
        #print objekt
        if  objekt:
            result.append(objekt)
            time.sleep(3)
        #print "result:", result
    writeData(result)
main()
