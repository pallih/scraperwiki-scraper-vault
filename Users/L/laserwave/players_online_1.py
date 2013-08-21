import scraperwiki
import re
import time

html = scraperwiki.scrape("http://www.neocodex.us/forum/index/") 
values = re.findall('<span class=\'value\'>(.*?)<\/span>', html)

ncposts = int(values[0].replace(",",""))
ncmembers = int(values[1].replace(",",""))

html = scraperwiki.scrape("http://zombians.com/forum/index.php")
values = re.findall('<span class=\'value\'>(.*?)<\/span>', html)

zposts = int(values[0].replace(",",""))
zmembers = int(values[1].replace(",",""))

html = scraperwiki.scrape("http://www.clraik.com/forum/forum.php") 
values = re.findall('<dd>([0-9\,]{4,7})</dd>', html)

clposts = int(values[1].replace(",",""))
clmembers = int(values[2].replace(",",""))

html = scraperwiki.scrape("http://www.darkztar.com/forum/forum.php")
values = re.findall('<dd>([0-9\,]{4,7})</dd>', html)

dzposts = int(values[1].replace(",",""))
dzmembers = int(values[2].replace(",",""))

data = {}
data['time'] = int(time.time())
data['ncposts'] = ncposts
data['ncmembers'] = ncmembers
data['clposts'] = clposts
data['clmembers'] = clmembers
data['dzposts'] = dzposts
data['dzmembers'] = dzmembers
data['zposts'] = zposts
data['zmembers'] = zmembers

scraperwiki.sqlite.save(unique_keys=['time'], data=data)

