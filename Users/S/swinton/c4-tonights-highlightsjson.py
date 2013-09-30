# Blank Python
import scraperwiki
import datetime
import json

today = datetime.date.today()

sourcescraper = 'c4-tonights-highlights'
scraperwiki.sqlite.attach(sourcescraper)
data = scraperwiki.sqlite.select( '''* from swdata where day='%s' order by time desc''' % today.strftime("%Y-%m-%d"))

print json.dumps(data)

# Blank Python
import scraperwiki
import datetime
import json

today = datetime.date.today()

sourcescraper = 'c4-tonights-highlights'
scraperwiki.sqlite.attach(sourcescraper)
data = scraperwiki.sqlite.select( '''* from swdata where day='%s' order by time desc''' % today.strftime("%Y-%m-%d"))

print json.dumps(data)

