import scraperwiki

import simplejson as json


scraperwiki.utils.httpresponseheader('Content-Type', 'application/json')
sourcescraper = "housingmarket"
scraperwiki.sqlite.attach(sourcescraper)

areas = scraperwiki.sqlite.select("DISTINCT area FROM housing_market")

result = {}

for item in areas:
    area = str(item.get("area"))
    area_data = scraperwiki.sqlite.select(
        """year,bungalow,detached,semi,terraced,flatmaisonetteconverted,flatmaisonetteoriginal,alldwellings FROM housing_market WHERE area = (?)""", (area)
    )
    result.update({area: area_data})

print json.dumps(result)

import scraperwiki

import simplejson as json


scraperwiki.utils.httpresponseheader('Content-Type', 'application/json')
sourcescraper = "housingmarket"
scraperwiki.sqlite.attach(sourcescraper)

areas = scraperwiki.sqlite.select("DISTINCT area FROM housing_market")

result = {}

for item in areas:
    area = str(item.get("area"))
    area_data = scraperwiki.sqlite.select(
        """year,bungalow,detached,semi,terraced,flatmaisonetteconverted,flatmaisonetteoriginal,alldwellings FROM housing_market WHERE area = (?)""", (area)
    )
    result.update({area: area_data})

print json.dumps(result)

