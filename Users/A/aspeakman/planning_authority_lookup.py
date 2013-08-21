# maintains a 'status' table showing the status of planning authority scrapers on OpenlyLocal and ScraperWiki

# authority details are derived from 3 downloaded reference tables:

# openlylocal - downloaded reference information on the local authorities known to OpenlyLocal.com
# mapit - downloaded reference information on the local authorities known to Mapit.mysociety.org (not used)
# authorities - downloaded reference information on planning authority scrapers on ScraperWiki (note includes National Parks, Crown Dependencies and others)

import scraperwiki
import urllib2, urllib
import time
import json
import sys
import re
from datetime import date
from datetime import datetime
from datetime import timedelta
import csv
import dateutil.parser
import gc

util = scraperwiki.utils.swimport("utility_library")
scrapemark = scraperwiki.utils.swimport("scrapemark_09")

NUM_TO_SCRAPE = 80

DEBUG = False
#CACHE_EXPIRY = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%S') # 1 month
TIMEOUT = 20
TODAY = date.today().strftime('%Y-%m-%d')
EXTRACT_FULL_POSTCODE = re.compile(r'\b([A-Z][A-Z]?\d(?:\d|[A-Z])?)\s*(\d[ABDEFGHJLNPQRSTUWXYZ]{2})\b', re.I) # ignore case

#National Parks - see
#http://www.ons.gov.uk/ons/guide-method/geography/geographic-policy/coding-and-naming-for-statistical-geographies/chd-look-ups/other-geography/national-parks--great-britain-.zip
# All others
#http://www.ons.gov.uk/ons/guide-method/geography/geographic-policy/coding-and-naming-for-statistical-geographies/chd-look-ups/administrative-geography/index.html

mapit_types = { 'MTD': 'Unitary',
    'LBO': 'Unitary',
    'LGD': 'Unitary',
    'UTA': 'Unitary',
    'COI': 'Unitary', # Scilly Isles
    'CTY': 'County', 
    'DIS': 'District', 
    'EUR': 'Region', 
    }

openlylocal_types = { 'Metropolitan Borough': 'Unitary',
    'London Borough': 'Unitary',
    'Unitary': 'Unitary',
    'Other': None, # Greater London Authority
    'County': 'County',
    'District': 'District', # however note Northern Ireland Districts are Unitary
    }

authority_types = [ 'region', 'unitary', 'district', 'county', 'crown_dependency', 'national_park', 'others' ]
# others NPI, ODA

OL_COUNCIL_URL = "http://openlylocal.com/councils/%s/planning_applications"
SCRAPE_OL_INFO = """
    <div id="planning_applications">
        {* <div class="planning_application"> <span class="date"> {{ [applics].application_date }} </span> </div> *}
    </div>"""
SW_SCRAPER_URL = "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=%s&query=%s"


"""def run(test_query = None):
    try:
        query = scraperwiki.utils.GET()
    except:
        query = {}
    if query and 'test' in query and test_query:
        query = test_query
    format = query.get('fmt', 'xml')
    options = 'authority'
    if not format or format == 'rss' or format == 'atom' or format == 'object':
        format = 'xml'
    if format == 'jsonp' or format == 'json':
        options = query.get('callback')
    if format == 'json' and query.get('callback'):
        util.set_content('jsonp')
    elif format:
        util.set_content(format)
    result = { }

    postcode = query.get('postcode')
    if postcode:
        postcode = locat.postcode_norm(postcode)  
    elif query.get('lat') and (query.get('lng') or query.get('lon')):
        lng =  query['lng'] if query.get('lng') else query['lon']
        plookup = locat.postcode_reverse(lng, query['lat'])
        if plookup and plookup.get('postcode'):
            postcode = locat.postcode_norm(plookup['postcode'])
    if postcode: # note postcode is now in normalised form
        specified_source = query.get('source') # specify a specific source if you want to override the default list
        existing_source = None
        ideal_source = locat.get_postcode_best_source(postcode) # ideal source is the first in the default list
        stale = None
        if specified_source:
            result = None # if source is specified, we always replace the cache entry
            if DEBUG: print "Source specified (", specified_source, ") skipping cache lookup"
        else:
            result = cache_fetch(postcode) # is this query result already in the database cache?
            if result:
                existing_source = result['source']
                if result['date_cached'] < CACHE_EXPIRY:
                    stale = True
                    if DEBUG: print "Found stale cache entry from", existing_source
                else:
                    stale = False
                    if DEBUG: print "Found fresh cache entry from", existing_source
            else:
                if DEBUG: print "Nothing in cache"
        if not result or existing_source <> ideal_source or stale: # try to get data afresh if no existing saved entry or it is not from the most preferred source or it's stale
            new_result = locat.geocode_postcode(postcode, existing_source, specified_source)
            if new_result:
                new_result['matched'] = locat.postcode_norm(new_result['postcode'])
                new_result['postcode'] = postcode # always key on the original normalised postcode, not the returned match which can be different e.g. partial
                new_result['date_cached'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
                cache_put(new_result) # put the new result in the cache
                result = new_result            
    if not result:
        result = { 'error': 'Query parameters not recognised', 'query': query }
    print util.data_output(result, format, options)

# query the database cache table
def cache_fetch(find):
    try:
        sql = "* from authorities where " +
            "snac_id = '%s' or gss_id = '%s' or name like '%%%s%%'" % (find, find, find.replace("'" "''"))
        results = scraperwiki.sqlite.select(sql)
        return results
    except:
        return None

def cache_put(data):
    if data.get('gss_id') and data.get('snac_id'):
        scraperwiki.sqlite.save(unique_keys=['snac_id', 'gss_id'], data=data, table_name='authorities', verbose=0)

#source = None
#fmt = 'xml'
#test_query = { 'find': 'Bolton', 'fmt': fmt, 'source': source  }

#run (test_query)"""


