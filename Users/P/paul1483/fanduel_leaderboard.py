import scraperwiki
import lxml.html    
import dateutil.parser
import json
from pprint import pprint


# Blank Python

x=30

while x<338:
    x=x+1
    url = "https://www.fanduel.com/api/leaders?metric=wins&name=main&monthId=53&startIndex=0&results=50&sort=rank&dir=asc&startIndex=%d&results=50" % (x*50)
    print url
    html = scraperwiki.scrape(url)  
    result = json.loads(html)
    for res in result["users"]:
        data = {
            'username' : res["username"]
        }
        scraperwiki.sqlite.save(unique_keys=['username'], data=data)

scraperwiki.sqlite.select("* from swdata")
