import re
import scraperwiki
from datetime import date

markets = ['en-US' , 'en-GB' , 'en-AU']
for market in markets:
    html = scraperwiki.scrape("http://www.bing.com/?setmkt=" + market)
    match = re.search('az.*?jpg' , html)
    if match:
        image_url = html[match.start():match.end()] 
        data = { 'market' : market , 'date' : date.today(), 'web':html, 'url' : 'http://www.bing.com/' + image_url }
        print data
        scraperwiki.sqlite.save(unique_keys=['date' , 'market'], data=data)