def mapit_authority(id):
    url = 'http://mapit.mysociety.org/area/' + str(id) # also http://mapit.mysociety.org/code/gss/' + str(id)
    if DEBUG: print 'Url', url
    result = util.json_get(url, None, TIMEOUT)
    if DEBUG: print 'Result', result
    if result and result.get('codes'):
        if 'gss' in result['codes']:
            gss_id = result['codes']['gss']
        else:
            gss_id = None
        return { 'mapit_id': result['id'],
            'snac_id': result['codes']['ons'],
            'gss_id': gss_id,
            'name': result['name'],
            'type': result['type_name'] }
    else:
        return None

def openlylocal_authority(id):
    url = 'http://openlylocal.com/councils/' + str(id) + '.json' 
    if DEBUG: print 'Url', url
    result = util.json_get(url, None, TIMEOUT)
    if DEBUG: print 'Result', result
    if result and result.get('council'):
        if result['council']['country'] == 'Northern Ireland':
            atype = 'Unitary'
        else:
            atype = result['council']['authority_type']
        return { 'openlylocal_id': result['council']['id'],
            'snac_id': result['council']['snac_id'],
            'gss_id': result['council']['gss_code'],
            'name': result['council']['name'],
            'type': atype }
    else:
        return None

def download_openlylocal_table():
    url = 'http://openlylocal.com/councils/all.json'
    if DEBUG: print 'Url', url
    result = util.json_get(url, None, TIMEOUT)
    if DEBUG: print 'Result', result
    if result and result.get('councils'):
        data = []
        for c in result['councils']:
            atype = openlylocal_types[c['authority_type']]
            if c['country'] == 'Northern Ireland':
                atype = 'Unitary'
            if not atype:
                continue
            item = { 'openlylocal_id': c['id'], 'snac_id': c['snac_id'], 'gss_id': c['gss_code'], 'name': c['name'], 'type': atype }
            data.append(item)
        scraperwiki.sqlite.execute('drop table if exists openlylocal')
        scraperwiki.sqlite.commit()
        scraperwiki.sqlite.save(unique_keys=['openlylocal_id'], data=data, table_name='openlylocal', verbose=0)
        return True
    else:
        return False

def download_mapit_table():
    types = mapit_types.keys()
    url = 'http://mapit.mysociety.org/areas/' + ','.join(types) 
    if DEBUG: print 'Url', url
    result = util.json_get(url, None, TIMEOUT)
    if DEBUG: print 'Result', result
    if result:
        data = []
        for k, v in result.items():
            if 'gss' in v['codes']:
                gss_id = v['codes']['gss']
            else:
                gss_id = None
            atype = mapit_types[v['type']]
            item = { 'mapit_id': int(k), 'snac_id': v['codes']['ons'], 'gss_id': gss_id, 'name': v['name'], 'type': atype }
            data.append(item)
        scraperwiki.sqlite.execute('drop table if exists mapit')
        scraperwiki.sqlite.commit()
        scraperwiki.sqlite.save(unique_keys=['mapit_id'], data=data, table_name='mapit', verbose=0)
        return True
    else:
        return False

