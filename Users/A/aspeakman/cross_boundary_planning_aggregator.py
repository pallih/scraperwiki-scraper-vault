# Planning applications aggregator for 15 National Parks, National Planning Infrastrucure and Olympic Delivery Authority
# i.e. planning authorities crossing local authority boundaries

# For each application it lists the appropriate UK local authorities (district/county/region
# note if county is empty, the district field holds the single unitary authority).

import scraperwiki
from datetime import datetime
import random
import urllib
import sys

locat = scraperwiki.utils.swimport("location_library")

scrapers = {
    'planningexplorer2': 'planningexplorer_system_planning_applications_2',
    'publicaccess': 'publicaccess_system_planning_applications',
    'idox': 'idox_system_planning_applications',
    'acolnet2': 'acolnet_system_planning_applications_2',
    'swiftlg2': 'swiftlg_system_planning_applications_2', 
    'swiftlg': 'swiftlg_system_planning_applications',
    'weeklywam': 'weeklywam_system_planning_applications',
    'national': 'nip_planning_applications', 
    'parks': 'national_parks_planning_applications',
}

for k, v in scrapers.items():
    scraperwiki.sqlite.attach(v, k)

systems = {
    'Brecon Beacons National Park': { 'type': 'idox', 'table': 'BreconBeacons' },
    'Broads Authority National Park': { 'type': 'idox', 'table': 'Broads' },
    'Loch Lomond & Trossachs National Park': { 'type': 'idox', 'table': 'LochLomond' },
    'South Downs National Park': { 'type': 'idox', 'table': 'SouthDowns' },
    'New Forest National Park': { 'type': 'acolnet2', 'table': 'NewForestPark' },
    'North York Moors National Park': { 'type': 'planningexplorer2', 'table': 'NorthYorkMoors' },
    'Lake District National Park': { 'type': 'swiftlg', 'table': 'LakeDistrict' },
    'Snowdonia National Park': { 'type': 'swiftlg2', 'table': 'Snowdonia' },
    'Dartmoor National Park': { 'type': 'weeklywam', 'table': 'Dartmoor' },
    'Cairngorms National Park': { 'type': 'idox', 'table': 'Cairngorms' },
    'Pembrokeshire Coast National Park': { 'type': 'parks', 'table': 'PembrokeshireCoast' },
    'Peak District National Park': { 'type': 'parks', 'table': 'PeakDistrict' },
    'Exmoor National Park': { 'type': 'parks', 'table': 'Exmoor' },
    'Northumberland National Park': { 'type': 'parks', 'table': 'NorthumberlandPark' },
    'Yorkshire Dales National Park': { 'type': 'parks', 'table': 'YorkshireDales' },
    'National Infrastructure Planning': { 'type': 'national', 'table': 'swdata' },
    'Olympic Delivery Authority': { 'type': 'publicaccess', 'table': 'OlympicDelivery' },
}

MAX = 100
db_query = "select * from %s where uid = '%s'"
db_url = "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=%s&query=%s"

#print scraperwiki.geo.osgb_to_lonlat('TM1140052500')
#print scraperwiki.geo.osgb_to_eastnorth('TM1140052500')

