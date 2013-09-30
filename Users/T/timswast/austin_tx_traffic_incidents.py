import scraperwiki
import pprint
import json

# Blank Python
jsonpstring = scraperwiki.scrape("http://www.austintexas.gov/GIS/TrafficViewer/Home/JsonpIncidents/query?f=json&where=1%3D1&returnGeometry=true&spatialRel=esriSpatialRelIntersects&outFields=*&outSR=4326&callback=f")
lines = jsonpstring.split(";")
jsons = [l[2:-1] for l in lines if l.strip() != ""]
data = json.loads(jsons[0])
#pprint.pprint(data)

# Save the data : convert into records
records = []
for row in data["features"]:
    record = {}
    records.append(record)
    record["geometry"] = row["geometry"]
    for attribute in row["attributes"]:
        record[attribute] = row["attributes"][attribute]
#pprint.pprint(records)

# Save in sqlite.
scraperwiki.sqlite.save(unique_keys=["Address",
      "CrossStreet",
      "CurrentDate"],
    data=records)

import scraperwiki
import pprint
import json

# Blank Python
jsonpstring = scraperwiki.scrape("http://www.austintexas.gov/GIS/TrafficViewer/Home/JsonpIncidents/query?f=json&where=1%3D1&returnGeometry=true&spatialRel=esriSpatialRelIntersects&outFields=*&outSR=4326&callback=f")
lines = jsonpstring.split(";")
jsons = [l[2:-1] for l in lines if l.strip() != ""]
data = json.loads(jsons[0])
#pprint.pprint(data)

# Save the data : convert into records
records = []
for row in data["features"]:
    record = {}
    records.append(record)
    record["geometry"] = row["geometry"]
    for attribute in row["attributes"]:
        record[attribute] = row["attributes"][attribute]
#pprint.pprint(records)

# Save in sqlite.
scraperwiki.sqlite.save(unique_keys=["Address",
      "CrossStreet",
      "CurrentDate"],
    data=records)

