# Scrape NASA's list of the Space Shuttle's missions.

import scraperwiki

html = scraperwiki.scrape("http://www.nasa.gov/mission_pages/shuttle/launch/orbiter_flights.html")

import datetime
def parseDate(mmddyy):
    [month, day, pairYear] = map(int, mmddyy.split("."))
    year = pairYear + (1900 if pairYear > 50 else 2000)
    return datetime.date(year, month, day)

import lxml.html 
root = lxml.html.fromstring(html)

# Alternate tables contain shuttle info and data.

# First collect shuttle info. This will collect an extra shuttle at the end.
shuttles = []
for _table in root.cssselect("b:contains(OV-)"):
    tokens = _table.text_content().split("|")
    name = tokens[0].strip()
    id = tokens[1].strip()
    shuttles.append(name)

def send(flight):
    scraperwiki.sqlite.save(unique_keys=['mission'], data=flight)

# Then collect a table per shuttle
for shuttleIndex,_table in enumerate(root.cssselect("b:contains(OV-)+br+table")):
    for _row in _table.cssselect("tr[valign='TOP']"):
        [missionId, timestamp, link] = _row.cssselect("td[bgcolor]")
        id = missionId.text_content().strip().strip("*") # remove footnotes
        when = parseDate(timestamp.text_content().strip().strip(".")) # workaround date typo
        url = link.cssselect("a[href]")[0].get("href")
        send({"mission": id, "ship": shuttles[shuttleIndex], "date": when, "url": url})
