# a library of functions for use in planning application scrapers

import scraperwiki
import urllib, urllib2
import socket
from datetime import date
from datetime import timedelta
from datetime import datetime
import urlparse
import dateutil.parser
import re
import mechanize
import time
import random
import warnings
import copy
import json

scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")
locat = scraperwiki.utils.swimport("location_library")

scraperwiki.sqlite.attach("planning_authorities", "src")
SOURCES = "src.authorities"
CONFIGS = "src.configurations"

APPLICATIONS = 'applications'
PROGRESS = 'authorities'
TIMEOUT = 120
DAYS_BLOCK = 14
INDEXED_FIELDS = ['authority', 'received_date', 'validated_date', 'lat', 'lng']
OTHER_REGEX = re.compile(r'{@.*?@}') # find scrapemark other page links
SUBS_REGEX = re.compile(r'%\([^\)]+\)') # find string substitutions
REF_REGEX = re.compile(r'^[\s\(\[]*([^\)\]\s]+).*$') # find reference number - removing spaces and brackets

MAX_REC_VALUE = 200 # default maximum records from one scrape of an authority
MAX_PAG_VALUE = 20 # default maximum pages

PROXY = 'http://www.speakman.org.uk/glype/browse.php?u=%s'

GATEWAY_URL = 'https://views.scraperwiki.com/run/paview_scraper_1/'
OL_URL = 'http://openlylocal.com/councils/%s/planning_applications/'
INFORMATION = {
    'title': 'Planning Gateway',
    'description': 'Authorities that can be scraped via this gateway',
    'link': GATEWAY_URL,
    'parameters': 'fmt, auth, day, month, year, ndays, date, ref',
}

CACHE = {} 

debug = False

# store planning application data, doing any necessary date translations and geocoding at the same time
def store_applications(auth_name, region, applications, applications_table = APPLICATIONS, scrape_date = date.today()):
    for applic in applications:
        applic['authority'] = auth_name
        applic['scrape_date'] = scrape_date.strftime(util.ISO8601_DATE)
        if applic.get('received_date'):
            recvd_dt = util.convert_dt(applic['received_date'], util.DATE_FORMAT, util.ISO8601_DATE, False)
            if recvd_dt:
                applic['received_date'] = recvd_dt
            else:
                del applic['received_date'] # badly formatted date, do not insert
        if applic.get('validated_date'):
            valid_dt = util.convert_dt(applic['validated_date'], util.DATE_FORMAT, util.ISO8601_DATE, False)
            if valid_dt:
                applic['validated_date'] = valid_dt
            else:
                del applic['validated_date'] # badly formatted date, do not insert
        if applic.get('address'):
            if not applic.get('postcode'):
                postcode = locat.extract_postcode(applic['address'])
                if postcode:
                    applic['postcode'] = postcode
        if not applic.get('lat') and not applic.get('lng'):
            locat.set_latlngpost(applic)
            #if applic.get('postcode'):
            #    pdata = util.postcode_lookup(applic['postcode'])
            #    if pdata and pdata.get('lat') and pdata.get('lng'): 
            #        applic['lat'] = str(pdata['lat'])
            #        applic['lng'] = str(pdata['lng'])
            #if applic.get('address') and (not applic.get('lat') and not applic.get('lng')):
            #    lat, lng, postcode = util.geocode(applic['address']) 
            #    if lat or lng:
            #        if not applic.get('postcode') and postcode: # NB only partial postcode returned
            #            applic['postcode'] = postcode
            #        applic['lat'] = str(lat)
            #        applic['lng'] = str(lng)
    scraperwiki.sqlite.save(unique_keys=['authority', 'reference'],
                                data=applications, table_name=applications_table)

# make an external XML request to the gateway, transforming the result to an object and handling timeouts etc
def gateway_request(query, timeout = TIMEOUT, gateway_url = GATEWAY_URL):
    if not timeout: timeout = 0
    url = gateway_url
    if query:
        url = url+'?'+urllib.urlencode(query)
    print_query = ''
    if query:
        print_query = '('+query.get('auth','')+' '+query.get('day','')+'/'+query.get('month','')+'/'+query.get('year','')+')'
    msg = ''
    try:
        response = util.get_response(url, None, None, 'text/xml', timeout)
        # if there is an Internet time out or other fetch error
        # have to cut losses and move on
    except IOError as e:
        if hasattr(e, 'reason'): # URLError
            msg = 'Cannot reach gateway (URL error): '+util.vstr(e)+': '+print_query
        elif hasattr(e, 'code'): # HTTPError
            msg = 'Gateway returned HTTP error: '+util.vstr(e)+': '+print_query
        else:
            msg = 'IO error accessing gateway: '+util.vstr(e)+': '+print_query
    except socket.timeout as e:
        msg = 'Socket timeout accessing gateway ('+str(timeout)+'s): '+util.vstr(e)+': '+print_query
    except Exception as e:
        msg = 'Other error accessing gateway: '+util.vstr(e)+': '+print_query
    else:
        try:
            xml = response.read()
            doc = util.get_doc_xml(xml)
            result = util.from_xml(doc)
        except Exception as e:
            msg = 'Bad XML doc returned from source ('+xml[0:39]+'): '+util.vstr(e)+': '+print_query
        else:
            return result, ''
    return None, msg

# try to gather at least max planning applications from one source
# timeout and gateway URL no longer required as makes direct request to each authority
def gather_applications(target, start, end, max, timeout = TIMEOUT, days_block = DAYS_BLOCK, gateway_url = GATEWAY_URL,
                    applications_table = APPLICATIONS, progress_table = PROGRESS):
    auth_name = target['name']
    try:
        auths = util.get_table_vals(progress_table, '', "name='"+auth_name+"'")
        auth = auths[0]
    except:
        auth = {}
        auth['total'] = 0
    auth.update(target)

    if days_block <= 0: days_block = 1

    db_start_date = util.get_dt(start, util.ISO8601_DATE)
    if not db_start_date:
        db_start_date = date.today() - timedelta(days=start)
    db_end_date = util.get_dt(end, util.ISO8601_DATE)
    if not db_end_date:
        db_end_date = date.today() - timedelta(days=end)
    if not db_start_date or not db_end_date or db_end_date < db_start_date or db_start_date > date.today() or db_end_date > date.today():
        print 'Configuration start / end dates error for '+auth_name
        return

    # 2 dates defining current range of data stored
    start_date = util.get_dt(auth.get('start_date', ''), util.ISO8601_DATE) # start
    last_date = util.get_dt(auth.get('last_date', ''), util.ISO8601_DATE) #end
    if not start_date or start_date > db_start_date: # current start point is empty or after required start point
        scrape_start = db_start_date # start scraping again from the beginning
        start_date = db_start_date
    elif not last_date or last_date < start_date: # no current end point or it is before current start point
        scrape_start = start_date
    elif auth.get('last_status', '') != 'OK': # last scrape was not successful, try again
        scrape_start = last_date
    else:
        scrape_start = last_date + timedelta(days=days_block) # start collecting 1 block after current end point
    if scrape_start > db_end_date:
        scrape_start = db_end_date
    
    result = {}
    total = 0
    status = 'OK'
    while total < max and scrape_start <= db_end_date and status == 'OK':
        result.update(auth)
        result['last_scrape'] = date.today().strftime(util.ISO8601_DATE)
        result['last_date'] = scrape_start.strftime(util.ISO8601_DATE)
        result['start_date'] = start_date.strftime(util.ISO8601_DATE)
        result['last_count'] = 0
        result['last_match_count'] = 0
        status = 'Error'
        result['last_status'] = status
        query = {
            'auth': auth_name,
            'day': str(scrape_start.day),
            'month': str(scrape_start.month),
            'year': str(scrape_start.year), 
            'ndays': str(-days_block), # a block of days preceding the current start date
        }
        msg = ''
        #query['fmt'] = 'xml' # OLD METHOD
        #planning, msg = gateway_request(query, timeout, gateway_url) # XML request via external gateway
        query['fmt'] = 'object'
        planning = execute_scrape(query) # NEW - direct scrape request bypassing external gateway
        if not planning:
            if msg:
                result['last_msg'] = msg
            else:
                result['last_msg'] = 'No planning information returned from source'
        else:
            try:
                test = planning['applications']
            except:
                result['last_msg'] = 'Bad planning information returned from source'
            else:
                status = planning.get('status', 'None')
                result['last_status'] = status
                if planning.get('request_date_type'):
                    result['scrape_date_type'] = planning['request_date_type']        
                if status <> 'OK':
                    result['last_msg'] = planning.get('message', 'None')
                else:
                    result['last_msg'] = 'OK'
                    count = int(planning['count']) if planning.get('count') else 0
                    match_count = int(planning['match_count']) if planning.get('match_count') else 0
                    result['last_count'] = count
                    result['last_match_count'] = match_count
                    if planning.get('until_date'):
                        scrape_start = util.get_dt(planning['until_date'])
                        if scrape_start >= db_end_date:
                            result['last_date'] = db_end_date.strftime(util.ISO8601_DATE)
                        else:
                            result['last_date'] = scrape_start.strftime(util.ISO8601_DATE)
                    if scrape_start < db_end_date:
                        scrape_start = scrape_start + timedelta(days=days_block) # next date block
                        if scrape_start > db_end_date:
                            scrape_start = db_end_date # make sure it enters the while loop next time
                    else:
                        scrape_start = scrape_start + timedelta(days=1) # add increment so it breaks out from the while loop next time
                    if count > 0:
                        applications = planning['applications']['application']
                        store_applications(auth_name, auth['region'], applications, applications_table) # data stored here
                        total = total + count
        scraperwiki.sqlite.save(unique_keys=['name'], data=result, table_name=progress_table, verbose=0)
        if status <> 'OK': last_err = result['last_msg']
        result.clear()
    print 'Scraped '+str(total)+' records from '+auth_name+' ('+str(auth.get('config', ''))+') --> '+status
    if status <> 'OK': print last_err
    if total > 0:
        try:
            applics = util.get_table_vals(applications_table, 'count(*) as total', "authority='"+auth_name+"'")
            count = applics[0]['total']
            util.set_table_vals(progress_table, { 'total': count }, "name='"+auth_name+"'")
        except:
            pass
    return

# clear data from a single planning authority
def restart_authority(auth_name, applications_table = APPLICATIONS, progress_table = PROGRESS):
    if auth_name: # clearing the applications 'start_date' value makes data gathering start again
        util.set_table_vals(progress_table, { 'start_date': '' }, "name='"+auth_name+"'")
        scraperwiki.sqlite.execute("delete from "+applications_table+" where authority='"+auth_name+"'")
        scraperwiki.sqlite.commit()
        print "Successfully cleared the authority data of "+auth_name
    else:
        print "You must specify a single authority name"

# remove a single planning authority permanently
def remove_authority(auth_name, applications_table = APPLICATIONS, progress_table = PROGRESS):
    if auth_name:
        scraperwiki.sqlite.execute("delete from "+progress_table+" where name='"+auth_name+"'")
        scraperwiki.sqlite.execute("delete from "+applications_table+" where authority='"+auth_name+"'")
        scraperwiki.sqlite.commit()
        print "Successfully deleted the authority data of "+auth_name
    else:
        print "You must specify a single authority name"

# get the list of all potential planning authority sources 
# filter by the region or list specified
# and match up with the actual authorities currently in the database
def get_auths(region_or_list = None, progress_table = PROGRESS):
    result = []
    try:
        #scraper, msg = gateway_request( { 'fmt': 'xml' } ) # OLD METHOD = XML request via external gateway
        scraper = execute_scrape( { 'fmt': 'object' } ) # NEW - direct request bypassing external gateway
        all_authorities = scraper['authorities']['authority']
    except:
        pass
    else:
        for auth in all_authorities:
            tagged = False
            if isinstance(region_or_list, list):
                if not region_or_list or auth['name'] in region_or_list:
                    tagged = True
            else:
                if not region_or_list or region_or_list in auth.get('region', ''):
                    tagged = True
            if tagged:
                details = util.get_table_vals(progress_table, '', "name='"+auth['name']+"'")
                if details:
                    details = details[0]
                    details.update(auth)
                else:
                    details = auth
                result.append(details)             
        result = sorted(result, cmp=lambda x,y: cmp(x['name'],y['name']))
    return result

# do housekeeping in the applications database
# 1. check for indexes
# 2. set dates not in standard format to null
# 3. delete any applications older than certain threshold ages (6 months validated, 8 months received)
def do_cleanup(received_days = -240, validated_days = -180, applications_table = APPLICATIONS, ):
    for field_name in INDEXED_FIELDS:
        scraperwiki.sqlite.execute("create index if not exists "+field_name+"_manual_index on "+applications_table+" ("+field_name+")")
    app_data = scraperwiki.sqlite.select("count(*) as records from "+applications_table)
    total = app_data[0]['records']
    scraperwiki.sqlite.execute("update "+applications_table+" set received_date = null where received_date is not null and received_date not like '%-%'")
    scraperwiki.sqlite.execute("update "+applications_table+" set validated_date = null where validated_date is not null and validated_date not like '%-%'")
    scraperwiki.sqlite.commit()
    scraperwiki.sqlite.execute("delete from "+applications_table+" where validated_date is null and received_date is null")
    if received_days < 0 and validated_days < 0 and received_days < validated_days:
        today = date.today().strftime(util.ISO8601_DATE)
        received_days_ago, st = util.inc_dt(today, util.ISO8601_DATE, received_days)
        validated_days_ago, st = util.inc_dt(today, util.ISO8601_DATE, validated_days)
        scraperwiki.sqlite.execute("delete from "+applications_table+" where ((validated_date is not null and validated_date < '"+validated_days_ago+"') or (validated_date is null and received_date is not null and received_date < '"+received_days_ago+"'))")
    scraperwiki.sqlite.commit()
    app_data = scraperwiki.sqlite.select("count(*) as records from "+applications_table)
    total = total - app_data[0]['records']
    print "Created indices, cleaned dates and cleared out "+str(total)+" old records"

