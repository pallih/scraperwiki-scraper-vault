# a library of utility functions for use in other scrapers

import scraperwiki
import lxml.html
import lxml.html.soupparser
from lxml import etree
import re
from datetime import date
import urllib, urllib2, urlparse
from datetime import datetime
from datetime import timedelta
import json
import mechanize
import socket
from pytz import timezone
from BeautifulSoup import BeautifulSoup
#from BeautifulSoup import MinimalSoup
from cStringIO import StringIO
from csv import reader
import random
import cookielib
scrapemark = scraperwiki.utils.swimport("scrapemark_09")

DATE_FORMAT = "%d/%m/%Y"
RFC822_DATE = "%a, %d %b %Y %H:%M:%S %z"
ISO8601_DATE = "%Y-%m-%d"
RFC3339_DATE = "%Y-%m-%dT%H:%M:%SZ"
GEOCODE_BASE_URL = 'http://maps.googleapis.com/maps/api/geocode/json'
GEOCODE2_BASE_URL = ' http://where.yahooapis.com/geocode'
POSTCODE_BASE_URL = 'http://geo.jamiethompson.co.uk/'
POSTCODE_REGEX = re.compile(r'[A-Z][A-Z]?\d(\d|[A-Z])? ?\d[ABDEFGHJLNPQRSTUWXYZ]{2}\b', re.I) # ignore case
TAGS_REGEX = re.compile(r'<[^<]+?>')
GAPS_REGEX = re.compile(r'\s+', re.U) # unicode spaces include html &nbsp;
TZ = timezone('Europe/London')
AUTHOR = 'AS' # for Atom feeds 
TIMEOUT = 120
SCRAPER = 'https://views.scraperwiki.com/run/paview_scraper_1/'
WEEKDAYS = { 'Mon': 0, 'Tue': 1, 'Wed': 2, 'Thu': 3, 'Fri': 4, 'Sat': 5, 'Sun': 6 }

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
        scraperwiki.sqlite.save(keys, add_list, table_name) # one save operation not many
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
    else:
        scraperwiki.utils.httpresponseheader("Content-Type", "text/xml")

# output a data dict in JSON, XML or RSS formats
def data_output(data, fmt = 'xml', options = None):
    if fmt == 'json':
        return json.dumps(data, indent=4)
    elif fmt == 'jsonp':
        if not options: options = 'callback'
        return options + '(' + json.dumps(data, indent=4) + ')'
    elif fmt == 'rss':
        root = to_rss(data, options, ISO8601_DATE)
        return etree.tostring(root, encoding="utf-8", xml_declaration=True, pretty_print=True)
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
    else:
        if not options:
            options = 'root'
        root = to_xml(options, data)
        return etree.tostring(root, encoding="utf-8", xml_declaration=True, pretty_print=True)
    
# use data to fill out an RSS 2.0 feed (with option for GeoRSS)
def to_rss(data, map, in_date_fmt = RFC822_DATE):
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
            twig.text = xunc(data[v])
    pubdate = datetime.now(TZ).strftime(RFC822_DATE)
    twig = etree.SubElement(branch, 'pubDate')
    twig.text = xunc(pubdate)
    for i in data[map['items']][map['item']]:
        twig = etree.SubElement(branch, "item")
        for k, v in map['sub_item'].items():
            if v in i:
                leaf = etree.SubElement(twig, k)
                leaf.text = xunc(i[v])
                if k == 'guid':
                    leaf.set("isPermaLink", "false")
        leaf = etree.SubElement(twig, 'pubDate')
        leaf.text = xunc(pubdate)
        for k, v in map['geo_item'].items():
            if v in i:
                leaf = etree.SubElement(twig, GEORSS+k)
                leaf.text = xunc(i[v])
    return root

