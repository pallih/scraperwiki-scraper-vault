# a library of utility functions

import scraperwiki
import lxml.html
import lxml.html.soupparser
from lxml import etree
import re
from datetime import date
import urllib, urllib2, urlparse
from datetime import datetime
from datetime import timedelta
import time
import json
import mechanize
from pytz import timezone
from BeautifulSoup import BeautifulSoup
#from BeautifulSoup import MinimalSoup
from cStringIO import StringIO
from csv import reader
import random
import cookielib
import matplotlib.pyplot as pl
import base64
import sys
import cPickle

DATE_FORMAT = "%d/%m/%Y"
RFC822_DATE = "%a, %d %b %Y %H:%M:%S %z"
ISO8601_DATE = "%Y-%m-%d"
RFC3339_DATE = "%Y-%m-%dT%H:%M:%SZ"
TABLE_REGEX = re.compile(r'create\s+table\s+(\S+)\s*\(([^\)]+)\)', re.I) # ignore case
INDEX_REGEX = re.compile(r'(create\s+(?:unique\s+)?index)\s+(\S+)\s+on\s+(\S+)\s+\(([^\)]+)\)', re.I) # ignore case
TAGS_REGEX = re.compile(r'<[^<]+?>')
GAPS_REGEX = re.compile(r'\s+', re.U) # unicode spaces include html &nbsp;
TZ = timezone('Europe/London')
AUTHOR = 'AS' # for Atom feeds 
WEEKDAYS = { 'Mon': 0, 'Tue': 1, 'Wed': 2, 'Thu': 3, 'Fri': 4, 'Sat': 5, 'Sun': 6 }
DEFAULT_CACHE_AGE = 43200 # default cache expiry in secs = 12 hours
SLOT_TIME = 60 # max processing time for processing slots = secs
NUM_SLOTS = 2 # number of processes
CACHE = {} # local memory cache
    
all_rss_fields = { # default map from data fields to RSS, to be overridden
        'title': 'title',
        'description': 'description',
        'link': 'link',
        'items': 'items',
        'item': 'item',
        'sub_item': {
            'title': 'title',
            'description': 'description',
            'link': 'link',
            'guid': 'id',
            },
        'geo_item': {
            'point': 'point'
            }
        }

all_atom_fields = { # default map from data fields to ATOM, to be overridden
        'title': 'title',
        'subtitle': 'description',
        'link': 'link',
        'id': 'id',
        'items': 'items',
        'item': 'item',
        'sub_item': {
            'title': 'title',
            'content': 'description',
            'link': 'link',
            'id': 'id',
            },
        'geo_item': {
            'point': 'point'
            }
        }

# import a full CSV file into a table or if match is set, update the one row where the key values match
def import_csv(csv_file_url, table_name, keys, match = None): 
    if not keys or not isinstance(keys, list):
        return 0
    if not isinstance(keys, list):
        keys = [ keys ]
    if match and not isinstance(match, list):
        match = [ match ]
    # NB no-cache headers do not work
    #headers =  { 'Cache-Control': 'no-cache',  'Pragma': 'no-cache',  }
    # instead add random url string to short circuit cache
    nocache = "%04x" % random.randint(0, 65535)
    url = add_to_query(csv_file_url, { 'nocache': nocache })
    csv_text = scraperwiki.scrape(url)
    #response = get_response(csv_file_url, None, headers, 'text/csv')
    #csv_text = response.read()
    lines = reader(StringIO(csv_text))
    headings = lines.next()
    add_list = []
    if match:
        matchup = dict(zip(keys, match))
    else:
        matchup = None
    for line in lines:
        values = dict(zip(headings, line)) 
        if matchup:
            use_values = True
            for key in keys:
                if matchup[key] != values[key]:
                    use_values = False
                    break # exit the keys loop, match condition failed
            if use_values: # all keys matched
                add_list.append(values)
                break # key matched so no need to continue with lines loop
        else:
            add_list.append(values)
    if add_list: 
        if not matchup:
            scraperwiki.sqlite.execute("drop table if exists " + table_name)
            scraperwiki.sqlite.commit()
        scraperwiki.sqlite.save(keys, add_list, table_name, verbose=0) # one save operation (= list of dics), not many
    return len(add_list)

# set content type for JSON, XML or RSS formats
def set_content(fmt = 'xml'): 
    if fmt == 'json':
        scraperwiki.utils.httpresponseheader("Content-Type", "application/json")
    elif fmt == 'jsonp':
        scraperwiki.utils.httpresponseheader("Content-Type", "application/javascript")
    elif fmt == 'rss':
        scraperwiki.utils.httpresponseheader("Content-Type", "application/rss+xml")
    elif fmt == 'atom':
        scraperwiki.utils.httpresponseheader("Content-Type", "application/atom+xml")
    elif fmt == 'html':
        scraperwiki.utils.httpresponseheader("Content-Type", "text/html")
    elif fmt == 'csv':
        scraperwiki.utils.httpresponseheader("Content-Type", "text/csv")   
    elif fmt == 'tsv':
        scraperwiki.utils.httpresponseheader("Content-Type", "text/tab-separated-values")   
    else: # XML always the default - see data_output()
        scraperwiki.utils.httpresponseheader("Content-Type", "text/xml")

# redirect to another web page
def redirect(url, code=303): 
    if code <= 307 and code >= 300:
        scraperwiki.utils.httpresponseheader("Location", url)
        scraperwiki.utils.httpstatuscode(code)
    else:
        scraperwiki.utils.httpresponseheader("Content-Type", "text/html")
        print """
        <html>
        <head>
        <meta http-equiv="Refresh" content="0; url=%s" />
        </head>
        <body>
        <p>Please follow this link: <a href="%s">%s</a>.</p>
        </body>
        </html>""" % (url, url, url)
    sys.exit()

# output a data dict in JSON, XML or RSS formats
def data_output(data, fmt = 'xml', options = None):
    if fmt == 'object':
        return data
    elif fmt == 'json':
        if options: # if this is set it's really JSONP
            return options + '(' + json.dumps(data, indent=4) + ');'
        else:
            return json.dumps(data, indent=4)
    elif fmt == 'jsonp':
        if not options: options = 'callback'
        return options + '(' + json.dumps(data, indent=4) + ');'
    elif fmt == 'rss':
        root = to_rss(data, options, ISO8601_DATE)
        root.addprevious(etree.PI('xml-stylesheet', 'type="text/xsl" title="XSL stylesheet" href="http://www.speakman.org.uk/rss.xsl"'))
        return etree.tostring(root.getroottree(), encoding="utf-8", xml_declaration=True, pretty_print=True)
    elif fmt == 'atom': 
        root = to_atom(data, options, ISO8601_DATE) 
        return etree.tostring(root, encoding="utf-8", xml_declaration=True, pretty_print=True)
    elif fmt == 'html':
        if not options:
            options = 'data'
        html_string = to_html('', data, options)
        root = lxml.html.fromstring(html_string)
        return etree.tostring(root, pretty_print=True, method="html")
        #return etree.tostring(root, encoding="utf-8", xml_declaration=True, pretty_print=True)
    else: # XML always the default - see set_content()
        if not options:
            options = 'root'
        root = to_xml(options, data)
        return etree.tostring(root, encoding="utf-8", xml_declaration=True, pretty_print=True)
    
# use data to fill out an RSS 2.0 feed (with option for GeoRSS)
def to_rss(data, map, in_date_fmt = ISO8601_DATE):
    GEORSS_NAMESPACE = "http://www.georss.org/georss"
    GEORSS = "{%s}" % GEORSS_NAMESPACE
    NSMAP = { 'georss': GEORSS_NAMESPACE }
    feed_type = 'rss'
    for i in data[map['items']][map['item']]:
        for k, v in map['geo_item'].items():
            if v in i:
                feed_type = 'georss'
                break
    if feed_type == 'georss':
        root = etree.Element('rss', nsmap=NSMAP)
    else:
        root = etree.Element('rss')
    root.set("version", "2.0")
    branch = etree.SubElement(root, "channel")
    for k, v in map.items():
        if k <> 'item' and  k <> 'items' and k <> 'geo_item' and k <> 'sub_item' and v in data:
            twig = etree.SubElement(branch, k)
            twig.text = vstr(data[v])
    pubdate = datetime.now(TZ).strftime(RFC822_DATE)
    twig = etree.SubElement(branch, 'pubDate')
    twig.text = vstr(pubdate)
    for i in data[map['items']][map['item']]:
        twig = etree.SubElement(branch, "item")
        no_date = True
        for k, v in map['sub_item'].items():
            if v in i:
                leaf = etree.SubElement(twig, k)
                if k == 'pubDate':
                    no_date = False
                    if in_date_fmt ==  ISO8601_DATE:
                        leaf.text = convert_dt(vstr(i[v])+'T12:00:00Z', RFC3339_DATE, RFC822_DATE) #  make time noon
                    else:
                        leaf.text = convert_dt(vstr(i[v]), in_date_fmt, RFC822_DATE) 
                else:
                    leaf.text = vstr(i[v])
                if k == 'guid':
                    leaf.set("isPermaLink", "false")
        if no_date:
            leaf = etree.SubElement(twig, 'pubDate')
            leaf.text = vstr(pubdate)
        for k, v in map['geo_item'].items():
            if v in i:
                leaf = etree.SubElement(twig, GEORSS+k)
                leaf.text = vstr(i[v])
    return root

# use data to fill out an ATOM feed (with option for GeoRSS)
def to_atom(data, map, in_date_fmt = ISO8601_DATE):
    GEORSS_NAMESPACE = "http://www.georss.org/georss"
    ATOM_NAMESPACE = "http://www.w3.org/2005/Atom"
    GEORSS = "{%s}" % GEORSS_NAMESPACE
    GEONSMAP = { None: ATOM_NAMESPACE, 'georss': GEORSS_NAMESPACE }
    NSMAP = { None: ATOM_NAMESPACE }
    feed_type = 'atom'
    for i in data[map['items']][map['item']]:
        for k, v in map['geo_item'].items():
            if v in i:
                feed_type = 'georss'
                break
    if feed_type == 'georss':
        root = etree.Element('feed', nsmap=GEONSMAP)
    else:
        root = etree.Element('feed', nsmap=NSMAP)
    for k, v in map.items():
        if k <> 'item' and  k <> 'items' and k <> 'geo_item' and k <> 'sub_item' and v in data:
            branch = etree.SubElement(root, k)
            if k == 'link':
                branch.set("href", vstr(data[v]))
                branch.set("rel", "self")
            else:
                branch.text = vstr(data[v])
    pubdate = datetime.now(TZ).strftime(RFC3339_DATE)
    branch = etree.SubElement(root, 'updated')
    branch.text = vstr(pubdate)
    for i in data[map['items']][map['item']]:
        branch = etree.SubElement(root, "entry")
        no_date = True
        for k, v in map['sub_item'].items():
            if v in i:
                leaf = etree.SubElement(branch, k)
                if k == 'link':
                    leaf.set("href", vstr(i[v]))
                elif k == 'published' or k == 'updated':
                    no_date = False
                    if in_date_fmt ==  ISO8601_DATE:
                        leaf.text = convert_dt(vstr(i[v])+'T12:00:00Z', RFC3339_DATE, RFC3339_DATE) #  make time noon
                    else:
                        leaf.text = convert_dt(vstr(i[v]), in_date_fmt, RFC3339_DATE) 
                else:
                    leaf.text = vstr(i[v])
                if k == 'summary' or k == 'content':
                    leaf.set("type", "html")
        if no_date:
            leaf = etree.SubElement(branch, 'updated')
            leaf.text = vstr(pubdate)
        leaf = etree.SubElement(branch, 'author')
        #end = etree.SubElement(leaf, 'name')
        #end.text = vstr(AUTHOR)
        for k, v in map['geo_item'].items():
            if v in i:
                leaf = etree.SubElement(branch, GEORSS+k)
                leaf.text = vstr(i[v])
    return root

