# Blank Python
sourcescraper = 'twitter_search_api_driving_1'

import scraperwiki           
scraperwiki.sqlite.attach("twitter_search_api_driving_1")

data = scraperwiki.sqlite.select ('''count(*) from twitter_search_api_driving_1.swdata''')

print data

