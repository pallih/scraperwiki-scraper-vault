import scraperwiki
import lxml.html

scraperwiki.sqlite.execute("delete from swdata")

response = scraperwiki.scrape("http://www.wienerlinien.at/itip/bf/?line=U1&route=1")
root = lxml.html.fromstring(response)

for link in root.cssselect("a"):    
    text = link.text_content()
    if text == "Startseite":
        # first link which is not needed
        break
    data = {
        'haltestelle' : text,
        'link' : "http://www.wienerlinien.at/itip/bf/" + link.attrib['href'],
        'ziel' : "",
        'abfahrt' : ""
    }
    scraperwiki.sqlite.save(unique_keys=['haltestelle'], data=data)

for data in scraperwiki.sqlite.select("* FROM swdata"):
    response = scraperwiki.scrape(data['link'])
    root = lxml.html.fromstring(response)

    for span in root.cssselect("span"):
        text = span.text_content()
        # Störung tritt offenbar nach 15 Abfragen immer auf
        if text.startswith("Auf Grund einer technischen"):
            data['abfahrt']="Störung bei der Abfrage"
            break
        if text.startswith("Ziel:"):
            data['ziel']=text[6:]
        if text.startswith("Abfahrt:"):
            data['abfahrt']=text[9:]
            break
        if text == "Keine Abfahrten gefunden.":
            data['abfahrt']=text
            break
    scraperwiki.sqlite.save(unique_keys=['haltestelle'], data=data)
