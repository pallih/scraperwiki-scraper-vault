import scraperwiki
import time

scraperwiki.sqlite.attach("uk_parliamentary_constituencies")
constituencies = scraperwiki.sqlite.select("id, country_name from uk_parliamentary_constituencies.swdata order by id")

last_id = scraperwiki.sqlite.get_var("last_id") or 0

for constituency in constituencies:
    if constituency["id"] <= last_id:
        continue

    # Think that Northern Ireland in general doesn't have map data.
    if constituency["country_name"] == "Northern Ireland":
        continue

    data = scraperwiki.scrape("http://mapit.mysociety.org/area/" + str(constituency["id"]) + ".kml")

    record = {
        "id": constituency["id"],
        "kml": data,
    }

    scraperwiki.sqlite.save(unique_keys=["id"], data=record)
    scraperwiki.sqlite.save_var("last_id", constituency["id"])    

    # Try to avoid annoying dracos too much.
    time.sleep(1)