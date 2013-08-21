import scraperwiki
import urllib
import cgi
import sys

util = scraperwiki.utils.swimport("utility_library")
locat = scraperwiki.utils.swimport("location_library")

processing_slot, slot_secs = util.get_slot() # gets a 60 second processing slot number if available
if processing_slot < 0:
    scraperwiki.utils.httpstatuscode(503) # should this go last?
    scraperwiki.utils.httpresponseheader("Retry-After", "60")
    print "Sorry, PA API is too busy, try again in "+ str(slot_secs)+ " seconds"
    sys.exit()

DBS = {
    'East England': "east_england_planning_applications",
    'East Midlands': "east_midlands_planning_applications",
    'London': "london_planning_applications", 
    'Northern Ireland': "northern_ireland_planning_applications", 
    'North East': "north_east_planning_applications", 
    'North West': "north_west_planning_applications", 
    'Scotland': "scotland_planning_applications", 
    'South East': "south_east_planning_applications", 
    'South West': "south_west_planning_applications", 
    'Wales': "wales_planning_applications",
    'West Midlands': "west_midlands_planning_applications",
    'Yorkshire and Humber': "yorkshire_planning_applications" 
    }

prefixed = { 'East Midlands', 'North East', 'North West', 'South East', 'South West', 'West Midlands' }

auth_info = {
    'title': 'Planning Authorities',
    'description': 'Planning authorities',
    'parameters': 'fmt, db, auth, dtype, from, to, pcode, lat, lng, dist, max',
}

applic_info = {
    'title': 'Planning Applications',
    'description': 'Selected planning applications',
}

default_db = 'London'
this_view = 'pa_api'
this_url = 'https://views.scraperwiki.com/run/'+this_view+'/'
max_list = 200 # default max applications to return in one list
tag_prefix = "tag:scraperwiki.com,2011:"+this_view+":"
default_dist = '1.0' # default search radius in km

# return a list of all planning authorities the database has records for
def show_authorities(query):
    data = {}
    data.update(auth_info)
    data['link'] = this_url+'?'+urllib.urlencode(query)
    dbase = query.get('db', default_db)
    if dbase in prefixed:
        data['description'] = data['description'] + ' in the ' + dbase + ' region of the UK'
    else:
        data['description'] = data['description'] + ' in ' + dbase + ' in the UK'
    data['title'] = dbase + ' ' + data['title']
    data['id'] = tag_prefix+urllib.quote_plus(dbase)+':authorities'
    fields = {
        'title': 'name',
        'description': 'long_name',
    }
    results = util.get_table_vals('authorities', fields, '', 'order by name asc')
    for r in results: 
        r['link'] = this_url+'?auth='+urllib.quote_plus(r['title'])
        if query:
            r['link'] = r['link']+'&'+urllib.urlencode(query)
        r['id'] = data['id']+':'+urllib.quote_plus(r['title'])
    data['authorities'] = { 'authority': results }
    options = ''
    format = query.get('fmt')
    if not format or format == 'object':
        format = 'xml'
    if format == 'rss':
        options = {}
        options.update(util.all_rss_fields)
        options.update({
        'items': 'authorities',
        'item': 'authority', })
    elif format == 'atom':
        options = {}
        options.update(util.all_atom_fields)
        options.update({ 
        'items': 'authorities',
        'item': 'authority', })
    elif format == 'xml' or format == 'html':
        options = 'active authorities'
    elif format == 'jsonp' or format == 'json':
        options = query.get('callback')
    return util.data_output(data, format, options)

