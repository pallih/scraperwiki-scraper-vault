# Blank Python
import scraperwiki
import lxml.html
import json
import datetime

url = "http://www.channel4.com/"

html = scraperwiki.scrape(url) 
root = lxml.html.fromstring(html)

today = datetime.date.today()

# TonightsHighlights on C4
for ul in root.cssselect("#TonightsHighlights ul"): 
    for li in ul:
        title = [title.text_content() for title in li.cssselect("h3 a")][0]
        time = today.strftime("%Y-%m-%d") + " " + [time.text_content() for time in li.cssselect("p.highlight-tx")][0]
        time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M")
        info = [info.text_content() for info in li.cssselect("p")][-1]
        img = url + ([img.attrib['src'] for img in li.cssselect("img")][0])
        data = dict(title=title, time=time, day=today, info=info, img=img)
        scraperwiki.sqlite.save(unique_keys=['time'], data=data)





# Blank Python
import scraperwiki
import lxml.html
import json
import datetime

url = "http://www.channel4.com/"

html = scraperwiki.scrape(url) 
root = lxml.html.fromstring(html)

today = datetime.date.today()

# TonightsHighlights on C4
for ul in root.cssselect("#TonightsHighlights ul"): 
    for li in ul:
        title = [title.text_content() for title in li.cssselect("h3 a")][0]
        time = today.strftime("%Y-%m-%d") + " " + [time.text_content() for time in li.cssselect("p.highlight-tx")][0]
        time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M")
        info = [info.text_content() for info in li.cssselect("p")][-1]
        img = url + ([img.attrib['src'] for img in li.cssselect("img")][0])
        data = dict(title=title, time=time, day=today, info=info, img=img)
        scraperwiki.sqlite.save(unique_keys=['time'], data=data)





