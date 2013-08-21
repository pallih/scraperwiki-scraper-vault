import scraperwiki
import json
from datetime import date

for i in range(1,1000):
    try:
        jsonPage = scraperwiki.scrape('http://fantasy.premierleague.com/web/api/elements/%d/'%(i))
        playerObj = json.loads(jsonPage)
        table_name = 'data' + str(date.today())
        scraperwiki.sqlite.save(unique_keys=['id'], data=playerObj, table_name=table_name)
    except:
        print 'Stopped at %d'%(i)
        break