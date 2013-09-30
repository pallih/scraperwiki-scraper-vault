import scraperwiki  
import lxml.html  
import datetime
import time



now = datetime.datetime.now() - datetime.timedelta(1)

mmdd =  now.strftime("%m%d")

datestring = now.strftime("%Y%m%d") 

url = "http://www.lanuv.nrw.de/luft/temes/"+mmdd+"/VMS2.htm"

html = scraperwiki.scrape(url)
         
root = lxml.html.fromstring(html)


for tr in root.cssselect("table"):
    trs = tr.cssselect("tr")
    for index, tr in enumerate(trs):
        index, tr.text_content()
        tds = tr.cssselect("td")
        if len(tds) > 3:
            if index % 2 != 0:
                data = {
                'TIME' : datestring+ "T" + str(tds[0].text_content()),
                'NO' : tds[3].text_content(),
                'NO2' : tds[4].text_content()
                }
                scraperwiki.sqlite.save(unique_keys=['TIME'], data=data)
                





         


import scraperwiki  
import lxml.html  
import datetime
import time



now = datetime.datetime.now() - datetime.timedelta(1)

mmdd =  now.strftime("%m%d")

datestring = now.strftime("%Y%m%d") 

url = "http://www.lanuv.nrw.de/luft/temes/"+mmdd+"/VMS2.htm"

html = scraperwiki.scrape(url)
         
root = lxml.html.fromstring(html)


for tr in root.cssselect("table"):
    trs = tr.cssselect("tr")
    for index, tr in enumerate(trs):
        index, tr.text_content()
        tds = tr.cssselect("td")
        if len(tds) > 3:
            if index % 2 != 0:
                data = {
                'TIME' : datestring+ "T" + str(tds[0].text_content()),
                'NO' : tds[3].text_content(),
                'NO2' : tds[4].text_content()
                }
                scraperwiki.sqlite.save(unique_keys=['TIME'], data=data)
                





         


