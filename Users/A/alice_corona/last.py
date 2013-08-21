import requests
import uuid
import scraperwiki
import lxml.html
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1328443200').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1328443200":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
                    