# unserialize an XML document to a dictionary (containing dicts, strings or lists)
def from_xml(element):
    if len(element) > 0:
        outdict = {}
        if element.get('type') == 'list':
            value = []
            for i in element:
                value.append(from_xml(i))
            outdict[element[0].tag] = value
        else:
            for i in element:
                outdict[i.tag] = from_xml(i)
        return outdict
    else:
        return element.text

# serialise the contents of a dictionary as simple XML
def to_xml(element_name, data):
    element_name = re.sub('\s', '_', element_name) # replace any spaces in the tag name with underscores
    element = etree.Element(element_name)
    if isinstance (data, dict):
        keys = data.keys()
        keys.sort() # output is in alphab order 
        for key in keys: # output simple string elements first
            if not isinstance(data[key], list) and not isinstance(data[key], dict):
                element.append(to_xml(key, data[key]))
        for key in keys: # any lists and dicts come afterwards
            if isinstance(data[key], list): # lists stay in original order
                element.set('type', 'list')
                for i in data[key]:
                    element.append(to_xml(key, i))
            elif isinstance(data[key], dict):
                element.append(to_xml(key, data[key]))
    else:
        element.text = vstr(data)
    return element

# serialise the contents of a dictionary as simple HTML (NB string output)
def to_html(container, data, title = ''):
    if title:
        title = re.sub('_', ' ', title) # replace any underscores with spaces
        title = title.title()
    if not container:
        output = "<html><head>"
        if title:
            output = output+"<title>"+title+"</title>"
        output = output+'</head><body>'
        if title:
            output = output+"<h1>"+title+"</h1>"
        output = output+to_html('body', data)
        return output+"</body></html>"
    elif isinstance (data, dict):
        output = ''
        if title:
            output = output+'<h2>'+title+'</h2>'
        list_strings = []
        list_structs = []
        keys = data.keys()
        for key in keys: # separate simple string elements from rest
            if isinstance(data[key], list) or isinstance(data[key], dict):
                list_structs.append(key)
            else:
                list_strings.append(key)
        if list_strings:
            list_strings.sort()
            output = output+'<ul>'
            for key in list_strings: # output simple string elements first
                output = output+to_html('ul', data[key], key)
            output = output+'</ul>'
        if list_structs:
            list_structs.sort()
            for key in list_structs: # output list and dict elements next
                output = output+to_html('body', data[key], key)
        return output
    elif isinstance (data, list):
        output = ''
        db_table = False
        if len(data) >= 1 and isinstance(data[0], dict):
            headers = data[0].keys()
            db_table = True
            test_len = len(headers)
            for i in data:
                if not isinstance(i, dict) or len(i) <> test_len:
                    db_table = False
                    break
        else:
            db_table = False
        if db_table:
            headers.sort()
            output = output+'<table><tr>'
            for i in headers:
                output = output+to_html('tr1', i)
            output = output+'</tr>'
            for i in data:
                output = output+'<tr>'
                for j in headers:
                    output = output+to_html('tr', i[j])
                output = output+'</tr>'
            return output+'</table>'
        else:
            if title:
                output = output+'<h2>'+title+'</h2>'
            output = output+'<ul>'
            for i in data:
                output = output+to_html('ul', i)
            return output+'</ul>'
    else:
        output = ''
        if container == 'body':
            if title:
                output = output+'<h3>'+title+'</h3>'
            return output+vstr(data)
        elif container == 'dl':
            if title:
                output = output+'<dt>'+title+'</dt>'
            return output+'<dd>'+vstr(data)+'</dd>'
        elif container == 'tr':
            output = output+'<td>'
            if title:
                output = output+'<strong>'+title+':</strong> '
            return output+vstr(data)+'</td>'
        elif container == 'tr1':
            output = output+'<th>'
            if title:
                output = output+'<strong>'+title+':</strong> '
            return output+vstr(data)+'</th>'
        elif container == 'ul':
            output = output+'<li>'
            if title:
                output = output+'<strong>'+title+':</strong> '
            return output+vstr(data)+'</li>'

# return valid string/unicode if not null, otherwise empty string
def vstr(s):
    if s:
        try:
            return unicode(s)
        except UnicodeDecodeError:
            return str(s)
    else:
        return u''

# remove any non ascii characters
def ascii(s): return "".join(i for i in s if ord(i)<128)

# add new data elements to the existing query of a URL
def add_to_query(url, data = {}):
    u = urlparse.urlsplit(url)
    qdict = dict(urlparse.parse_qsl(u.query))
    qdict.update(data)
    query = urllib.urlencode(qdict)
    url = urlparse.urlunsplit((u.scheme, u.netloc, u.path, query, u.fragment))
    return url

# get a date in standard format or None if the string cannot be parsed
def get_dt(date_string, date_format=DATE_FORMAT):
    try:
        dt = datetime.strptime(date_string, date_format)
        return dt.date()
    except:
        return None

# convert a date string from one format to another
def convert_dt(date_string, in_date_format=DATE_FORMAT, out_date_format=RFC822_DATE, on_error_original=True):
    if on_error_original and in_date_format == out_date_format:
        return date_string
    else:
        try:
            dt = datetime.strptime(date_string, in_date_format)
            dt = dt.replace(tzinfo=TZ)
            return dt.strftime(out_date_format)
        except:
            if on_error_original:
                return date_string
            else:
                return None

# increment a date by a number OR to the next available weekday if a string
# return the start and end dates of the permissible range
def inc_dt(date_string, date_format=DATE_FORMAT, increment=1):
    try:
        start_dt = datetime.strptime(date_string, date_format)
        if not increment:
            increment = 0
        if isinstance(increment, int) or increment.isdigit() or (increment.startswith('-') and increment[1:].isdigit()):
            day_inc = int(increment)
            if day_inc < 0:
                end_dt = start_dt
                start_dt = end_dt + timedelta(days=day_inc)
            else:
                end_dt = start_dt + timedelta(days=day_inc)
        elif increment == 'Year':
            start_dt = date(start_dt.year, 1, 1) # first day of this year
            end_dt = date(start_dt.year, 12, 31) # last day of this year
        elif increment == 'Month': 
            start_dt = date(start_dt.year, start_dt.month, 1) # first day of this month
            if start_dt.month == 12:
                end_dt = date(start_dt.year+1, 1, 1) # first day of next year
            else:
                end_dt = date(start_dt.year, start_dt.month+1, 1) # first day of next month
            end_dt = end_dt - timedelta(days=1)
        elif increment.startswith('-'): 
            wday = WEEKDAYS.get(increment[1:4].capitalize(), 0) # supplied is a week day defining beginning of week for a weekly list
            day_inc = wday - start_dt.weekday()
            if day_inc > 0: 
                day_inc = day_inc - 7
            start_dt = start_dt + timedelta(days=day_inc)
            end_dt = start_dt + timedelta(days=6)
        else:
            wday = WEEKDAYS.get(increment[0:3].capitalize(), 6) # supplied is a week day defining end of week for a weekly list
            day_inc = wday - start_dt.weekday()
            if day_inc < 0:
                day_inc = day_inc + 7
            end_dt = start_dt + timedelta(days=day_inc)
            start_dt = end_dt - timedelta(days=6)
        return start_dt.strftime(date_format), end_dt.strftime(date_format)
    except:
        return date_string, date_string

# test if a date is within a permissible range
def match_dt(date_to_test, date_from, date_to, date_format=DATE_FORMAT):
    try:
        test_dt = datetime.strptime(date_to_test, date_format)
        from_dt = datetime.strptime(date_from, date_format)
        to_dt = datetime.strptime(date_to, date_format)
        if test_dt <= to_dt and test_dt >= from_dt:
            return True
        else:
            return False
    except:
        return False

# test if a date is before or after a reference date
def test_dt(date_to_test, ref_date, date_format=DATE_FORMAT):
    try:
        test_dt = datetime.strptime(date_to_test, date_format)
        ref_dt = datetime.strptime(ref_date, date_format)
        if test_dt > ref_dt:
            return 1
        elif test_dt < ref_dt:
            return -1
        elif test_dt == ref_dt:
            return 0
        else:
            return None
    except:
        return None

# get a response from a url
def get_response(url, data = None, headers = None, accept = 'text/html', timeout = None):
    request = urllib2.Request(url)
    request.add_header('Accept', accept)
    if headers:
        for k, v in headers.items():
            request.add_header(k, v)
    """if multipart:
        opener = urllib2.build_opener(MultipartPostHandler)
        if timeout:
            response = opener.open(request, data, timeout)
        else:
            response = opener.open(request, data)
    else:
    """
    if timeout:
        response = urllib2.urlopen(request, data, timeout)
    else:
        response = urllib2.urlopen(request, data)
    return response

# get JSON data from a url
def json_get(url, data = None, timeout = None):
    try:
        sf = urllib2.urlopen(url, data, timeout)
        result = json.load(sf)  
    except:
        result = None; sf = None
    finally:
        if sf: sf.close()
    return result

# put a cookie in the jar
def set_cookie(cookie_jar, cname, cvalue, cdomain=None, cpath='/'):
    ck = cookielib.Cookie(version=0, name=str(cname), value=str(cvalue), domain=cdomain, path=cpath, 
            port=None, port_specified=False, domain_specified=False, expires=None, 
            domain_initial_dot=False, path_specified=True, secure=False, 
            discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
    cookie_jar.set_cookie(ck)

# gets a mechanize browser 
# NB the internal handler contains an lxml Html Element that can be used for DOM based methods
def get_browser(headers = None, factory = '', proxy = ''):
    if factory == 'robust':
        br = mechanize.Browser(factory=mechanize.RobustFactory()) # using BeautifulSoup 2 parser
    elif factory == 'xhtml':
        br = mechanize.Browser(factory=mechanize.DefaultFactory(i_want_broken_xhtml_support=True))
    else:
        br = mechanize.Browser()

    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)

    if proxy:
        # see http://www.publicproxyservers.com/proxy/list_uptime1.html
        br.set_proxies({"https": proxy, "http": proxy}) 
        # https tunnel via http proxy not working - bug fixed below but same problem?
        # http://sourceforge.net/mailarchive/forum.php?thread_name=alpine.DEB.2.00.0910062211230.8646%40alice&forum_name=wwwsearch-general
    br.set_handle_robots(False)
    if headers: 
        br.addheaders = headers.items() # Note addheaders is a data object (list of tuples) not a method
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    handler = EtreeHandler()
    br.add_handler(handler)
    return br, handler, cj

