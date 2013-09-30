import scraperwiki
import lxml.html
import re

html = scraperwiki.scrape("http://www.uoit.ca/eventcalendar/calendar_display.php")
root = lxml.html.fromstring(html)
events = root.cssselect("td.event_day div.event")
    
columns = ["name", "date", "time", "location", "category"]

data = {}
for row_num, event in enumerate(events):
    data['category'] = event.cssselect("div.categories")[0].text_content().replace(" ","")
    
    eventinfo = event.cssselect("div[style='padding: 5px; font-size: .75em']")[0]
    lines = eventinfo.text_content().split("\n")
    data['name'] = eventinfo[0].text_content().encode('latin-1','ignore').replace("’","'")
    data['date'] = lines[2].strip("\t")
    data['time'] = lines[3].strip("\t")
    data['location'] = lines[4].strip("\t").replace("Click for more info", "")
    m = re.search("id=([0-9]*)",event.cssselect("a.thickbox")[0].get("href"))
    data['id'] = m.group(1)
    print data
        
    scraperwiki.sqlite.save(unique_keys=['id'], data=data)
import scraperwiki
import lxml.html
import re

html = scraperwiki.scrape("http://www.uoit.ca/eventcalendar/calendar_display.php")
root = lxml.html.fromstring(html)
events = root.cssselect("td.event_day div.event")
    
columns = ["name", "date", "time", "location", "category"]

data = {}
for row_num, event in enumerate(events):
    data['category'] = event.cssselect("div.categories")[0].text_content().replace(" ","")
    
    eventinfo = event.cssselect("div[style='padding: 5px; font-size: .75em']")[0]
    lines = eventinfo.text_content().split("\n")
    data['name'] = eventinfo[0].text_content().encode('latin-1','ignore').replace("’","'")
    data['date'] = lines[2].strip("\t")
    data['time'] = lines[3].strip("\t")
    data['location'] = lines[4].strip("\t").replace("Click for more info", "")
    m = re.search("id=([0-9]*)",event.cssselect("a.thickbox")[0].get("href"))
    data['id'] = m.group(1)
    print data
        
    scraperwiki.sqlite.save(unique_keys=['id'], data=data)
