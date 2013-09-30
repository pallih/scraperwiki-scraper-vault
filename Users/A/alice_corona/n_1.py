import requests
import scraperwiki
import lxml.html
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1326024000').text
root = lxml.html.fromstring(html)
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1326024000":
                for item in root.cssselect ("span.rankItem-position" ), ("span.rankItem-title")]:
                        print unixtime, item.text_content()

import requests
import scraperwiki
import lxml.html
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1326024000').text
root = lxml.html.fromstring(html)
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1326024000":
                for item in root.cssselect ("span.rankItem-position" ), ("span.rankItem-title")]:
                        print unixtime, item.text_content()

