# Planning applications aggregator for Durham County Council

#This is a unitary authority with planning structure devolved to the original 8 districts. 
#This scraper collects together all applications from the 8 sources.

import scraperwiki
import gc

scraperwiki.sqlite.attach('appsearchserv_system_planning_applications', 'appsearchserv')
scraperwiki.sqlite.attach('publicaccess_system_planning_applications', 'publicaccess')
scraperwiki.sqlite.attach('durham_district_planning_applications', 'custom')

systems = {
    'Crook (Wear Valley)': { 'type': 'appsearchserv', 'table': 'Crook' },
    'Easington': { 'type': 'appsearchserv', 'table': 'Easington' },
    'Chester-le-Street': { 'type': 'publicaccess', 'table': 'ChesterLeStreet' },
    'Durham (City)': { 'type': 'publicaccess', 'table': 'DurhamCity' },
    'Consett (Derwentside)': { 'type': 'custom', 'table': 'Consett' },
    'Sedgefield': { 'type': 'custom', 'table': 'Sedgefield' },
    'Barnard Castle (Teesdale)': { 'type': 'custom', 'table': 'BarnardCastle' },
    'Durham (County)': { 'type': 'custom', 'table': 'DurhamCounty' },
}

num_saved = 0
for k, v in systems.items():
    try:
        sql = '* from ' + v['type'] + '.' + v['table']
        data = scraperwiki.sqlite.select(sql)
        for datum in data:
            datum['district'] = k
        scraperwiki.sqlite.save(['uid'], data)
        print 'Source:', k, ' (saved', len(data), 'rows)'
        num_saved += len(data)
        data = None
        gc.collect()
    except:
        print 'Error:', k, ' (no data aggregated)'
print "Total applications stored =", num_saved

scraperwiki.sqlite.execute("create index if not exists date_scraped_manual_index on swdata (date_scraped)")
scraperwiki.sqlite.execute("create index if not exists start_date_manual_index on swdata (start_date)")



# Planning applications aggregator for Durham County Council

#This is a unitary authority with planning structure devolved to the original 8 districts. 
#This scraper collects together all applications from the 8 sources.

import scraperwiki
import gc

scraperwiki.sqlite.attach('appsearchserv_system_planning_applications', 'appsearchserv')
scraperwiki.sqlite.attach('publicaccess_system_planning_applications', 'publicaccess')
scraperwiki.sqlite.attach('durham_district_planning_applications', 'custom')

systems = {
    'Crook (Wear Valley)': { 'type': 'appsearchserv', 'table': 'Crook' },
    'Easington': { 'type': 'appsearchserv', 'table': 'Easington' },
    'Chester-le-Street': { 'type': 'publicaccess', 'table': 'ChesterLeStreet' },
    'Durham (City)': { 'type': 'publicaccess', 'table': 'DurhamCity' },
    'Consett (Derwentside)': { 'type': 'custom', 'table': 'Consett' },
    'Sedgefield': { 'type': 'custom', 'table': 'Sedgefield' },
    'Barnard Castle (Teesdale)': { 'type': 'custom', 'table': 'BarnardCastle' },
    'Durham (County)': { 'type': 'custom', 'table': 'DurhamCounty' },
}

num_saved = 0
for k, v in systems.items():
    try:
        sql = '* from ' + v['type'] + '.' + v['table']
        data = scraperwiki.sqlite.select(sql)
        for datum in data:
            datum['district'] = k
        scraperwiki.sqlite.save(['uid'], data)
        print 'Source:', k, ' (saved', len(data), 'rows)'
        num_saved += len(data)
        data = None
        gc.collect()
    except:
        print 'Error:', k, ' (no data aggregated)'
print "Total applications stored =", num_saved

scraperwiki.sqlite.execute("create index if not exists date_scraped_manual_index on swdata (date_scraped)")
scraperwiki.sqlite.execute("create index if not exists start_date_manual_index on swdata (start_date)")