# selects a form and sets up its fields, action, method etc
# in the case of HTML select tags, the particular control used is always selected by name
# e.g. <select name="name"> <option value="value"> label </option> </select>
# however the option selected can be via the value attribute or by label (if the key starts with #)
# controls can be disabled by setting them to None
def setup_form(br, form = None, fields = None, action = None, method = None):
    if not form:
        br.select_form(nr=0)
    elif form.isdigit():
        br.select_form(nr=int(form))
    else:
        br.select_form(name=form)
    if action:
        current_action = br.form.action
        new_action = urlparse.urljoin(current_action, action)
        br.form.action = new_action
    if method and method.upper() == 'GET':
        br.form.method = method
    #print br.form
    if fields:
        add_controls = []
        for k, v in fields.items():
            try:
                if k.startswith('#'):
                    control = br.find_control(name=k[1:], nr=0) # find first control named k
                else:
                    control = br.find_control(name=k, nr=0) # find first control named k
            except mechanize._form.ControlNotFoundError as e: # if the control does not exist, we create a dummy hidden control to hold the value
                if k.startswith('#'):
                    add_controls.append(k[1:])
                else:
                    add_controls.append(k)
        if add_controls:
            for k in add_controls:
                br.form.new_control('hidden', k, {'value':''} )
            br.form.fixup()
        br.form.set_all_readonly(False)
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
        # NB throws except mechanize._form.ItemNotFoundError as e: if field select/check/radio option does not exist


# returns response after submitting a form via a mechanize browser
# submit parameter is a submit control name/number or an id (if it starts with a '#')
def submit_form(br, submit = None):
    if not submit:
        response = br.submit()
    elif submit.isdigit():
        response = br.submit(nr=int(submit))
    elif submit.startswith('#'):
        control = br.find_control(id=submit[1:], nr=0) # find first control with id submit
        if control.disabled: control.disabled = False
        response = br.submit(id=submit[1:], nr=0)
    else:
        control = br.find_control(name=submit, nr=0) # find first control named submit
        if control.disabled: control.disabled = False
        response = br.submit(name=submit, nr=0)
    return response

# returns a response after following a link via a mechanize browser
# link paramter is a link text value or number or a name (if it starts with a '!')
def process_link(br, link = None):
    if not link:
        response = br.follow_link()
    elif link.isdigit():
        response = br.follow_link(nr=int(link))
    elif link.startswith('!'):
        response = br.follow_link(name=str(link[1:]))
    else:
        response = br.follow_link(text=str(link))
    return response

# makes a direct url request via the browser supplying GET or POST parameters
def open_url(br, url, data = None, method = None):
    if data:
        for k, v in data.items():
            if v and isinstance(v, list):
                data[k] = v[0]
    else:
        return br.open(url)
    if method and method.upper() == 'GET':
        url = add_to_query(url, data)
        return br.open(url)
    else:
        return br.open(url, urllib.urlencode(data))

# return an HTML Element document from an html string
def get_doc(raw_html, url = ''):
    doc = lxml.html.fromstring(raw_html) # lxml fast parser
    if url:
        doc.make_links_absolute(url)
    return doc

# return an XML Element document from an xml string
def get_doc_xml(raw_xml):
    doc = etree.fromstring(raw_xml)
    return doc

# returns a child dictionary updated with any missing values specified in its parents
def dict_inherited(container, child_name, parent_key = 'parent'):
    child_dict = {}
    if child_name in container:
        child_dict.update(container[child_name])
        while child_dict.get(parent_key):
            next_dict = container[child_dict[parent_key]]
            del child_dict[parent_key]
            for k, v in next_dict.items():
                if not child_dict.get(k):
                    child_dict[k] = v
                elif child_dict[k] == '__None__':
                    child_dict[k] = None
                elif child_dict[k] == '__Clear__':
                    del child_dict[k]
    return child_dict 

# return the text value of an xpath or cssselect expression
def xpath_text(element, expression, thistype='xpath'):
    if element is None or not expression:
            return ''
    if thistype == 'css':
        value = element.cssselect(expression)
    else:
        value = element.xpath(expression)
    return text_content(value)
        
# returns trimmed html content with tags removed, entities converted
def text_content(value):
    if value is None:
        return ''
    if isinstance (value, list):
        if len(value) > 0:
            value = value[0]
        else:
            return ''
    if isinstance (value, lxml.html.HtmlElement):
        text = lxml.html.tostring(value)
        text = TAGS_REGEX.sub(' ', text) # replace any html tag content with spaces
        # use beautiful soup to convert html entities to unicode strings
        text = BeautifulSoup(text, convertEntities="html").contents[0].string
    else:
        text = vstr(value)
        text = TAGS_REGEX.sub(' ', text) # replace any html tag content with spaces
        # use beautiful soup to convert html entities to unicode strings
        text = BeautifulSoup(text, convertEntities="html").contents[0].string
    return trim(text)
    
# return text with internal white space compressed and external space stripped off
def trim(text):
    str_trim = GAPS_REGEX.sub(' ', text) # replace internal gaps with single spaces
    return str_trim.strip() # remove space at left and right

# return text with all internal white space removed
def no_space(text):
    return GAPS_REGEX.sub('', text) # remove internal gaps

#get selected table fields from database as list of maps
def get_table_vals(table = '', fields = '', where = '', orderetc = ''):
    if not fields:
        sql_fields = '*'
    elif isinstance(fields, list):
        sql_fields = ",".join(fields)
    elif isinstance(fields, dict):
        sql_fields = ''
        for k, v in fields.items():
            sql_fields = sql_fields+","+v+" as "+k
        sql_fields = sql_fields[1:]
    else:
        sql_fields = fields
    if where:
        where = " where "+where+' '+orderetc
    else:
        where = ' '+orderetc
    return scraperwiki.sqlite.select(sql_fields+" from "+table+where)

#convert list of maps resulting from SQL query to keyed dictionary (alternatively source is a table name)
def get_map(source, key, value=None):
    data = {}
    if not isinstance(source, list):
        source = get_table_vals(source)
    for map in source:
        if value:
            data[map[key]] = map[value]
        else:
            data[map[key]] = map
    return data

#convert list of maps resulting from SQL query to simple list (alternatively source is a table name)
def get_list(source, key):
    data = []
    if not isinstance(source, list):
        source = get_table_vals(source)
    for map in source:
        if map.get(key):
            data.append(map[key])
    return data 

# replace matching values with a substitution string in a single table column
# if no replace type is specified, it just prints the number of matching rows
def replace_vals(table, field, match, subst, replace_type= '', confirm = None):
    match = match.replace("'", "''")
    if replace_type.lower() == 'prefix':
        where = " where "+field+" like '"+match+"%'"
    elif replace_type.lower() == 'suffix':
        where = " where "+field+" like '%"+match+"'"
    else:
        where = " where "+field+" like '%"+match+"%'"
    subst = subst.replace("'", "''")
    if replace_type.lower() == 'prefix':
        where2 = " where "+field+" like '"+subst+"%'"
    elif replace_type.lower() == 'suffix':
        where2 = " where "+field+" like '%"+subst+"'"
    else:
        where2 = " where "+field+" like '%"+subst+"%'"
    sql = "select count(*) from "+table+where
    result1 = scraperwiki.sqlite.execute(sql)
    sql = "select count(*) from "+table+where2
    result2 = scraperwiki.sqlite.execute(sql)
    print "Found %d match strings and %d substitution strings before replacement" % (result1['data'][0][0], result2['data'][0][0])
    if confirm:
        sql = "update "+table+" set "+field+" = replace ("+field+", '"+match+"', '"+subst+"')"+where
        scraperwiki.sqlite.execute(sql)
        scraperwiki.sqlite.commit()
        sql = "select count(*) from "+table+where
        result1 = scraperwiki.sqlite.execute(sql)
        sql = "select count(*) from "+table+where2
        result2 = scraperwiki.sqlite.execute(sql)
        print "Found %d match strings and %d substitution strings after replacement" % (result1['data'][0][0], result2['data'][0][0])
    else:
        print "No substitutions made"

# list distinct URL prefixes in a field
def list_url_prefixes(table, field = 'url'):
    dump = get_list(table, field)
    prefixes = []
    for i in dump:
        parsed = urlparse.urlparse(i)
        prefix = 'http://' + parsed.netloc + parsed.path
        if prefix not in prefixes:
            prefixes.append(prefix)
    print "Distinct URL prefixes found in the '" + field + "' field of the " + table + " table:"
    for p in prefixes:
        print p

# set map values in a database table NB stores values as unicode strings
def set_table_vals(table, map, where = ''):
    clause = ''
    for k, v in map.items():
        if v:
            store = vstr(v).replace("'", "''")
            clause = clause+', '+k+"='"+store+"'"
        else:
            clause = clause+', '+k+"=''"
    clause = clause[2:]
    if where:
        where = " where "+where
    else:
        where = ''
    scraperwiki.sqlite.execute("update "+table+" set "+clause+where)
    scraperwiki.sqlite.commit()

# return a simple list of database table columns
def get_table_cols(table):
    result = scraperwiki.sqlite.execute("select * from "+table+" limit 1")
    return result['keys']

# return columns for a table - new version returns dict of columns with constraints as values
def get_table_columns(table='swdata'):
    schemas = scraperwiki.sqlite.select("sql from sqlite_master where type='table' and name='"+table+"'")
    columns = {}
    for schema in schemas:
        table_match = TABLE_REGEX.search(schema['sql'].replace('`', ''))
        if table_match:
            if table_match.group(1) == table:
                fields = table_match.group(2).split(',')
                for field in fields:
                    parts = field.split()
                    column = parts[0]
                    if len(parts) > 0:
                        columns[column] = ' '.join(parts[1:])
                    else:
                        columns[column] = ''
                break
    return columns

# get a create table schema
def create_table_schema(columns, table='swdata'):
    if not columns:
        return None
    elif isinstance(columns, dict):
        fields = []
        for k, v in columns.items():
            fields.append("`" + k + "` " + v)
        return "create table `" + table + "` (" + ', '.join(fields) + ')'
    elif isinstance(columns, list):
        return "create table `" + table + "` (" + ', '.join(columns) + ')'
    else:
        return None

# get a create index schema
def create_index_schemas(indices, table='swdata'):
    if indices and isinstance(indices, dict):
        results = []
        for k, v in indices.items():
            if v['unique']:
                create = 'create unique index '
            else:
                create = 'create index '
            results.append(create + v['name'] + " on " + table + " (" + k + ")")
        return results
    else:
        return []

# return column indexes for a table - returns dict of indexed columns with name and whether unique as values
def get_table_indices(table='swdata'):
    schemas = scraperwiki.sqlite.select("sql from sqlite_master where type='index' and tbl_name='"+table+"'")
    indices = {}
    for schema in schemas:
        index_match = INDEX_REGEX.search(schema['sql'].replace('`', ''))
        if index_match:
            if index_match.group(3) == table:
                unique = False
                if 'unique' in index_match.group(1).lower(): unique = True
                result = { 'name': index_match.group(2), 'unique': unique }
                indices[index_match.group(4)] = result
    return indices

# adds column(s) to a database table if found not to exist
def update_columns(table, columns, constraint = 'text'):
    existing = get_table_columns(table)
    if not constraint: constraint = ''
    if isinstance(columns, list):
        for col in columns:
            if not col in existing.keys():
                scraperwiki.sqlite.execute("alter table "+table+" add column "+col+" "+constraint)
                scraperwiki.sqlite.commit()
    elif isinstance(columns, str) or isinstance(columns, unicode):
        if not columns in existing.keys():
                scraperwiki.sqlite.execute("alter table "+table+" add column "+columns+" "+constraint)
                scraperwiki.sqlite.commit()

