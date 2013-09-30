import requests
import uuid
import scraperwiki
import lxml.html
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1326024000').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1326024000":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1326628800').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1326628800":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1327233600').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1327233600":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1327838400').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1327838400":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
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
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1329048000').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1329048000":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1329652800').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1329652800":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1330257600').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1330257600":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1330862400').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1330862400":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1331467200').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1331467200":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1332072000').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1332072000":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1332676800').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1332676800":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1333281600').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1333281600":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1333886400').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1333886400":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1334491200').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1334491200":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1335096000').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1335096000":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1335700800').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1335700800":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1336305600').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1336305600":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1336910400').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1336910400":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1337515200').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1337515200":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1338120000').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1338120000":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1338724800').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1338724800":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1339329600').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1339329600":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1339934400').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1339934400":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1340539200').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1340539200":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1341144000').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1341144000":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
                    


print data

import requests
import uuid
import scraperwiki
import lxml.html
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1326024000').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1326024000":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1326628800').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1326628800":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1327233600').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1327233600":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1327838400').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1327838400":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
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
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1329048000').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1329048000":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1329652800').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1329652800":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1330257600').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1330257600":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1330862400').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1330862400":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1331467200').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1331467200":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1332072000').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1332072000":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1332676800').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1332676800":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1333281600').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1333281600":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1333886400').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1333886400":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1334491200').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1334491200":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1335096000').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1335096000":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1335700800').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1335700800":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1336305600').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1336305600":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1336910400').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1336910400":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1337515200').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1337515200":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1338120000').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1338120000":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1338724800').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1338724800":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1339329600').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1339329600":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1339934400').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1339934400":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1340539200').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1340539200":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
html = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1341144000').text
root = lxml.html.fromstring(html)
key = uuid.uuid4()
for optgroup in root.cssselect("#weekpicker-weeks optgroup"):
    year = optgroup.get("label")
    if year == "2012":
        for option in optgroup.cssselect("option"):
            unixtime = option.get("value")
            if unixtime == "1341144000":
                for item in root.cssselect("span.rankItem-title"):
                        data = {
                          'DATE' : option.get("value"),
                          'TRACK' : item.text_content(),
                          'N' : key   
                                  }
                        scraperwiki.sqlite.save(unique_keys=['N'], data=data)
                    


print data

