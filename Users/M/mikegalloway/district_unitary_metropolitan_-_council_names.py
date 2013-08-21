import scraperwiki
import json

page = scraperwiki.scrape("http://mapit.mysociety.org/areas/DIS,UTA,MTD")
data = json.loads(page)

for entry in data.values():
    record = {
        "id": entry["id"],
        "gss_code": entry["codes"]["gss"],
        "type": entry["type"],
        "name": entry["name"],
        "country": entry["country"],
    }
    scraperwiki.sqlite.save(unique_keys=["id"], data=record)

