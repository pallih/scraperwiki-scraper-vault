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
                print option.text, year, option.get("value")
                for item in root.cssselect("span.rankItem-title"):
                    rank = "value" in "rankItem-position"
                    print item.text_content(), ("value")

                for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
                        record = { "time" : (option.text, year) }  
                        scraperwiki.sqlite.save(["time"], record)  
                for item in root.cssselect("span.rankItem-title"):
                            record = { "Artist-title" : item.text_content() }  
                            scraperwiki.sqlite.save(["Artist-title"], record)
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
                print option.text, year, option.get("value")
                for item in root.cssselect("span.rankItem-title"):
                    rank = "value" in "rankItem-position"
                    print item.text_content(), ("value")

                for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
                        record = { "time" : (option.text, year) }  
                        scraperwiki.sqlite.save(["time"], record)  
                for item in root.cssselect("span.rankItem-title"):
                            record = { "Artist-title" : item.text_content() }  
                            scraperwiki.sqlite.save(["Artist-title"], record)
