import scraperwiki
import re
import time

html = scraperwiki.scrape("http://www.neopets.com/index.phtml") 
online = re.findall('Players Online\:</b> (.*?) \|', html)
online = int(online[0].replace(",",""))

data = {}
data['time'] = int(time.time())
data['online'] = online

scraperwiki.sqlite.save(unique_keys=['time'], data=data)