# renames a column by copying data to a temp table and renaming
# note if new _column is null or empty the column is deleted
def rename_column(table, column, new_column, temp_table = 'temp_copy'):
    scraperwiki.sqlite.execute("drop table if exists "+temp_table)
    columns = get_table_columns(table)
    #print columns
    if not column in columns.keys(): return
    old_fields = []; new_fields = []; # note array used because order is important
    for k, v in columns.items():
        if k == column:
            del columns[column]
            if new_column:
                columns[new_column] = v
                new_fields.append(new_column)
                old_fields.append(column)
        else:
            new_fields.append(k)
            old_fields.append(k)
    sql_new_schema = create_table_schema(columns, temp_table)
    #print sql_new_schema
    scraperwiki.sqlite.execute(sql_new_schema)
    index_schemas = get_table_indices(table) # save index details before rename
    new_index_schemas = {}
    for k, v in index_schemas.items(): # filter out non-applicable indices
        field_list = k.split(',')
        new_field_list = []
        for field in field_list:
            if field == column:
                if new_column: 
                    new_field_list.append(new_column)
            else:
                new_field_list.append(field)
        if new_field_list:
            new_index_schemas[', '.join(new_field_list)] = v
    #print new_index_schemas
    sql_index_schemas = create_index_schemas(new_index_schemas, table)
    #print sql_index_schemas
    insert = "insert into "+temp_table+" ("+", ".join(new_fields)+") select "+", ".join(old_fields)+" from "+table
    #print insert
    scraperwiki.sqlite.execute(insert)
    scraperwiki.sqlite.execute("drop table "+table) # deletes associated indexes
    scraperwiki.sqlite.execute("alter table " + temp_table + " rename to " + table)
    for sql in sql_index_schemas: # re-apply indices
        scraperwiki.sqlite.execute(sql)
    scraperwiki.sqlite.commit()

# query the database cache table
def cache_fetch(key):
    tstamp = time.time()
    #if isinstance(key, dict):
    #    key = hash(tuple(sorted(key.iteritems())))
    #elif isinstance(key, list):
    #    key = hash(tuple(key))
    #else:
    #    key = hash(key)
    ser_key = cPickle.dumps(key)
    try:
        sql = "value from cache where key = '" + ser_key.replace("'", "''") + "' and expires >= " + str(tstamp)
        results = scraperwiki.sqlite.select(sql)
    except:
        results = None
    if results:
        return cPickle.loads(str(results[0]['value']))
    else:
        return None

# clear the database cache table
def cache_clear():
    scraperwiki.sqlite.execute("delete from cache")
    scraperwiki.sqlite.commit()

# insert a value in the database cache table
# this is a slow operation, so we also take the opportunity to clear stale cache entries
def cache_put(key, value, age = DEFAULT_CACHE_AGE): # default expiry in 12 hours
    tstamp = time.time()
    try:
        scraperwiki.sqlite.execute("delete from cache where expires < "+str(tstamp))
        scraperwiki.sqlite.commit()
    except:
        pass
    if age and age > 0:
        expires = tstamp + age
    else:
        expires = tstamp + DEFAULT_CACHE_AGE
    #if isinstance(key, dict):
    #    key = hash(tuple(sorted(key.iteritems())))
    #elif isinstance(key, list):
    #    key = hash(tuple(key))
    #else:
    #    key = hash(key)
    store = { 'key': cPickle.dumps(key), 'value': cPickle.dumps(value), 'expires': expires }
    scraperwiki.sqlite.save(unique_keys=['key'], data=store, table_name='cache', verbose=0)

# get a processing slot
def get_slot(num_slots = NUM_SLOTS, slot_time = SLOT_TIME):
    timestamp = time.time()
    next_free_slot = slot_time
    for i in range(0, num_slots):
        slot_name = "slot" + str(i)
        slot_expires = scraperwiki.sqlite.get_var(slot_name, 0)
        if not slot_expires or slot_expires < timestamp:
            scraperwiki.sqlite.save_var(slot_name, timestamp + slot_time) # we have the lock, so just block it for the next slot_time secs
            return i, slot_time
        else:
            this_expires = slot_expires - timestamp
            if this_expires > 0 and this_expires < next_free_slot: 
                next_free_slot = this_expires
    return -1, next_free_slot # time until next available slot is free

# free up a processing slot
def free_slot(slot_num):
    slot_name = "slot" + str(slot_num)
    scraperwiki.sqlite.save_var(slot_name, 0)

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

# get an item from the local memory cache
# make copy, otherwise the cached version is mutable
def mcache_fetch(key):
    if isinstance(key, dict):
        keyhash = hash(tuple(sorted(key.iteritems())))
    elif isinstance(key, list):
        keyhash = hash(tuple(key))
    else:
        keyhash = hash(key)
    return copy.deepcopy(CACHE.get(keyhash))

#Given a list of dates as ISO8601 values, plot a histogram by month.
# output is a base64 encoded PNG string
def plotdates(dts, dpi=50, mindate = None, maxdate = None):
    if not dts: return None
    if not mindate: mindate=min(dts)
    if not maxdate: maxdate=max(dts)
    ym=mindate[:7]; 
    months=[]; counts=[]
    while ym<=maxdate[:7]:
        try:
            m = int(ym[5:7]); y = int(ym[:4])
        except:
            return None
        months.append(date(y, m, 1))
        counts.append(sum([1 if (dd[:7]==ym) else 0 for dd in dts]))
        m = m + 1
        if m > 12: y = y + 1; m = 1
        ym = str(y)+'-'+format(m, '02d')
    fig=pl.figure()
    ax=fig.add_subplot(111)
    ax.bar(months,counts,width=20.0)
    for xlabel_i in ax.get_xticklabels():
        xlabel_i.set_fontsize(20)
    for ylabel_i in ax.get_yticklabels():
        ylabel_i.set_fontsize(20) 
    ax.xaxis_date()
    fig.autofmt_xdate()
    #pl.draw()
    cout = StringIO()
    pl.savefig(cout, format="png", dpi=dpi)
    #print counts, months
    return base64.encodestring(cout.getvalue())

#default css for views
def base_css():
    css = """
body {
    margin: 10 20;
    padding: 0;
    background: #FFF;
    color: #191919;
    font-weight: normal;
    font-family: Helvetica, Arial, sans-serif;
    font-size: 75%;
}
    /*------------------- HEADERS -------------------*/
h1, h2, h3, h4, h5, h6 {
  margin: 6px 0;
  padding: 0;
  font-weight: normal;
  font-family: Helvetica, Arial, sans-serif;
}

h1 {font-size: 2em;}
h2 {font-size: 1.8em; line-height: 1.8em;}
h3 {font-size: 1.6em;}
h4 {font-size: 1.4em;}
h5 {font-size: 1.2em;}
h6 {font-size: 1em;}
/*------------------- HEADERS -------------------*/

/*------------------- TEXT/LINKS/IMG -------------------*/
p {margin: 10px 0 18px; padding: 10px;}

em {font-style:italic;}

strong {font-weight:bold;}

a:link, a:visited {color: #027AC6; text-decoration: none; outline:none;}

a:hover {color: #0062A0; text-decoration: underline;}

a:active, a.active {color: #5895be;}

img, a img {border: none;}

abbr,acronym {
    /*indicating to users that more info is available */
    border-bottom:1px dotted #000;
    cursor:help;
}

/*------------------- TEXT/LINKS/IMG -------------------*/

hr {
  margin: 0;
  padding: 0;
  border: none;
  height: 1px;
  background: #5294c1;
}

/*Change in format*/
ul, blockquote, quote, code, fieldset {margin: 16px 0;}

pre {  padding: 0; margin: 0; font-size: 1.3em; 
    white-space: -moz-pre-wrap !important; /* Mozilla, supported since 1999 */
    white-space: -pre-wrap; /* Opera 4 - 6 */
    white-space: -o-pre-wrap; /* Opera 7 */
    white-space: pre-wrap; /* CSS3 */
    word-wrap: break-word; /* IE 5.5+ */
}


/*------------------- LISTS -------------------*/

ul {margin-left:32px;}

ol,ul,dl {margin-left:32px;}
ol, ul, dl {margin-left:32px;}
ul, ol {margin: 8px 0 16px; padding: 0;}
ol li, ul li {margin: 7px 0 7px 32px;}
ul ul li {margin-left: 10px;}

ul li {padding: 0 0 4px 6px; list-style: disc outside;}
ul li ul li {list-style: circle outside;}

ol li {padding: 0 0 5px; list-style: decimal outside;}

dl {margin: 8px 0 16px 24px;}
dl dt {font-weight:bold;}
dl dd {margin: 0 0 8px 20px;}

/*------------------- LISTS -------------------*/


/*------------------- FORMS -------------------*/
input {
  font: 1em/1.2em Verdana, sans-serif;
  color: #191919;
}
textarea, select {
  font: 1em/1.2em Verdana, sans-serif;
  color: #191919;
}
textarea {resize:none;}
/*------------------- FORMS -------------------*/


/*------------------- TABLES -------------------*/

table {margin: 16px 0; width: 90%; font-size: 0.92em; border-collapse:collapse; }

th {
  border:1px solid #000; 
  background-color: #d3e7f4;
  font-weight: bold;
}

td {padding: 4px 6px; margin: 0; border:1px solid #000;}

caption {margin-bottom:8px; text-align:center;}

/*------------------- TABLES -------------------*/
    """
    return css

"""
class MinimalSoupHandler(mechanize.BaseHandler):
    def http_response(self, request, response):
        if not hasattr(response, "seek"):
            response = mechanize.response_seek_wrapper(response)
        # only use if response is html
        if response.info().dict.has_key('content-type') and ('html' in response.info().dict['content-type']):
            soup = MinimalSoup (response.get_data())
            response.set_data(soup.prettify())
        return response
"""

class BeautifulSoupHandler(mechanize.BaseHandler):
    def http_response(self, request, response):
        if not hasattr(response, "seek"):
            response = mechanize.response_seek_wrapper(response)
        # only use if response is html
        if response.info().dict.has_key('content-type') and ('html' in response.info().dict['content-type']):
            #soup = BeautifulSoup (response.get_data())
            self.element = lxml.html.soupparser.fromstring(response.get_data())
            #response.set_data(soup.prettify())
            response.set_data(etree.tostring(self.element, pretty_print=True, method="html"))
        return response

class EtreeHandler(mechanize.BaseHandler):
    def http_response(self, request, response):
        if not hasattr(response, "seek"):
            response = mechanize.response_seek_wrapper(response)
        # only use if response is html
        if response.info().dict.has_key('content-type') and ('html' in response.info().dict['content-type']):
            #clean_up = lxml.html.clean.clean_html(response.get_data()) # not tested yet ? put in new EtreeCleanHandler
            #self.element = etree.HTML(response.get_data())
            tag_soup = response.get_data()
            try:
                self.element = lxml.html.fromstring(tag_soup)
                ignore = etree.tostring(self.element, encoding=unicode) # check the unicode entity conversion has worked
            except (UnicodeDecodeError, etree.XMLSyntaxError):
                self.element = lxml.html.soupparser.fromstring(tag_soup) # fall back to beautiful soup if there is an error    
            response.set_data(etree.tostring(self.element, pretty_print=True, method="html"))      
        return response


