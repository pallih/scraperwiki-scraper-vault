import scraperwiki,json
from datetime import datetime
from datetime import date
from time import *

import cgi, os
qstring=os.getenv("QUERY_STRING")


output='logfile'

#defaults
scrapername='opencorporates_trawler'
scrapertable='directors_RoyalShell_2_2'

if qstring!=None:
    get = dict(cgi.parse_qsl(qstring))
    if 'output' in get: output=get['output']
    if 'scraper' in get: scrapername=get['scraper']
    if 'table' in get: scrapertable=get['table']

scraperwiki.sqlite.attach(  scrapername )
q = '* FROM `'+scrapertable+'` ORDER BY `start_date`'
data = scraperwiki.sqlite.select(q)

#`directors_RoyalShell_2_2` (`end_date` text, `ocid` text, `id` integer, `cname` text, `position` text, `opencorporates_url` text, `start_date` text, `name` text)

log=[]

if output=='logfile':
    from operator import itemgetter

    scraperwiki.utils.httpresponseheader("Content-Type", "application/json")
    for d in data:
        dt=int(mktime(strptime(d['start_date'],"%Y-%m-%d")))
        #1301612404|687369|A|www.isinet.com/WoK/UA
        log.append( ('|'.join([ str(dt),d['name'].replace(' ','_'), 'A', d['cname'].replace(' ','_') ]), dt) )
        if d['end_date']!=None:
            dt=int(mktime(strptime(d['end_date'],"%Y-%m-%d")))
        #else: dt=int(mktime( strptime(date.today().strftime('%Y-%m-%d'),"%Y-%m-%d") ))
        log.append( ( '|'.join([ str(dt) ,d['name'].replace(' ','_'), 'D', d['cname'].replace(' ','_') ]), int(dt) ) )

    slog= sorted(log, key=itemgetter(1))
    for (record, t) in slog: print record