num_saved = 0
items = systems.items()
random.shuffle(items)
for k, v in items:
    table_name = v['type'] + '.' + v['table']
    # find MAX applications not in the aggregator and most recently scraped
    first_sql = '* from ' + table_name + ' where address is not null order by date_scraped desc limit ' + str(MAX)
    next_sql = '* from ' + table_name + " where address is not null and uid not in (select uid from swdata) order by date_scraped desc limit " + str(MAX)
    try:
        data = scraperwiki.sqlite.select(next_sql)
    except:
        data = scraperwiki.sqlite.select(first_sql)
    new_data = []
    for applic in data:
        store = {}
        store['date_aggregated'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        store['national_authority'] = k
        store['uid'] = applic['uid']
        store['scraper'] = scrapers[v['type']]
        store['table'] = v['table']
        query = db_query % (v['table'], store['uid'])
        #print query
        url = db_url % (urllib.quote_plus(scrapers[v['type']]), urllib.quote_plus(query))
        #print url
        store['data_url'] = url
        store['source_url'] = applic['url']
        #print applic
        locat.set_latlngpost(applic)
        #print applic
        if applic.get('postcode'):
            extra = locat.postcode_lookup(applic['postcode'])
            if extra:
                #print extra
                store['postcode'] = applic['postcode']
                store['lat'] = extra['lat']
                store['lng'] = extra['lng']
                store['easting'] = extra['easting']
                store['northing'] = extra['northing']
                if extra.get('region'):
                    store['region'] = extra['region']
                    store['region_gss'] = extra['region_gss']
                    store['region_snac'] = extra['region_snac']
                if extra.get('county'):
                    store['county'] = extra['county']
                    store['county_gss'] = extra['county_gss']
                    store['county_snac'] = extra['county_snac']
                if extra.get('district'):
                    store['district'] = extra['district']
                    store['district_gss'] = extra['district_gss']
                    store['district_snac'] = extra['district_snac']
                #print store
                #sys.exit()
            new_data.append(store)
            #break  
    #print new_data
    scraperwiki.sqlite.save(['uid'], new_data)
    print 'Source:', k, ' (saved', len(new_data), 'rows)'
    num_saved += len(new_data)
    #break
print "Total applications stored =", num_saved

# Planning applications aggregator for 15 National Parks, National Planning Infrastrucure and Olympic Delivery Authority
# i.e. planning authorities crossing local authority boundaries

# For each application it lists the appropriate UK local authorities (district/county/region
# note if county is empty, the district field holds the single unitary authority).

import scraperwiki
from datetime import datetime
import random
import urllib
import sys

locat = scraperwiki.utils.swimport("location_library")

scrapers = {
    'planningexplorer2': 'planningexplorer_system_planning_applications_2',
    'publicaccess': 'publicaccess_system_planning_applications',
    'idox': 'idox_system_planning_applications',
    'acolnet2': 'acolnet_system_planning_applications_2',
    'swiftlg2': 'swiftlg_system_planning_applications_2', 
    'swiftlg': 'swiftlg_system_planning_applications',
    'weeklywam': 'weeklywam_system_planning_applications',
    'national': 'nip_planning_applications', 
    'parks': 'national_parks_planning_applications',
}

for k, v in scrapers.items():
    scraperwiki.sqlite.attach(v, k)

systems = {
    'Brecon Beacons National Park': { 'type': 'idox', 'table': 'BreconBeacons' },
    'Broads Authority National Park': { 'type': 'idox', 'table': 'Broads' },
    'Loch Lomond & Trossachs National Park': { 'type': 'idox', 'table': 'LochLomond' },
    'South Downs National Park': { 'type': 'idox', 'table': 'SouthDowns' },
    'New Forest National Park': { 'type': 'acolnet2', 'table': 'NewForestPark' },
    'North York Moors National Park': { 'type': 'planningexplorer2', 'table': 'NorthYorkMoors' },
    'Lake District National Park': { 'type': 'swiftlg', 'table': 'LakeDistrict' },
    'Snowdonia National Park': { 'type': 'swiftlg2', 'table': 'Snowdonia' },
    'Dartmoor National Park': { 'type': 'weeklywam', 'table': 'Dartmoor' },
    'Cairngorms National Park': { 'type': 'idox', 'table': 'Cairngorms' },
    'Pembrokeshire Coast National Park': { 'type': 'parks', 'table': 'PembrokeshireCoast' },
    'Peak District National Park': { 'type': 'parks', 'table': 'PeakDistrict' },
    'Exmoor National Park': { 'type': 'parks', 'table': 'Exmoor' },
    'Northumberland National Park': { 'type': 'parks', 'table': 'NorthumberlandPark' },
    'Yorkshire Dales National Park': { 'type': 'parks', 'table': 'YorkshireDales' },
    'National Infrastructure Planning': { 'type': 'national', 'table': 'swdata' },
    'Olympic Delivery Authority': { 'type': 'publicaccess', 'table': 'OlympicDelivery' },
}

MAX = 100
db_query = "select * from %s where uid = '%s'"
db_url = "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=%s&query=%s"

#print scraperwiki.geo.osgb_to_lonlat('TM1140052500')
#print scraperwiki.geo.osgb_to_eastnorth('TM1140052500')

num_saved = 0
items = systems.items()
random.shuffle(items)
for k, v in items:
    table_name = v['type'] + '.' + v['table']
    # find MAX applications not in the aggregator and most recently scraped
    first_sql = '* from ' + table_name + ' where address is not null order by date_scraped desc limit ' + str(MAX)
    next_sql = '* from ' + table_name + " where address is not null and uid not in (select uid from swdata) order by date_scraped desc limit " + str(MAX)
    try:
        data = scraperwiki.sqlite.select(next_sql)
    except:
        data = scraperwiki.sqlite.select(first_sql)
    new_data = []
    for applic in data:
        store = {}
        store['date_aggregated'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        store['national_authority'] = k
        store['uid'] = applic['uid']
        store['scraper'] = scrapers[v['type']]
        store['table'] = v['table']
        query = db_query % (v['table'], store['uid'])
        #print query
        url = db_url % (urllib.quote_plus(scrapers[v['type']]), urllib.quote_plus(query))
        #print url
        store['data_url'] = url
        store['source_url'] = applic['url']
        #print applic
        locat.set_latlngpost(applic)
        #print applic
        if applic.get('postcode'):
            extra = locat.postcode_lookup(applic['postcode'])
            if extra:
                #print extra
                store['postcode'] = applic['postcode']
                store['lat'] = extra['lat']
                store['lng'] = extra['lng']
                store['easting'] = extra['easting']
                store['northing'] = extra['northing']
                if extra.get('region'):
                    store['region'] = extra['region']
                    store['region_gss'] = extra['region_gss']
                    store['region_snac'] = extra['region_snac']
                if extra.get('county'):
                    store['county'] = extra['county']
                    store['county_gss'] = extra['county_gss']
                    store['county_snac'] = extra['county_snac']
                if extra.get('district'):
                    store['district'] = extra['district']
                    store['district_gss'] = extra['district_gss']
                    store['district_snac'] = extra['district_snac']
                #print store
                #sys.exit()
            new_data.append(store)
            #break  
    #print new_data
    scraperwiki.sqlite.save(['uid'], new_data)
    print 'Source:', k, ' (saved', len(new_data), 'rows)'
    num_saved += len(new_data)
    #break
print "Total applications stored =", num_saved

