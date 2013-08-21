import scraperwiki
import json
from scraperwiki.sqlite import save 

from lxml import html
url="https://www.eventbrite.com/json/event_search?app_key=M2CIAOV4Y4WSOY27VX&keywords=hack%20fun&free"
from urllib import urlopen
response = urlopen (url)

jsonresponse = json.loads (response.read())

print jsonresponse

for item in jsonresponse['events'][1:]: # [] means dictionary
    print item['event']

    save([], {"eventid": item['event']['id'],"date": item['event']['start_date']})

