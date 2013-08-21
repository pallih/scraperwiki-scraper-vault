# Am Anfang müssen wir ein paar Sachen importieren
from BeautifulSoup import BeautifulSoup
import urllib
import urllib2
import re
import json
import scraperwiki

google_maps_baseurl = "http://maps.google.com/maps/api/geocode/json?address="

# Loop mit jedem Anfangsbuchstaben
for char in "abcdefghijklmnopqrstuvwxyz":
    # Webseite herunterladen
    # (Das »"url%s" % char« ersetzt das »%s« im String durch die Variable char,
    # wenn man das mit mehreren machen wollte, ginge das so: »"url%sblah%sblah%i" % (string, noch_ein_string, zahl)«)
    website = scraperwiki.scrape("http://www.berlin.de/tickets/suche/az-orte.php?firstchar=%s" % char)
    # Neue Instanz von BeautifulSoup mit dem gerade heruntergeladenen Quelltext erstellen
    soup = BeautifulSoup(website)
    
    # Jetzt suchen wir alle tags, die in ihrem href-Attribut »ort.php« stehen haben
    for a in soup.findAll(href=re.compile("ort.php")):
        # Das hier kann man sich denken
        print a.string
        print a["href"]
        
        # Hier wird die URL zusammengebaut, die wir dem hcard-Scraper übergeben wollen
        # hcard: http://microformats.org/wiki/hcard
        # Da wir die URL im Querystring übergeben, müssen wir sie vorher noch entsprechend encodieren,
        # so dass z. B. alle Sonderzeichen enkodiert werden usw.
        url = urllib.quote("http://www.berlin.de%s" % a["href"])
        # Die REST-API des hcard-Scrapers aufrufen, mit der eben enkodierten URL als Argument
        info = urllib.urlopen("http://microformatique.com/optimus/?uri=%s&format=json" % url)
        # Und das JSON, das wir zurück bekommen, in ein gewöhnliches Python-Objekt umwandeln
        info = json.load(info)

        # Jetzt schauen wir zur Sicherheit, ob es auch wirklich eine hcard in dem uns zurückgegebenen JSON gibt,
        # und ob in der hcard auch ein adr-Objekt ist
        if "hcard" in info and "adr" in info["hcard"]:
            print info["hcard"]
            
            # Man hätte hier natürlich auch gleich mit der Google-Maps-API das reverse geocoding machen können
            # (denen die Adresse geben, die GPS-Koordination bekommen), aber meine Güte, ich bin krank
            # und FLo hat bestimmt Langeweile, der spielt eh immer zu viel Fifa

            address = "%s, %s %s" % (info["hcard"]["adr"][0]["street-address"][0], info["hcard"]["adr"][0]["postal-code"], info["hcard"]["adr"][0]["locality"])
            gmaps_url = "%s%s&sensor=false" % (google_maps_baseurl, urllib.quote_plus(address.encode("utf-8")))
            response = urllib2.urlopen(gmaps_url)
            geodata = json.load(response)
                        
            # Das zusammenbauen, was wir gleich speichern wollen
            record = {
                "name": a.string,
                "adr": info["hcard"]["adr"],
                "from": a["href"]
            }
            
            if geodata["status"] == "OK" and len(geodata["results"]):
                print geodata
                record["geo"] = str(geodata["results"][0])
            
            # Und dann speichern –
            # Das erste Argument ist (anscheinend), welche Eigenschaften unserer Daten indiziert werden sollen,
            # in diesem Fall der Name, so dass man später den Ort nach Namen heraussuchen kann.
            # Man könnte zusätzlich auch noch andere Eigenschaften so indizieren lassen, z. B. ["name", "from"],
            # so dass man’s auch anhand der URL von berlin.de wieder raussuchen könnte.
            scraperwiki.datastore.save(["name"], record)