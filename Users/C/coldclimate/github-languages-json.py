import scraperwiki           
import lxml.html
import datetime


project = "https://github.com/ariya/phantomjs"

page = scraperwiki.scrape(project)
root = lxml.html.fromstring(page)
results = {}
now = datetime.datetime.now()
index = "%d_%d_%d_%d_%d" % (now.year, now.month, now.day, now.hour, now.minute)
results['timestamp'] = now
for el in root.cssselect("div.repository-lang-stats-graph")[0]:
    value = el.attrib['style'].split(";")[0].split(":")[1]
    name = (str)(el.text_content())
    results[name]=value