# a library of utility functions

import scraperwiki
import lxml.html
import lxml.html.soupparser
from lxml import etree
import re
from datetime import date
import urllib, urllib2, urlparse
from datetime import datetime
from datetime import timedelta
import time
import json
import mechanize
from pytz import timezone
from BeautifulSoup import BeautifulSoup
#from BeautifulSoup import MinimalSoup
from cStringIO import StringIO
from csv import reader
import random
import cookielib
import matplotlib.pyplot as pl
import base64
import sys
import cPickle

DATE_FORMAT = "%d/%m/%Y"
RFC822_DATE = "%a, %d %b %Y %H:%M:%S %z"
ISO8601_DATE = "%Y-%m-%d"
RFC3339_DATE = "%Y-%m-%dT%H:%M:%SZ"
TABLE_REGEX = re.compile(r'create\s+table\s+(\S+)\s*\(([^\)]+)\)', re.I) # ignore case
INDEX_REGEX = re.compile(r'(create\s+(?:unique\s+)?index)\s+(\S+)\s+on\s+(\S+)\s+\(([^\)]+)\)', re.I) # ignore case
TAGS_REGEX = re.compile(r'<[^<]+?>')
GAPS_REGEX = re.compile(r'\s+', re.U) # unicode spaces include html &nbsp;
TZ = timezone('Europe/London')
AUTHOR = 'AS' # for Atom feeds 
WEEKDAYS = { 'Mon': 0, 'Tue': 1, 'Wed': 2, 'Thu': 3, 'Fri': 4, 'Sat': 5, 'Sun': 6 }
DEFAULT_CACHE_AGE = 43200 # default cache expiry in secs = 12 hours
SLOT_TIME = 60 # max processing time for processing slots = secs
NUM_SLOTS = 2 # number of processes
CACHE = {} # local memory cache
    
all_rss_fields = { # default map from data fields to RSS, to be overridden
        'title': 'title',
        'description': 'description',
        'link': 'link',
        'items': 'items',
        'item': 'item',
        'sub_item': {
            'title': 'title',
            'description': 'description',
            'link': 'link',
            'guid': 'id',
            },
        'geo_item': {
            'point': 'point'
            }
        }

all_atom_fields = { # default map from data fields to ATOM, to be overridden
        'title': 'title',
        'subtitle': 'description',
        'link': 'link',
        'id': 'id',
        'items': 'items',
        'item': 'item',
        'sub_item': {
            'title': 'title',
            'content': 'description',
            'link': 'link',
            'id': 'id',
            },
        'geo_item': {
            'point': 'point'
            }
        }

# import a full CSV file into a table or if match is set, update the one row where the key values match
def import_csv(csv_file_url, table_name, keys, match = None): 
    if not keys or not isinstance(keys, list):
        return 0
    if not isinstance(keys, list):
        keys = [ keys ]
    if match and not isinstance(match, list):
        match = [ match ]
    # NB no-cache headers do not work
    #headers =  { 'Cache-Control': 'no-cache',  'Pragma': 'no-cache',  }
    # instead add random url string to short circuit cache
    nocache = "%04x" % random.randint(0, 65535)
    url = add_to_query(csv_file_url, { 'nocache': nocache })
    csv_text = scraperwiki.scrape(url)
    #response = get_response(csv_file_url, None, headers, 'text/csv')
    #csv_text = response.read()
    lines = reader(StringIO(csv_text))
    headings = lines.next()
    add_list = []
    if match:
        matchup = dict(zip(keys, match))
    else:
        matchup = None
    for line in lines:
        values = dict(zip(headings, line)) 
        if matchup:
            use_values = True
            for key in keys:
                if matchup[key] != values[key]:
                    use_values = False
                    break # exit the keys loop, match condition failed
            if use_values: # all keys matched
                add_list.append(values)
                break # key matched so no need to continue with lines loop
        else:
            add_list.append(values)
    if add_list: 
        if not matchup:
            scraperwiki.sqlite.execute("drop table if exists " + table_name)
            scraperwiki.sqlite.commit()
        scraperwiki.sqlite.save(keys, add_list, table_name, verbose=0) # one save operation (= list of dics), not many
    return len(add_list)

# set content type for JSON, XML or RSS formats
def set_content(fmt = 'xml'): 
    if fmt == 'json':
        scraperwiki.utils.httpresponseheader("Content-Type", "application/json")
    elif fmt == 'jsonp':
        scraperwiki.utils.httpresponseheader("Content-Type", "application/javascript")
    elif fmt == 'rss':
        scraperwiki.utils.httpresponseheader("Content-Type", "application/rss+xml")
    elif fmt == 'atom':
        scraperwiki.utils.httpresponseheader("Content-Type", "application/atom+xml")
    elif fmt == 'html':
        scraperwiki.utils.httpresponseheader("Content-Type", "text/html")
    elif fmt == 'csv':
        scraperwiki.utils.httpresponseheader("Content-Type", "text/csv")   
    elif fmt == 'tsv':
        scraperwiki.utils.httpresponseheader("Content-Type", "text/tab-separated-values")   
    else: # XML always the default - see data_output()
        scraperwiki.utils.httpresponseheader("Content-Type", "text/xml")

# redirect to another web page
def redirect(url, code=303): 
    if code <= 307 and code >= 300:
        scraperwiki.utils.httpresponseheader("Location", url)
        scraperwiki.utils.httpstatuscode(code)
    else:
        scraperwiki.utils.httpresponseheader("Content-Type", "text/html")
        print """
        <html>
        <head>
        <meta http-equiv="Refresh" content="0; url=%s" />
        </head>
        <body>
        <p>Please follow this link: <a href="%s">%s</a>.</p>
        </body>
        </html>""" % (url, url, url)
    sys.exit()

# output a data dict in JSON, XML or RSS formats
def data_output(data, fmt = 'xml', options = None):
    if fmt == 'object':
        return data
    elif fmt == 'json':
        if options: # if this is set it's really JSONP
            return options + '(' + json.dumps(data, indent=4) + ');'
        else:
            return json.dumps(data, indent=4)
    elif fmt == 'jsonp':
        if not options: options = 'callback'
        return options + '(' + json.dumps(data, indent=4) + ');'
    elif fmt == 'rss':
        root = to_rss(data, options, ISO8601_DATE)
        root.addprevious(etree.PI('xml-stylesheet', 'type="text/xsl" title="XSL stylesheet" href="http://www.speakman.org.uk/rss.xsl"'))
        return etree.tostring(root.getroottree(), encoding="utf-8", xml_declaration=True, pretty_print=True)
    elif fmt == 'atom': 
        root = to_atom(data, options, ISO8601_DATE) 
        return etree.tostring(root, encoding="utf-8", xml_declaration=True, pretty_print=True)
    elif fmt == 'html':
        if not options:
            options = 'data'
        html_string = to_html('', data, options)
        root = lxml.html.fromstring(html_string)
        return etree.tostring(root, pretty_print=True, method="html")
        #return etree.tostring(root, encoding="utf-8", xml_declaration=True, pretty_print=True)
    else: # XML always the default - see set_content()
        if not options:
            options = 'root'
        root = to_xml(options, data)
        return etree.tostring(root, encoding="utf-8", xml_declaration=True, pretty_print=True)
    
# use data to fill out an RSS 2.0 feed (with option for GeoRSS)
def to_rss(data, map, in_date_fmt = ISO8601_DATE):
    GEORSS_NAMESPACE = "http://www.georss.org/georss"
    GEORSS = "{%s}" % GEORSS_NAMESPACE
    NSMAP = { 'georss': GEORSS_NAMESPACE }
    feed_type = 'rss'
    for i in data[map['items']][map['item']]:
        for k, v in map['geo_item'].items():
            if v in i:
                feed_type = 'georss'
                break
    if feed_type == 'georss':
        root = etree.Element('rss', nsmap=NSMAP)
    else:
        root = etree.Element('rss')
    root.set("version", "2.0")
    branch = etree.SubElement(root, "channel")
    for k, v in map.items():
        if k <> 'item' and  k <> 'items' and k <> 'geo_item' and k <> 'sub_item' and v in data:
            twig = etree.SubElement(branch, k)
            twig.text = vstr(data[v])
    pubdate = datetime.now(TZ).strftime(RFC822_DATE)
    twig = etree.SubElement(branch, 'pubDate')
    twig.text = vstr(pubdate)
    for i in data[map['items']][map['item']]:
        twig = etree.SubElement(branch, "item")
        no_date = True
        for k, v in map['sub_item'].items():
            if v in i:
                leaf = etree.SubElement(twig, k)
                if k == 'pubDate':
                    no_date = False
                    if in_date_fmt ==  ISO8601_DATE:
                        leaf.text = convert_dt(vstr(i[v])+'T12:00:00Z', RFC3339_DATE, RFC822_DATE) #  make time noon
                    else:
                        leaf.text = convert_dt(vstr(i[v]), in_date_fmt, RFC822_DATE) 
                else:
                    leaf.text = vstr(i[v])
                if k == 'guid':
                    leaf.set("isPermaLink", "false")
        if no_date:
            leaf = etree.SubElement(twig, 'pubDate')
            leaf.text = vstr(pubdate)
        for k, v in map['geo_item'].items():
            if v in i:
                leaf = etree.SubElement(twig, GEORSS+k)
                leaf.text = vstr(i[v])
    return root

# use data to fill out an ATOM feed (with option for GeoRSS)
def to_atom(data, map, in_date_fmt = ISO8601_DATE):
    GEORSS_NAMESPACE = "http://www.georss.org/georss"
    ATOM_NAMESPACE = "http://www.w3.org/2005/Atom"
    GEORSS = "{%s}" % GEORSS_NAMESPACE
    GEONSMAP = { None: ATOM_NAMESPACE, 'georss': GEORSS_NAMESPACE }
    NSMAP = { None: ATOM_NAMESPACE }
    feed_type = 'atom'
    for i in data[map['items']][map['item']]:
        for k, v in map['geo_item'].items():
            if v in i:
                feed_type = 'georss'
                break
    if feed_type == 'georss':
        root = etree.Element('feed', nsmap=GEONSMAP)
    else:
        root = etree.Element('feed', nsmap=NSMAP)
    for k, v in map.items():
        if k <> 'item' and  k <> 'items' and k <> 'geo_item' and k <> 'sub_item' and v in data:
            branch = etree.SubElement(root, k)
            if k == 'link':
                branch.set("href", vstr(data[v]))
                branch.set("rel", "self")
            else:
                branch.text = vstr(data[v])
    pubdate = datetime.now(TZ).strftime(RFC3339_DATE)
    branch = etree.SubElement(root, 'updated')
    branch.text = vstr(pubdate)
    for i in data[map['items']][map['item']]:
        branch = etree.SubElement(root, "entry")
        no_date = True
        for k, v in map['sub_item'].items():
            if v in i:
                leaf = etree.SubElement(branch, k)
                if k == 'link':
                    leaf.set("href", vstr(i[v]))
                elif k == 'published' or k == 'updated':
                    no_date = False
                    if in_date_fmt ==  ISO8601_DATE:
                        leaf.text = convert_dt(vstr(i[v])+'T12:00:00Z', RFC3339_DATE, RFC3339_DATE) #  make time noon
                    else:
                        leaf.text = convert_dt(vstr(i[v]), in_date_fmt, RFC3339_DATE) 
                else:
                    leaf.text = vstr(i[v])
                if k == 'summary' or k == 'content':
                    leaf.set("type", "html")
        if no_date:
            leaf = etree.SubElement(branch, 'updated')
            leaf.text = vstr(pubdate)
        leaf = etree.SubElement(branch, 'author')
        #end = etree.SubElement(leaf, 'name')
        #end.text = vstr(AUTHOR)
        for k, v in map['geo_item'].items():
            if v in i:
                leaf = etree.SubElement(branch, GEORSS+k)
                leaf.text = vstr(i[v])
    return root

