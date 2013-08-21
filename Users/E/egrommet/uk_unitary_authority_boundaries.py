import scraperwiki
import json

page = scraperwiki.scrape("http://mapit.mysociety.org/areas/UTE")
data = json.loads(page)

# TODO: Figure out whether we need to pay attention to low/high
# generations from the mapit API, to discount out-of-date constituencies.
for entry in data.values():
    record = {
        "id": entry["id"],
        "gss": entry["codes"]["gss"],
        "name": entry["name"],
        "country_name": entry["country_name"],
        "parent_area": entry["parent_area"],
    }

    scraperwiki.sqlite.save(unique_keys=["id"], data=record)