def download_authorities_table():
    url = 'https://docs.google.com/spreadsheet/pub?hl=en_GB&key=0Al4N5JeEnLXAdGtyS1ZJTW9nSEIySWRNN3F5RG1DVVE&single=true&gid=0&output=csv'
    if DEBUG: print 'Url', url
    result = scraperwiki.scrape(url)
    if DEBUG: print 'Result', result
    if result:
        reader = csv.DictReader(result.splitlines())
        data = []
        for r in reader:
            item = { 'authority_id': int(r['authority_id']), 'snac_id': r['snac_id'], 'gss_id': r['gss_id'], 'name': r['name'].strip(), 'long_name': r['long_name'].strip(), 'scraper': r['scraper'].strip(), 'table_name': r['table_name'].strip()}
            data.append(item)
        scraperwiki.sqlite.execute('drop table if exists authorities')
        scraperwiki.sqlite.commit()
        scraperwiki.sqlite.save(unique_keys=['authority_id'], data=data, table_name='authorities', verbose=0)
        return True
    else:
        return False

# gather latest date information on an OpenlyLocal planning authority
def get_ol_latest_date(openlylocal_id):
    try:
        query = OL_COUNCIL_URL % str(openlylocal_id)
        response = urllib2.urlopen(query)
        html = response.read()
        response.close()
        result = scrapemark.scrape(SCRAPE_OL_INFO, html)
        for i in result['applics']:
            this_date = dateutil.parser.parse(i['application_date'], dayfirst=True).date().strftime('%Y-%m-%d')
            if this_date <= TODAY:
                return this_date
        return None
    except:
        return None

# gather latest date information on a ScraperWiki planning authority
def get_sw_latest_date(scraper, table_name = None):
    if not table_name:
        table_name = 'swdata'
    date_prefs = [ 'start_date', 'date_received', 'date_validated' ]
    for i in date_prefs:
        try:
            sql = "select %s from %s where %s is not null and %s <= '%s' order by %s desc limit 1" % (i, table_name, i, i, TODAY, i)
            if DEBUG: print sql
            url = SW_SCRAPER_URL % (scraper, urllib.quote_plus(sql))
            result = util.json_get(url, None, TIMEOUT)
            if DEBUG: print result
            if not result: continue
            dt = result[0][i]
            return dateutil.parser.parse(dt, dayfirst=True).date().strftime('%Y-%m-%d')
        except:
            pass
    return None

