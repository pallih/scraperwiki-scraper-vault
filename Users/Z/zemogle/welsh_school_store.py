import datetime
import scraperwiki

data = {}
data['name'] = 'Cardiff High School'
data['postcode'] = 'CF10 3XX'

scraperwiki.sqlite.save(['name'],data,"school")

results = scraperwiki.sqlite.select("name from school where name like 'Cardiff%'")
print results
import datetime
import scraperwiki

data = {}
data['name'] = 'Cardiff High School'
data['postcode'] = 'CF10 3XX'

scraperwiki.sqlite.save(['name'],data,"school")

results = scraperwiki.sqlite.select("name from school where name like 'Cardiff%'")
print results
