"""

Sevilla Weather. Hourly

Author: Jaime de Aquino
Modified: Carlos Cobo <toqueteos at auruv dot org>

"""

import scraperwiki
from BeautifulSoup import BeautifulSoup

DEFAULT_WEATHER = "Ninguno"
DEFAULT_WIND_DIR = "Ninguna"

starting_url = "http://www.eltiempo.es/sevilla.html?v=por_hora"

# Retrieve a page
html = scraperwiki.scrape(starting_url)

# print "> debug: HTML => %s" % html

# Soupify
soup = BeautifulSoup(html)

# Get all <tr> tags
trs = soup.findAll("tr")

# SQLite row counter
i = 0

# Iterate through table rows
for tr in trs:

    # If <td> tag with ".hour" class present (CSS)
    if tr.find("td", "hour"):

        # Debug
        # print "> debug: tr => %s" % tr

        # Ignore this, future improvement
        # td = tr.findAll("td")
        # classes = [
        #     "hour",
        #     "weather",
        #     "temp",
        #     "wind-direction",
        #     "precipitation",
        #     "cloudiness",
        #     "thunder-probability",
        #     "relative-moist",
        #     "air-pressure",
        # ]

        td = {
            "time": tr.find("td", "hour"),
            "weather": tr.find("td", "weather"),
            "temp": tr.find("td", "temp"),
            "wind_dir": tr.find("td", "wind-direction"),
            "precip": tr.find("td", "precipitation"),
            "cloud": tr.find("td", "cloudiness"),
            "thunder": tr.find("td", "thunder-probability"),
            "relative": tr.find("td", "relative-moist"),
            "air": tr.find("td", "air-pressure"),
        }
    
        # Compound sqlite dict to store
        record = {
            "n": i,
            "time": td["time"].text,
            "weather": DEFAULT_WEATHER,
            "temp": td["temp"].text,
            "windDirection": DEFAULT_WIND_DIR,
            "precipitation": td["precip"].text,
            "cloudiness": td["cloud"].text,
            "thunderProbability": td["thunder"].text,
            "relativeMoist": td["relative"].text,
            "airPressure": td["air"].text,
        }

        # Special cases
        # It's not perfect, but it works!
        if len(td["weather"].contents) > 1:
            record["weather"] = td["weather"].find("div")["title"]
        if len(td["wind_dir"].contents) > 1:
            record["windDirection"] = td["wind_dir"].find("div")["title"]

        # Debug
        # print record

        # Save in SQLite
        scraperwiki.sqlite.save(["n"], record)

        i += 1