# adds location and date information to a planning record
def add_location_etc(record, default_date = None, default_date_type = None, in_date_format = util.DATE_FORMAT):
    if not in_date_format:
        in_date_format = util.DATE_FORMAT
    if record.get('address'):
        record['address'] = util.text_content(record['address']) # strip any html markup and replace with spaces
    if record.get('address') and not record.get('postcode'):
        postcode = locat.extract_postcode(record['address'])
        if postcode:
            record['postcode'] = postcode
    if record.get('received_date'):
        try:
            if in_date_format and in_date_format.startswith('%m'):
                uk_dates = False
            else:
                uk_dates = True
            dt = dateutil.parser.parse(record['received_date'], dayfirst=uk_dates).date()
            record['received_date'] = dt.strftime(util.DATE_FORMAT)
        except:
            try:
                dt = util.get_dt(record['received_date'], in_date_format)
                record['received_date'] = dt.strftime(util.DATE_FORMAT)
            except:
                del record['received_date'] # not a valid date - remove the entry
    elif default_date and default_date_type and default_date_type == 'received':
        record['received_date'] = default_date
    elif 'received_date' in record:
        del record['received_date']
    if record.get('validated_date'):
        try:
            dt = dateutil.parser.parse(record['validated_date'], dayfirst=True).date()
            record['validated_date'] = dt.strftime(util.DATE_FORMAT)
        except:
            try:
                dt = util.get_dt(record['validated_date'], in_date_format)
                record['validated_date'] = dt.strftime(util.DATE_FORMAT)
            except:
                del record['validated_date'] # not a valid date - remove the entry
    elif default_date and default_date_type and default_date_type == 'validated':
        record['validated_date'] = default_date
    elif 'validated_date' in record:
        del record['validated_date']
    if not record.get('reference'):
        if record.get('info_url'):
            record['reference'] = record['info_url'] # reference is a key so cannot be null
        else:
            record['reference'] = 'Empty' # reference is a key so cannot be null
    return record

# tweaks the raw html (NB after it is parsed by the mechanize browser)
def adjust_html(br, subs = None):
    response = br.response()  # this is a copy of the current browser response
    html = response.get_data()
    if debug: print "dbg: html pre sub:", html
    if not subs:
        return response
    for k, v in subs.items():
        html = re.sub(k, v, html, 0, re.U|re.S|re.I) # unicode|dot matches new line|ignore case
    if debug: print "dbg: html post sub:", html
    response.set_data(html)
    br.set_response(response)
    return response

# tweak urls to remove any extraneous stuff
# it is applied to the info_url in the record and to the next link if derived from an href
def adjust_url(url, subs = None):
    if debug: print "dbg: url pre sub:", url
    if not subs:
        return url
    #u = urlparse.urlsplit(url)
    #query = u.query
    #for k, v in subs.items():
    #    query = re.sub(k, v, query, 0, re.U|re.S|re.I) # unicode|dot matches new line|ignore case
    #url = urlparse.urlunsplit((u.scheme, u.netloc, u.path, query, u.fragment))
    for k, v in subs.items():
        url = re.sub(k, v, url, 0, re.U|re.S|re.I) # unicode|dot matches new line|ignore case
    if debug: print "dbg: url post sub:", url
    return url

# return authority/application sources for this scraper in object, XML, JSON or HTML format
def show_data(data, query):
    options = 'planning'
    if 'authorities' in data:
        options = 'scraper'
    fmt = query.get('fmt', '')
    if fmt == 'rss' or fmt == 'atom':
        fmt = 'xml'
    return util.data_output(data, fmt, options)

# set date field(s) using date config
def set_date_fields(fields, config, date, drop_down = False):
    if '{' in config:
        dmy = eval(config)
        if not dmy or ('month' not in dmy and 'MONTH' not in dmy) or 'year' not in dmy:
            raise ScrapeError('invalid date config: '+config)
        date_parts = date.split('/')
        if not date_parts or len(date_parts) != 3:
            raise ScrapeError('date not in d/m/y format: '+date)
        if 'day' in dmy:
            fields[dmy['day']] = [ date_parts[0] ]
        if 'month' in dmy:
            fields[dmy['month']] = [ date_parts[1] ]
        elif 'MONTH' in dmy:
            fields[dmy['MONTH']] = [ date_parts[1].upper() ]
        fields[dmy['year']] = [ date_parts[2] ]
    else:
        if drop_down:
            fields[config] = [ date ]
        else:
            fields[config] = date
    return fields

# get the form settings as a dict with keys 'namenum', 'fields' and 'submit'
# supplied is a string which is a simple form name/number or a dict to be evaluated
def get_form_settings(supplied = None):
    if not supplied:
        return { }
    elif '{' in supplied: 
        return eval(supplied)
    else: # was using isalnum but does not match dashes and underscores
        return { 'namenum': supplied }

# adds field values to the currently selected form
# can be ok to fail if a control exists but the supplied select option does not exist
def add_fields(br, fields, ok_to_fail = False):
    if fields:
        add_controls = []
        for k, v in fields.items():
            try:
                if k.startswith('#'):
                    control = br.find_control(name=k[1:], nr=0) # find first control named k
                else:
                    control = br.find_control(name=k, nr=0) # find first control named k
            #except mechanize._form.AmbiguityError as e: # more than one control with same name
            #    if debug: print "dbg: more than one form control named "+k
            #    raise
            except mechanize._form.ControlNotFoundError as e: # if the control does not exist, we create a dummy hidden control to hold the value
                if debug: print "dbg: cannot find form control "+k+", creating a dummy hidden control"
                if k.startswith('#'):
                    add_controls.append(k[1:])
                else:
                    add_controls.append(k)
        if add_controls:
            for k in add_controls:
                br.form.new_control('hidden', k, {'value':''} )
            br.form.fixup()
        br.form.set_all_readonly(False)
        try:
            for k, v in fields.items():
                if k.startswith('#'): # used to set a named control using option label
                    control = br.find_control(name=k[1:], nr=0) # find first control named k
                    if v is None:
                        control.disabled = True
                    elif isinstance(v, list):
                        if control.disabled: control.disabled = False
                        for i in v:
                            control.get(label=i, nr=0).selected = True # set the value by selecting its label (v[i])
                    else:
                        if control.disabled: control.disabled = False
                        control.get(label=v, nr=0).selected = True # set the value by selecting its label (v)
                        # NB label matches any white space compressed sub string so there is potential for ambiguity errors
                else:
                    #br[k] = v # default is to directly assign the named control a value (v)
                    control = br.find_control(name=k, nr=0) # find first control named k
                    if debug: print "dbg: form control "+control.name+" has type "+control.type
                    if v is None:
                        control.disabled = True
                    elif (control.type == 'radio' or control.type == 'checkbox' or control.type == 'select') and not isinstance (v, list):
                        if control.disabled: control.disabled = False
                        control.value = [ v ]
                    elif (control.type != 'radio' and control.type != 'checkbox' and control.type != 'select') and v and isinstance (v, list):
                        if control.disabled: control.disabled = False
                        control.value = v [0]
                    else:
                        if control.disabled: control.disabled = False
                        control.value = v
        except mechanize._form.ItemNotFoundError as e: # field select/check/radio option does not exist
            if ok_to_fail:
                return False
            else:
                if debug: print "dbg: form exception type: "+str(type(e))
                raise ScrapeError('cannot set form field '+k+': '+util.vstr(e))
        except Exception as e:
            if debug: print "dbg: form exception type: "+str(type(e))
            raise ScrapeError('cannot set form field '+k+': '+util.vstr(e))
    return True

# bypasses a scraped form, makes a direct url request supplying GET or POST parameter
def pseudo_form(br, url = None, action = None, fields = None, date_fields = None, method = None):
    if action:
        url = urlparse.urljoin(url, action)
    if debug: print "dbg: pseudo url:", url
    if debug: print "dbg: pseudo form fields:", fields
    if debug: print "dbg: pseudo date fields:", date_fields
    data = {}
    if fields:
        data.update(fields)
    if date_fields:
        data.update(date_fields)
    for k, v in data.items():
        if v and isinstance(v, list):
            data[k] = v[0]
    if method and method == 'GET':
        url = util.add_to_query(url, data)
        if debug: print "dbg: new url:", url
        return br.open(url)
    else:
        return br.open(url, urllib.urlencode(data))

# selects the form and sets up the form fields
# returns False if the requested date range is not available, otherwise True
def setup_form(br, form = None, action = None, fields = None, date_fields = None, method = None):
    if debug:
        msg = 'dbg: forms list:'
        i = 0
        try:
            for tform in br.forms():
                if tform.name: msg = msg+' '+tform.name
                else: msg = msg+' '+str(i)
                i = i + 1
            print msg
        except:
            pass
    try:
        if not form:
            form = '0'
            br.select_form(nr=0)
        elif form.isdigit():
            br.select_form(nr=int(form))
        else:
            br.select_form(name=form)
    except mechanize.ParseError:
        raise # ParseError has a bug which means it cannot seem to return its message via str()
        #raise ScrapeError('cannot find form '+form+': parse error '+msg)
    except Exception as e:
        raise ScrapeError('cannot find form '+form+': '+util.vstr(e))
    if debug: 
        try:
            print "dbg: form dump1:", br.form # can throw an error if the form contains unicode
        except:
            pass
    if action:
        current_action = br.form.action
        new_action = urlparse.urljoin(current_action, action)
        br.form.action = new_action
    if method and method == 'GET':
        br.form.method = method
    if debug: print "dbg: form fields:", fields
    if fields:
        add_fields(br, fields)
    if date_fields:
        if not add_fields(br, date_fields, True):
            if debug: print "dbg: date select option does not exist:", date_fields
            return False # if date control exists but select options are not available raise a flag
    if debug:        
        try:
            print "dbg: form dump2:", br.form # can throw an error if the form contains unicode
        except:
            pass
    return True

# returns response after submitting a form via a mechanize browser
# submit paramter is a submit control name/number or an id (starts with a #)
def submit_form(br, submit = None):
    try:
        if not submit:
            submit = ''
            response = br.submit()
        elif submit.isdigit():
            response = br.submit(nr=int(submit))
        elif submit.startswith('-'):
            for control in br.form.controls:
                if control.type == "submit":
                    control.disabled = True
            response = br.submit()
        elif submit.startswith('#'): 
            control = br.find_control(id=submit[1:], nr=0) # find first control with id submit
            if control.disabled: control.disabled = False
            response = br.submit(id=submit[1:], nr=0)
        else:
            control = br.find_control(name=submit, nr=0) # find first control named submit
            if control.disabled: control.disabled = False
            response = br.submit(name=submit, nr=0)
        return response
    except Exception as e:
        raise ScrapeError('error during form submit ('+submit+'): '+util.vstr(e))

# returns a response after following a link via a mechanize browser
# link paramter is a link text value or number or a name (starts with a !)
def process_link(br, link = None):
    try:
        if not link:
            link = ''
            response = br.follow_link()
        elif link.isdigit():
            response = br.follow_link(nr=int(link))
        elif link.startswith('!'):
            response = br.follow_link(name=str(link[1:]))
        else:
            response = br.follow_link(text=str(link))
        return response
    except Exception as e:
        raise ScrapeError('cannot follow link '+link+': '+util.vstr(e))

# create full list of all active planning authorities from source
def get_authorities_template():
    authorities = util.get_table_vals(SOURCES, '', '', 'order by name')
    auths = []
    for authority in authorities:
        auth_status = authority.get('status')
        if not auth_status or auth_status == 'active':
            new_auth = {}
            for k, v in authority.items():
                if v: 
                    if k == 'openly_local_id':
                        new_auth['openly_local_url'] = OL_URL % v
                    new_auth[k] = v
            auths.append(new_auth)
    data = {}
    data.update(INFORMATION)
    data['authorities'] = {}
    data['authorities'].update ( { 'authority': auths } )
    return data

# get template for planning data
def get_planning_template(query):
    data = {}
    data['status'] = 'Error'
    link_query = query.copy()
    if link_query.get('fmt') and link_query['fmt'] == 'object':
        del link_query['fmt']
    data['link'] = GATEWAY_URL + '?' + urllib.urlencode(link_query)
    auth = query.get('authority')
    if not auth:
        auth = query.get('auth')
    if not auth:
        data['message'] = 'authority not specified'
        return data
    authority = mcache_fetch('aut:'+auth)
    if not authority:
        if auth.isdigit():
            authority = util.get_table_vals(SOURCES, '', "openly_local_id="+auth)
        else:
            authority = util.get_table_vals(SOURCES, '', "name='"+auth+"'")
        if authority:
            authority = authority[0]
            mcache_put('aut:'+auth, authority)
    if not authority:
        data['message'] = '"'+auth+'" not in list of sources'
        return data
    data['authority_short_name'] = auth
    data['authority_name'] = authority.get('long_name', '')
    data['search_url'] = authority['search_url']
    if authority.get('table_name'):
        data['data_table'] = authority['table_name']
        thistable = authority['table_name']
    else:
        thistable = 'swdata'
    if authority.get('scraper') and authority.get('config', '').startswith('ScraperWiki'):
        data['scrape_url'] = 'https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=htmltable&name=' + authority['scraper']
        sqlquery = 'select * from ' + thistable + ' where date_scraped is not null order by start_date desc limit 100'
        data['scrape_url'] = util.add_to_query(data['scrape_url'], { 'query': sqlquery } )
    elif authority.get('scrape_url'):
        data['scrape_url'] = authority['scrape_url']
    if authority.get('openly_local_id'):
        data['openly_local_id'] = authority['openly_local_id']
        #data['openly_local_url'] = OL_URL % authority['openly_local_id']
    data['config'] = authority.get('config', '')
    data['authority_info'] = authority.get('info', '')
    auth_status = authority.get('status')
    if not debug and auth_status and auth_status != 'active':
        data['message'] = 'this authority scraper is not active'
        return data
    if query.get('ref'):
        data['requested_ref'] = query['ref']
    else:
        if query.get('date'):
            try:
                dt = dateutil.parser.parse(query['date'], dayfirst=True).date()
                data['requested_date'] = dt.strftime(util.DATE_FORMAT)
            except:
                data['message'] = 'invalid date parameter: '+query['date']
                return data
        else:
            missing_params = ''
            if not query.get('day'):     missing_params += 'day '
            if not query.get('month'):   missing_params += 'month '
            if not query.get('year'):    missing_params += 'year '
            if missing_params:
                data['message'] = missing_params+'not specified'
                return data
            try:
                dt = date(int(query['year']), int(query['month']), int(query['day']))
                data['requested_date'] = dt.strftime(util.DATE_FORMAT)
            except:
                data['message'] = 'invalid date parameters: day='+query['day']+', month='+query['month']+', year='+query['year']
                return data
        if query.get('ndays'):
            data['requested_days'] = query['ndays']
    data['scraped_date'] = date.today().strftime(util.DATE_FORMAT)
    data['scraped_at'] = datetime.today().strftime(util.RFC822_DATE) # full date and time
    data['status'] = 'OK'
    data['count'] = '0'
    data['applications'] = { 'application': [] }
    return data

