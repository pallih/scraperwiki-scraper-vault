import scraperwiki
import time

scraperwiki.sqlite.attach("uk_unitary_authority_boundaries")
ward = scraperwiki.sqlite.select("id, country_name from uk_unitary_authority_boundaries.swdata order by id")

last_id = scraperwiki.sqlite.get_var("last_id") or 0

for ward in ward:
    if ward["id"] <= last_id:
        continue

    # In original this was used to take out NI, I'm going to see if it works for England as I only want the Welsh data.
    if ward["country_name"] == "England":
        continue

    data = scraperwiki.scrape("http://mapit.mysociety.org/area/" + str(ward["id"]) + ".kml")

    record = {
        "id": ward["id"],
        "kml": data,
    }

    scraperwiki.sqlite.save(unique_keys=["id"], data=record)
    scraperwiki.sqlite.save_var("last_id", ward["id"])    

    # Try to avoid annoying dracos too much.
    time.sleep(1)import scraperwiki
import time

scraperwiki.sqlite.attach("uk_unitary_authority_boundaries")
ward = scraperwiki.sqlite.select("id, country_name from uk_unitary_authority_boundaries.swdata order by id")

last_id = scraperwiki.sqlite.get_var("last_id") or 0

for ward in ward:
    if ward["id"] <= last_id:
        continue

    # In original this was used to take out NI, I'm going to see if it works for England as I only want the Welsh data.
    if ward["country_name"] == "England":
        continue

    data = scraperwiki.scrape("http://mapit.mysociety.org/area/" + str(ward["id"]) + ".kml")

    record = {
        "id": ward["id"],
        "kml": data,
    }

    scraperwiki.sqlite.save(unique_keys=["id"], data=record)
    scraperwiki.sqlite.save_var("last_id", ward["id"])    

    # Try to avoid annoying dracos too much.
    time.sleep(1)