# use data to fill out an ATOM feed (with option for GeoRSS)
def to_atom(data, map, in_date_fmt = RFC822_DATE):
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
                branch.set("href", xunc(data[v]))
                branch.set("rel", "self")
            else:
                branch.text = xunc(data[v])
    pubdate = datetime.now(TZ).strftime(RFC3339_DATE)
    branch = etree.SubElement(root, 'updated')
    branch.text = xunc(pubdate)
    for i in data[map['items']][map['item']]:
        branch = etree.SubElement(root, "entry")
        for k, v in map['sub_item'].items():
            if v in i:
                leaf = etree.SubElement(branch, k)
                if k == 'link':
                    leaf.set("href", xunc(i[v]))
                else:
                    leaf.text = xunc(i[v])
        leaf = etree.SubElement(branch, 'updated')
        leaf.text = xunc(pubdate)
        leaf = etree.SubElement(branch, 'author')
        end = etree.SubElement(leaf, 'name')
        end.text = xunc(AUTHOR)
        for k, v in map['geo_item'].items():
            if v in i:
                leaf = etree.SubElement(branch, GEORSS+k)
                leaf.text = xunc(i[v])
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
        element.text = xunc(data)
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
            return output+xunc(data)
        elif container == 'dl':
            if title:
                output = output+'<dt>'+title+'</dt>'
            return output+'<dd>'+xunc(data)+'</dd>'
        elif container == 'tr':
            output = output+'<td>'
            if title:
                output = output+'<strong>'+title+':</strong> '
            return output+xunc(data)+'</td>'
        elif container == 'tr1':
            output = output+'<th>'
            if title:
                output = output+'<strong>'+title+':</strong> '
            return output+xunc(data)+'</th>'
        elif container == 'ul':
            output = output+'<li>'
            if title:
                output = output+'<strong>'+title+':</strong> '
            return output+xunc(data)+'</li>'

# return unicode string if not null, otherwise empty string
def xunc(s):
    return unicode(s) if s else u''

# add new data elements to the existing query of a URL
def add_to_query(url, data = {}):
    u = urlparse.urlsplit(url)
    qdict = dict(urlparse.parse_qsl(u.query))
    data.update(qdict)
    query = urllib.urlencode(data)
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

def extract_postcode(text):
    postcode_match = POSTCODE_REGEX.search(text)
    if postcode_match:
        return postcode_match.group()
    else:
        return ''

def geopostcode(postcode): # uses geo.jamiethompson.co.uk
    url = POSTCODE_BASE_URL + urllib.quote(postcode) + '.json'
    result = json.load(urllib.urlopen(url))  
    if len(result['geo'])>0:
        lat = result['geo']['lat']
        lng = result['geo']['lng']
        postal = result['postcode']
    else:
        lat = 0
        lng = 0
        postal = ''
    return lat, lng, postal

def geocode(address): # uses Google
    geo_args = {
        'sensor': 'false',
        'address': address.encode('utf-8'),
        'region': 'uk'
    }
    url = GEOCODE_BASE_URL + '?' + urllib.urlencode(geo_args)
    result = json.load(urllib.urlopen(url))  
    if len(result['results'])>0:
        lat = result['results'][0]['geometry']['location']['lat']
        lng = result['results'][0]['geometry']['location']['lng']
        postal = ''
        for comp in result['results'][0]['address_components']:
            if 'postal_code' in comp['types']:
                postal = comp['long_name']
    else:
        lat = 0
        lng = 0
        postal = ''
    return lat, lng, postal

def geocode2(address, region = 'London'): # uses Yahoo
    geo_args = {
        'location': address.encode('utf-8'),
        'locale': 'en_GB',
        'flags': 'J',
        'gflags': 'L'
    }
    url = GEOCODE2_BASE_URL + '?' + urllib.urlencode(geo_args)
    result = json.load(urllib.urlopen(url)) 
    count = result['ResultSet']['Found']
    if count > 0:
        lat = result['ResultSet']['Results'][0]['latitude']
        lng = result['ResultSet']['Results'][0]['longitude']
        postal = result['ResultSet']['Results'][0]['uzip']
        if not postal: postal = result['ResultSet']['Results'][0]['postal']
        if region and count > 1:
            for i in result['ResultSet']['Results']:
                if i['city'] == region or i['county'] == region:
                    lat = i['latitude']
                    lng = i['longitude']
                    postal = i['uzip']
                    if not postal: postal = i['postal']
                    break
    else:
        lat = 0
        lng = 0
        postal = ''
    return lat, lng, postal

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
        text = str(value)
        text = TAGS_REGEX.sub(' ', text) # replace any html tag content with spaces
        # use beautiful soup to convert html entities to unicode strings
        text = BeautifulSoup(text, convertEntities="html").contents[0].string
    return trim(text)
    