# scrape one page of records
def scrape_page(cfg, br, html_subs, url_subs, default_url, follow_links = True, single_day = False):
    response = adjust_html(br, html_subs)
    html = response.read()
    url = response.geturl()
    if debug: print 'dbg: scraping from: ', url
    scrape_stuff = str(util.trim(cfg['scrape_records']))
    if not follow_links:
        scrape_stuff = OTHER_REGEX.sub('', scrape_stuff) # remove any other page links
    if debug: print 'dbg: records config:', scrape_stuff
    result = scrapemark.scrape(scrape_stuff, html, url)
    if debug: print 'dbg: scraped records:', result

    single_rec = False
    if not result or not result.get('records'):
        result = None
        if cfg.get('scrape_one_rec'):
            scrape_stuff = str(util.trim(cfg['scrape_one_rec']))
            if not follow_links:
                scrape_stuff = OTHER_REGEX.sub('', scrape_stuff) # remove any other page links
            if debug: print 'dbg: one record config:', scrape_stuff, url
            result = scrapemark.scrape(scrape_stuff, html, url)
            if debug: print 'dbg: scraped record:', result
        if not result:
            cfg_max_recs = str(util.trim(cfg['scrape_max_recs']))
            if cfg_max_recs == '__continue__':
                return [], html, url # if we are continuing without limit, zero records found is a normal return
            if debug: print 'dbg: no recs config:', cfg['scrape_no_recs']
            result = scrapemark.scrape(str(util.trim(cfg['scrape_no_recs'])), html)
            if not result:
                raise ScrapeError('invalid results page returned at: '+url)
            else:
                return [], html, url # no records indicator found, normal return with zero records found
        else:
            single_rec = True
            records = [ result ]
    else:
        records = result['records']

    # used to adjust any stored info_urls
    orig_url = adjust_url(url, url_subs) # any tweaks required?
    if default_url:
        default_url = urlparse.urljoin(orig_url, default_url)
        if debug: print 'dbg: start url:', orig_url
        if debug: print 'dbg: adjusted default url:', default_url

    for record in records:
        if not record.get('info_url'):
            if default_url: # if present, try to use the default url and/or reference
                info_url = default_url
                if info_url.endswith('='):
                    info_url += urllib.quote_plus(record.get('reference', ''))
            else:
                info_url = re.sub (r'[&\?]nocache=\w\w\w\w$', '', orig_url) # fallback for any record without an info_url -> use the current URL
            record['info_url'] = info_url 
        else:
            link = record['info_url']
            link = adjust_url(link, url_subs) # any tweaks required?
            record['info_url'] = urlparse.urljoin(orig_url, link) # make link absolute
        if follow_links and not single_rec and (record.get('info_url') or record.get('form_link')) and (cfg.get('scrape_info') or (cfg.get('scrape_dates') and not single_day)):
        # don't try to get detail if not following links or this is a single record only
            if record.get('form_link'):
                fset = get_form_settings(cfg.get('detail_form'))
                if fset.get('link_field'):
                    fields = fset.get('fields', {})
                    fields[fset['link_field']] = urllib.unquote_plus(record['form_link']) # assumes quoted at the moment (=Sefton) but some might not be in future
                    fset['fields'] = fields
                else:
                    fset['submit'] = record['form_link']
                if debug: print 'dbg: form link fset ', fset
                setup_form(br, fset.get('namenum'), fset.get('action'), fset.get('fields'), None, fset.get('method'))
                response = submit_form(br, fset.get('submit'))
                response = adjust_html(br, html_subs)
                exthtml = response.read()
                br.back()
                del record['form_link']
            elif record.get('info_url'):
                response = br.open(record['info_url'])
                response = adjust_html(br, html_subs)
                exthtml = response.read()
                br.back()
            else:
                raise ScrapeError('invalid config - no info_url or form_link to scrape detail info')
            if cfg.get('scrape_info'):
                extra = scrapemark.scrape(str(util.trim(cfg['scrape_info'])), exthtml)
                if debug: print 'dbg: extra info scrape:', extra
                if extra:
                    record.update(extra)
            #if not single_day and cfg.get('scrape_dates'):
            if cfg.get('scrape_dates'):
                extra = scrapemark.scrape(str(util.trim(cfg['scrape_dates'])), exthtml)
                if debug: print 'dbg: extra dates scrape:', extra 
                if extra:
                    record.update(extra)
    return records, html, url

# use config settings to establish the environment for scraping
def scrape_envt(cfg, scrape_url, search_url):

    if not scrape_url:
        scrape_url = search_url

    if cfg.get('headers'):
        headers = eval(cfg.get('headers'))
    else:
        headers = cfg.get('headers')
    
    #load a proxy if the scrape_url port is not empty or 80 or 443 - not required any more
    o = urlparse.urlsplit(scrape_url)
    if (o.scheme == 'http' and o.port and o.port != 80) or (o.scheme == 'https' and o.port and o.port != 443):
        br, handler, cj = util.get_browser(headers, '', PROXY)
        if debug: print 'dbg: on port', o.port, 'using proxy:', PROXY
    else:
        br, handler, cj = util.get_browser(headers)

    if debug:
        br.set_debug_http(True)

    if cfg.get('cookies'):
        cookies = eval(cfg.get('cookies'))
        for ck in cookies:
            util.set_cookie(cj, ck['name'], ck['value'], ck.get('domain'), ck.get('path', '/'))   
        if debug:
            print 'Cookies'
            for index, cookie in enumerate(cj):
                print index, ' : ', cookie

    if cfg.get('html_subs'):
        html_subs = eval(cfg.get('html_subs'))
        if debug: print "dbg: html_subs", html_subs
    else:
        html_subs = None
    if cfg.get('url_subs'):
        url_subs = eval(cfg.get('url_subs'))
        if debug: print "dbg: url_subs", url_subs
    else:
        url_subs = None
    if search_url:
        if cfg.get('ref_url'):
            default_url = urlparse.urljoin(search_url, cfg['ref_url'])
        else:
            default_url = search_url
    elif cfg.get('ref_url'):
        default_url = cfg['ref_url']
    else:
        default_url = None

    # any pre_start page which must be opened before anything else happens?
    if cfg.get('pre_start'):
        try:
            br.set_handle_redirect(False)
            response = br.open(cfg['pre_start'])
            if debug: print response.read()
        except:
            pass
        br.set_handle_redirect(True)

    # kludge adds a random query parameter to bypass scraperwiki caching - to force fetch of a fresh page each time
    # otherwise causes problems with some systems = Idox
    # NB Cache-Control no-cache headers etc do not work
    if not cfg.get('nocache_param_off'):
        nocache = "%04x" % random.randint(0, 65535)
        scrape_url = util.add_to_query(scrape_url, { 'nocache': nocache })

    # any POST parameters necessary to open the scrape_url?
    start_post = None
    if cfg.get('start_post'):
        start_post = urllib.urlencode(eval(cfg['start_post']))

    return br, handler, scrape_url, default_url, html_subs, url_subs, start_post

# substitute strings in the values of a target dict
def sub_dict(target, subs):
    result = False
    if target and subs:
        for k, v in target.items():
            if (isinstance(v, str) or isinstance(v, unicode)) and subs and SUBS_REGEX.search(v): # there are strings to substitute in the fields
                result = True
                target[k] = v % subs
    return result

# scrape one application from its ref number
def scrape_application(cfg, scrape_url, search_url, ref_req, follow_links = True):

    br, handler, scrape_url, default_url, html_subs, url_subs, start_post = scrape_envt(cfg, scrape_url, search_url)

    if cfg.get('ref_rel'):
        scrape_url = urlparse.urljoin(scrape_url, cfg['ref_rel'])

    fset = get_form_settings(cfg.get('form'))
    if cfg.get('ref_form'): # extra form setting to get applic using reference value
        fset_ref = get_form_settings(cfg['ref_form'])
        fset.update(fset_ref)

    response = br.open(scrape_url, start_post)
    if debug: print "dbg: html response info:", response.info() # headers
    response = adjust_html(br, html_subs)

    if fset.get('fields'):
        fields = fset['fields']
    else:
        fields = {}
    if fields.get('query'):
        fields['query'] = util.trim(fields['query'])
    if cfg.get('ref_field'):
        ref_req = REF_REGEX.sub(r'\1', ref_req) # remove spaces and brackets
        if not sub_dict(fields, { cfg['ref_field']: ref_req} ):
            fields[cfg['ref_field']] = ref_req
    else:
        return [] # if no ref field cannot make request
                
    if fset.get('no_form'): # pseudo form input if there is a 'no_form' key word
        response = pseudo_form(br, scrape_url, fset.get('action'), fields, None, fset.get('method'))
    else:
        form_ok = setup_form(br, fset.get('namenum'), fset.get('action'), fields, None, fset.get('method'))
        response = submit_form(br, fset.get('submit'))

    if debug: print "dbg: follow_links:", follow_links

    if cfg.get('ref_scrape'):
        cfg['scrape_records'] = cfg['ref_scrape']
    
    records, html, url = scrape_page(cfg, br, html_subs, url_subs, default_url, follow_links)
    if not records:
        return [] # zero records found
    else:
        return records


