import scraperwiki

sourcescraper = 'river_levels'

scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select('''* from river_levels.swdata where name == 'Foss Barrier' order by datetime  limit 10 ''')

print "Datetime, Height in m"
for row in data:
    print row['datetime'], ",", row['level']


import scraperwiki

sourcescraper = 'river_levels'

scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select('''* from river_levels.swdata where name == 'Foss Barrier' order by datetime  limit 10 ''')

print "Datetime, Height in m"
for row in data:
    print row['datetime'], ",", row['level']