# gather full status information on a ScraperWiki planning authority
def get_sw_latest_info(scraper, table_name = None):
    if not table_name:
        table_name = 'swdata'
    result = {}
    field_names = scraper_field_names(scraper, table_name)
    if not field_names:
        return result
    result['field_names'] = ', '.join(field_names)
    recent = datetime.now() - timedelta(days=7) # records scraped within the last week are 'recent'
    current = date.today() - timedelta(days=60) # records with start dates within the last 60 days are 'current'
    too_late = date.today() + timedelta(days=240) # max valid record date that can be set in the future
    too_early = date(1990,1,1) # min valid record date in the past
    subs = { 'rct': recent.strftime('%Y-%m-%d'), 'crt': current.strftime('%Y-%m-%d'), 'tdy': TODAY, 'tbl': table_name, 
        'erl': too_early.strftime('%Y-%m-%d'), 'tlt': too_late.strftime('%Y-%m-%d')}
    extra_fields_test = ''
    if 'url' in field_names:
        extra_fields_test += ", sum(CASE WHEN url is null or url = '' THEN 0 ELSE 1 END) as url_count"
    else:
        extra_fields_test += ", 0 as url_count"
    if 'address' in field_names:
        extra_fields_test += ", sum(CASE WHEN address is null or address = '' THEN 0 ELSE 1 END) as address_count"
    else:
        extra_fields_test += ", 0 as address_count"
    if 'description' in field_names:
        extra_fields_test += ", sum(CASE WHEN description is null or description = '' THEN 0 ELSE 1 END) as description_count"
    else:
        extra_fields_test += ", 0 as description_count"
    if 'start_date' in field_names:
        subs['sdt'] = 'start_date'
    elif 'date_received' in field_names:
        subs['sdt'] = 'date_received'
    elif 'date_validated' in field_names:
        subs['sdt'] = 'date_validated'
    else:
        subs['sdt'] = 'start_date'
    eft = ", sum(CASE WHEN %(sdt)s is null or %(sdt)s < '%(erl)s' or %(sdt)s > '%(tdy)s' THEN 0 ELSE 1 END) as used_sdate_count" % subs
    subs['eft'] = extra_fields_test + eft
    full_records_query = """select count(*) as num_full_recs %(eft)s from %(tbl)s where date_scraped is not null""" % subs
    temp_result = scraper_query(scraper, full_records_query)
    if not temp_result:
        return {}
    result.update(temp_result)
    current_records_query = """select count(*) as num_current,
        sum(CASE WHEN date_scraped >= '%(rct)s' THEN 1 ELSE 0 END) as num_recently_scraped,
        min(date_scraped) as first_recently_scraped, max(date_scraped) as last_recently_scraped,
        min(%(sdt)s) as first_current, max(%(sdt)s) as last_current
        from %(tbl)s where date_scraped is not null and %(sdt)s is not null and %(sdt)s >= '%(crt)s'
        and %(sdt)s <= '%(tdy)s'""" % subs
    date_range_query = """select min(%(sdt)s) as first_full_rec, max(%(sdt)s) as last_full_rec from %(tbl)s 
        where date_scraped is not null and %(sdt)s is not null and %(sdt)s > '%(erl)s' and %(sdt)s <= '%(tdy)s'""" % subs
    num_recs_query = "select count(*) as num_recs from %s" % table_name
    num_idonly_query = "select count(*) as num_idonly from %s where date_scraped is null" % table_name
    result.update(scraper_query(scraper, current_records_query))
    result.update(scraper_query(scraper, date_range_query))
    result.update(scraper_query(scraper, num_recs_query))
    result.update(scraper_query(scraper, num_idonly_query))
    result.update(scraper_runinfo(scraper))

    # plot of good dates distribution
    good_date_query = """select %(sdt)s from %(tbl)s where date_scraped is not null and %(sdt)s is not null
            and %(sdt)s >= '%(erl)s' and %(sdt)s <= '%(tlt)s'""" % subs
    temp_result = scraper_query(scraper, good_date_query, False)
    if temp_result:
        dlist = util.get_list(temp_result, subs['sdt'])
        result['date_plot'] = util.plotdates(dlist, 25)
    else:
        result['date_plot'] = None
    # bad dates field list
    bad_date_fields = []
    for i in field_names:
        if i <> 'date_scraped' and (i.startswith('date_') or i.endswith('_date')):
            subs['dnm'] = i
            bad_date_query = """select %(dnm)s from %(tbl)s where date_scraped is not null and %(dnm)s is not null
                    and (%(dnm)s < '%(erl)s' or %(dnm)s > '%(tlt)s')""" % subs
            temp_result = scraper_query(scraper, bad_date_query, False)
            if temp_result:
                if DEBUG: print temp_result
                bad_date_fields.append(i + '(' + str(len(temp_result)) + ')')
    result['bad_date_fields'] = ', '.join(bad_date_fields)
    # estimate of percent invalid postcodes
    postcodes_percent = 0.0
    if 'postcode' in field_names:
        postcode_query = """select address || ' ' || postcode as address from %(tbl)s where date_scraped is not null order by date_scraped desc limit 1000""" % subs
    else:
        postcode_query = """select address from %(tbl)s where date_scraped is not null order by date_scraped desc limit 1000""" % subs
    temp_result = scraper_query(scraper, postcode_query, False)
    if temp_result:
        postcodes_count = 0
        for r in temp_result:
            if r.get('address') and EXTRACT_FULL_POSTCODE.search(r['address']):
                postcodes_count += 1
        postcodes_percent = 100.0 * float(postcodes_count) / float(len(temp_result))
    result['postcodes_percent'] = postcodes_percent
    return result

def scraper_query(scraper, sql = None, first_only = True, url_sub = 'https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=%s&query=%s'):
    if DEBUG: print sql
    if sql:
        query = url_sub % (urllib.quote_plus(scraper), urllib.quote_plus(sql))
    else:
        query = url_sub % urllib.quote_plus(scraper)
    if DEBUG: print query
    result = util.json_get(query, None, TIMEOUT)
    if DEBUG: print result
    if result and 'error' not in result:
        if first_only: return result[0]
        else: return result
    else:
        return {}

