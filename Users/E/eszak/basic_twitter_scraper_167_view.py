# Blank Python
#sourcescraper = 'basic_twitter_scraper_167'

import scraperwiki           
scraperwiki.sqlite.attach("basic_twitter_scraper_167")

data = scraperwiki.sqlite.select(           
    '''* from basic_twitter_scraper_167.swdata 
    order by date desc limit 10'''
)
print data

print "<table>"           
# Blank Python
#sourcescraper = 'basic_twitter_scraper_167'

import scraperwiki           
scraperwiki.sqlite.attach("basic_twitter_scraper_167")

data = scraperwiki.sqlite.select(           
    '''* from basic_twitter_scraper_167.swdata 
    order by date desc limit 10'''
)
print data

print "<table>"           