# scrape one authority - get applications received on the specific date (and for a number of days after)
# return any records and the dates from and to (some sites cannot return just a single day e.g one week)
def scrape_authority(cfg, scrape_url, search_url, date_req, days_req, follow_links = True, max_rec_value = MAX_REC_VALUE, max_pag_value = MAX_PAG_VALUE):

    br, handler, scrape_url, default_url, html_subs, url_subs, start_post = scrape_envt(cfg, scrape_url, search_url)

    fset = get_form_settings(cfg.get('form'))
    
    date_fields = {}
    single_day = False
    if not cfg.get('date_to') and not cfg.get('date_from'):
        #raise ScrapeError('no to or from date value specified in the configuration')
        date_from = None
        date_to = None
        if debug: print 'dbg: no dates sought - static applications list'
        # dates need to be set to max and min of any dates returned
    else:
        try:
            min_days_req = int(cfg.get('ndays'))
        except:
            min_days_req = 0
        try:
            int_days_req = int(days_req)
        except:
            int_days_req = min_days_req
        if int_days_req < -1: 
            days_extra =  int_days_req + 1
            date_req, dummy_date = util.inc_dt(date_req, util.DATE_FORMAT, days_extra)
            days_extra = abs(days_extra)
        elif int_days_req > 1:
            days_extra = int_days_req - 1
        else:
            days_extra = 0
        date_inc = cfg.get('date_inc', '')
        if '&' in date_inc and '@' in date_inc:
            dummy_date, date_to = util.inc_dt(date_req, util.DATE_FORMAT, days_extra + 1) # end date is exclusive
            date_from, dummy_date = util.inc_dt(date_req, util.DATE_FORMAT, -1) # start date is exclusive
        elif date_inc == '&':
            date_from, date_to = util.inc_dt(date_req, util.DATE_FORMAT, days_extra + 1) # end date is exclusive
        elif date_inc == '@':
            dummy_date, date_to = util.inc_dt(date_req, util.DATE_FORMAT, days_extra)
            date_from, dummy_date = util.inc_dt(date_req, util.DATE_FORMAT, -1) # start date is exclusive
        elif date_inc == 'Month': # one whole month around the supplied date
            date_from, date_to = util.inc_dt(date_req, util.DATE_FORMAT, date_inc)
            max_rec_value = max_rec_value * 2
        elif date_inc[0:1] == '-': # custom negative increment and optional positive one around requested date
            nums = date_inc.split('+')
            date_from, dummy_date = util.inc_dt(date_req, util.DATE_FORMAT, nums[0])
            if len(nums) > 1:
                dummy_date, date_to = util.inc_dt(date_req, util.DATE_FORMAT, nums[1])
            else:
                date_to = date_req
        elif date_inc.isalpha(): # weekday
            if cfg.get('date_to') and cfg.get('date_from'):
                raise ScrapeError('weekday date_inc can only apply with either a to OR from date in the configuration')
            elif cfg.get('date_from'):
                date_inc = '-' + date_inc
            date_from, date_to = util.inc_dt(date_req, util.DATE_FORMAT, date_inc)
        elif date_inc.isdigit() and int(date_inc) > 1: # overrides min number of days to return
            date_from, date_to = util.inc_dt(date_req, util.DATE_FORMAT, int(date_inc))
        elif days_extra > 0: 
            date_from, date_to = util.inc_dt(date_req, util.DATE_FORMAT, days_extra)
        else:
            date_from = date_req
            date_to = date_req
        if debug: print 'dbg: date range sought after any increment:', date_from, date_req, date_to
        if cfg.get('request_date_format'):
            set_date_to = util.convert_dt(date_to, util.DATE_FORMAT, cfg.get('request_date_format'))
            set_date_from = util.convert_dt(date_from, util.DATE_FORMAT, cfg.get('request_date_format'))
            set_date_req = util.convert_dt(date_req, util.DATE_FORMAT, cfg.get('request_date_format'))
            if debug: print 'dbg: date range sought after format conversion', set_date_from, set_date_req, set_date_to
        else:
            set_date_to = date_to
            set_date_from = date_from
            set_date_req = date_req
        if cfg.get('date_from') and cfg.get('date_to'):
            if cfg.get('date_from') == cfg.get('date_to'): # one field named twice means use original requested date not incremented dates
                set_date_fields(date_fields, cfg['date_to'], set_date_req)
            else:
                set_date_fields(date_fields, cfg['date_to'], set_date_to)
                set_date_fields(date_fields, cfg['date_from'], set_date_from)
        elif cfg.get('date_to'):
            if fset.get('no_form'):
                set_date_fields(date_fields, cfg['date_to'], set_date_to)
            else:
                set_date_fields(date_fields, cfg['date_to'], set_date_to, True) # assumed to be drop down controls by default
        else:
            if fset.get('no_form'):
                set_date_fields(date_fields, cfg['date_from'], set_date_from)
            else:
                set_date_fields(date_fields, cfg['date_from'], set_date_from, True) # assumed to be drop down controls by default
        if '&' in date_inc:
            date_to, dummy_date = util.inc_dt(date_to, util.DATE_FORMAT, -1) # end date is exclusive, decrement it by 1
        if '@' in date_inc:
            dummy_date, date_from = util.inc_dt(date_from, util.DATE_FORMAT, 1) # start date is exclusive, increment it by 1
        if debug: print 'dbg: real date range after increments/decrements removed :', date_from, date_req, date_to
        if date_from == date_to: single_day = True

    if fset.get('fields'):
        fields = fset['fields']
    else:
        fields = {}
    if fields.get('query'):
        fields['query'] = util.trim(fields['query'])
    if fields and date_fields and sub_dict(fields, date_fields): # test if substitutions were made
        date_fields = None # if so remove them as separate fields
    
    if fset.get('no_form'): # pseudo form input if there is a 'no_form' key word

        if fset.get('list_url'): # scrape the link to a fixed list of applications
            response = br.open(scrape_url, start_post)
            if debug: print "dbg: html response info:", response.info() # headers
            response = adjust_html(br, html_subs)
            if debug: print 'dbg: cfg list_url:', fset.get('list_url')
            html = response.read()
            url = response.geturl()
            result = scrapemark.scrape(str(util.trim(fset.get('list_url'))), html, url)
            if not result or not result.get('list_url'):
                raise ScrapeError('no valid list_url found: '+fset.get('list_url'))
            else:
                if debug: print 'dbg: scraped list_url record:', result
                response = br.open(result.get('list_url'))
            
        else: # otherwise simulate form submission with POST/GET request

            response = pseudo_form(br, scrape_url, fset.get('action'), fields, date_fields, fset.get('method'))

    else:

        response = br.open(scrape_url, start_post)
        if debug: print "dbg: html response info:", response.info() # headers
        response = adjust_html(br, html_subs)
    
        form_ok = setup_form(br, fset.get('namenum'), fset.get('action'), fields, date_fields, fset.get('method'))
        if not form_ok: # form cannot find the requested date select options = normal zero return
            return date_from, date_to, []
        
        response = submit_form(br, fset.get('submit'))

    if debug: print "dbg: follow_links:", follow_links
    
    records, html, url = scrape_page(cfg, br, html_subs, url_subs, default_url, follow_links, single_day)
    if not records:
        return date_from, date_to, [] # normal return with zero records found

    current_page = 1
    max_recs = 0 # no scrape_max_recs config means the next page is never sought
    max_pages = 0
    if cfg.get('scrape_max_recs'):
        max_recs = max_rec_value # prevent any run away loop
        max_pages = max_pag_value
        cfg_max_recs = str(util.trim(cfg['scrape_max_recs']))
        if cfg_max_recs == '__continue__':
            pass # this means keep following any next page link until system max number of records or pages is reached or a page returns no values
        elif cfg_max_recs.isdigit():
            max_recs = int(cfg_max_recs) # specified max records limit in configuration
        else:
            result = scrapemark.scrape(cfg_max_recs, html) 
            if result:
                rec_value = result.get('max_recs', '')
                pag_value = result.get('max_pages', '')
                if rec_value:
                    rec_value_list = rec_value.split()
                    rec_value = rec_value_list[-1] # can be a space separated list, so take the last value
                    if rec_value.isdigit():
                        max_recs = int(rec_value)
                    elif rec_value.lower() == 'one': # awkward bastards
                        max_recs = 1
                    else:
                        raise ScrapeError('max records value is no good: '+rec_value)
                elif pag_value:
                    pag_value_list = pag_value.split()
                    pag_value = pag_value_list[-1] # can be a space separated list, so take the last value
                    if pag_value.isdigit():
                        max_pages = int(pag_value)
                    else:
                        raise ScrapeError('max pages value is no good: '+pag_value)
                else:
                    raise ScrapeError('no valid max records or max pages value found: '+util.vstr(result))
            else:
                max_recs = 0 # no valid max_recs or max_pages found means the next page is never sought
                max_pages = 0
            if max_recs > max_rec_value:
                max_recs = max_rec_value # prevent any run away loop
            if max_pages > max_pag_value:
                max_pages = max_pag_value # prevent any run away loop
            if debug: print "dbg: scrape max_recs:", result, util.vstr(max_recs), util.vstr(max_pages)

    while (len(records) > 1 and len(records) < max_recs and current_page < max_pages):

        try:
            if cfg.get('next_type', '') == 'scrape':
            #if cfg.get('scrape_next_link'): 
                result = scrapemark.scrape(str(util.trim(cfg['next_page'])), html, url)
                if debug: print "dbg: scrape next_page:", result
                if not result:
                    raise ScrapeError('no next link scraped')
                link = result['next_link']
                link = adjust_url(link, url_subs) # any tweaks required?
                response = br.open(link)
            elif cfg.get('next_type', '') == 'href':
                link = xpath_text(handler.element, cfg['next_page'])
                if not link:
                    raise ScrapeError('no next link found via xpath')
                link = adjust_url(link, url_subs) # any tweaks required?
                response = br.open(link)
            elif cfg.get('next_type', '') == 'link':
                response = process_link(br, cfg['next_page'])
            elif cfg.get('next_type', '') == 'form':
                fset = get_form_settings(cfg.get('next_page'))
                setup_form(br, fset.get('namenum'), fset.get('action'), fset.get('fields'), None, fset.get('method'))
                response = submit_form(br, fset.get('submit'))
            else:
                break # normal exit = no way defined to get to next page = single page only
        except Exception as e:
            if max_recs < max_rec_value or max_pages < max_pag_value: # if there are still pages or records to get, this is an error
                raise ScrapeError("cannot follow next page link: "+util.vstr(e))
            else:
                break # normal exit = reached end = no next page to follow

        new_records, html, url = scrape_page(cfg, br, html_subs, url_subs, default_url, follow_links, single_day)
        if not new_records:
            break # NB different from previous - in this case normal return keeping previous records found so far

        records.extend(new_records)
        current_page = current_page + 1

    return date_from, date_to, records

# perform a scrape of one data block from an external authority
def execute_scrape(query = None):
    warnings.simplefilter("error", category=UnicodeWarning)
    if not query or (len(query) == 1 and 'fmt' in query) or (len(query) == 2 and 'fmt' in query and 'ndays' in query):
        data = mcache_fetch('_auths_')
        if not data:
            data = get_authorities_template()
            mcache_put('_auths_', data)
        return show_data(data, query)
    else: 
        start_clock = time.time()
        data = get_planning_template(query)
        if data['status'] == 'OK':
            table = 'swdata'
            if data.get('data_table'): 
                table = data['data_table']
            auth = data['authority_short_name']
            config_name = data['config']
            if not config_name:
                data['status'] = 'Error'
                data['message'] = 'missing named configuration for '+auth
            else:
                cfg = mcache_fetch('cfg:'+config_name)
                if not cfg:
                    config_list = util.get_table_vals(CONFIGS)
                    config_map = util.get_map(config_list, 'name')
                    if config_map and config_map.get(config_name):
                        cfg = util.dict_inherited(config_map, config_name)
                        mcache_put('cfg:'+config_name, cfg)
                if not cfg:
                    data['status'] = 'Error'
                    data['message'] = 'no settings found for '+auth+' configuration = '+config_name
                else:
                    if cfg.get('form'): # per authority adjustment to configuration - don't cache this
                        cfg['form'] = cfg['form'].replace('+authority+', auth)
                        cfg['form'] = cfg['form'].replace('+table+', table)
                    if cfg.get('ref_form'): # per authority adjustment to configuration - don't cache this
                        cfg['ref_form'] = cfg['ref_form'].replace('+authority+', auth)
                        cfg['ref_form'] = cfg['ref_form'].replace('+table+', table)
                    if debug: print "dbg: config:", cfg 
                    if debug: print "dbg: data:", data 
                    if query.get('no_detail'):
                        follow_links = False
                    else:
                        follow_links = True
                    try:
                        default_date = None
                        if data.get('requested_ref'):
                            records = scrape_application(cfg, data.get('scrape_url'), data['search_url'], data['requested_ref'], follow_links)
                            date_began = None; date_reached = None;
                        else:
                            date_began, date_reached, records = scrape_authority(cfg, data.get('scrape_url'), data['search_url'], data['requested_date'], data.get('requested_days'), follow_links)
                            if date_began and date_reached and date_began == date_reached and date_reached == data['requested_date']:
                                default_date = date_reached
                        request_date_type = cfg.get('request_date_type', '')
                        match_count = 0
                        date_min = None
                        date_max = None
                        for record in records:
                            record = add_location_etc(record, default_date, request_date_type, cfg.get('received_date_format', util.DATE_FORMAT))
                            if date_began and date_reached: # a particular date was requested, so return the range around that
                                if request_date_type == 'received':
                                    if util.match_dt(record.get('received_date'), date_began, date_reached):
                                        match_count = match_count + 1
                                elif request_date_type == 'validated':
                                    if util.match_dt(record.get('validated_date'), date_began, date_reached):
                                        match_count = match_count + 1
                            else: # no date was requested, so work out the range of active dates within the list and return that
                                if record.get('received_date'):
                                    if not date_min or util.test_dt(date_min, record.get('received_date')) > 0:
                                        date_min = record.get('received_date')
                                    if not date_max or util.test_dt(date_max, record.get('received_date')) < 0:
                                        date_max = record.get('received_date')
                                elif record.get('validated_date'):
                                    if not date_min or util.test_dt(date_min, record.get('validated_date')) > 0:
                                        date_min = record.get('validated_date')
                                    if not date_max or util.test_dt(date_max, record.get('validated_date')) < 0:
                                        date_max = record.get('validated_date')
                            data['applications']['application'].append(record)
                        data['count'] = str(len(records))
                        if not data.get('requested_ref'):
                            if request_date_type:
                                data['request_date_type'] = request_date_type
                                if request_date_type == 'received' or request_date_type == 'validated':
                                    data['match_count'] = str(match_count)
                            else:
                                data['request_date_type'] = 'unused'
                        if date_began and date_reached:
                            data['from_date'] = date_began
                            data['until_date'] = date_reached
                        elif date_min and date_max:
                            data['from_date'] = date_min
                            data['until_date'] = date_max  
                    except Exception as e:
                        data['status'] = 'Error'
                        data['message'] = util.vstr(e)
                        if debug: raise   #   NB  
        data['elapsed_secs'] = time.time() - start_clock
        return show_data(data, query)

# put an item into the local memory cache
# make copy, otherwise the cached version is mutable 
def mcache_put(key, value):
    if isinstance(key, dict):
        keyhash = hash(tuple(sorted(key.iteritems())))
    elif isinstance(key, list):
        keyhash = hash(tuple(key))
    else:
        keyhash = hash(key)
    CACHE[keyhash] = copy.deepcopy(value)
    if debug: print "dbg: cache insert:", key, keyhash

# get an item from the local memory cache
# make copy, otherwise the cached version is mutable
def mcache_fetch(key):
    if isinstance(key, dict):
        keyhash = hash(tuple(sorted(key.iteritems())))
    elif isinstance(key, list):
        keyhash = hash(tuple(key))
    else:
        keyhash = hash(key)
    result = copy.deepcopy(CACHE.get(keyhash))
    if debug:
        if result: print "dbg: cache hit:", key, keyhash
        else: print "dbg: cache miss:", key, keyhash
    return result

class ScrapeError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message

# scrape a block of data from another scraperwiki scraper
# works but not in use
def get_from_scraper(scraper, table, fields, sequence, sequence_from, sequence_to = None, limit = None, scrape_date = 'date_scraped'):
    query = []
    for k, v in fields.items():
        if v: query.append(v + ' as ' + k)
        else: query.append(k)
    query_string = "select %s from %s where %s is not null" % (", ".join(query), table, scrape_date)
    if sequence and (sequence.startswith('date_') or sequence.endswith('_date')):
        query_string += " and %s is not null and length(%s) = 10 and %s >= '%s'" % (sequence, sequence, sequence, sequence_from.strftime(util.ISO8601_DATE))
        if sequence_to: 
            query_string += " and %s <= '%s'" % (sequence, sequence_to.strftime(util.ISO8601_DATE))
    elif sequence:
        query_string += " and %s is not null and %s >= %s" % (sequence, sequence, sequence_from)
        if sequence_to: 
            query_string += " %s <= %s" % (sequence, sequence_to)
    query_string += " order by %s desc" % scrape_date
    if limit: query_string += " limit " + str(limit)
    #print query_string
    db_url = "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=%s&query=%s" % (scraper, urllib.quote_plus(query_string))
    return json.load(urllib2.urlopen(db_url, None, 10))  # 10 sec timeout

""" if __name__ == 'scraper':
    fields = { 'reference': 'uid',
        'address': '',
        'postcode': '',
        'description': '',
        'received_date': 'date_received',
        'validated_date': 'date_validated', }
    date_from = date(2012, 1, 31)
    result = get_from_scraper('denbighshire_planning_applications', 'swdata', fields, 'start_date', date_from)
    print result
    print len(result) """




