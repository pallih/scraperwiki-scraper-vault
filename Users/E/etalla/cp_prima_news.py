# This retrieves news from CP Prima, an Indonesian shrimp producer.
import lxml.html
import scraperwiki
import urllib, urlparse
from dateutil import parser

url = "http://www.cpp.co.id/Entries.aspx?entry_id=45"
root = lxml.html.fromstring(scraperwiki.scrape(url))

news_box = root.cssselect("div")
news = {}

for i in news_box:
    if i.get("id")=="step02":
        selection = i

for i in selection:
    try: 
        news["link"] = "http://www.cpp.co.id/" +str(i.findall("a")[0].get("href"))
        news["title"] = lxml.html.tostring(i).split("<a")[0].strip("<p>").strip(" - ")
        year = [int(s) for s in news["title"].split() if s.isdigit()][0]
        date = "%s-01-01" %(year)
        news["date"] = parser.parse(date)
        scraperwiki.sqlite.save(['link'], news)
    except:
        try:
            for row in i:
                news["link"] = "http://www.cpp.co.id/" +str(row.findall("a")[0].get("href"))
                news["title"]= row.findall("a")[0].text_content()
                year, month,day = news["title"].split()[-1].strip(","),news["title"].split()[-2].strip(","),news["title"].split()[-3].strip(",")
                date = "%s-%s-%s" %(year, month, day)
                news["date"] = parser.parse(date)
                scraperwiki.sqlite.save(['link'], news)
        except:
            pass

    