# return a GeoRSS encoded list of planning applications
def show_applications(query):
    data = {}
    data.update(applic_info)
    data['link'] = this_url+'?'+urllib.urlencode(query)
    max = query.get('max', str(max_list))
    if not max.isdigit() or int(max) <= 0:
        max = str(max_list)
    auths_map = util.get_map(util.get_table_vals('authorities', 'name, long_name'), 'name', 'long_name') # cache this?
    auth = query.get('auth')
    if query.get('auth') or query.get('pcode'): 
        subregion = ' (' + query.get('auth', '') + query.get('pcode', '') + ')'
    else:    
        subregion = ''
    dbase = query.get('db', default_db)
    if dbase in prefixed:
        data['description'] = data['description'] + ' from the ' + dbase + subregion + ' region of the UK'
    else:
        data['description'] = data['description'] + ' from ' + dbase + subregion + ' in the UK'
    data['title'] = dbase + subregion + ' ' + data['title']
    data['id'] = tag_prefix+urllib.quote_plus(dbase)+':applications'
    format = query.get('fmt')
    if not format or format == 'object':
        format = 'xml'
    orderetc = 'order by CASE WHEN received_date IS NULL THEN validated_date ELSE received_date END desc, authority asc, reference asc limit '+max
    where = applications_query(query)
    data['sql_query'] = where + ' ' + orderetc
    results = util.get_table_vals('applications', '', where, orderetc)
    for r in results:
        latlng = None
        if r.get('lat') and r.get('lng'):
            latlng = ("%.5f" % r['lat']) + ',' + ("%.5f" % r['lng'])   
            r['point'] = latlng.replace(',', ' ')
        dateid = ''
        if r.get('received_date'):
            dateid = 'rcvd:'+urllib.quote_plus(r['received_date'])
            this_date = r['received_date']
        elif r.get('validated_date'):
            dateid = 'vlid:'+urllib.quote_plus(r['validated_date'])
            this_date = r['validated_date']
        else:
            this_date = ''
        r['id'] = data['id']+':'+urllib.quote_plus(r['authority'])+':'+urllib.quote_plus(r['reference'])+':'+dateid
        r['authority_long_name'] = auths_map[r['authority']]
        if format == 'atom' or format == 'rss':
            r['date'] = this_date
            full_description = '<p>'+r['description']+'</p>' + \
                     '<p>Authority: '+r['authority_long_name']+' | '+ \
                     'Reference: '+r['reference']+'</p>'
            extras = ''
            if r.get('received_date'): 
                extras = 'Received: '+util.convert_dt(r['received_date'],util.ISO8601_DATE,util.DATE_FORMAT)
            if r.get('validated_date'):
                if extras: extras = extras + ' | '
                extras = extras+'Validated: '+util.convert_dt(r['validated_date'],util.ISO8601_DATE,util.DATE_FORMAT)
            if extras: full_description = full_description + '<p>' + extras + '</p>'
            extras = ''
            if r.get('postcode'): 
                extras = 'Postcode: '+r['postcode']
            if latlng:
                if extras: extras = extras + ' | '
                extras += 'Lat,Lng: '+latlng
            if extras: full_description = full_description + '<p>' + extras + '</p>'
            full_description = full_description+'<p><a href="'+r['info_url']+'" target="_blank">View application</a> | '
            gquery = urllib.quote_plus(util.ascii(r['address']))
            if latlng: gquery += '@'+latlng
            full_description = full_description+'<a href="http://maps.google.co.uk/?q='+gquery+'" target="_blank">Show on map</a></p>'
            r['description'] = full_description
    data['applications'] = { 'application': results }
    options = ''
    if format == 'rss':
        options = {}
        options.update(util.all_rss_fields)
        options.update({ # field map for items within RSS feed
        'items': 'applications',
        'item': 'application',
        'sub_item': {
            'title': 'address',
            'description': 'description',
            'guid': 'id',
            'link': 'info_url',
            'pubDate': 'date'
            }})
    elif format == 'atom':
        options = {}
        options.update(util.all_atom_fields)
        options.update({ # field map for items within ATOM feed
        'items': 'applications',
        'item': 'application',
        'sub_item': {
            'title': 'address',
            'summary': 'description',
            'id': 'id',
            'link': 'info_url',
            'published': 'date'
            }})
    elif format == 'xml' or format == 'html':
        options = 'active applications'
    elif format == 'jsonp' or format == 'json':
        options = query.get('callback')
    return util.data_output(data, format, options)