# return text with internal white space compressed and external space stripped off
def trim(text):
    str_trim = GAPS_REGEX.sub(' ', text) # replace internal gaps with single spaces
    return str_trim.strip() # remove space at left and right

#get selected table fields from database as list of maps
def get_table_vals(table, fields = '', where = '', orderetc = ''):
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

#convert list of maps to keyed map of maps
def get_map(list_of_maps, key):
    data = {}
    for map in list_of_maps:
        data[map[key]] = map
    return data 

# set map values in a database table NB stores values as unicode strings
def set_table_vals(table, map, where = ''):
    clause = ''
    for k, v in map.items():
        if v:
            store = unicode(v).replace("'", "''")
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

# return a list of database table columns
def get_table_cols(table):
    result = scraperwiki.sqlite.execute("select * from "+table+" limit 1")
    return result['keys']

# adds columns to a database table if they are found not to exist
def update_columns(table, columns):
    clist = get_table_cols(table)
    if isinstance(columns, list):
        for col in columns:
            if not col in clist:
                scraperwiki.sqlite.execute("alter table "+table+" add column "+col)
                scraperwiki.sqlite.commit()
    elif isinstance(columns, str) or isinstance(columns, unicode):
        if not columns in clist:
                scraperwiki.sqlite.execute("alter table "+table+" add column "+columns)
                scraperwiki.sqlite.commit()

# store planning application data, doing any necessary date translations and geocoding at the same time
def store_applications(auth_name, applications, applications_table = 'applications', scrape_date = date.today()):
    for applic in applications:
        applic['authority'] = auth_name
        applic['scrape_date'] = scrape_date.strftime(ISO8601_DATE)
        if applic.get('received_date'):
            recvd_dt = convert_dt(applic['received_date'], DATE_FORMAT, ISO8601_DATE, False)
            if recvd_dt:
                applic['received_date'] = recvd_dt
            else:
                del applic['received_date'] # badly formatted date, do not insert
        if applic.get('validated_date'):
            valid_dt = convert_dt(applic['validated_date'], DATE_FORMAT, ISO8601_DATE, False)
            if valid_dt:
                applic['validated_date'] = valid_dt
            else:
                del applic['validated_date'] # badly formatted date, do not insert
        if applic.get('address'):
            if not applic.get('postcode'):
                postcode = extract_postcode(applic['address'])
                if postcode and len(postcode) > 0:
                    applic['postcode'] = postcode
        if not applic.get('lat') or not applic.get('lng'):
                if applic.get('postcode'):
                    try:
                        lat, lng = scraperwiki.geo.gb_postcode_to_latlng(applic['postcode'])
                        applic['lat'] = lat
                        applic['lng'] = lng
                    except:
                        try:
                            lat, lng, postal = geopostcode(applic['postcode'])
                            applic['lat'] = lat
                            applic['lng'] = lng
                        except:
                            pass
                if applic.get('address') and (not applic.get('lat') or not applic.get('lng')):
                    try:
                        lat, lng, postcode = geocode(applic['address']) # Google geocode
                        if lat and lng:
                            if 'postcode' not in applic and postcode: 
                                applic['postcode'] = postcode
                            applic['lat'] = lat
                            applic['lng'] = lng
                        else:
                            lat, lng, postcode = geocode2(applic['address']) # Yahoo geocode
                            if lat and lng:
                                if 'postcode' not in applic and postcode: 
                                    applic['postcode'] = postcode
                                applic['lat'] = lat
                                applic['lng'] = lng     
                    except:
                        pass
    scraperwiki.sqlite.save(unique_keys=['authority', 'reference'],
                                data=applications, table_name=applications_table)