# a library of functions for use in planning application scrapers

import scraperwiki
import urllib, urllib2
import socket
from datetime import date
from datetime import timedelta
from datetime import datetime
import urlparse
import dateutil.parser
import re
import mechanize
import time
import random
import warnings
import copy
import json

scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")
locat = scraperwiki.utils.swimport("location_library")

scraperwiki.sqlite.attach("planning_authorities", "src")
SOURCES = "src.authorities"
CONFIGS = "src.configurations"

APPLICATIONS = 'applications'
PROGRESS = 'authorities'
TIMEOUT = 120
DAYS_BLOCK = 14
INDEXED_FIELDS = ['authority', 'received_date', 'validated_date', 'lat', 'lng']
OTHER_REGEX = re.compile(r'{@.*?@}') # find scrapemark other page links
SUBS_REGEX = re.compile(r'%\([^\)]+\)') # find string substitutions
REF_REGEX = re.compile(r'^[\s\(\[]*([^\)\]\s]+).*$') # find reference number - removing spaces and brackets

MAX_REC_VALUE = 200 # default maximum records from one scrape of an authority
MAX_PAG_VALUE = 20 # default maximum pages

PROXY = 'http://www.speakman.org.uk/glype/browse.php?u=%s'

GATEWAY_URL = 'https://views.scraperwiki.com/run/paview_scraper_1/'
OL_URL = 'http://openlylocal.com/councils/%s/planning_applications/'
INFORMATION = {
    'title': 'Planning Gateway',
    'description': 'Authorities that can be scraped via this gateway',
    'link': GATEWAY_URL,
    'parameters': 'fmt, auth, day, month, year, ndays, date, ref',
}

CACHE = {} 

debug = False

# store planning application data, doing any necessary date translations and geocoding at the same time
def store_applications(auth_name, region, applications, applications_table = APPLICATIONS, scrape_date = date.today()):
    for applic in applications:
        applic['authority'] = auth_name
        applic['scrape_date'] = scrape_date.strftime(util.ISO8601_DATE)
        if applic.get('received_date'):
            recvd_dt = util.convert_dt(applic['received_date'], util.DATE_FORMAT, util.ISO8601_DATE, False)
            if recvd_dt:
                applic['received_date'] = recvd_dt
            else:
                del applic['received_date'] # badly formatted date, do not insert
        if applic.get('validated_date'):
            valid_dt = util.convert_dt(applic['validated_date'], util.DATE_FORMAT, util.ISO8601_DATE, False)
            if valid_dt:
                applic['validated_date'] = valid_dt
            else:
                del applic['validated_date'] # badly formatted date, do not insert
        if applic.get('address'):
            if not applic.get('postcode'):
                postcode = locat.extract_postcode(applic['address'])
                if postcode:
                    applic['postcode'] = postcode
        if not applic.get('lat') and not applic.get('lng'):
            locat.set_latlngpost(applic)
            #if applic.get('postcode'):
            #    pdata = util.postcode_lookup(applic['postcode'])
            #    if pdata and pdata.get('lat') and pdata.get('lng'): 
            #        applic['lat'] = str(pdata['lat'])
            #        applic['lng'] = str(pdata['lng'])
            #if applic.get('address') and (not applic.get('lat') and not applic.get('lng')):
            #    lat, lng, postcode = util.geocode(applic['address']) 
            #    if lat or lng:
            #        if not applic.get('postcode') and postcode: # NB only partial postcode returned
            #            applic['postcode'] = postcode
            #        applic['lat'] = str(lat)
            #        applic['lng'] = str(lng)
    scraperwiki.sqlite.save(unique_keys=['authority', 'reference'],
                                data=applications, table_name=applications_table)

# make an external XML request to the gateway, transforming the result to an object and handling timeouts etc
def gateway_request(query, timeout = TIMEOUT, gateway_url = GATEWAY_URL):
    if not timeout: timeout = 0
    url = gateway_url
    if query:
        url = url+'?'+urllib.urlencode(query)
    print_query = ''
    if query:
        print_query = '('+query.get('auth','')+' '+query.get('day','')+'/'+query.get('month','')+'/'+query.get('year','')+')'
    msg = ''
    try:
        response = util.get_response(url, None, None, 'text/xml', timeout)
        # if there is an Internet time out or other fetch error
        # have to cut losses and move on
    except IOError as e:
        if hasattr(e, 'reason'): # URLError
            msg = 'Cannot reach gateway (URL error): '+util.vstr(e)+': '+print_query
        elif hasattr(e, 'code'): # HTTPError
            msg = 'Gateway returned HTTP error: '+util.vstr(e)+': '+print_query
        else:
            msg = 'IO error accessing gateway: '+util.vstr(e)+': '+print_query
    except socket.timeout as e:
        msg = 'Socket timeout accessing gateway ('+str(timeout)+'s): '+util.vstr(e)+': '+print_query
    except Exception as e:
        msg = 'Other error accessing gateway: '+util.vstr(e)+': '+print_query
    else:
        try:
            xml = response.read()
            doc = util.get_doc_xml(xml)
            result = util.from_xml(doc)
        except Exception as e:
            msg = 'Bad XML doc returned from source ('+xml[0:39]+'): '+util.vstr(e)+': '+print_query
        else:
            return result, ''
    return None, msg

# try to gather at least max planning applications from one source
# timeout and gateway URL no longer required as makes direct request to each authority
def gather_applications(target, start, end, max, timeout = TIMEOUT, days_block = DAYS_BLOCK, gateway_url = GATEWAY_URL,
                    applications_table = APPLICATIONS, progress_table = PROGRESS):
    auth_name = target['name']
    try:
        auths = util.get_table_vals(progress_table, '', "name='"+auth_name+"'")
        auth = auths[0]
    except:
        auth = {}
        auth['total'] = 0
    auth.update(target)

    if days_block <= 0: days_block = 1

    db_start_date = util.get_dt(start, util.ISO8601_DATE)
    if not db_start_date:
        db_start_date = date.today() - timedelta(days=start)
    db_end_date = util.get_dt(end, util.ISO8601_DATE)
    if not db_end_date:
        db_end_date = date.today() - timedelta(days=end)
    if not db_start_date or not db_end_date or db_end_date < db_start_date or db_start_date > date.today() or db_end_date > date.today():
        print 'Configuration start / end dates error for '+auth_name
        return

    # 2 dates defining current range of data stored
    start_date = util.get_dt(auth.get('start_date', ''), util.ISO8601_DATE) # start
    last_date = util.get_dt(auth.get('last_date', ''), util.ISO8601_DATE) #end
    if not start_date or start_date > db_start_date: # current start point is empty or after required start point
        scrape_start = db_start_date # start scraping again from the beginning
        start_date = db_start_date
    elif not last_date or last_date < start_date: # no current end point or it is before current start point
        scrape_start = start_date
    elif auth.get('last_status', '') != 'OK': # last scrape was not successful, try again
        scrape_start = last_date
    else:
        scrape_start = last_date + timedelta(days=days_block) # start collecting 1 block after current end point
    if scrape_start > db_end_date:
        scrape_start = db_end_date
    
    result = {}
    total = 0
    status = 'OK'
    while total < max and scrape_start <= db_end_date and status == 'OK':
        result.update(auth)
        result['last_scrape'] = date.today().strftime(util.ISO8601_DATE)
        result['last_date'] = scrape_start.strftime(util.ISO8601_DATE)
        result['start_date'] = start_date.strftime(util.ISO8601_DATE)
        result['last_count'] = 0
        result['last_match_count'] = 0
        status = 'Error'
        result['last_status'] = status
        query = {
            'auth': auth_name,
            'day': str(scrape_start.day),
            'month': str(scrape_start.month),
            'year': str(scrape_start.year), 
            'ndays': str(-days_block), # a block of days preceding the current start date
        }
        msg = ''
        #query['fmt'] = 'xml' # OLD METHOD
        #planning, msg = gateway_request(query, timeout, gateway_url) # XML request via external gateway
        query['fmt'] = 'object'
        planning = execute_scrape(query) # NEW - direct scrape request bypassing external gateway
        if not planning:
            if msg:
                result['last_msg'] = msg
            else:
                result['last_msg'] = 'No planning information returned from source'
        else:
            try:
                test = planning['applications']
            except:
                result['last_msg'] = 'Bad planning information returned from source'
            else:
                status = planning.get('status', 'None')
                result['last_status'] = status
                if planning.get('request_date_type'):
                    result['scrape_date_type'] = planning['request_date_type']        
                if status <> 'OK':
                    result['last_msg'] = planning.get('message', 'None')
                else:
                    result['last_msg'] = 'OK'
                    count = int(planning['count']) if planning.get('count') else 0
                    match_count = int(planning['match_count']) if planning.get('match_count') else 0
                    result['last_count'] = count
                    result['last_match_count'] = match_count
                    if planning.get('until_date'):
                        scrape_start = util.get_dt(planning['until_date'])
                        if scrape_start >= db_end_date:
                            result['last_date'] = db_end_date.strftime(util.ISO8601_DATE)
                        else:
                            result['last_date'] = scrape_start.strftime(util.ISO8601_DATE)
                    if scrape_start < db_end_date:
                        scrape_start = scrape_start + timedelta(days=days_block) # next date block
                        if scrape_start > db_end_date:
                            scrape_start = db_end_date # make sure it enters the while loop next time
                    else:
                        scrape_start = scrape_start + timedelta(days=1) # add increment so it breaks out from the while loop next time
                    if count > 0:
                        applications = planning['applications']['application']
                        store_applications(auth_name, auth['region'], applications, applications_table) # data stored here
                        total = total + count
        scraperwiki.sqlite.save(unique_keys=['name'], data=result, table_name=progress_table, verbose=0)
        if status <> 'OK': last_err = result['last_msg']
        result.clear()
    print 'Scraped '+str(total)+' records from '+auth_name+' ('+str(auth.get('config', ''))+') --> '+status
    if status <> 'OK': print last_err
    if total > 0:
        try:
            applics = util.get_table_vals(applications_table, 'count(*) as total', "authority='"+auth_name+"'")
            count = applics[0]['total']
            util.set_table_vals(progress_table, { 'total': count }, "name='"+auth_name+"'")
        except:
            pass
    return

# clear data from a single planning authority
def restart_authority(auth_name, applications_table = APPLICATIONS, progress_table = PROGRESS):
    if auth_name: # clearing the applications 'start_date' value makes data gathering start again
        util.set_table_vals(progress_table, { 'start_date': '' }, "name='"+auth_name+"'")
        scraperwiki.sqlite.execute("delete from "+applications_table+" where authority='"+auth_name+"'")
        scraperwiki.sqlite.commit()
        print "Successfully cleared the authority data of "+auth_name
    else:
        print "You must specify a single authority name"

# remove a single planning authority permanently
def remove_authority(auth_name, applications_table = APPLICATIONS, progress_table = PROGRESS):
    if auth_name:
        scraperwiki.sqlite.execute("delete from "+progress_table+" where name='"+auth_name+"'")
        scraperwiki.sqlite.execute("delete from "+applications_table+" where authority='"+auth_name+"'")
        scraperwiki.sqlite.commit()
        print "Successfully deleted the authority data of "+auth_name
    else:
        print "You must specify a single authority name"

# get the list of all potential planning authority sources 
# filter by the region or list specified
# and match up with the actual authorities currently in the database
def get_auths(region_or_list = None, progress_table = PROGRESS):
    result = []
    try:
        #scraper, msg = gateway_request( { 'fmt': 'xml' } ) # OLD METHOD = XML request via external gateway
        scraper = execute_scrape( { 'fmt': 'object' } ) # NEW - direct request bypassing external gateway
        all_authorities = scraper['authorities']['authority']
    except:
        pass
    else:
        for auth in all_authorities:
            tagged = False
            if isinstance(region_or_list, list):
                if not region_or_list or auth['name'] in region_or_list:
                    tagged = True
            else:
                if not region_or_list or region_or_list in auth.get('region', ''):
                    tagged = True
            if tagged:
                details = util.get_table_vals(progress_table, '', "name='"+auth['name']+"'")
                if details:
                    details = details[0]
                    details.update(auth)
                else:
                    details = auth
                result.append(details)             
        result = sorted(result, cmp=lambda x,y: cmp(x['name'],y['name']))
    return result

# do housekeeping in the applications database
# 1. check for indexes
# 2. set dates not in standard format to null
# 3. delete any applications older than certain threshold ages (6 months validated, 8 months received)
def do_cleanup(received_days = -240, validated_days = -180, applications_table = APPLICATIONS, ):
    for field_name in INDEXED_FIELDS:
        scraperwiki.sqlite.execute("create index if not exists "+field_name+"_manual_index on "+applications_table+" ("+field_name+")")
    app_data = scraperwiki.sqlite.select("count(*) as records from "+applications_table)
    total = app_data[0]['records']
    scraperwiki.sqlite.execute("update "+applications_table+" set received_date = null where received_date is not null and received_date not like '%-%'")
    scraperwiki.sqlite.execute("update "+applications_table+" set validated_date = null where validated_date is not null and validated_date not like '%-%'")
    scraperwiki.sqlite.commit()
    scraperwiki.sqlite.execute("delete from "+applications_table+" where validated_date is null and received_date is null")
    if received_days < 0 and validated_days < 0 and received_days < validated_days:
        today = date.today().strftime(util.ISO8601_DATE)
        received_days_ago, st = util.inc_dt(today, util.ISO8601_DATE, received_days)
        validated_days_ago, st = util.inc_dt(today, util.ISO8601_DATE, validated_days)
        scraperwiki.sqlite.execute("delete from "+applications_table+" where ((validated_date is not null and validated_date < '"+validated_days_ago+"') or (validated_date is null and received_date is not null and received_date < '"+received_days_ago+"'))")
    scraperwiki.sqlite.commit()
    app_data = scraperwiki.sqlite.select("count(*) as records from "+applications_table)
    total = total - app_data[0]['records']
    print "Created indices, cleaned dates and cleared out "+str(total)+" old records"