# formats a 'where' query based on authority, dates or distance from a point
def applications_query(query):
    auth = query.get('auth')
    dt_type = query.get('dtype', '') # date type = received, validated or either
    dt_from = query.get('from')
    dt_to = query.get('to')
    slat = query.get('lat')
    slng = query.get('lng')
    pcode = query.get('pcode')
    dist = query.get('dist') # distance from centre of search zone in km
    where = []
    if auth:
        auth_list = auth.split(',')
        joinup = "','".join(auth_list)
        where.append("authority in ('"+joinup+"')")
    if dt_from and dt_to:
        dtfm = util.convert_dt(dt_from, util.DATE_FORMAT, util.ISO8601_DATE)
        dtto = util.convert_dt(dt_to, util.DATE_FORMAT, util.ISO8601_DATE)
        q = '('
        if dt_type != 'validated':
            q += "(received_date is not null and received_date between '"+dtfm+"' and '"+dtto+"')"
        if dt_type != 'received' and dt_type != 'validated':
            q += ' or '
        if dt_type != 'received':
            q += "(validated_date is not null and validated_date between '"+dtfm+"' and '"+dtto+"')"
        where.append(q+')')
    elif dt_from:
        dtfm = util.convert_dt(dt_from, util.DATE_FORMAT, util.ISO8601_DATE)
        q = '('
        if dt_type != 'validated':
            q += "(received_date is not null and received_date >= '"+dtfm+"')"
        if dt_type != 'received' and dt_type != 'validated':
            q += ' or '
        if dt_type != 'received':
            q += "(validated_date is not null and validated_date >= '"+dtfm+"')"
        where.append(q+')')
    elif dt_to:
        dtto = util.convert_dt(dt_to, util.DATE_FORMAT, util.ISO8601_DATE)
        where.append('(')
        if dt_type != 'validated':
            q += "(received_date is not null and received_date <= '"+dtto+"')"
        if dt_type != 'received' and dt_type != 'validated':
            q += ' or '
        if dt_type != 'received':
            q += "(validated_date is not null and validated_date <= '"+dtto+"')"
        where.append(q+')')
    if (slat and slng) or pcode:
        if not slat and not slng:
            slat = '0'
            slng = '0'
            pdata = locat.postcode_lookup(pcode)
            if pdata:
                slat = str(pdata['lat'])
                slng = str(pdata['lng'])
        if not dist:
            dist = default_dist
        #realdist = "distance ("+slat+", "+slng+", cast(lat as real), cast(lng as real)) <= "+str(dist) # does not work in the where clause?
        #where.append(realdist)
        distsq = str(float(dist) * float(dist)) # compare square of Euclidean distance
        where.append("( ((lat - "+slat+") * 111) * ((lat - "+slat+") * 111) ) + ( ((lng - "+slng+") * 68) * ((lng - "+slng+") * 68) ) <= "+distsq)
        # degree of lat (S-N) approx 111km
        # degree of longitude (E-W) in UK = 68 km (in Wales) (see http://www.csgnetwork.com/degreelenllavcalc.html)
        # London, 51.5 lat = 69.5 km
        # Wales, 52.3 lat = 68 km
        # North West, 54 lat = 65.5 km
        # Scotland 56.7 lat = 61 km
        # diff between lat and lon = 1/ cos(lat) or approx 1.6
    return " and ".join(where)


# proper Haversine spherical distance calc NB not in use and not checked
"""def distance(lat1, lon1, lat2, lon2):
    radius = 6371 # radius of the Earth in km
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
    return d """

# unimplemented and untested method to get true distance function above into sqlite
# note there does seem to be user function that does this in the Scraperwiki sqlite dataproxy as distance (lat1, lon1, lat2, lon2)
# see https://bitbucket.org/ScraperWiki/scraperwiki/src/839c259ba2b9/uml/dataproxy/sqlite_functions.py
# but not working with field names as parameterss
"""def radius_query():
    con = sqlite3.connect(source_scraper)
    print conn
    conn.create_function("dist", 1, distance)
    cur = conn.cursor()
    print cur.execute("select distance(?, ?, lat, lon) <= ?", (slat, slon, sdist))"""

def run(test_query = None):
    try:
        query = scraperwiki.utils.GET()
    except:
        query = {}
    if query and 'test' in query and test_query:
        query = test_query
    format = query.get('fmt', 'xml')
    if format and format == 'json' and query.get('callback'):
        util.set_content('jsonp')
    else:
        util.set_content(format)
    result = util.cache_fetch(query) # is this query result already in the 12 hour database cache?
    if not result:          
        dbase = query.get('db', default_db)
        try:
            scraperwiki.sqlite.attach(DBS.get(dbase))
        except:
            scraperwiki.sqlite.attach(DBS.get(default_db))
            del query['db']
        if 'auth' in query or 'from' in query or 'to' in query or 'dist' in query or 'pcode' in query or 'lat' in query or 'lng' in query or 'dtype' in query or 'max' in query:
            result = show_applications(query)
        else:
            result = show_authorities(query)
        util.cache_put(query, result) # put the result in the cache with the default 12 hour timeout
    print result
    util.free_slot(processing_slot) # successful completion, so hand back the 60 sec processing slot

#test_query = { 'auth': 'Barnet', 'from': '27/08/2011' }
#test_query = { 'auth': 'Westminster,Barnet', 'from': '02/08/2011', 'to': '05/08/2011', 'dist': '3.0', 'pcode': 'N16 5JE', 'fmt': 'xml' }
#test_query = { 'dist': '10.0', 'pcode': 'IG11 8UN', 'fmt': 'json' }
test_query = { 'auth': 'Hackney', 'from': '19/09/2011', 'to': '19/09/2011', 'dtype': 'received', 'db': 'London' }
test_query = { 'dist': '1.98', 'pcode': 'N16 5BB', 'fmt': 'xml', 'db': 'London', 'max': '30'  }
#test_query = { 'dist': '2', 'pcode': 'N16 j', 'fmt': 'xml', 'db': 'Wales', 'max': '200'  }
#test_query = { 'auth': 'Barnet', 'db': 'London'  }
#test_query = { 'db': 'East Midlands'  }
#test_query = { 'db': 'London', 'auth': 'Barnet,Hackney', 'max': '28', 'fmt': 'xml'   }
#test_query = { 'dist': '1.5', 'pcode': 'L32 6LB', 'fmt': 'xml', 'db': 'London', 'max': '200'  }


run(test_query)





