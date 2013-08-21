# who's watching the watchers? i am!
# and I'm also watching the forkers.

import scraperwiki
import lxml.html
import urlparse
import time, datetime

base_url = "http://github.com/openplans" # our repo listing.

html = scraperwiki.scrape(base_url)    
root = lxml.html.fromstring(html)

today = datetime.date.today()

for el in root.cssselect("li.public"):
    data = {
    # repo name
    'repo': el.cssselect("li.public h3")[0].text_content(),
    # repo watchers, a.k.a. stargazers
    'stargazers': el.cssselect(".stargazers")[0].text_content(),
    # repo forks
    'forks': el.cssselect(".forks")[0].text_content(),
    'date': today        
    }
    scraperwiki.sqlite.save(unique_keys=['date', 'repo'], data=data)
    