import scraperwiki
import lxml.html
import re
import datetime

now = datetime.date.today()
months = [now.month, (now+datetime.timedelta(31)).month]

for month in months:
    html = scraperwiki.scrape("http://www.oshawa.ca/events.asp?month=" + str(month))
    root = lxml.html.fromstring(html)
    events = root.cssselect("table")
    
    data = {}
    for row_num, event in enumerate(events):
        
        if row_num < 4:
            continue
        lines = event.cssselect("tr")
        data['name'] = lines[0].text_content().strip()
        data['date'] = lines[1][1].text_content()
        data['description'] = lines[2].text_content().strip()
        for line in lines:
            tds = line.cssselect('td')
            if tds[0].text_content() == 'Location:':
                data['location'] = tds[1].text_content()
        print data
            
        scraperwiki.sqlite.save(unique_keys=['name'], data=data)
