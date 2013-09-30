import scraperwiki
import lxml.html
import csv

SITE_URL = "http://wiid.twdb.state.tx.us/ims/resinfo/BushButton/lakeStatus.asp"
CSV_URL = "http://dl.dropbox.com/u/72154039/res_lat_lons.csv"

data = scraperwiki.scrape(CSV_URL)

reader = csv.reader(data.splitlines())

latlon_data = {}

for row in reader:
    latlon_data[row[0]] = { "lat" : row[1], "lon" : row[2] }

print latlon_data

def main():

    html = scraperwiki.scrape(SITE_URL)
    root = lxml.html.fromstring(html)
    table = root.cssselect("table")[6].cssselect("tr")
    table = table[1:]
    
    datastore = []
    
    for row in table:
        payload = {}

        name = row.cssselect("td")[0].text_content().strip()
        
        payload["name"] =  name
        payload["top_conservation_pool"] =  row.cssselect("td")[1].text_content().strip().replace(",","")
        payload["stage"] =  row.cssselect("td")[2].text_content().strip().replace(",","")
        payload["feet_above_top"] =  row.cssselect("td")[3].text_content().strip().replace(",","")
        payload["capacity"] =  row.cssselect("td")[4].text_content().strip().replace(",","")
        payload["conservation_storage"] =  row.cssselect("td")[5].text_content().strip().replace(",","")
        payload["percent_full"] =  row.cssselect("td")[6].text_content().strip().replace(",","")
        payload["tx_share_capacity"] =  row.cssselect("td")[7].text_content().strip().replace(",","")
        payload["tx_share_storage"] =  row.cssselect("td")[8].text_content().strip().replace(",","")
        payload["lat"] = latlon_data[name]["lat"]
        payload["lon"] = latlon_data[name]["lon"]
    
        datastore.append(payload)

    scraperwiki.sqlite.save(["name"], data=datastore)

main()import scraperwiki
import lxml.html
import csv

SITE_URL = "http://wiid.twdb.state.tx.us/ims/resinfo/BushButton/lakeStatus.asp"
CSV_URL = "http://dl.dropbox.com/u/72154039/res_lat_lons.csv"

data = scraperwiki.scrape(CSV_URL)

reader = csv.reader(data.splitlines())

latlon_data = {}

for row in reader:
    latlon_data[row[0]] = { "lat" : row[1], "lon" : row[2] }

print latlon_data

def main():

    html = scraperwiki.scrape(SITE_URL)
    root = lxml.html.fromstring(html)
    table = root.cssselect("table")[6].cssselect("tr")
    table = table[1:]
    
    datastore = []
    
    for row in table:
        payload = {}

        name = row.cssselect("td")[0].text_content().strip()
        
        payload["name"] =  name
        payload["top_conservation_pool"] =  row.cssselect("td")[1].text_content().strip().replace(",","")
        payload["stage"] =  row.cssselect("td")[2].text_content().strip().replace(",","")
        payload["feet_above_top"] =  row.cssselect("td")[3].text_content().strip().replace(",","")
        payload["capacity"] =  row.cssselect("td")[4].text_content().strip().replace(",","")
        payload["conservation_storage"] =  row.cssselect("td")[5].text_content().strip().replace(",","")
        payload["percent_full"] =  row.cssselect("td")[6].text_content().strip().replace(",","")
        payload["tx_share_capacity"] =  row.cssselect("td")[7].text_content().strip().replace(",","")
        payload["tx_share_storage"] =  row.cssselect("td")[8].text_content().strip().replace(",","")
        payload["lat"] = latlon_data[name]["lat"]
        payload["lon"] = latlon_data[name]["lon"]
    
        datastore.append(payload)

    scraperwiki.sqlite.save(["name"], data=datastore)

main()