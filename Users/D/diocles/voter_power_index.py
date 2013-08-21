# Google Spreadsheet with the original data:
# http://www.guardian.co.uk/news/datablog/2010/apr/09/general-election-vote-power-index-constituency#data

import scraperwiki
import json
import warnings

url = 'https://spreadsheets.google.com/feeds/list/tIShvliXbYL8uzJEO1HzQWA/1/public/values?alt=json'

data = scraperwiki.scrape(url)
spreadsheet = json.loads(data)

# TODO: read the second worksheet, and translate to ONS names
for row in spreadsheet["feed"]["entry"]:
    if row["gsx$constituency"]["$t"] == "":
        continue

    record = {
        "constituency_pa_name": row["gsx$constituency"]["$t"],
        "votepowerindex":       row["gsx$votepowerindex"]["$t"],
    }

    scraperwiki.sqlite.save(unique_keys=["constituency_pa_name"], data=record)
