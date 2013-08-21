import scraperwiki
import lxml.html



NUMROWS = 5000

source = scraperwiki.scrape("http://data.seattle.gov/api/views/7ais-f98f/rows.xml?max_rows="+str(NUMROWS))
root = lxml.html.fromstring(source)



crimes = root.cssselect("row row")

for curr in crimes:

    offnum = int(curr.cssselect("general_offense_number")[0].text)
    offtype = curr.cssselect("summarized_offense_description")[0].text
    repdate = curr.cssselect("date_reported")[0].text
    beat = curr.cssselect("zone_beat")[0].text
    longitude = float(curr.cssselect("longitude")[0].text)
    latitude = float(curr.cssselect("latitude")[0].text)



    data = {
        'Offense_Number': offnum,
        'Offense_Type': offtype,
        'Date_Reported': repdate,
        'Beat': beat,
        'Longitude': longitude,
        'Latitude': latitude
    }

    scraperwiki.sqlite.save(unique_keys=['Offense_Number'],data=data)    