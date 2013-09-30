import scraperwiki
import lxml.html
import dateutil.parser

html = scraperwiki.scrape("http://sywellaerodrome.co.uk/events.php")
root = lxml.html.fromstring(html)

events = []

for tr in root.cssselect("table[class='menu'] tr"):
    tds = tr.cssselect("td")
    # ignore table header
    if not tds:
        continue

    date = tds[0].text_content()
    # ignore blank lines
    if date == u'\xa0':
        continue

    data = {
        'date' : dateutil.parser.parse(date).date(),
        'summary' : tds[1].text_content()
    }

    events.append(data)

# iterate events to find start/end dates
# this assumes events spanning multiple days are adjacent and don't have other events in the middle
last_event = {
    'date': None,
    'summary': None
}
last_event = events[0]
start_date = events[0]['date']
for event in events:
    #print event

    if last_event['summary'] != event['summary']:
        #print last_event['summary'], start_date, last_event['date']
        data = {
            'summary' : last_event['summary'],
            'start_date' : start_date,
            'end_date' : last_event['date'],
        }
        scraperwiki.sqlite.save(unique_keys=['summary'], data=data)
        start_date = event['date']
    last_event = event


import scraperwiki
import lxml.html
import dateutil.parser

html = scraperwiki.scrape("http://sywellaerodrome.co.uk/events.php")
root = lxml.html.fromstring(html)

events = []

for tr in root.cssselect("table[class='menu'] tr"):
    tds = tr.cssselect("td")
    # ignore table header
    if not tds:
        continue

    date = tds[0].text_content()
    # ignore blank lines
    if date == u'\xa0':
        continue

    data = {
        'date' : dateutil.parser.parse(date).date(),
        'summary' : tds[1].text_content()
    }

    events.append(data)

# iterate events to find start/end dates
# this assumes events spanning multiple days are adjacent and don't have other events in the middle
last_event = {
    'date': None,
    'summary': None
}
last_event = events[0]
start_date = events[0]['date']
for event in events:
    #print event

    if last_event['summary'] != event['summary']:
        #print last_event['summary'], start_date, last_event['date']
        data = {
            'summary' : last_event['summary'],
            'start_date' : start_date,
            'end_date' : last_event['date'],
        }
        scraperwiki.sqlite.save(unique_keys=['summary'], data=data)
        start_date = event['date']
    last_event = event


