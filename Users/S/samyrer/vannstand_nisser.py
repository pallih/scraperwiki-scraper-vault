from datetime import datetime
import scraperwiki           
html = scraperwiki.scrape("http://www.nissedal.kommune.no/nb-NO/Tenester/Lokalt/Vasstanden.aspx")
import lxml.html           
root = lxml.html.fromstring(html)
nodes = root.cssselect("html body form#mainform div#pagewrapper div#sublayoutWrapper div#rightColumn div#sublayout_0_leftContentColumn.leftContentColumn p strong")
for node in nodes:
     unformatted = node.text
     level =  float(unformatted.replace(unformatted[:unformatted.rfind(":")+2], "").replace(",","."))     
     scraperwiki.sqlite.save(unique_keys=['timestamp'], data={'timestamp':datetime.now(), 'level':level})
     continue

from datetime import datetime
import scraperwiki           
html = scraperwiki.scrape("http://www.nissedal.kommune.no/nb-NO/Tenester/Lokalt/Vasstanden.aspx")
import lxml.html           
root = lxml.html.fromstring(html)
nodes = root.cssselect("html body form#mainform div#pagewrapper div#sublayoutWrapper div#rightColumn div#sublayout_0_leftContentColumn.leftContentColumn p strong")
for node in nodes:
     unformatted = node.text
     level =  float(unformatted.replace(unformatted[:unformatted.rfind(":")+2], "").replace(",","."))     
     scraperwiki.sqlite.save(unique_keys=['timestamp'], data={'timestamp':datetime.now(), 'level':level})
     continue

