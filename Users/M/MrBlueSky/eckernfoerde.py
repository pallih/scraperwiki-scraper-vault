import scraperwiki
import lxml.html   
import time
import datetime
      
html = scraperwiki.scrape("http://www.eckernfoerde.de/index.phtml?mNavID=296.42&sNavID=296.52&La=1")
root = lxml.html.fromstring(html)

for tr in root.cssselect("h4.mtp_ti_text a"):
    
    data = {
          'url' : "http://www.eckernfoerde.de"+tr.attrib['href'],
          'link' : "http://www.eckernfoerde.de"+tr.attrib['href'],
          'guid' : "http://www.eckernfoerde.de"+tr.attrib['href'],
          'title' : tr.text_content(),
          'description' : '',
          'pubDate' : datetime.datetime.today()
      
    }
    print data
    scraperwiki.sqlite.save(unique_keys=['url'], data=data)