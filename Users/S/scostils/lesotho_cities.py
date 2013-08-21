 # -*- coding: iso-8859-1 -*-
import scraperwiki
import lxml.html


import re


# Blank Python
useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17"
html = scraperwiki.scrape("http://en.wikipedia.org/wiki/List_of_cities_in_Lesotho", "", useragent)
root = lxml.html.fromstring(html)
for a in root.cssselect("table.wikitable tr td:nth-child(2) a"):
    city_name = a.get('title')
    html = scraperwiki.scrape("http://en.wikipedia.org" + a.get('href'), "", useragent)
    city = lxml.html.fromstring(html)
    city = lxml.html.fromstring(lxml.html.tostring(city, encoding='iso-8859-1'))
    for span in city.cssselect(".latitude"):
        latitude = span.text_content().encode(encoding = 'iso-8859-1', errors='replace')

    for span in city.cssselect(".longitude"):
        longitude = span.text_content().encode(encoding = 'iso-8859-1', errors='replace')

    data = {
        'country' : 'Zimbabwe',
        'city' : city_name,
        'latitude': latitude,
        'longitude': longitude
    }

    scraperwiki.sqlite.save(unique_keys=['city'], data=data)