from scraperwiki import swimport
from scraperwiki.sqlite import select
import re
from requests import post

swimport('eventbrite').scrape('http://jdcdc.eventbrite.com/')
twitter_handles = [row['Twitter Handle'] for row in select('`Twitter Handle` from swdata WHERE `Twitter Handle` IS NOT NULL')]

for twitter_handle in twitter_handles:
    h = re.sub(r'^.*[@/]', '', twitter_handle)
    print hfrom scraperwiki import swimport
from scraperwiki.sqlite import select
import re
from requests import post

swimport('eventbrite').scrape('http://jdcdc.eventbrite.com/')
twitter_handles = [row['Twitter Handle'] for row in select('`Twitter Handle` from swdata WHERE `Twitter Handle` IS NOT NULL')]

for twitter_handle in twitter_handles:
    h = re.sub(r'^.*[@/]', '', twitter_handle)
    print h