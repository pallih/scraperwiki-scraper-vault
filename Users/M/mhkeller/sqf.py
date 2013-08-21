import scraperwiki
from urllib2 import urlopen
import datetime
import pprint
import itertools
import sys
import simplejson

updateandreturn = lambda d,k: d.update(k) or d

#def updateandreturn(d,k):
#    #print repr((d,k))
#    d.update(k)
#    return d

mosques = {
1: 'Imam Al-Khoei Islamic Center - Al-Khoei Benevolent Foundation',
2: 'The Bronx Muslim Center',
3: 'Islamic Center of Bay Ridge',
4: 'Alavi Foundation',
5: 'Islamic Institute of NY/Razi School/Imam Ali Mosque',
6: 'Iran Mission to the United Nations',
7: 'Masjid Al-Rahman',
8: 'Al-Mahdi Foundation',
9: 'Al-Hussini Madressa',
}

scraperwiki.sqlite.save_var('step',1)
#scraperwiki.sqlite.save_var('partstep',None)

#http://dl.dropbox.com/u/6535582/2006joinedfinal.csv
#http://sw.thomaslevine.com/sqf_subset.csv
#http://www.tuxmachine.com/.scraperwiki-jdcny2012-02/keller-SQF/2006joinedfinal.part{{0..4}}.csv
# to split: $ part=4; sed -n "1p;$((part*103000+2)),$(( (part+1)*103000+1))p" < 2006joinedfinal.csv > 2006joinedfinal.part${part}.csv

parturl = "http://www.tuxmachine.com/.scraperwiki-jdcny2012-02/keller-SQF/2006joinedfinal.part%d.csv"

def fixfields(d):
    d['haserror'] = None
    d['distance'] = float(d['distance'])
    try:
        datestop = datetime.datetime.strptime(d['datestop'],'%m/%d/%Y %H:%M:%S')
        d['datestop'] = datestop.strftime('%Y-%m-%d %H:%M:%S')
        d['yearmonth'] = datestop.strftime('%Y-%m')
    except ValueError:
        d['haserror'] = "DATESTOP"
        print 'datestop ValueError row: %r' % (d,)
        print 'datestop ValueError exception: %r' % (sys.exc_info(),)
    return d

if scraperwiki.sqlite.get_var('step')==None:
    partstep = scraperwiki.sqlite.get_var('partstep') or 0
    if partstep == 0:
        scraperwiki.sqlite.execute('drop table if exists `swdata`')
    f=urlopen(parturl % partstep)
    d=list(fixfields(i) for i in scraperwiki.swimport("csv2sw").csv2json(f))
    pprint.pprint(d[:40])
    scraperwiki.sqlite.save([],d)
    if partstep < 4: #4 or -1
        scraperwiki.sqlite.save_var('partstep',partstep+1)
    else:
        scraperwiki.sqlite.save_var('step',1)
elif scraperwiki.sqlite.get_var('step')==1:
    months = tuple(itertools.chain.from_iterable([unicode("%04d-%02d") % (y,m) for m in range(1,13)] for y in range(2005,2011)))
    months = dict(zip(months,[0]*len(months)))
    pprint.pprint(months.keys())
    agg=scraperwiki.sqlite.select('count(*) as "data", fid_2 as "name", yearmonth from `swdata` group by yearmonth,fid_2 order by fid_2')
    agg1=itertools.groupby(agg,lambda x:x['name'])
    agg=[
        dict([
            ['name',mosques[int(k)]],
            ['data',
                map(lambda y: y[1],sorted(updateandreturn(
                    months.copy(),
                    [(m['yearmonth'],m['data']) for m in g if m['yearmonth'] in months.keys()]
                ).items(),key=lambda x: x[0]))
            ]
        ]) for k,g in agg1
    ]
    pprint.pprint(agg)
    simplejson.dumps(agg)