# try to gather at least max planning applications from one source
def gather_applications(target, start, end, max, timeout = TIMEOUT, scraper_url = SCRAPER,
                    applications_table = 'applications', progress_table = 'authorities'):
    auth_name = target['name']
    try:
        auths = get_table_vals(progress_table, '', "name='"+auth_name+"'")
        auth = auths[0]
    except:
        auth = {}
        auth['total'] = 0
    auth.update(target)
    if not timeout: timeout = 0

    db_start_date = get_dt(start, ISO8601_DATE)
    if not db_start_date:
        db_start_date = date.today() - timedelta(days=start)
    db_end_date = get_dt(end, ISO8601_DATE)
    if not db_end_date:
        db_end_date = date.today() - timedelta(days=end)
    if not db_start_date or not db_end_date or db_end_date < db_start_date or db_start_date >= date.today() or db_end_date >= date.today():
        print 'Configuration start / end dates error for '+auth_name
        return

    # 2 dates defining current range of data stored
    start_date = get_dt(auth.get('start_date', ''), ISO8601_DATE) # start
    last_date = get_dt(auth.get('last_date', ''), ISO8601_DATE) #end
    if not start_date or start_date > db_start_date: # current start point is empty or after required start point
        scrape_start = db_start_date # start scraping again from the beginning
        start_date = db_start_date.strftime(ISO8601_DATE)
    elif not last_date or last_date < start_date: # no current end point or it is before current start point
        scrape_start = start_date
    elif auth.get('last_status', '') != 'OK': # last scrape was not successful, try again
        scrape_start = last_date
    else:
        scrape_start = last_date + timedelta(days=1) # start collecting 1 day after current end point
    
    result = {}
    total = 0
    status = 'OK'
    today = date.today().strftime(ISO8601_DATE)
    while total < max and scrape_start < db_end_date and status == 'OK':
        result.update(auth)
        result['last_scrape'] = today
        result['last_date'] = scrape_start.strftime(ISO8601_DATE)
        result['start_date'] = start_date
        result['last_count'] = 0
        result['last_match_count'] = 0
        status = 'Error'
        result['last_status'] = status   
        query = {
            'auth': auth_name,
            'day': str(scrape_start.day),
            'month': str(scrape_start.month),
            'year': str(scrape_start.year),
        }
        url = scraper_url+'?'+urllib.urlencode(query)
        print_query = '('+query['auth']+' '+query['day']+'/'+query['month']+'/'+query['year']+')'
        try: 
            response = get_response(url, None, None, 'text/xml', timeout)
            # if there is an Internet time out or other fetch error
            # have to cut losses and move on to the next authority
        except IOError as e:
            if hasattr(e, 'reason'): # URLError
                result['last_msg'] = 'Cannot reach scraper (URL error): '+unicode(e)+': '+print_query
            elif hasattr(e, 'code'): # HTTPError
                result['last_msg'] = 'Scraper returned HTTP error: '+unicode(e)+': '+print_query
            else:
                result['last_msg'] = 'IO error accessing scraper: '+unicode(e)+': '+print_query
        except socket.timeout as e:
            result['last_msg'] = 'Socket timeout accessing scraper ('+str(timeout)+'s): '+unicode(e)+': '+print_query
        except Exception as e:
            result['last_msg'] = 'Other error accessing scraper: '+unicode(e)+': '+print_query
        else:
            xml = ''
            try:
                xml = response.read()
                doc = get_doc_xml(xml)
                planning = from_xml(doc)
            except Exception as e:
                result['last_msg'] = 'Bad XML doc returned from scraper ('+xml[0:39]+'): '+unicode(e)+': '+print_query
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
                        scrape_start = get_dt(planning['until_date']) 
                        if scrape_start >= db_end_date:
                            result['last_date'] = db_end_date.strftime(ISO8601_DATE) 
                        else:
                            result['last_date'] = scrape_start.strftime(ISO8601_DATE) 
                    if count > 0:
                        applications = planning['applications']['application']
                        store_applications(auth_name, applications, applications_table) # data stored here
                        total = total + count        
        scraperwiki.sqlite.save(unique_keys=['name'], data=result, table_name=progress_table)
        scrape_start = scrape_start + timedelta(days=1) # next day
        if status <> 'OK': last_err = result['last_msg']
        result.clear()
    print 'Scraped '+str(total)+' records from '+auth_name+' ('+str(auth.get('config', ''))+') --> '+status
    if status <> 'OK': print last_err
    if total > 0:
        try:
            applics = get_table_vals(applications_table, 'count(*) as total', "authority='"+auth_name+"'")
            count = applics[0]['total']
            set_table_vals(progress_table, { 'total': count }, "name='"+auth_name+"'")
        except:
            pass
    return

