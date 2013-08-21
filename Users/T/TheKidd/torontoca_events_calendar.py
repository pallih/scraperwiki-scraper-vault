import scraperwiki
import datetime
import feedparser

events = feedparser.parse('http://wx.toronto.ca/festevents.nsf/torontoalleventsfeed.xml')

data = {}
for row_num, event in enumerate(events.entries):
    
    data['name'] = event['title'].partition(" ")[2]
    data['date'] = "-".join(str(i) for i in event['date_parsed'][:3])
    data['description'] = event['description']
    
    scraperwiki.sqlite.save(unique_keys=['name'], data=data)

    print data