# adds location and date information to a planning record
def add_location_etc(record, default_date = None, default_date_type = None, in_date_format = util.DATE_FORMAT):
    if not in_date_format:
        in_date_format = util.DATE_FORMAT
    if record.get('address'):
        record['address'] = util.text_content(record['address']) # strip any html markup and replace with spaces
    if record.get('address') and not record.get('postcode'):
        postcode = locat.extract_postcode(record['address'])
        if postcode:
            record['postcode'] = postcode
    if record.get('received_date'):
        try:
            if in_date_format and in_date_format.startswith('%m'):
                uk_dates = False
            else:
                uk_dates = True
            dt = dateutil.parser.parse(record['received_date'], dayfirst=uk_dates).date()
            record['received_date'] = dt.strftime(util.DATE_FORMAT)
        except:
            try:
                dt = util.get_dt(record['received_date'], in_date_format)
                record['received_date'] = dt.strftime(util.DATE_FORMAT)
            except:
                del record['received_date'] # not a valid date - remove the entry
    elif default_date and default_date_type and default_date_type == 'received':
        record['received_date'] = default_date
    elif 'received_date' in record:
        del record['received_date']
    if record.get('validated_date'):
        try:
            dt = dateutil.parser.parse(record['validated_date'], dayfirst=True).date()
            record['validated_date'] = dt.strftime(util.DATE_FORMAT)
        except:
            try:
                dt = util.get_dt(record['validated_date'], in_date_format)
                record['validated_date'] = dt.strftime(util.DATE_FORMAT)
            except:
                del record['validated_date'] # not a valid date - remove the entry
    elif default_date and default_date_type and default_date_type == 'validated':
        record['validated_date'] = default_date
    elif 'validated_date' in record:
        del record['validated_date']
    if not record.get('reference'):
        if record.get('info_url'):
            record['reference'] = record['info_url'] # reference is a key so cannot be null
        else:
            record['reference'] = 'Empty' # reference is a key so cannot be null
    return record

# tweaks the raw html (NB after it is parsed by the mechanize browser)
def adjust_html(br, subs = None):
    response = br.response()  # this is a copy of the current browser response
    html = response.get_data()
    if debug: print "dbg: html pre sub:", html
    if not subs:
        return response
    for k, v in subs.items():
        html = re.sub(k, v, html, 0, re.U|re.S|re.I) # unicode|dot matches new line|ignore case
    if debug: print "dbg: html post sub:", html
    response.set_data(html)
    br.set_response(response)
    return response

# tweak urls to remove any extraneous stuff
# it is applied to the info_url in the record and to the next link if derived from an href
def adjust_url(url, subs = None):
    if debug: print "dbg: url pre sub:", url
    if not subs:
        return url
    #u = urlparse.urlsplit(url)
    #query = u.query
    #for k, v in subs.items():
    #    query = re.sub(k, v, query, 0, re.U|re.S|re.I) # unicode|dot matches new line|ignore case
    #url = urlparse.urlunsplit((u.scheme, u.netloc, u.path, query, u.fragment))
    for k, v in subs.items():
        url = re.sub(k, v, url, 0, re.U|re.S|re.I) # unicode|dot matches new line|ignore case
    if debug: print "dbg: url post sub:", url
    return url

# return authority/application sources for this scraper in object, XML, JSON or HTML format
def show_data(data, query):
    options = 'planning'
    if 'authorities' in data:
        options = 'scraper'
    fmt = query.get('fmt', '')
    if fmt == 'rss' or fmt == 'atom':
        fmt = 'xml'
    return util.data_output(data, fmt, options)

# set date field(s) using date config
def set_date_fields(fields, config, date, drop_down = False):
    if '{' in config:
        dmy = eval(config)
        if not dmy or ('month' not in dmy and 'MONTH' not in dmy) or 'year' not in dmy:
            raise ScrapeError('invalid date config: '+config)
        date_parts = date.split('/')
        if not date_parts or len(date_parts) != 3:
            raise ScrapeError('date not in d/m/y format: '+date)
        if 'day' in dmy:
            fields[dmy['day']] = [ date_parts[0] ]
        if 'month' in dmy:
            fields[dmy['month']] = [ date_parts[1] ]
        elif 'MONTH' in dmy:
            fields[dmy['MONTH']] = [ date_parts[1].upper() ]
        fields[dmy['year']] = [ date_parts[2] ]
    else:
        if drop_down:
            fields[config] = [ date ]
        else:
            fields[config] = date
    return fields

# get the form settings as a dict with keys 'namenum', 'fields' and 'submit'
# supplied is a string which is a simple form name/number or a dict to be evaluated
def get_form_settings(supplied = None):
    if not supplied:
        return { }
    elif '{' in supplied: 
        return eval(supplied)
    else: # was using isalnum but does not match dashes and underscores
        return { 'namenum': supplied }

# adds field values to the currently selected form
# can be ok to fail if a control exists but the supplied select option does not exist
def add_fields(br, fields, ok_to_fail = False):
    if fields:
        add_controls = []
        for k, v in fields.items():
            try:
                if k.startswith('#'):
                    control = br.find_control(name=k[1:], nr=0) # find first control named k
                else:
                    control = br.find_control(name=k, nr=0) # find first control named k
            #except mechanize._form.AmbiguityError as e: # more than one control with same name
            #    if debug: print "dbg: more than one form control named "+k
            #    raise
            except mechanize._form.ControlNotFoundError as e: # if the control does not exist, we create a dummy hidden control to hold the value
                if debug: print "dbg: cannot find form control "+k+", creating a dummy hidden control"
                if k.startswith('#'):
                    add_controls.append(k[1:])
                else:
                    add_controls.append(k)
        if add_controls:
            for k in add_controls:
                br.form.new_control('hidden', k, {'value':''} )
            br.form.fixup()
        br.form.set_all_readonly(False)
        try:
            for k, v in fields.items():
                if k.startswith('#'): # used to set a named control using option label
                    control = br.find_control(name=k[1:], nr=0) # find first control named k
                    if v is None:
                        control.disabled = True
                    elif isinstance(v, list):
                        if control.disabled: control.disabled = False
                        for i in v:
                            control.get(label=i, nr=0).selected = True # set the value by selecting its label (v[i])
                    else:
                        if control.disabled: control.disabled = False
                        control.get(label=v, nr=0).selected = True # set the value by selecting its label (v)
                        # NB label matches any white space compressed sub string so there is potential for ambiguity errors
                else:
                    #br[k] = v # default is to directly assign the named control a value (v)
                    control = br.find_control(name=k, nr=0) # find first control named k
                    if debug: print "dbg: form control "+control.name+" has type "+control.type
                    if v is None:
                        control.disabled = True
                    elif (control.type == 'radio' or control.type == 'checkbox' or control.type == 'select') and not isinstance (v, list):
                        if control.disabled: control.disabled = False
                        control.value = [ v ]
                    elif (control.type != 'radio' and control.type != 'checkbox' and control.type != 'select') and v and isinstance (v, list):
                        if control.disabled: control.disabled = False
                        control.value = v [0]
                    else:
                        if control.disabled: control.disabled = False
                        control.value = v
        except mechanize._form.ItemNotFoundError as e: # field select/check/radio option does not exist
            if ok_to_fail:
                return False
            else:
                if debug: print "dbg: form exception type: "+str(type(e))
                raise ScrapeError('cannot set form field '+k+': '+util.vstr(e))
        except Exception as e:
            if debug: print "dbg: form exception type: "+str(type(e))
            raise ScrapeError('cannot set form field '+k+': '+util.vstr(e))
    return True

# bypasses a scraped form, makes a direct url request supplying GET or POST parameter
def pseudo_form(br, url = None, action = None, fields = None, date_fields = None, method = None):
    if action:
        url = urlparse.urljoin(url, action)
    if debug: print "dbg: pseudo url:", url
    if debug: print "dbg: pseudo form fields:", fields
    if debug: print "dbg: pseudo date fields:", date_fields
    data = {}
    if fields:
        data.update(fields)
    if date_fields:
        data.update(date_fields)
    for k, v in data.items():
        if v and isinstance(v, list):
            data[k] = v[0]
    if method and method == 'GET':
        url = util.add_to_query(url, data)
        if debug: print "dbg: new url:", url
        return br.open(url)
    else:
        return br.open(url, urllib.urlencode(data))

# selects the form and sets up the form fields
# returns False if the requested date range is not available, otherwise True
def setup_form(br, form = None, action = None, fields = None, date_fields = None, method = None):
    if debug:
        msg = 'dbg: forms list:'
        i = 0
        try:
            for tform in br.forms():
                if tform.name: msg = msg+' '+tform.name
                else: msg = msg+' '+str(i)
                i = i + 1
            print msg
        except:
            pass
    try:
        if not form:
            form = '0'
            br.select_form(nr=0)
        elif form.isdigit():
            br.select_form(nr=int(form))
        else:
            br.select_form(name=form)
    except mechanize.ParseError:
        raise # ParseError has a bug which means it cannot seem to return its message via str()
        #raise ScrapeError('cannot find form '+form+': parse error '+msg)
    except Exception as e:
        raise ScrapeError('cannot find form '+form+': '+util.vstr(e))
    if debug: 
        try:
            print "dbg: form dump1:", br.form # can throw an error if the form contains unicode
        except:
            pass
    if action:
        current_action = br.form.action
        new_action = urlparse.urljoin(current_action, action)
        br.form.action = new_action
    if method and method == 'GET':
        br.form.method = method
    if debug: print "dbg: form fields:", fields
    if fields:
        add_fields(br, fields)
    if date_fields:
        if not add_fields(br, date_fields, True):
            if debug: print "dbg: date select option does not exist:", date_fields
            return False # if date control exists but select options are not available raise a flag
    if debug:        
        try:
            print "dbg: form dump2:", br.form # can throw an error if the form contains unicode
        except:
            pass
    return True

# returns response after submitting a form via a mechanize browser
# submit paramter is a submit control name/number or an id (starts with a #)
def submit_form(br, submit = None):
    try:
        if not submit:
            submit = ''
            response = br.submit()
        elif submit.isdigit():
            response = br.submit(nr=int(submit))
        elif submit.startswith('-'):
            for control in br.form.controls:
                if control.type == "submit":
                    control.disabled = True
            response = br.submit()
        elif submit.startswith('#'): 
            control = br.find_control(id=submit[1:], nr=0) # find first control with id submit
            if control.disabled: control.disabled = False
            response = br.submit(id=submit[1:], nr=0)
        else:
            control = br.find_control(name=submit, nr=0) # find first control named submit
            if control.disabled: control.disabled = False
            response = br.submit(name=submit, nr=0)
        return response
    except Exception as e:
        raise ScrapeError('error during form submit ('+submit+'): '+util.vstr(e))

# returns a response after following a link via a mechanize browser
# link paramter is a link text value or number or a name (starts with a !)
def process_link(br, link = None):
    try:
        if not link:
            link = ''
            response = br.follow_link()
        elif link.isdigit():
            response = br.follow_link(nr=int(link))
        elif link.startswith('!'):
            response = br.follow_link(name=str(link[1:]))
        else:
            response = br.follow_link(text=str(link))
        return response
    except Exception as e:
        raise ScrapeError('cannot follow link '+link+': '+util.vstr(e))

# create full list of all active planning authorities from source
def get_authorities_template():
    authorities = util.get_table_vals(SOURCES, '', '', 'order by name')
    auths = []
    for authority in authorities:
        auth_status = authority.get('status')
        if not auth_status or auth_status == 'active':
            new_auth = {}
            for k, v in authority.items():
                if v: 
                    if k == 'openly_local_id':
                        new_auth['openly_local_url'] = OL_URL % v
                    new_auth[k] = v
            auths.append(new_auth)
    data = {}
    data.update(INFORMATION)
    data['authorities'] = {}
    data['authorities'].update ( { 'authority': auths } )
    return data

# get template for planning data
def get_planning_template(query):
    data = {}
    data['status'] = 'Error'
    link_query = query.copy()
    if link_query.get('fmt') and link_query['fmt'] == 'object':
        del link_query['fmt']
    data['link'] = GATEWAY_URL + '?' + urllib.urlencode(link_query)
    auth = query.get('authority')
    if not auth:
        auth = query.get('auth')
    if not auth:
        data['message'] = 'authority not specified'
        return data
    authority = mcache_fetch('aut:'+auth)
    if not authority:
        if auth.isdigit():
            authority = util.get_table_vals(SOURCES, '', "openly_local_id="+auth)
        else:
            authority = util.get_table_vals(SOURCES, '', "name='"+auth+"'")
        if authority:
            authority = authority[0]
            mcache_put('aut:'+auth, authority)
    if not authority:
        data['message'] = '"'+auth+'" not in list of sources'
        return data
    data['authority_short_name'] = auth
    data['authority_name'] = authority.get('long_name', '')
    data['search_url'] = authority['search_url']
    if authority.get('table_name'):
        data['data_table'] = authority['table_name']
        thistable = authority['table_name']
    else:
        thistable = 'swdata'
    if authority.get('scraper') and authority.get('config', '').startswith('ScraperWiki'):
        data['scrape_url'] = 'https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=htmltable&name=' + authority['scraper']
        sqlquery = 'select * from ' + thistable + ' where date_scraped is not null order by start_date desc limit 100'
        data['scrape_url'] = util.add_to_query(data['scrape_url'], { 'query': sqlquery } )
    elif authority.get('scrape_url'):
        data['scrape_url'] = authority['scrape_url']
    if authority.get('openly_local_id'):
        data['openly_local_id'] = authority['openly_local_id']
        #data['openly_local_url'] = OL_URL % authority['openly_local_id']
    data['config'] = authority.get('config', '')
    data['authority_info'] = authority.get('info', '')
    auth_status = authority.get('status')
    if not debug and auth_status and auth_status != 'active':
        data['message'] = 'this authority scraper is not active'
        return data
    if query.get('ref'):
        data['requested_ref'] = query['ref']
    else:
        if query.get('date'):
            try:
                dt = dateutil.parser.parse(query['date'], dayfirst=True).date()
                data['requested_date'] = dt.strftime(util.DATE_FORMAT)
            except:
                data['message'] = 'invalid date parameter: '+query['date']
                return data
        else:
            missing_params = ''
            if not query.get('day'):     missing_params += 'day '
            if not query.get('month'):   missing_params += 'month '
            if not query.get('year'):    missing_params += 'year '
            if missing_params:
                data['message'] = missing_params+'not specified'
                return data
            try:
                dt = date(int(query['year']), int(query['month']), int(query['day']))
                data['requested_date'] = dt.strftime(util.DATE_FORMAT)
            except:
                data['message'] = 'invalid date parameters: day='+query['day']+', month='+query['month']+', year='+query['year']
                return data
        if query.get('ndays'):
            data['requested_days'] = query['ndays']
    data['scraped_date'] = date.today().strftime(util.DATE_FORMAT)
    data['scraped_at'] = datetime.today().strftime(util.RFC822_DATE) # full date and time
    data['status'] = 'OK'
    data['count'] = '0'
    data['applications'] = { 'application': [] }
    return data

