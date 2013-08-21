import scraperwiki
import urlparse
import lxml.html

scraperwiki.sqlite.attach("airbed")
listingnum = scraperwiki.sqlite.select("id from airbed.swdata limit 10")
listingnum = listingnum[4]['id']
print listingnum

base_url = 'https://www.airbnb.co.uk/rooms/'
starting_url = urlparse.urljoin(base_url, listingnum)
html = scraperwiki.scrape(starting_url)
print html


