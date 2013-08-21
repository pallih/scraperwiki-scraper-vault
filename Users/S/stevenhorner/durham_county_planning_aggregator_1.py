# Planning applications aggregator for the former Wear Valley Dsitrict Council

#This is a unitary authority with planning structure devolved to the original 8 districts. 
#This scraper collects together all applications from the 8 sources.

import scraperwiki

scraperwiki.sqlite.attach('appsearchserv_system_planning_applications', 'appsearchserv')
scraperwiki.sqlite.attach('publicaccess_system_planning_applications', 'publicaccess')
scraperwiki.sqlite.attach('durham_district_planning_applications', 'custom')

systems = {
    'Crook (Wear Valley)': { 'type': 'appsearchserv', 'table': 'Crook' },

}

num_saved = 0
for k, v in systems.items():
    data = scraperwiki.sqlite.select('* from ' + v['type'] + '.' + v['table'])
    scraperwiki.sqlite.save(['uid'], data)
    print 'Source:', k, ' (saved', len(data), 'rows)'
    num_saved += len(data)
print "Total applications stored =", num_saved