# clear data from a single planning authority
def restart_authority(auth_name, applications_table = 'applications', progress_table = 'authorities'):
    if auth_name: # clearing the applications 'start_date' value makes data gathering start again
        set_table_vals(progress_table, { 'start_date': '' }, "name='"+auth_name+"'")
        scraperwiki.sqlite.execute("delete from "+applications_table+" where authority='"+auth_name+"'")
        scraperwiki.sqlite.commit()
        print "Successfully cleared the authority data of "+auth_name
    else:
        print "You must specify a single authority name"

# remove a single planning authority permanently
def remove_authority(auth_name, applications_table = 'applications', progress_table = 'authorities'):
    if auth_name: 
        scraperwiki.sqlite.execute("delete from "+progress_table+" where name='"+auth_name+"'")
        scraperwiki.sqlite.execute("delete from "+applications_table+" where authority='"+auth_name+"'")
        scraperwiki.sqlite.commit()
        print "Successfully deleted the authority data of "+auth_name
    else:
        print "You must specify a single authority name"

# get the list of planning authorities from the scraper
def get_auths(region_or_list = None, scrape_url = SCRAPER):
    result = []
    try:
        response = get_response(scrape_url, None, None, 'text/xml')
        xml = response.read()
        doc = get_doc_xml(xml) 
        scraper = from_xml(doc)
        authorities = scraper['authorities']['authority']
    except:
        pass 
    else:
        for auth in authorities:
            if isinstance(region_or_list, list):
                if not region_or_list or auth['name'] in region_or_list:
                    result.append(auth)
            else:
                if not region_or_list or region_or_list in auth.get('region', ''):
                    result.append(auth)
        result = sorted(result, cmp=lambda x,y: cmp(x['name'],y['name']))
    return result

# do housekeeping in the applications database
# 1. set dates not in standard format to null
# 2. delete any applications older than certain threshold ages (4 months validated, 8 months received)
def do_cleanup(received_days = -240, validated_days = -120, applications_table = 'applications', ):
    scraperwiki.sqlite.execute("update "+applications_table+" set received_date = null where received_date is not null and received_date not like '%-%'")
    scraperwiki.sqlite.execute("update "+applications_table+" set validated_date = null where validated_date is not null and validated_date not like '%-%'")
    scraperwiki.sqlite.commit()
    if received_days < 0 and validated_days < 0 and received_days < validated_days:
        today = date.today().strftime(ISO8601_DATE)
        received_days_ago, st = inc_dt(today, ISO8601_DATE, received_days)
        validated_days_ago, st = inc_dt(today, ISO8601_DATE, validated_days)
        scraperwiki.sqlite.execute("delete from "+applications_table+" where ((validated_date is not null and validated_date < '"+validated_days_ago+"') or (validated_date is null and received_date is not null and received_date < '"+received_days_ago+"'))")
        scraperwiki.sqlite.commit()
    print "Cleaned dates and cleared out old records"

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

table {margin: 16px 0; width: 90%; font-size: 0.92em;}

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




