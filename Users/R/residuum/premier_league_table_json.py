import json
import scraperwiki
scraperwiki.sqlite.attach("premier_league_table_2")

data = scraperwiki.sqlite.select('''* from premier_league_table_2.swdata order by pos''')
for dataset in data:
    dataset['team_filename'] = dataset['team'].lower().replace(' ', '_')
scraperwiki.utils.httpresponseheader("Content-Type", "text/json") 
print json.dumps(data)
import json
import scraperwiki
scraperwiki.sqlite.attach("premier_league_table_2")

data = scraperwiki.sqlite.select('''* from premier_league_table_2.swdata order by pos''')
for dataset in data:
    dataset['team_filename'] = dataset['team'].lower().replace(' ', '_')
scraperwiki.utils.httpresponseheader("Content-Type", "text/json") 
print json.dumps(data)