def scraper_runinfo(scraper, url_sub = 'https://api.scraperwiki.com/api/1.0/scraper/getruninfo?format=jsondict&name=%s'):
    result = scraper_query(scraper, None, True, url_sub)
    if result:
        info = {}
        info['last_run'] = result.get('run_ended')
        output = result.get('output')
        info['last_msg'] = output[:250]
        m = re.search(r"EXECUTIONSTATUS: ([\d\.]+) seconds elapsed", output)
        if m:
            info['last_run_time'] = float(m.group(1))
        else:
            info['last_run_time'] = 0.0
        return info
    else:
        return result

def scraper_field_names(scraper, table_name = None):
    if not table_name:
        table_name = 'swdata'
    query = "PRAGMA table_info(%s)" % table_name
    result = scraper_query(scraper, query, False)
    if result:
        field_names = []
        for i in result:
            field_names.append(i['name'])
        return field_names
    else:
        return []   

# gather status information on ScraperWiki and OpenlyLocal planning scrapers
def update_scraper_status(max = 100):
    ids_toupdate = []
    try:
        result = scraperwiki.sqlite.select('authority_id FROM status')
        existing_ids = []
        for i in result:
            existing_ids.append(str(i['authority_id']))
    except:
        existing_ids = []
    sql = """authority_id, au.snac_id as snac_id, openlylocal_id, au.name as name, au.long_name as sw_name, ol.name as ol_name FROM 
        authorities as au left outer join openlylocal as ol on ol.snac_id = au.snac_id
        where authority_id not in ( """ + ",".join(existing_ids) + ' ) limit ' + str(max)
    untested_ids = scraperwiki.sqlite.select(sql)
    if DEBUG: print "Untested", len(untested_ids), untested_ids
    ids_toupdate.extend(untested_ids)
    remainder = max - len(untested_ids)
    if remainder > 0:
        try :
            least_recent_ids = scraperwiki.sqlite.select('* FROM status where authority_id is not null order by checked_at asc limit ' + str(remainder))
        except:
            least_recent_ids = []
        if DEBUG: print "Recent", len(least_recent_ids), least_recent_ids
        ids_toupdate.extend(least_recent_ids)
    update_count = 0; failed_count = 0
    for i in ids_toupdate:
        save = {}
        save.update(i)
        ol_ok = None
        if save.get('openlylocal_id'):
            ol_check = get_ol_latest_date(save['openlylocal_id'])
            if not ol_check: 
                print "No OpenlyLocal info for :", save['name']
                ol_ok = False
            else:
                ol_ok = True
            save['ol_most_recent'] = ol_check
        result = scraperwiki.sqlite.select('name, scraper, table_name FROM authorities where authority_id = ' + str(save['authority_id']))
        sw_ok = None
        if not result:
            print "No ScraperWiki info for :", save['name']
            name = None; scraper = None; table_name = None
        else:
            name = result[0]['name']
            scraper = result[0]['scraper']
            table_name = result[0]['table_name']
        if scraper:
            this_r = get_sw_latest_info(scraper, table_name)
            if not this_r or not this_r.get('last_full_rec'):
                print "No Scraperwiki update info for:", save['name'], save['scraper'], save['table_name'], this_r
                sw_ok = False
            else:
                save.update(this_r)
                save['sw_most_recent'] = this_r['last_full_rec']
                sw_ok = True
        if (sw_ok and ol_ok) or (sw_ok is None and ol_ok) or (not ol_ok and sw_ok):
            save['checked_at'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            update_count += 1
            scraperwiki.sqlite.save(unique_keys=['authority_id'],data=save, table_name='status')
        else:
            failed_count += 1
            print "Not updated:", save['name'], ol_ok, sw_ok
    print "Finished updating status of scrapers: ok %d, failed %d" % (update_count, failed_count)

#print get_ol_latest_date(380)
#print scraperwiki.sqlite.select('scraper, table_name FROM authorities where authority_id = 789')
#print get_sw_latest_info('bournemouth_planning_applications') 
#print get_sw_latest_date('_planning_applications')
#print get_sw_latest_info('swiftlg_system_planning_applications', 'Enfield')
#print get_sw_latest_info('brent_planning_applications')
#sys.exit()


#scraperwiki.sqlite.execute('drop table if exists status')
#scraperwiki.sqlite.commit()

#download_openlylocal_table()
#download_mapit_table()
download_authorities_table() # changes over time

update_scraper_status(NUM_TO_SCRAPE)

