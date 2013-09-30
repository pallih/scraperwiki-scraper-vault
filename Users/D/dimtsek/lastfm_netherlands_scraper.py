import scraperwiki
import requests
import lxml.html
html = requests.get('http://www.last.fm/charts/tracks/top/place/Greece?ending=1326024000').text
root = lxml.html.fromstring(html)
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2013":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            html2 = requests.get('http://www.last.fm/charts/tracks/top/place/Greece?ending=' + unixtime).text
            root2 = lxml.html.fromstring(html2)
            for box in root2.cssselect("li.rankItem"):
                print unixtime, box.cssselect("span.rankItem-title")[0].text_content(),box.cssselect("span.rankItem-position")[0].text_content()
                data = {
                    'DATE' : unixtime,
                    'POSITION' : box.cssselect("span.rankItem-position")[0].text_content(),
                    'TRACK' : box.cssselect("span.rankItem-title")[0].text_content(),
                        }
                scraperwiki.sqlite.save(unique_keys=['DATE','TRACK'], data=data)
                    

                import scraperwiki
import requests
import lxml.html
html = requests.get('http://www.last.fm/charts/tracks/top/place/Greece?ending=1326024000').text
root = lxml.html.fromstring(html)
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2013":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            html2 = requests.get('http://www.last.fm/charts/tracks/top/place/Greece?ending=' + unixtime).text
            root2 = lxml.html.fromstring(html2)
            for box in root2.cssselect("li.rankItem"):
                print unixtime, box.cssselect("span.rankItem-title")[0].text_content(),box.cssselect("span.rankItem-position")[0].text_content()
                data = {
                    'DATE' : unixtime,
                    'POSITION' : box.cssselect("span.rankItem-position")[0].text_content(),
                    'TRACK' : box.cssselect("span.rankItem-title")[0].text_content(),
                        }
                scraperwiki.sqlite.save(unique_keys=['DATE','TRACK'], data=data)
                    

                