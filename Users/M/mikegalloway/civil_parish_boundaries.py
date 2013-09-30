import scraperwiki
import json

page = scraperwiki.scrape("http://mapit.mysociety.org/areas/CPC")
data = json.loads(page)

for entry in data.values():
    record = {
        "id": entry["id"],
        "codes": entry["codes"],
        "type": entry["type"],
        "name": entry["name"],
        "parent_area": entry["parent_area"],
    }
    scraperwiki.sqlite.save(unique_keys=["id"], data=record)
import scraperwiki
import json

page = scraperwiki.scrape("http://mapit.mysociety.org/areas/CPC")
data = json.loads(page)

for entry in data.values():
    record = {
        "id": entry["id"],
        "codes": entry["codes"],
        "type": entry["type"],
        "name": entry["name"],
        "parent_area": entry["parent_area"],
    }
    scraperwiki.sqlite.save(unique_keys=["id"], data=record)
