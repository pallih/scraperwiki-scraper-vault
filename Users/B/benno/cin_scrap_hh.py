#Blank Python
# -*- coding: iso-8859-15 -*-
import scraperwiki
import lxml.html
import datetime

html = scraperwiki.scrape("http://hamburg.stadtus.de/kino/kinoprogramm.html") #  die quelle, eine tabelle wird zeilenweise gescrapt..
root = lxml.html.fromstring(html)
result = []
movies = []
movies_clone = []
tagesprogramm = {"filme": []}                                 # unser tagesprogramm aller berliner kinos als liste von dictionaries
count = 0
cinema_count = 0
filmname = ""

def createEvent(element):                             #     Datum, Kino_name, Filme, (Film_Url), Zeiten
    cinema = {"name": "name"}
    cinema_flag = 0
    global movies
    global cinema_count
    global movies_clone
    global tagesprogramm
    global filmname
    index = cinema_count - 1

    for kino in element.cssselect("b a"):                      # kinos werden erstellt
        try:
            cinema["name"] = kino.text[:-1].encode("utf-8")
        except:
            print "Error kinoname"
        cinema["datum"] = datetime.date.today()                    #das script ab 1Uhr früh laufen lassen
        cinema["url"] = kino.attrib["href"]
        #kino_daten = kino.getparent().getparent().findtext("div.smalltxt")
        #print "kino_daten: ", kino.getparent().getparent().text_content(), kino_daten
        cinema_count += 1
        cinema_flag += 1
        movies_clone = []

    for zeit in element.cssselect("td.smalltxt"):                # filme und zeiten sind in der class"smalltxt", beim 1.mal filmname, beim2.mal zeit!
        for film in element.cssselect("a.link1"):                  # zu jedem kino wird eine list der filme und ihrer zeiten und url's erstellt
            try:
                filmname = film.text.encode("utf-8")
            except:
                print " Error filmname: ", type(filmname), filmname
        if not element.cssselect("a.link1"):
            zeiten = zeit.text_content().split()
            #print "zeiten: ", zeiten
            for z in range(len(zeiten)):
                if len(zeiten[z]) > 5:
                    zeit = zeiten[z][0:5]
                    add_info = zeiten[z][5:]
                    #print "zeit, add_info: ", zeit, add_info
                else:
                    zeit = zeiten[z]
                    add_info = u""
                movies_clone.append({"filmname": filmname, "kino": result[index]["name"], "datum": result[index]["datum"], "zeit": zeit, "add_info": add_info})
            movies = movies_clone

    if  cinema_flag > 0:
        result.append(cinema)                         
        #print "im %d.ten kino!!!!!!!!!!!" % cinema_count, movies
        if  movies != []:
            tagesprogramm["filme"].append(movies)

def tableScrape():
    for el in root.cssselect("span[id='intelliTXT'] tr"):      #in allen reihen <tr> innerhalb <span id=..>
        for td in el.cssselect("td"):                         #fr alle zellen <td> element in result anlegen
            createEvent(td)
        global count
        count += 1

def writeData():
    tagesprogramm["filme"].append(movies)
    scraperwiki.sqlite.execute("drop table if exists cin_hh")
    scraperwiki.sqlite.execute("create table cin_hh ( `kino` text, `film` text, `zeit` text, `add_info` text, `datum` text)")
    scraperwiki.sqlite.commit()
    print "Anzahl Filme: ", len(tagesprogramm["filme"])
    for i in range(len(tagesprogramm["filme"])):
        for j in range(len(tagesprogramm["filme"][i])):                       
            location = tagesprogramm["filme"][i][j]["kino"]
            film_titel = tagesprogramm["filme"][i][j]["filmname"]
            film_zeit = tagesprogramm["filme"][i][j]["zeit"]
            film_add_info = tagesprogramm["filme"][i][j]["add_info"]
            film_datum = tagesprogramm["filme"][i][j]["datum"]
            kinoprogramm = {"zeit": film_zeit, "add_info": film_add_info, "datum": film_datum, "kino": location, "film": film_titel}
            scraperwiki.sqlite.save(unique_keys=["kino", "datum", "zeit", "add_info", "film"], data=kinoprogramm, table_name="cin_hh", verbose=5)

def main():
    tableScrape()
    writeData()

main()