# unserialize an XML document to a dictionary (containing dicts, strings or lists)
def from_xml(element):
    if len(element) > 0:
        outdict = {}
        if element.get('type') == 'list':
            value = []
            for i in element:
                value.append(from_xml(i))
            outdict[element[0].tag] = value
        else:
            for i in element:
                outdict[i.tag] = from_xml(i)
        return outdict
    else:
        return element.text

# serialise the contents of a dictionary as simple XML
def to_xml(element_name, data):
    element_name = re.sub('\s', '_', element_name) # replace any spaces in the tag name with underscores
    element = etree.Element(element_name)
    if isinstance (data, dict):
        keys = data.keys()
        keys.sort() # output is in alphab order 
        for key in keys: # output simple string elements first
            if not isinstance(data[key], list) and not isinstance(data[key], dict):
                element.append(to_xml(key, data[key]))
        for key in keys: # any lists and dicts come afterwards
            if isinstance(data[key], list): # lists stay in original order
                element.set('type', 'list')
                for i in data[key]:
                    element.append(to_xml(key, i))
            elif isinstance(data[key], dict):
                element.append(to_xml(key, data[key]))
    else:
        element.text = vstr(data)
    return element

# serialise the contents of a dictionary as simple HTML (NB string output)
def to_html(container, data, title = ''):
    if title:
        title = re.sub('_', ' ', title) # replace any underscores with spaces
        title = title.title()
    if not container:
        output = "<html><head>"
        if title:
            output = output+"<title>"+title+"</title>"
        output = output+'</head><body>'
        if title:
            output = output+"<h1>"+title+"</h1>"
        output = output+to_html('body', data)
        return output+"</body></html>"
    elif isinstance (data, dict):
        output = ''
        if title:
            output = output+'<h2>'+title+'</h2>'
        list_strings = []
        list_structs = []
        keys = data.keys()
        for key in keys: # separate simple string elements from rest
            if isinstance(data[key], list) or isinstance(data[key], dict):
                list_structs.append(key)
            else:
                list_strings.append(key)
        if list_strings:
            list_strings.sort()
            output = output+'<ul>'
            for key in list_strings: # output simple string elements first
                output = output+to_html('ul', data[key], key)
            output = output+'</ul>'
        if list_structs:
            list_structs.sort()
            for key in list_structs: # output list and dict elements next
                output = output+to_html('body', data[key], key)
        return output
    elif isinstance (data, list):
        output = ''
        db_table = False
        if len(data) >= 1 and isinstance(data[0], dict):
            headers = data[0].keys()
            db_table = True
            test_len = len(headers)
            for i in data:
                if not isinstance(i, dict) or len(i) <> test_len:
                    db_table = False
                    break
        else:
            db_table = False
        if db_table:
            headers.sort()
            output = output+'<table><tr>'
            for i in headers:
                output = output+to_html('tr1', i)
            output = output+'</tr>'
            for i in data:
                output = output+'<tr>'
                for j in headers:
                    output = output+to_html('tr', i[j])
                output = output+'</tr>'
            return output+'</table>'
        else:
            if title:
                output = output+'<h2>'+title+'</h2>'
            output = output+'<ul>'
            for i in data:
                output = output+to_html('ul', i)
            return output+'</ul>'
    else:
        output = ''
        if container == 'body':
            if title:
                output = output+'<h3>'+title+'</h3>'
            return output+vstr(data)
        elif container == 'dl':
            if title:
                output = output+'<dt>'+title+'</dt>'
            return output+'<dd>'+vstr(data)+'</dd>'
        elif container == 'tr':
            output = output+'<td>'
            if title:
                output = output+'<strong>'+title+':</strong> '
            return output+vstr(data)+'</td>'
        elif container == 'tr1':
            output = output+'<th>'
            if title:
                output = output+'<strong>'+title+':</strong> '
            return output+vstr(data)+'</th>'
        elif container == 'ul':
            output = output+'<li>'
            if title:
                output = output+'<strong>'+title+':</strong> '
            return output+vstr(data)+'</li>'

# return valid string/unicode if not null, otherwise empty string
def vstr(s):
    if s:
        try:
            return unicode(s)
        except UnicodeDecodeError:
            return str(s)
    else:
        return u''

# remove any non ascii characters
def ascii(s): return "".join(i for i in s if ord(i)<128)

# add new data elements to the existing query of a URL
def add_to_query(url, data = {}):
    u = urlparse.urlsplit(url)
    qdict = dict(urlparse.parse_qsl(u.query))
    qdict.update(data)
    query = urllib.urlencode(qdict)
    url = urlparse.urlunsplit((u.scheme, u.netloc, u.path, query, u.fragment))
    return url

# get a date in standard format or None if the string cannot be parsed
def get_dt(date_string, date_format=DATE_FORMAT):
    try:
        dt = datetime.strptime(date_string, date_format)
        return dt.date()
    except:
        return None

# convert a date string from one format to another
def convert_dt(date_string, in_date_format=DATE_FORMAT, out_date_format=RFC822_DATE, on_error_original=True):
    if on_error_original and in_date_format == out_date_format:
        return date_string
    else:
        try:
            dt = datetime.strptime(date_string, in_date_format)
            dt = dt.replace(tzinfo=TZ)
            return dt.strftime(out_date_format)
        except:
            if on_error_original:
                return date_string
            else:
                return None

# increment a date by a number OR to the next available weekday if a string
# return the start and end dates of the permissible range
def inc_dt(date_string, date_format=DATE_FORMAT, increment=1):
    try:
        start_dt = datetime.strptime(date_string, date_format)
        if not increment:
            increment = 0
        if isinstance(increment, int) or increment.isdigit() or (increment.startswith('-') and increment[1:].isdigit()):
            day_inc = int(increment)
            if day_inc < 0:
                end_dt = start_dt
                start_dt = end_dt + timedelta(days=day_inc)
            else:
                end_dt = start_dt + timedelta(days=day_inc)
        elif increment == 'Year':
            start_dt = date(start_dt.year, 1, 1) # first day of this year
            end_dt = date(start_dt.year, 12, 31) # last day of this year
        elif increment == 'Month': 
            start_dt = date(start_dt.year, start_dt.month, 1) # first day of this month
            if start_dt.month == 12:
                end_dt = date(start_dt.year+1, 1, 1) # first day of next year
            else:
                end_dt = date(start_dt.year, start_dt.month+1, 1) # first day of next month
            end_dt = end_dt - timedelta(days=1)
        elif increment.startswith('-'): 
            wday = WEEKDAYS.get(increment[1:4].capitalize(), 0) # supplied is a week day defining beginning of week for a weekly list
            day_inc = wday - start_dt.weekday()
            if day_inc > 0: 
                day_inc = day_inc - 7
            start_dt = start_dt + timedelta(days=day_inc)
            end_dt = start_dt + timedelta(days=6)
        else:
            wday = WEEKDAYS.get(increment[0:3].capitalize(), 6) # supplied is a week day defining end of week for a weekly list
            day_inc = wday - start_dt.weekday()
            if day_inc < 0:
                day_inc = day_inc + 7
            end_dt = start_dt + timedelta(days=day_inc)
            start_dt = end_dt - timedelta(days=6)
        return start_dt.strftime(date_format), end_dt.strftime(date_format)
    except:
        return date_string, date_string

# test if a date is within a permissible range
def match_dt(date_to_test, date_from, date_to, date_format=DATE_FORMAT):
    try:
        test_dt = datetime.strptime(date_to_test, date_format)
        from_dt = datetime.strptime(date_from, date_format)
        to_dt = datetime.strptime(date_to, date_format)
        if test_dt <= to_dt and test_dt >= from_dt:
            return True
        else:
            return False
    except:
        return False

# test if a date is before or after a reference date
def test_dt(date_to_test, ref_date, date_format=DATE_FORMAT):
    try:
        test_dt = datetime.strptime(date_to_test, date_format)
        ref_dt = datetime.strptime(ref_date, date_format)
        if test_dt > ref_dt:
            return 1
        elif test_dt < ref_dt:
            return -1
        elif test_dt == ref_dt:
            return 0
        else:
            return None
    except:
        return None

# get a response from a url
def get_response(url, data = None, headers = None, accept = 'text/html', timeout = None):
    request = urllib2.Request(url)
    request.add_header('Accept', accept)
    if headers:
        for k, v in headers.items():
            request.add_header(k, v)
    """if multipart:
        opener = urllib2.build_opener(MultipartPostHandler)
        if timeout:
            response = opener.open(request, data, timeout)
        else:
            response = opener.open(request, data)
    else:
    """
    if timeout:
        response = urllib2.urlopen(request, data, timeout)
    else:
        response = urllib2.urlopen(request, data)
    return response

# get JSON data from a url
def json_get(url, data = None, timeout = None):
    try:
        sf = urllib2.urlopen(url, data, timeout)
        result = json.load(sf)  
    except:
        result = None; sf = None
    finally:
        if sf: sf.close()
    return result

# put a cookie in the jar
def set_cookie(cookie_jar, cname, cvalue, cdomain=None, cpath='/'):
    ck = cookielib.Cookie(version=0, name=str(cname), value=str(cvalue), domain=cdomain, path=cpath, 
            port=None, port_specified=False, domain_specified=False, expires=None, 
            domain_initial_dot=False, path_specified=True, secure=False, 
            discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
    cookie_jar.set_cookie(ck)

# gets a mechanize browser 
# NB the internal handler contains an lxml Html Element that can be used for DOM based methods
def get_browser(headers = None, factory = '', proxy = ''):
    if factory == 'robust':
        br = mechanize.Browser(factory=mechanize.RobustFactory()) # using BeautifulSoup 2 parser
    elif factory == 'xhtml':
        br = mechanize.Browser(factory=mechanize.DefaultFactory(i_want_broken_xhtml_support=True))
    else:
        br = mechanize.Browser()

    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)

    if proxy:
        # see http://www.publicproxyservers.com/proxy/list_uptime1.html
        br.set_proxies({"https": proxy, "http": proxy}) 
        # https tunnel via http proxy not working - bug fixed below but same problem?
        # http://sourceforge.net/mailarchive/forum.php?thread_name=alpine.DEB.2.00.0910062211230.8646%40alice&forum_name=wwwsearch-general
    br.set_handle_robots(False)
    if headers: 
        br.addheaders = headers.items() # Note addheaders is a data object (list of tuples) not a method
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    handler = EtreeHandler()
    br.add_handler(handler)
    return br, handler, cj

