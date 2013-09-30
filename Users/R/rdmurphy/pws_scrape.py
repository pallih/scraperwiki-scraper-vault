import scraperwiki
import lxml.html
import csv

URL = "http://www.tceq.texas.gov/drinkingwater/trot/droughtw.html"
CSV_URL = "http://static.texastribune.org.s3.amazonaws.com/media/flatpages/pws-tracker/pwsgis.csv"

csv_data = scraperwiki.scrape(CSV_URL)

latlon_data = {}

for row in csv.reader(csv_data.splitlines()):
    latlon_data[row[0]] = { "lat" : row[1], "lon" : row[2] }

def scrape():
    
    html = scraperwiki.scrape(URL)
    root = lxml.html.fromstring(html)
    content_area = root.cssselect("#content-core")[0]
    date = content_area.cssselect("p")[0].text_content()[13:][:-1]
    table = content_area.cssselect("table")[0]
    rows = table.cssselect("tr")[1:]

    datastore = []

    for row in rows:
        payload = {}

        cells = row.cssselect("td")
        
        pws_id = cells[0].text_content().strip()
        
        payload["pws_id"] = pws_id
        payload["pws_name"] = cells[1].text_content().strip()
        payload["county"] = cells[2].text_content().strip()
        payload["priority"] = cells[3].text_content().strip()
        payload["tceq_stage"] = cells[4].text_content().strip()
        payload["population"] = cells[5].text_content().strip()
        payload["connections"] = cells[6].text_content().strip()
        payload["notified"] = cells[7].text_content().strip()
        payload["source"] = cells[8].text_content().strip()
        try:
            payload["lat"] = latlon_data[pws_id]["lat"]
            payload["lon"] = latlon_data[pws_id]["lon"]
        except:
            print "Failed lat/lon match on " + payload["pws_name"] + ":" + pws_id + "."
            pass
        payload["last_updated"] = date

        datastore.append(payload)

    scraperwiki.sqlite.save(["pws_id"], data=datastore)

scrape()
import scraperwiki
import lxml.html
import csv

URL = "http://www.tceq.texas.gov/drinkingwater/trot/droughtw.html"
CSV_URL = "http://static.texastribune.org.s3.amazonaws.com/media/flatpages/pws-tracker/pwsgis.csv"

csv_data = scraperwiki.scrape(CSV_URL)

latlon_data = {}

for row in csv.reader(csv_data.splitlines()):
    latlon_data[row[0]] = { "lat" : row[1], "lon" : row[2] }

def scrape():
    
    html = scraperwiki.scrape(URL)
    root = lxml.html.fromstring(html)
    content_area = root.cssselect("#content-core")[0]
    date = content_area.cssselect("p")[0].text_content()[13:][:-1]
    table = content_area.cssselect("table")[0]
    rows = table.cssselect("tr")[1:]

    datastore = []

    for row in rows:
        payload = {}

        cells = row.cssselect("td")
        
        pws_id = cells[0].text_content().strip()
        
        payload["pws_id"] = pws_id
        payload["pws_name"] = cells[1].text_content().strip()
        payload["county"] = cells[2].text_content().strip()
        payload["priority"] = cells[3].text_content().strip()
        payload["tceq_stage"] = cells[4].text_content().strip()
        payload["population"] = cells[5].text_content().strip()
        payload["connections"] = cells[6].text_content().strip()
        payload["notified"] = cells[7].text_content().strip()
        payload["source"] = cells[8].text_content().strip()
        try:
            payload["lat"] = latlon_data[pws_id]["lat"]
            payload["lon"] = latlon_data[pws_id]["lon"]
        except:
            print "Failed lat/lon match on " + payload["pws_name"] + ":" + pws_id + "."
            pass
        payload["last_updated"] = date

        datastore.append(payload)

    scraperwiki.sqlite.save(["pws_id"], data=datastore)

scrape()
