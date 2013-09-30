# Google Spreadsheet with the original data:
# http://www.guardian.co.uk/news/datablog/2010/apr/09/general-election-vote-power-index-constituency#data

import scraperwiki
import json

url = 'https://spreadsheets.google.com/feeds/list/tIShvliXbYL8uzJEO1HzQWA/2/public/values?alt=json'

data = scraperwiki.scrape(url)
spreadsheet = json.loads(data)

for row in spreadsheet["feed"]["entry"]:
    record = {
        "pa_id":                 row["gsx$pacode"]["$t"],
        "aristotle_id":          row["gsx$aristotleid"]["$t"],
        "constituency_pa_name":  row["gsx$pressassocpaname"]["$t"],
        "constituency_ons_name": row["gsx$onsname"]["$t"],
    }

    scraperwiki.sqlite.save(unique_keys=["pa_id"], data=record)
# Google Spreadsheet with the original data:
# http://www.guardian.co.uk/news/datablog/2010/apr/09/general-election-vote-power-index-constituency#data

import scraperwiki
import json

url = 'https://spreadsheets.google.com/feeds/list/tIShvliXbYL8uzJEO1HzQWA/2/public/values?alt=json'

data = scraperwiki.scrape(url)
spreadsheet = json.loads(data)

for row in spreadsheet["feed"]["entry"]:
    record = {
        "pa_id":                 row["gsx$pacode"]["$t"],
        "aristotle_id":          row["gsx$aristotleid"]["$t"],
        "constituency_pa_name":  row["gsx$pressassocpaname"]["$t"],
        "constituency_ons_name": row["gsx$onsname"]["$t"],
    }

    scraperwiki.sqlite.save(unique_keys=["pa_id"], data=record)
