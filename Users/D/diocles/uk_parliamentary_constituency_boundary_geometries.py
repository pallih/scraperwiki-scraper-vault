import scraperwiki
import json

scraperwiki.sqlite.attach("uk_parliamentary_constituencies")
constituencies = scraperwiki.sqlite.select("* from uk_parliamentary_constituencies.swdata")

areas = []
for constituency in constituencies:

    # Think that Northern Ireland in general doesn't have map data.
    if constituency["country_name"] == "Northern Ireland":
        continue

    areas.append(constituency["id"])

page = scraperwiki.scrape("http://mapit.mysociety.org/areas/" + ','.join(map(str, areas)) + "/geometry")
data = json.loads(page)

for id in data:
    record = data[id]
    record["id"] = id

    scraperwiki.sqlite.save(unique_keys=["id"], data=record)import scraperwiki
import json

scraperwiki.sqlite.attach("uk_parliamentary_constituencies")
constituencies = scraperwiki.sqlite.select("* from uk_parliamentary_constituencies.swdata")

areas = []
for constituency in constituencies:

    # Think that Northern Ireland in general doesn't have map data.
    if constituency["country_name"] == "Northern Ireland":
        continue

    areas.append(constituency["id"])

page = scraperwiki.scrape("http://mapit.mysociety.org/areas/" + ','.join(map(str, areas)) + "/geometry")
data = json.loads(page)

for id in data:
    record = data[id]
    record["id"] = id

    scraperwiki.sqlite.save(unique_keys=["id"], data=record)