# selects a form and sets up its fields, action, method etc
# in the case of HTML select tags, the particular control used is always selected by name
# e.g. <select name="name"> <option value="value"> label </option> </select>
# however the option selected can be via the value attribute or by label (if the key starts with #)
# controls can be disabled by setting them to None
def setup_form(br, form = None, fields = None, action = None, method = None):
    if not form:
        br.select_form(nr=0)
    elif form.isdigit():
        br.select_form(nr=int(form))
    else:
        br.select_form(name=form)
    if action:
        current_action = br.form.action
        new_action = urlparse.urljoin(current_action, action)
        br.form.action = new_action
    if method and method.upper() == 'GET':
        br.form.method = method
    #print br.form
    if fields:
        add_controls = []
        for k, v in fields.items():
            try:
                if k.startswith('#'):
                    control = br.find_control(name=k[1:], nr=0) # find first control named k
                else:
                    control = br.find_control(name=k, nr=0) # find first control named k
            except mechanize._form.ControlNotFoundError as e: # if the control does not exist, we create a dummy hidden control to hold the value
                if k.startswith('#'):
                    add_controls.append(k[1:])
                else:
                    add_controls.append(k)
        if add_controls:
            for k in add_controls:
                br.form.new_control('hidden', k, {'value':''} )
            br.form.fixup()
        br.form.set_all_readonly(False)
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
        # NB throws except mechanize._form.ItemNotFoundError as e: if field select/check/radio option does not exist


# returns response after submitting a form via a mechanize browser
# submit parameter is a submit control name/number or an id (if it starts with a '#')
def submit_form(br, submit = None):
    if not submit:
        response = br.submit()
    elif submit.isdigit():
        response = br.submit(nr=int(submit))
    elif submit.startswith('#'):
        control = br.find_control(id=submit[1:], nr=0) # find first control with id submit
        if control.disabled: control.disabled = False
        response = br.submit(id=submit[1:], nr=0)
    else:
        control = br.find_control(name=submit, nr=0) # find first control named submit
        if control.disabled: control.disabled = False
        response = br.submit(name=submit, nr=0)
    return response

# returns a response after following a link via a mechanize browser
# link paramter is a link text value or number or a name (if it starts with a '!')
def process_link(br, link = None):
    if not link:
        response = br.follow_link()
    elif link.isdigit():
        response = br.follow_link(nr=int(link))
    elif link.startswith('!'):
        response = br.follow_link(name=str(link[1:]))
    else:
        response = br.follow_link(text=str(link))
    return response

# makes a direct url request via the browser supplying GET or POST parameters
def open_url(br, url, data = None, method = None):
    if data:
        for k, v in data.items():
            if v and isinstance(v, list):
                data[k] = v[0]
    else:
        return br.open(url)
    if method and method.upper() == 'GET':
        url = add_to_query(url, data)
        return br.open(url)
    else:
        return br.open(url, urllib.urlencode(data))

# return an HTML Element document from an html string
def get_doc(raw_html, url = ''):
    doc = lxml.html.fromstring(raw_html) # lxml fast parser
    if url:
        doc.make_links_absolute(url)
    return doc

# return an XML Element document from an xml string
def get_doc_xml(raw_xml):
    doc = etree.fromstring(raw_xml)
    return doc

# returns a child dictionary updated with any missing values specified in its parents
def dict_inherited(container, child_name, parent_key = 'parent'):
    child_dict = {}
    if child_name in container:
        child_dict.update(container[child_name])
        while child_dict.get(parent_key):
            next_dict = container[child_dict[parent_key]]
            del child_dict[parent_key]
            for k, v in next_dict.items():
                if not child_dict.get(k):
                    child_dict[k] = v
                elif child_dict[k] == '__None__':
                    child_dict[k] = None
                elif child_dict[k] == '__Clear__':
                    del child_dict[k]
    return child_dict 

# return the text value of an xpath or cssselect expression
def xpath_text(element, expression, thistype='xpath'):
    if element is None or not expression:
            return ''
    if thistype == 'css':
        value = element.cssselect(expression)
    else:
        value = element.xpath(expression)
    return text_content(value)
        
# returns trimmed html content with tags removed, entities converted
def text_content(value):
    if value is None:
        return ''
    if isinstance (value, list):
        if len(value) > 0:
            value = value[0]
        else:
            return ''
    if isinstance (value, lxml.html.HtmlElement):
        text = lxml.html.tostring(value)
        text = TAGS_REGEX.sub(' ', text) # replace any html tag content with spaces
        # use beautiful soup to convert html entities to unicode strings
        text = BeautifulSoup(text, convertEntities="html").contents[0].string
    else:
        text = vstr(value)
        text = TAGS_REGEX.sub(' ', text) # replace any html tag content with spaces
        # use beautiful soup to convert html entities to unicode strings
        text = BeautifulSoup(text, convertEntities="html").contents[0].string
    return trim(text)
    
# return text with internal white space compressed and external space stripped off
def trim(text):
    str_trim = GAPS_REGEX.sub(' ', text) # replace internal gaps with single spaces
    return str_trim.strip() # remove space at left and right

# return text with all internal white space removed
def no_space(text):
    return GAPS_REGEX.sub('', text) # remove internal gaps

#get selected table fields from database as list of maps
def get_table_vals(table = '', fields = '', where = '', orderetc = ''):
    if not fields:
        sql_fields = '*'
    elif isinstance(fields, list):
        sql_fields = ",".join(fields)
    elif isinstance(fields, dict):
        sql_fields = ''
        for k, v in fields.items():
            sql_fields = sql_fields+","+v+" as "+k
        sql_fields = sql_fields[1:]
    else:
        sql_fields = fields
    if where:
        where = " where "+where+' '+orderetc
    else:
        where = ' '+orderetc
    return scraperwiki.sqlite.select(sql_fields+" from "+table+where)

#convert list of maps resulting from SQL query to keyed dictionary (alternatively source is a table name)
def get_map(source, key, value=None):
    data = {}
    if not isinstance(source, list):
        source = get_table_vals(source)
    for map in source:
        if value:
            data[map[key]] = map[value]
        else:
            data[map[key]] = map
    return data

#convert list of maps resulting from SQL query to simple list (alternatively source is a table name)
def get_list(source, key):
    data = []
    if not isinstance(source, list):
        source = get_table_vals(source)
    for map in source:
        if map.get(key):
            data.append(map[key])
    return data 

# replace matching values with a substitution string in a single table column
# if no replace type is specified, it just prints the number of matching rows
def replace_vals(table, field, match, subst, replace_type= '', confirm = None):
    match = match.replace("'", "''")
    if replace_type.lower() == 'prefix':
        where = " where "+field+" like '"+match+"%'"
    elif replace_type.lower() == 'suffix':
        where = " where "+field+" like '%"+match+"'"
    else:
        where = " where "+field+" like '%"+match+"%'"
    subst = subst.replace("'", "''")
    if replace_type.lower() == 'prefix':
        where2 = " where "+field+" like '"+subst+"%'"
    elif replace_type.lower() == 'suffix':
        where2 = " where "+field+" like '%"+subst+"'"
    else:
        where2 = " where "+field+" like '%"+subst+"%'"
    sql = "select count(*) from "+table+where
    result1 = scraperwiki.sqlite.execute(sql)
    sql = "select count(*) from "+table+where2
    result2 = scraperwiki.sqlite.execute(sql)
    print "Found %d match strings and %d substitution strings before replacement" % (result1['data'][0][0], result2['data'][0][0])
    if confirm:
        sql = "update "+table+" set "+field+" = replace ("+field+", '"+match+"', '"+subst+"')"+where
        scraperwiki.sqlite.execute(sql)
        scraperwiki.sqlite.commit()
        sql = "select count(*) from "+table+where
        result1 = scraperwiki.sqlite.execute(sql)
        sql = "select count(*) from "+table+where2
        result2 = scraperwiki.sqlite.execute(sql)
        print "Found %d match strings and %d substitution strings after replacement" % (result1['data'][0][0], result2['data'][0][0])
    else:
        print "No substitutions made"

# list distinct URL prefixes in a field
def list_url_prefixes(table, field = 'url'):
    dump = get_list(table, field)
    prefixes = []
    for i in dump:
        parsed = urlparse.urlparse(i)
        prefix = 'http://' + parsed.netloc + parsed.path
        if prefix not in prefixes:
            prefixes.append(prefix)
    print "Distinct URL prefixes found in the '" + field + "' field of the " + table + " table:"
    for p in prefixes:
        print p

# set map values in a database table NB stores values as unicode strings
def set_table_vals(table, map, where = ''):
    clause = ''
    for k, v in map.items():
        if v:
            store = vstr(v).replace("'", "''")
            clause = clause+', '+k+"='"+store+"'"
        else:
            clause = clause+', '+k+"=''"
    clause = clause[2:]
    if where:
        where = " where "+where
    else:
        where = ''
    scraperwiki.sqlite.execute("update "+table+" set "+clause+where)
    scraperwiki.sqlite.commit()

# return a simple list of database table columns
def get_table_cols(table):
    result = scraperwiki.sqlite.execute("select * from "+table+" limit 1")
    return result['keys']

# return columns for a table - new version returns dict of columns with constraints as values
def get_table_columns(table='swdata'):
    schemas = scraperwiki.sqlite.select("sql from sqlite_master where type='table' and name='"+table+"'")
    columns = {}
    for schema in schemas:
        table_match = TABLE_REGEX.search(schema['sql'].replace('`', ''))
        if table_match:
            if table_match.group(1) == table:
                fields = table_match.group(2).split(',')
                for field in fields:
                    parts = field.split()
                    column = parts[0]
                    if len(parts) > 0:
                        columns[column] = ' '.join(parts[1:])
                    else:
                        columns[column] = ''
                break
    return columns

# get a create table schema
def create_table_schema(columns, table='swdata'):
    if not columns:
        return None
    elif isinstance(columns, dict):
        fields = []
        for k, v in columns.items():
            fields.append("`" + k + "` " + v)
        return "create table `" + table + "` (" + ', '.join(fields) + ')'
    elif isinstance(columns, list):
        return "create table `" + table + "` (" + ', '.join(columns) + ')'
    else:
        return None

# get a create index schema
def create_index_schemas(indices, table='swdata'):
    if indices and isinstance(indices, dict):
        results = []
        for k, v in indices.items():
            if v['unique']:
                create = 'create unique index '
            else:
                create = 'create index '
            results.append(create + v['name'] + " on " + table + " (" + k + ")")
        return results
    else:
        return []

# return column indexes for a table - returns dict of indexed columns with name and whether unique as values
def get_table_indices(table='swdata'):
    schemas = scraperwiki.sqlite.select("sql from sqlite_master where type='index' and tbl_name='"+table+"'")
    indices = {}
    for schema in schemas:
        index_match = INDEX_REGEX.search(schema['sql'].replace('`', ''))
        if index_match:
            if index_match.group(3) == table:
                unique = False
                if 'unique' in index_match.group(1).lower(): unique = True
                result = { 'name': index_match.group(2), 'unique': unique }
                indices[index_match.group(4)] = result
    return indices

# adds column(s) to a database table if found not to exist
def update_columns(table, columns, constraint = 'text'):
    existing = get_table_columns(table)
    if not constraint: constraint = ''
    if isinstance(columns, list):
        for col in columns:
            if not col in existing.keys():
                scraperwiki.sqlite.execute("alter table "+table+" add column "+col+" "+constraint)
                scraperwiki.sqlite.commit()
    elif isinstance(columns, str) or isinstance(columns, unicode):
        if not columns in existing.keys():
                scraperwiki.sqlite.execute("alter table "+table+" add column "+columns+" "+constraint)
                scraperwiki.sqlite.commit()

