import scraperwiki
import re
import time

html = scraperwiki.scrape("http://www.neocodex.us/forum/itemdb/")
pricing = re.findall("<td class='row2' width='35%'>(.*?)</td>", html)
pricers = int(pricing[5])

data = {}
data['time'] = int(time.time())
data['pricers'] = pricers

scraperwiki.sqlite.save(unique_keys=['time'], data=data)