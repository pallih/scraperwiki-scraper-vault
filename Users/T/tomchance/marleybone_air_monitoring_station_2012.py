import scraperwiki
import lxml.html
import time
import datetime

today_date = str(datetime.datetime.now())

# retrieve the page
starting_url = 'http://www.londonair.org.uk/london/asp/publicstats.asp?mapview=PM10b&statyear=2012&MapType=Google&region=0&site=MY7&postcode=&la_id=&objective=All'
html = scraperwiki.scrape(starting_url)

# get all the td tags in the stats table
root = lxml.html.fromstring(html)
tds = root.cssselect('table#sitestatssub td span')

# save them
for td in tds:
    record = { "date_scraped" : today_date, "exceedences" : td.text }
    if (td.text != 'YES'):
        print record
        scraperwiki.sqlite.save(["exceedences"], record)
import scraperwiki
import lxml.html
import time
import datetime

today_date = str(datetime.datetime.now())

# retrieve the page
starting_url = 'http://www.londonair.org.uk/london/asp/publicstats.asp?mapview=PM10b&statyear=2012&MapType=Google&region=0&site=MY7&postcode=&la_id=&objective=All'
html = scraperwiki.scrape(starting_url)

# get all the td tags in the stats table
root = lxml.html.fromstring(html)
tds = root.cssselect('table#sitestatssub td span')

# save them
for td in tds:
    record = { "date_scraped" : today_date, "exceedences" : td.text }
    if (td.text != 'YES'):
        print record
        scraperwiki.sqlite.save(["exceedences"], record)