# renames a column by copying data to a temp table and renaming
# note if new _column is null or empty the column is deleted
def rename_column(table, column, new_column, temp_table = 'temp_copy'):
    scraperwiki.sqlite.execute("drop table if exists "+temp_table)
    columns = get_table_columns(table)
    #print columns
    if not column in columns.keys(): return
    old_fields = []; new_fields = []; # note array used because order is important
    for k, v in columns.items():
        if k == column:
            del columns[column]
            if new_column:
                columns[new_column] = v
                new_fields.append(new_column)
                old_fields.append(column)
        else:
            new_fields.append(k)
            old_fields.append(k)
    sql_new_schema = create_table_schema(columns, temp_table)
    #print sql_new_schema
    scraperwiki.sqlite.execute(sql_new_schema)
    index_schemas = get_table_indices(table) # save index details before rename
    new_index_schemas = {}
    for k, v in index_schemas.items(): # filter out non-applicable indices
        field_list = k.split(',')
        new_field_list = []
        for field in field_list:
            if field == column:
                if new_column: 
                    new_field_list.append(new_column)
            else:
                new_field_list.append(field)
        if new_field_list:
            new_index_schemas[', '.join(new_field_list)] = v
    #print new_index_schemas
    sql_index_schemas = create_index_schemas(new_index_schemas, table)
    #print sql_index_schemas
    insert = "insert into "+temp_table+" ("+", ".join(new_fields)+") select "+", ".join(old_fields)+" from "+table
    #print insert
    scraperwiki.sqlite.execute(insert)
    scraperwiki.sqlite.execute("drop table "+table) # deletes associated indexes
    scraperwiki.sqlite.execute("alter table " + temp_table + " rename to " + table)
    for sql in sql_index_schemas: # re-apply indices
        scraperwiki.sqlite.execute(sql)
    scraperwiki.sqlite.commit()

# query the database cache table
def cache_fetch(key):
    tstamp = time.time()
    #if isinstance(key, dict):
    #    key = hash(tuple(sorted(key.iteritems())))
    #elif isinstance(key, list):
    #    key = hash(tuple(key))
    #else:
    #    key = hash(key)
    ser_key = cPickle.dumps(key)
    try:
        sql = "value from cache where key = '" + ser_key.replace("'", "''") + "' and expires >= " + str(tstamp)
        results = scraperwiki.sqlite.select(sql)
    except:
        results = None
    if results:
        return cPickle.loads(str(results[0]['value']))
    else:
        return None

# clear the database cache table
def cache_clear():
    scraperwiki.sqlite.execute("delete from cache")
    scraperwiki.sqlite.commit()

# insert a value in the database cache table
# this is a slow operation, so we also take the opportunity to clear stale cache entries
def cache_put(key, value, age = DEFAULT_CACHE_AGE): # default expiry in 12 hours
    tstamp = time.time()
    try:
        scraperwiki.sqlite.execute("delete from cache where expires < "+str(tstamp))
        scraperwiki.sqlite.commit()
    except:
        pass
    if age and age > 0:
        expires = tstamp + age
    else:
        expires = tstamp + DEFAULT_CACHE_AGE
    #if isinstance(key, dict):
    #    key = hash(tuple(sorted(key.iteritems())))
    #elif isinstance(key, list):
    #    key = hash(tuple(key))
    #else:
    #    key = hash(key)
    store = { 'key': cPickle.dumps(key), 'value': cPickle.dumps(value), 'expires': expires }
    scraperwiki.sqlite.save(unique_keys=['key'], data=store, table_name='cache', verbose=0)

# get a processing slot
def get_slot(num_slots = NUM_SLOTS, slot_time = SLOT_TIME):
    timestamp = time.time()
    next_free_slot = slot_time
    for i in range(0, num_slots):
        slot_name = "slot" + str(i)
        slot_expires = scraperwiki.sqlite.get_var(slot_name, 0)
        if not slot_expires or slot_expires < timestamp:
            scraperwiki.sqlite.save_var(slot_name, timestamp + slot_time) # we have the lock, so just block it for the next slot_time secs
            return i, slot_time
        else:
            this_expires = slot_expires - timestamp
            if this_expires > 0 and this_expires < next_free_slot: 
                next_free_slot = this_expires
    return -1, next_free_slot # time until next available slot is free

# free up a processing slot
def free_slot(slot_num):
    slot_name = "slot" + str(slot_num)
    scraperwiki.sqlite.save_var(slot_name, 0)

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

# get an item from the local memory cache
# make copy, otherwise the cached version is mutable
def mcache_fetch(key):
    if isinstance(key, dict):
        keyhash = hash(tuple(sorted(key.iteritems())))
    elif isinstance(key, list):
        keyhash = hash(tuple(key))
    else:
        keyhash = hash(key)
    return copy.deepcopy(CACHE.get(keyhash))

#Given a list of dates as ISO8601 values, plot a histogram by month.
# output is a base64 encoded PNG string
def plotdates(dts, dpi=50, mindate = None, maxdate = None):
    if not dts: return None
    if not mindate: mindate=min(dts)
    if not maxdate: maxdate=max(dts)
    ym=mindate[:7]; 
    months=[]; counts=[]
    while ym<=maxdate[:7]:
        try:
            m = int(ym[5:7]); y = int(ym[:4])
        except:
            return None
        months.append(date(y, m, 1))
        counts.append(sum([1 if (dd[:7]==ym) else 0 for dd in dts]))
        m = m + 1
        if m > 12: y = y + 1; m = 1
        ym = str(y)+'-'+format(m, '02d')
    fig=pl.figure()
    ax=fig.add_subplot(111)
    ax.bar(months,counts,width=20.0)
    for xlabel_i in ax.get_xticklabels():
        xlabel_i.set_fontsize(20)
    for ylabel_i in ax.get_yticklabels():
        ylabel_i.set_fontsize(20) 
    ax.xaxis_date()
    fig.autofmt_xdate()
    #pl.draw()
    cout = StringIO()
    pl.savefig(cout, format="png", dpi=dpi)
    #print counts, months
    return base64.encodestring(cout.getvalue())

#default css for views
def base_css():
    css = """
body {
    margin: 10 20;
    padding: 0;
    background: #FFF;
    color: #191919;
    font-weight: normal;
    font-family: Helvetica, Arial, sans-serif;
    font-size: 75%;
}
    /*------------------- HEADERS -------------------*/
h1, h2, h3, h4, h5, h6 {
  margin: 6px 0;
  padding: 0;
  font-weight: normal;
  font-family: Helvetica, Arial, sans-serif;
}

h1 {font-size: 2em;}
h2 {font-size: 1.8em; line-height: 1.8em;}
h3 {font-size: 1.6em;}
h4 {font-size: 1.4em;}
h5 {font-size: 1.2em;}
h6 {font-size: 1em;}
/*------------------- HEADERS -------------------*/

/*------------------- TEXT/LINKS/IMG -------------------*/
p {margin: 10px 0 18px; padding: 10px;}

em {font-style:italic;}

strong {font-weight:bold;}

a:link, a:visited {color: #027AC6; text-decoration: none; outline:none;}

a:hover {color: #0062A0; text-decoration: underline;}

a:active, a.active {color: #5895be;}

img, a img {border: none;}

abbr,acronym {
    /*indicating to users that more info is available */
    border-bottom:1px dotted #000;
    cursor:help;
}

/*------------------- TEXT/LINKS/IMG -------------------*/

hr {
  margin: 0;
  padding: 0;
  border: none;
  height: 1px;
  background: #5294c1;
}

/*Change in format*/
ul, blockquote, quote, code, fieldset {margin: 16px 0;}

pre {  padding: 0; margin: 0; font-size: 1.3em; 
    white-space: -moz-pre-wrap !important; /* Mozilla, supported since 1999 */
    white-space: -pre-wrap; /* Opera 4 - 6 */
    white-space: -o-pre-wrap; /* Opera 7 */
    white-space: pre-wrap; /* CSS3 */
    word-wrap: break-word; /* IE 5.5+ */
}


/*------------------- LISTS -------------------*/

ul {margin-left:32px;}

ol,ul,dl {margin-left:32px;}
ol, ul, dl {margin-left:32px;}
ul, ol {margin: 8px 0 16px; padding: 0;}
ol li, ul li {margin: 7px 0 7px 32px;}
ul ul li {margin-left: 10px;}

ul li {padding: 0 0 4px 6px; list-style: disc outside;}
ul li ul li {list-style: circle outside;}

ol li {padding: 0 0 5px; list-style: decimal outside;}

dl {margin: 8px 0 16px 24px;}
dl dt {font-weight:bold;}
dl dd {margin: 0 0 8px 20px;}

/*------------------- LISTS -------------------*/


/*------------------- FORMS -------------------*/
input {
  font: 1em/1.2em Verdana, sans-serif;
  color: #191919;
}
textarea, select {
  font: 1em/1.2em Verdana, sans-serif;
  color: #191919;
}
textarea {resize:none;}
/*------------------- FORMS -------------------*/


/*------------------- TABLES -------------------*/

table {margin: 16px 0; width: 90%; font-size: 0.92em; border-collapse:collapse; }

th {
  border:1px solid #000; 
  background-color: #d3e7f4;
  font-weight: bold;
}

td {padding: 4px 6px; margin: 0; border:1px solid #000;}

caption {margin-bottom:8px; text-align:center;}

/*------------------- TABLES -------------------*/
    """
    return css

"""
class MinimalSoupHandler(mechanize.BaseHandler):
    def http_response(self, request, response):
        if not hasattr(response, "seek"):
            response = mechanize.response_seek_wrapper(response)
        # only use if response is html
        if response.info().dict.has_key('content-type') and ('html' in response.info().dict['content-type']):
            soup = MinimalSoup (response.get_data())
            response.set_data(soup.prettify())
        return response
"""

class BeautifulSoupHandler(mechanize.BaseHandler):
    def http_response(self, request, response):
        if not hasattr(response, "seek"):
            response = mechanize.response_seek_wrapper(response)
        # only use if response is html
        if response.info().dict.has_key('content-type') and ('html' in response.info().dict['content-type']):
            #soup = BeautifulSoup (response.get_data())
            self.element = lxml.html.soupparser.fromstring(response.get_data())
            #response.set_data(soup.prettify())
            response.set_data(etree.tostring(self.element, pretty_print=True, method="html"))
        return response

class EtreeHandler(mechanize.BaseHandler):
    def http_response(self, request, response):
        if not hasattr(response, "seek"):
            response = mechanize.response_seek_wrapper(response)
        # only use if response is html
        if response.info().dict.has_key('content-type') and ('html' in response.info().dict['content-type']):
            #clean_up = lxml.html.clean.clean_html(response.get_data()) # not tested yet ? put in new EtreeCleanHandler
            #self.element = etree.HTML(response.get_data())
            tag_soup = response.get_data()
            try:
                self.element = lxml.html.fromstring(tag_soup)
                ignore = etree.tostring(self.element, encoding=unicode) # check the unicode entity conversion has worked
            except (UnicodeDecodeError, etree.XMLSyntaxError):
                self.element = lxml.html.soupparser.fromstring(tag_soup) # fall back to beautiful soup if there is an error    
            response.set_data(etree.tostring(self.element, pretty_print=True, method="html"))      
        return response