# scrape one page of records
def scrape_page(cfg, br, html_subs, url_subs, default_url, follow_links = True, single_day = False):
    response = adjust_html(br, html_subs)
    html = response.read()
    url = response.geturl()
    if debug: print 'dbg: scraping from: ', url
    scrape_stuff = str(util.trim(cfg['scrape_records']))
    if not follow_links:
        scrape_stuff = OTHER_REGEX.sub('', scrape_stuff) # remove any other page links
    if debug: print 'dbg: records config:', scrape_stuff
    result = scrapemark.scrape(scrape_stuff, html, url)
    if debug: print 'dbg: scraped records:', result

    single_rec = False
    if not result or not result.get('records'):
        result = None
        if cfg.get('scrape_one_rec'):
            scrape_stuff = str(util.trim(cfg['scrape_one_rec']))
            if not follow_links:
                scrape_stuff = OTHER_REGEX.sub('', scrape_stuff) # remove any other page links
            if debug: print 'dbg: one record config:', scrape_stuff, url
            result = scrapemark.scrape(scrape_stuff, html, url)
            if debug: print 'dbg: scraped record:', result
        if not result:
            cfg_max_recs = str(util.trim(cfg['scrape_max_recs']))
            if cfg_max_recs == '__continue__':
                return [], html, url # if we are continuing without limit, zero records found is a normal return
            if debug: print 'dbg: no recs config:', cfg['scrape_no_recs']
            result = scrapemark.scrape(str(util.trim(cfg['scrape_no_recs'])), html)
            if not result:
                raise ScrapeError('invalid results page returned at: '+url)
            else:
                return [], html, url # no records indicator found, normal return with zero records found
        else:
            single_rec = True
            records = [ result ]
    else:
        records = result['records']

    # used to adjust any stored info_urls
    orig_url = adjust_url(url, url_subs) # any tweaks required?
    if default_url:
        default_url = urlparse.urljoin(orig_url, default_url)
        if debug: print 'dbg: start url:', orig_url
        if debug: print 'dbg: adjusted default url:', default_url

    for record in records:
        if not record.get('info_url'):
            if default_url: # if present, try to use the default url and/or reference
                info_url = default_url
                if info_url.endswith('='):
                    info_url += urllib.quote_plus(record.get('reference', ''))
            else:
                info_url = re.sub (r'[&\?]nocache=\w\w\w\w$', '', orig_url) # fallback for any record without an info_url -> use the current URL
            record['info_url'] = info_url 
        else:
            link = record['info_url']
            link = adjust_url(link, url_subs) # any tweaks required?
            record['info_url'] = urlparse.urljoin(orig_url, link) # make link absolute
        if follow_links and not single_rec and (record.get('info_url') or record.get('form_link')) and (cfg.get('scrape_info') or (cfg.get('scrape_dates') and not single_day)):
        # don't try to get detail if not following links or this is a single record only
            if record.get('form_link'):
                fset = get_form_settings(cfg.get('detail_form'))
                if fset.get('link_field'):
                    fields = fset.get('fields', {})
                    fields[fset['link_field']] = urllib.unquote_plus(record['form_link']) # assumes quoted at the moment (=Sefton) but some might not be in future
                    fset['fields'] = fields
                else:
                    fset['submit'] = record['form_link']
                if debug: print 'dbg: form link fset ', fset
                setup_form(br, fset.get('namenum'), fset.get('action'), fset.get('fields'), None, fset.get('method'))
                response = submit_form(br, fset.get('submit'))
                response = adjust_html(br, html_subs)
                exthtml = response.read()
                br.back()
                del record['form_link']
            elif record.get('info_url'):
                response = br.open(record['info_url'])
                response = adjust_html(br, html_subs)
                exthtml = response.read()
                br.back()
            else:
                raise ScrapeError('invalid config - no info_url or form_link to scrape detail info')
            if cfg.get('scrape_info'):
                extra = scrapemark.scrape(str(util.trim(cfg['scrape_info'])), exthtml)
                if debug: print 'dbg: extra info scrape:', extra
                if extra:
                    record.update(extra)
            #if not single_day and cfg.get('scrape_dates'):
            if cfg.get('scrape_dates'):
                extra = scrapemark.scrape(str(util.trim(cfg['scrape_dates'])), exthtml)
                if debug: print 'dbg: extra dates scrape:', extra 
                if extra:
                    record.update(extra)
    return records, html, url

# use config settings to establish the environment for scraping
def scrape_envt(cfg, scrape_url, search_url):

    if not scrape_url:
        scrape_url = search_url

    if cfg.get('headers'):
        headers = eval(cfg.get('headers'))
    else:
        headers = cfg.get('headers')
    
    #load a proxy if the scrape_url port is not empty or 80 or 443 - not required any more
    o = urlparse.urlsplit(scrape_url)
    if (o.scheme == 'http' and o.port and o.port != 80) or (o.scheme == 'https' and o.port and o.port != 443):
        br, handler, cj = util.get_browser(headers, '', PROXY)
        if debug: print 'dbg: on port', o.port, 'using proxy:', PROXY
    else:
        br, handler, cj = util.get_browser(headers)

    if debug:
        br.set_debug_http(True)

    if cfg.get('cookies'):
        cookies = eval(cfg.get('cookies'))
        for ck in cookies:
            util.set_cookie(cj, ck['name'], ck['value'], ck.get('domain'), ck.get('path', '/'))   
        if debug:
            print 'Cookies'
            for index, cookie in enumerate(cj):
                print index, ' : ', cookie

    if cfg.get('html_subs'):
        html_subs = eval(cfg.get('html_subs'))
        if debug: print "dbg: html_subs", html_subs
    else:
        html_subs = None
    if cfg.get('url_subs'):
        url_subs = eval(cfg.get('url_subs'))
        if debug: print "dbg: url_subs", url_subs
    else:
        url_subs = None
    if search_url:
        if cfg.get('ref_url'):
            default_url = urlparse.urljoin(search_url, cfg['ref_url'])
        else:
            default_url = search_url
    elif cfg.get('ref_url'):
        default_url = cfg['ref_url']
    else:
        default_url = None

    # any pre_start page which must be opened before anything else happens?
    if cfg.get('pre_start'):
        try:
            br.set_handle_redirect(False)
            response = br.open(cfg['pre_start'])
            if debug: print response.read()
        except:
            pass
        br.set_handle_redirect(True)

    # kludge adds a random query parameter to bypass scraperwiki caching - to force fetch of a fresh page each time
    # otherwise causes problems with some systems = Idox
    # NB Cache-Control no-cache headers etc do not work
    if not cfg.get('nocache_param_off'):
        nocache = "%04x" % random.randint(0, 65535)
        scrape_url = util.add_to_query(scrape_url, { 'nocache': nocache })

    # any POST parameters necessary to open the scrape_url?
    start_post = None
    if cfg.get('start_post'):
        start_post = urllib.urlencode(eval(cfg['start_post']))

    return br, handler, scrape_url, default_url, html_subs, url_subs, start_post

# substitute strings in the values of a target dict
def sub_dict(target, subs):
    result = False
    if target and subs:
        for k, v in target.items():
            if (isinstance(v, str) or isinstance(v, unicode)) and subs and SUBS_REGEX.search(v): # there are strings to substitute in the fields
                result = True
                target[k] = v % subs
    return result

# scrape one application from its ref number
def scrape_application(cfg, scrape_url, search_url, ref_req, follow_links = True):

    br, handler, scrape_url, default_url, html_subs, url_subs, start_post = scrape_envt(cfg, scrape_url, search_url)

    if cfg.get('ref_rel'):
        scrape_url = urlparse.urljoin(scrape_url, cfg['ref_rel'])

    fset = get_form_settings(cfg.get('form'))
    if cfg.get('ref_form'): # extra form setting to get applic using reference value
        fset_ref = get_form_settings(cfg['ref_form'])
        fset.update(fset_ref)

    response = br.open(scrape_url, start_post)
    if debug: print "dbg: html response info:", response.info() # headers
    response = adjust_html(br, html_subs)

    if fset.get('fields'):
        fields = fset['fields']
    else:
        fields = {}
    if fields.get('query'):
        fields['query'] = util.trim(fields['query'])
    if cfg.get('ref_field'):
        ref_req = REF_REGEX.sub(r'\1', ref_req) # remove spaces and brackets
        if not sub_dict(fields, { cfg['ref_field']: ref_req} ):
            fields[cfg['ref_field']] = ref_req
    else:
        return [] # if no ref field cannot make request
                
    if fset.get('no_form'): # pseudo form input if there is a 'no_form' key word
        response = pseudo_form(br, scrape_url, fset.get('action'), fields, None, fset.get('method'))
    else:
        form_ok = setup_form(br, fset.get('namenum'), fset.get('action'), fields, None, fset.get('method'))
        response = submit_form(br, fset.get('submit'))

    if debug: print "dbg: follow_links:", follow_links

    if cfg.get('ref_scrape'):
        cfg['scrape_records'] = cfg['ref_scrape']
    
    records, html, url = scrape_page(cfg, br, html_subs, url_subs, default_url, follow_links)
    if not records:
        return [] # zero records found
    else:
        return records


