#Blank Python
# -*- coding: iso-8859-15 -*-
import scraperwiki
import lxml.html
import datetime

result = []
cinema_flag = 0
tagesprogramm = {"filme": []}
cinema_count = 0
count_id = 12345

def createEvent(element):
    cinema = {}
    global cinema_count
    if len(element.cssselect("td")) == 7 and element.cssselect("td")[0].text_content() != None:
        #print "start create!!!!!!!!!!"
        cinema["name"] = element.cssselect("td a")[0].text_content().encode("utf-8")
        cinema["url"] = element.cssselect("td a")[0].attrib["href"]
        cinema["adresse"] = element.cssselect("td")[3].text.encode("utf-8")
        cinema["plz"] = element.cssselect("td")[5].text.strip().split()[0]
        cinema["ort"] = element.cssselect("td")[5].text.strip().split()[1]
        try:
            cinema["telefon"] = element.cssselect("td a")[1].text.strip()
        except:
            cinema["telefon"] = ""
        cinema_count += 1
        #print "cinema: ", cinema
        result.append(cinema)

def tableScrape(root, tables):
    for tr in tables[2].cssselect("tr"):
        createEvent(tr)

def getLinks(td):
    global cinema_flag
    links = []
    for el in range(len(td[1].cssselect("a"))-2):
        links.append(td[1].cssselect("a")[el+1].attrib["href"])
    print "links: ", links
    cinema_flag = 1
    return links

def getUid():
    global count_id
    count_id += 1
    return str(count_id)

def writeData():
    scraperwiki.sqlite.execute("drop table if exists cinema_list_mun")
    scraperwiki.sqlite.execute("create table cinema_list_mun ( `kino` text, `adresse` text, `plz` text, `ort` text, `telefon` text, `uid` text, `url` text)")
    scraperwiki.sqlite.commit()
    print "Anzahl Kinos: ", len(result)
    for i in range(len(result)):
        cinema_name = result[i]["name"]
        cinema_adresse = result[i]["adresse"]
        cinema_ort = result[i]["ort"]
        cinema_plz = result[i]["plz"]
        cinema_telefon = result[i]["telefon"]
        cinema_url = result[i]["url"]
        cinema_uid = getUid()
        data = {"kino": cinema_name, "adresse": cinema_adresse, "plz": cinema_plz, "ort": cinema_ort, "telefon": cinema_telefon, "url": cinema_url, "uid": cinema_uid}
        scraperwiki.sqlite.save(unique_keys=["kino", "adresse", "plz", "ort", "telefon", "url", "uid"], data=data, table_name="cinema_list_mun", verbose=7)

def main():
    html = scraperwiki.scrape("http://www.munig.com/kino/kinos_region_munig.html")
    root = lxml.html.fromstring(html)
    roots = []
    tables = root.cssselect("span[id='intelliTXT'] table")
    tableScrape(root, tables)
    if cinema_flag == 0:
        td =  tables[3].cssselect("td")
        roots = getLinks(td)
    for el in range(len(roots)):
        html = scraperwiki.scrape(roots[el])
        root = lxml.html.fromstring(html)
        tables = root.cssselect("span[id='intelliTXT'] table")
        #print "ROOOOOT: ", roots[el]
        tableScrape(root, tables)
    writeData()

main()

