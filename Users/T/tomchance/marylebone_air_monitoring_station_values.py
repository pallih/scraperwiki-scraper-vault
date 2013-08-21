###############################################################################
# Air pollution monitoring site scraper
###############################################################################

import scraperwiki
import lxml.html
import time
import datetime

today_date = str(datetime.datetime.now())

# retrieve the page
starting_url = 'http://www.londonair.org.uk/london/asp/publicstats.asp?region=0&site=MY7&bulletin=hourly&la_id=&statyear=2011&postcode=&MapType=Google&zoom=9&lat=51.431751825946115&lon=-0.17578125&Species=All'
html = scraperwiki.scrape(starting_url)

# get all the td tags in the stats table
root = lxml.html.fromstring(html)
tds = root.cssselect('table#sitestatssub td span')

# save them
i = 1
for td in tds:
    record = { "date_scraped" : today_date, "td" : td.text, "no" : i }
    print record
    scraperwiki.sqlite.save(["td"], record)
    i = i + 1