# scrape one authority - get applications received on the specific date (and for a number of days after)
# return any records and the dates from and to (some sites cannot return just a single day e.g one week)
def scrape_authority(cfg, scrape_url, search_url, date_req, days_req, follow_links = True, max_rec_value = MAX_REC_VALUE, max_pag_value = MAX_PAG_VALUE):

    br, handler, scrape_url, default_url, html_subs, url_subs, start_post = scrape_envt(cfg, scrape_url, search_url)

    fset = get_form_settings(cfg.get('form'))
    
    date_fields = {}
    single_day = False
    if not cfg.get('date_to') and not cfg.get('date_from'):
        #raise ScrapeError('no to or from date value specified in the configuration')
        date_from = None
        date_to = None
        if debug: print 'dbg: no dates sought - static applications list'
        # dates need to be set to max and min of any dates returned
    else:
        try:
            min_days_req = int(cfg.get('ndays'))
        except:
            min_days_req = 0
        try:
            int_days_req = int(days_req)
        except:
            int_days_req = min_days_req
        if int_days_req < -1: 
            days_extra =  int_days_req + 1
            date_req, dummy_date = util.inc_dt(date_req, util.DATE_FORMAT, days_extra)
            days_extra = abs(days_extra)
        elif int_days_req > 1:
            days_extra = int_days_req - 1
        else:
            days_extra = 0
        date_inc = cfg.get('date_inc', '')
        if '&' in date_inc and '@' in date_inc:
            dummy_date, date_to = util.inc_dt(date_req, util.DATE_FORMAT, days_extra + 1) # end date is exclusive
            date_from, dummy_date = util.inc_dt(date_req, util.DATE_FORMAT, -1) # start date is exclusive
        elif date_inc == '&':
            date_from, date_to = util.inc_dt(date_req, util.DATE_FORMAT, days_extra + 1) # end date is exclusive
        elif date_inc == '@':
            dummy_date, date_to = util.inc_dt(date_req, util.DATE_FORMAT, days_extra)
            date_from, dummy_date = util.inc_dt(date_req, util.DATE_FORMAT, -1) # start date is exclusive
        elif date_inc == 'Month': # one whole month around the supplied date
            date_from, date_to = util.inc_dt(date_req, util.DATE_FORMAT, date_inc)
            max_rec_value = max_rec_value * 2
        elif date_inc[0:1] == '-': # custom negative increment and optional positive one around requested date
            nums = date_inc.split('+')
            date_from, dummy_date = util.inc_dt(date_req, util.DATE_FORMAT, nums[0])
            if len(nums) > 1:
                dummy_date, date_to = util.inc_dt(date_req, util.DATE_FORMAT, nums[1])
            else:
                date_to = date_req
        elif date_inc.isalpha(): # weekday
            if cfg.get('date_to') and cfg.get('date_from'):
                raise ScrapeError('weekday date_inc can only apply with either a to OR from date in the configuration')
            elif cfg.get('date_from'):
                date_inc = '-' + date_inc
            date_from, date_to = util.inc_dt(date_req, util.DATE_FORMAT, date_inc)
        elif date_inc.isdigit() and int(date_inc) > 1: # overrides min number of days to return
            date_from, date_to = util.inc_dt(date_req, util.DATE_FORMAT, int(date_inc))
        elif days_extra > 0: 
            date_from, date_to = util.inc_dt(date_req, util.DATE_FORMAT, days_extra)
        else:
            date_from = date_req
            date_to = date_req
        if debug: print 'dbg: date range sought after any increment:', date_from, date_req, date_to
        if cfg.get('request_date_format'):
            set_date_to = util.convert_dt(date_to, util.DATE_FORMAT, cfg.get('request_date_format'))
            set_date_from = util.convert_dt(date_from, util.DATE_FORMAT, cfg.get('request_date_format'))
            set_date_req = util.convert_dt(date_req, util.DATE_FORMAT, cfg.get('request_date_format'))
            if debug: print 'dbg: date range sought after format conversion', set_date_from, set_date_req, set_date_to
        else:
            set_date_to = date_to
            set_date_from = date_from
            set_date_req = date_req
        if cfg.get('date_from') and cfg.get('date_to'):
            if cfg.get('date_from') == cfg.get('date_to'): # one field named twice means use original requested date not incremented dates
                set_date_fields(date_fields, cfg['date_to'], set_date_req)
            else:
                set_date_fields(date_fields, cfg['date_to'], set_date_to)
                set_date_fields(date_fields, cfg['date_from'], set_date_from)
        elif cfg.get('date_to'):
            if fset.get('no_form'):
                set_date_fields(date_fields, cfg['date_to'], set_date_to)
            else:
                set_date_fields(date_fields, cfg['date_to'], set_date_to, True) # assumed to be drop down controls by default
        else:
            if fset.get('no_form'):
                set_date_fields(date_fields, cfg['date_from'], set_date_from)
            else:
                set_date_fields(date_fields, cfg['date_from'], set_date_from, True) # assumed to be drop down controls by default
        if '&' in date_inc:
            date_to, dummy_date = util.inc_dt(date_to, util.DATE_FORMAT, -1) # end date is exclusive, decrement it by 1
        if '@' in date_inc:
            dummy_date, date_from = util.inc_dt(date_from, util.DATE_FORMAT, 1) # start date is exclusive, increment it by 1
        if debug: print 'dbg: real date range after increments/decrements removed :', date_from, date_req, date_to
        if date_from == date_to: single_day = True

    if fset.get('fields'):
        fields = fset['fields']
    else:
        fields = {}
    if fields.get('query'):
        fields['query'] = util.trim(fields['query'])
    if fields and date_fields and sub_dict(fields, date_fields): # test if substitutions were made
        date_fields = None # if so remove them as separate fields
    
    if fset.get('no_form'): # pseudo form input if there is a 'no_form' key word

        if fset.get('list_url'): # scrape the link to a fixed list of applications
            response = br.open(scrape_url, start_post)
            if debug: print "dbg: html response info:", response.info() # headers
            response = adjust_html(br, html_subs)
            if debug: print 'dbg: cfg list_url:', fset.get('list_url')
            html = response.read()
            url = response.geturl()
            result = scrapemark.scrape(str(util.trim(fset.get('list_url'))), html, url)
            if not result or not result.get('list_url'):
                raise ScrapeError('no valid list_url found: '+fset.get('list_url'))
            else:
                if debug: print 'dbg: scraped list_url record:', result
                response = br.open(result.get('list_url'))
            
        else: # otherwise simulate form submission with POST/GET request

            response = pseudo_form(br, scrape_url, fset.get('action'), fields, date_fields, fset.get('method'))

    else:

        response = br.open(scrape_url, start_post)
        if debug: print "dbg: html response info:", response.info() # headers
        response = adjust_html(br, html_subs)
    
        form_ok = setup_form(br, fset.get('namenum'), fset.get('action'), fields, date_fields, fset.get('method'))
        if not form_ok: # form cannot find the requested date select options = normal zero return
            return date_from, date_to, []
        
        response = submit_form(br, fset.get('submit'))

    if debug: print "dbg: follow_links:", follow_links
    
    records, html, url = scrape_page(cfg, br, html_subs, url_subs, default_url, follow_links, single_day)
    if not records:
        return date_from, date_to, [] # normal return with zero records found

    current_page = 1
    max_recs = 0 # no scrape_max_recs config means the next page is never sought
    max_pages = 0
    if cfg.get('scrape_max_recs'):
        max_recs = max_rec_value # prevent any run away loop
        max_pages = max_pag_value
        cfg_max_recs = str(util.trim(cfg['scrape_max_recs']))
        if cfg_max_recs == '__continue__':
            pass # this means keep following any next page link until system max number of records or pages is reached or a page returns no values
        elif cfg_max_recs.isdigit():
            max_recs = int(cfg_max_recs) # specified max records limit in configuration
        else:
            result = scrapemark.scrape(cfg_max_recs, html) 
            if result:
                rec_value = result.get('max_recs', '')
                pag_value = result.get('max_pages', '')
                if rec_value:
                    rec_value_list = rec_value.split()
                    rec_value = rec_value_list[-1] # can be a space separated list, so take the last value
                    if rec_value.isdigit():
                        max_recs = int(rec_value)
                    elif rec_value.lower() == 'one': # awkward bastards
                        max_recs = 1
                    else:
                        raise ScrapeError('max records value is no good: '+rec_value)
                elif pag_value:
                    pag_value_list = pag_value.split()
                    pag_value = pag_value_list[-1] # can be a space separated list, so take the last value
                    if pag_value.isdigit():
                        max_pages = int(pag_value)
                    else:
                        raise ScrapeError('max pages value is no good: '+pag_value)
                else:
                    raise ScrapeError('no valid max records or max pages value found: '+util.vstr(result))
            else:
                max_recs = 0 # no valid max_recs or max_pages found means the next page is never sought
                max_pages = 0
            if max_recs > max_rec_value:
                max_recs = max_rec_value # prevent any run away loop
            if max_pages > max_pag_value:
                max_pages = max_pag_value # prevent any run away loop
            if debug: print "dbg: scrape max_recs:", result, util.vstr(max_recs), util.vstr(max_pages)

    while (len(records) > 1 and len(records) < max_recs and current_page < max_pages):

        try:
            if cfg.get('next_type', '') == 'scrape':
            #if cfg.get('scrape_next_link'): 
                result = scrapemark.scrape(str(util.trim(cfg['next_page'])), html, url)
                if debug: print "dbg: scrape next_page:", result
                if not result:
                    raise ScrapeError('no next link scraped')
                link = result['next_link']
                link = adjust_url(link, url_subs) # any tweaks required?
                response = br.open(link)
            elif cfg.get('next_type', '') == 'href':
                link = xpath_text(handler.element, cfg['next_page'])
                if not link:
                    raise ScrapeError('no next link found via xpath')
                link = adjust_url(link, url_subs) # any tweaks required?
                response = br.open(link)
            elif cfg.get('next_type', '') == 'link':
                response = process_link(br, cfg['next_page'])
            elif cfg.get('next_type', '') == 'form':
                fset = get_form_settings(cfg.get('next_page'))
                setup_form(br, fset.get('namenum'), fset.get('action'), fset.get('fields'), None, fset.get('method'))
                response = submit_form(br, fset.get('submit'))
            else:
                break # normal exit = no way defined to get to next page = single page only
        except Exception as e:
            if max_recs < max_rec_value or max_pages < max_pag_value: # if there are still pages or records to get, this is an error
                raise ScrapeError("cannot follow next page link: "+util.vstr(e))
            else:
                break # normal exit = reached end = no next page to follow

        new_records, html, url = scrape_page(cfg, br, html_subs, url_subs, default_url, follow_links, single_day)
        if not new_records:
            break # NB different from previous - in this case normal return keeping previous records found so far

        records.extend(new_records)
        current_page = current_page + 1

    return date_from, date_to, records

# perform a scrape of one data block from an external authority
def execute_scrape(query = None):
    warnings.simplefilter("error", category=UnicodeWarning)
    if not query or (len(query) == 1 and 'fmt' in query) or (len(query) == 2 and 'fmt' in query and 'ndays' in query):
        data = mcache_fetch('_auths_')
        if not data:
            data = get_authorities_template()
            mcache_put('_auths_', data)
        return show_data(data, query)
    else: 
        start_clock = time.time()
        data = get_planning_template(query)
        if data['status'] == 'OK':
            table = 'swdata'
            if data.get('data_table'): 
                table = data['data_table']
            auth = data['authority_short_name']
            config_name = data['config']
            if not config_name:
                data['status'] = 'Error'
                data['message'] = 'missing named configuration for '+auth
            else:
                cfg = mcache_fetch('cfg:'+config_name)
                if not cfg:
                    config_list = util.get_table_vals(CONFIGS)
                    config_map = util.get_map(config_list, 'name')
                    if config_map and config_map.get(config_name):
                        cfg = util.dict_inherited(config_map, config_name)
                        mcache_put('cfg:'+config_name, cfg)
                if not cfg:
                    data['status'] = 'Error'
                    data['message'] = 'no settings found for '+auth+' configuration = '+config_name
                else:
                    if cfg.get('form'): # per authority adjustment to configuration - don't cache this
                        cfg['form'] = cfg['form'].replace('+authority+', auth)
                        cfg['form'] = cfg['form'].replace('+table+', table)
                    if cfg.get('ref_form'): # per authority adjustment to configuration - don't cache this
                        cfg['ref_form'] = cfg['ref_form'].replace('+authority+', auth)
                        cfg['ref_form'] = cfg['ref_form'].replace('+table+', table)
                    if debug: print "dbg: config:", cfg 
                    if debug: print "dbg: data:", data 
                    if query.get('no_detail'):
                        follow_links = False
                    else:
                        follow_links = True
                    try:
                        default_date = None
                        if data.get('requested_ref'):
                            records = scrape_application(cfg, data.get('scrape_url'), data['search_url'], data['requested_ref'], follow_links)
                            date_began = None; date_reached = None;
                        else:
                            date_began, date_reached, records = scrape_authority(cfg, data.get('scrape_url'), data['search_url'], data['requested_date'], data.get('requested_days'), follow_links)
                            if date_began and date_reached and date_began == date_reached and date_reached == data['requested_date']:
                                default_date = date_reached
                        request_date_type = cfg.get('request_date_type', '')
                        match_count = 0
                        date_min = None
                        date_max = None
                        for record in records:
                            record = add_location_etc(record, default_date, request_date_type, cfg.get('received_date_format', util.DATE_FORMAT))
                            if date_began and date_reached: # a particular date was requested, so return the range around that
                                if request_date_type == 'received':
                                    if util.match_dt(record.get('received_date'), date_began, date_reached):
                                        match_count = match_count + 1
                                elif request_date_type == 'validated':
                                    if util.match_dt(record.get('validated_date'), date_began, date_reached):
                                        match_count = match_count + 1
                            else: # no date was requested, so work out the range of active dates within the list and return that
                                if record.get('received_date'):
                                    if not date_min or util.test_dt(date_min, record.get('received_date')) > 0:
                                        date_min = record.get('received_date')
                                    if not date_max or util.test_dt(date_max, record.get('received_date')) < 0:
                                        date_max = record.get('received_date')
                                elif record.get('validated_date'):
                                    if not date_min or util.test_dt(date_min, record.get('validated_date')) > 0:
                                        date_min = record.get('validated_date')
                                    if not date_max or util.test_dt(date_max, record.get('validated_date')) < 0:
                                        date_max = record.get('validated_date')
                            data['applications']['application'].append(record)
                        data['count'] = str(len(records))
                        if not data.get('requested_ref'):
                            if request_date_type:
                                data['request_date_type'] = request_date_type
                                if request_date_type == 'received' or request_date_type == 'validated':
                                    data['match_count'] = str(match_count)
                            else:
                                data['request_date_type'] = 'unused'
                        if date_began and date_reached:
                            data['from_date'] = date_began
                            data['until_date'] = date_reached
                        elif date_min and date_max:
                            data['from_date'] = date_min
                            data['until_date'] = date_max  
                    except Exception as e:
                        data['status'] = 'Error'
                        data['message'] = util.vstr(e)
                        if debug: raise   #   NB  
        data['elapsed_secs'] = time.time() - start_clock
        return show_data(data, query)

# put an item into the local memory cache
# make copy, otherwise the cached version is mutable 
def mcache_put(key, value):
    if isinstance(key, dict):
        keyhash = hash(tuple(sorted(key.iteritems())))
    elif isinstance(key, list):
        keyhash = hash(tuple(key))
    else:
        keyhash = hash(key)
    CACHE[keyhash] = copy.deepcopy(value)
    if debug: print "dbg: cache insert:", key, keyhash

# get an item from the local memory cache
# make copy, otherwise the cached version is mutable
def mcache_fetch(key):
    if isinstance(key, dict):
        keyhash = hash(tuple(sorted(key.iteritems())))
    elif isinstance(key, list):
        keyhash = hash(tuple(key))
    else:
        keyhash = hash(key)
    result = copy.deepcopy(CACHE.get(keyhash))
    if debug:
        if result: print "dbg: cache hit:", key, keyhash
        else: print "dbg: cache miss:", key, keyhash
    return result

class ScrapeError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message

# scrape a block of data from another scraperwiki scraper
# works but not in use
def get_from_scraper(scraper, table, fields, sequence, sequence_from, sequence_to = None, limit = None, scrape_date = 'date_scraped'):
    query = []
    for k, v in fields.items():
        if v: query.append(v + ' as ' + k)
        else: query.append(k)
    query_string = "select %s from %s where %s is not null" % (", ".join(query), table, scrape_date)
    if sequence and (sequence.startswith('date_') or sequence.endswith('_date')):
        query_string += " and %s is not null and length(%s) = 10 and %s >= '%s'" % (sequence, sequence, sequence, sequence_from.strftime(util.ISO8601_DATE))
        if sequence_to: 
            query_string += " and %s <= '%s'" % (sequence, sequence_to.strftime(util.ISO8601_DATE))
    elif sequence:
        query_string += " and %s is not null and %s >= %s" % (sequence, sequence, sequence_from)
        if sequence_to: 
            query_string += " %s <= %s" % (sequence, sequence_to)
    query_string += " order by %s desc" % scrape_date
    if limit: query_string += " limit " + str(limit)
    #print query_string
    db_url = "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=%s&query=%s" % (scraper, urllib.quote_plus(query_string))
    return json.load(urllib2.urlopen(db_url, None, 10))  # 10 sec timeout

""" if __name__ == 'scraper':
    fields = { 'reference': 'uid',
        'address': '',
        'postcode': '',
        'description': '',
        'received_date': 'date_received',
        'validated_date': 'date_validated', }
    date_from = date(2012, 1, 31)
    result = get_from_scraper('denbighshire_planning_applications', 'swdata', fields, 'start_date', date_from)
    print result
    print len(result) """




