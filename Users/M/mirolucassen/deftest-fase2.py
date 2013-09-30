import scraperwiki

scraperwiki.sqlite.attach("deftest")

position = int(scraperwiki.sqlite.get_var("position", 1)) #variabele in de data store

links = scraperwiki.sqlite.select("id, URL from 'deftest'.swdata where id>= %d order by id" % position) #maak een id per record; dit helpt al de scraper er uit knalt tijdens proces; bij herhaling krijg je alleen nieuwe records

#dictionary uit opgeslagen scraper
for link in links:
    url = link("URL") #PAK DE URL

    html = scraperwiki.scrape(url) #pak de html-inhoud
    data = {"URL: url, "HTML": html} #maak er een dictionary van
    scraperwiki.sqlite.save ["URL"], data #ophalen en bewaren in de data storage
    scraperwiki.sqlite.save_var("position", link["id"] #gebruik dezelfde als in je eerdere fase scraper

#hierna ga je soupen met de html in de datastore
import scraperwiki

scraperwiki.sqlite.attach("deftest")

position = int(scraperwiki.sqlite.get_var("position", 1)) #variabele in de data store

links = scraperwiki.sqlite.select("id, URL from 'deftest'.swdata where id>= %d order by id" % position) #maak een id per record; dit helpt al de scraper er uit knalt tijdens proces; bij herhaling krijg je alleen nieuwe records

#dictionary uit opgeslagen scraper
for link in links:
    url = link("URL") #PAK DE URL

    html = scraperwiki.scrape(url) #pak de html-inhoud
    data = {"URL: url, "HTML": html} #maak er een dictionary van
    scraperwiki.sqlite.save ["URL"], data #ophalen en bewaren in de data storage
    scraperwiki.sqlite.save_var("position", link["id"] #gebruik dezelfde als in je eerdere fase scraper

#hierna ga je soupen met de html in de datastore
