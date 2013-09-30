import httplib
import json
import lxml.html
import re
import scraperwiki
import urllib
import urllib2
import datetime

geolink_regexp = re.compile("@(-?[0-9]+\\.[0-9]+),\\+? ?(-?[0-9]+\\.[0-9]+)")
postcode_regexp = re.compile("\\b[a-zA-Z]{1,2}[0-9]{1,2}[a-zA-Z]? ?[0-9a-zA-Z]{3}")
postcode_translations = {}

scraperwiki.sqlite.attach("appsearchserv_system_planning_applications", "appss")
json_dateformat = "%Y-%m-%dT%H:%M:%S"
max_scrapes = 100
min_pkid = 100603 # Smallest PKID identifier value in the system. Authority-specific value.

# Return the largest-known PKID value from the Openly Local planning scraper. We'll assume that there are no records with a larger PKID than this.
def get_max_pkid():
    applications = scraperwiki.sqlite.select("url from appss.Ealing ORDER BY url DESC LIMIT 1");
    if len(applications) == 1:
        return int(applications[0]["url"].split("=")[1]);

def get_next_pkids():
    start_id = scraperwiki.sqlite.get_var('last_id')
    if start_id is None or start_id == 0:
        start_id = min_pkid
    else:
        start_id = int(start_id)
    return range(start_id + 1, min(start_id + max_scrapes + 1, get_max_pkid() + 1))

def get_recent_applications():
    last_scrape_str = scraperwiki.sqlite.get_var('last_scrape_date') or "1970-01-01T00:00:00"
    last_scrape_date = datetime.datetime.strptime(last_scrape_str, json_dateformat)
    pkids = []
    applications = scraperwiki.sqlite.select("* from appss.Ealing WHERE date_scraped IS NOT NULL AND address IS NOT NULL ORDER BY date_scraped DESC LIMIT 500");
    for app in applications:
        if datetime.datetime.strptime(app["date_scraped"], json_dateformat) > last_scrape_date:
            pkids.append(app["url"].replace('ApplicationSearchServlet', 'TPOSearchServlet'))
    return pkids

def main():
    num_successful_scrapes = 0
    now = datetime.datetime.now()
    #pkids = get_recent_applications()
    pkids = get_next_pkids()
    last_id = 0

    for id in pkids:
        application_data = scrape_application(id)

        # Save the data
        if application_data is not None:
            save_data(application_data)
            num_successful_scrapes += 1

        last_id = id

    scraperwiki.sqlite.save_var('last_id', last_id)
    scraperwiki.sqlite.save_var('last_scrape_date', now.strftime(json_dateformat))

def scrape_application(url):
    application_data = None
    # url could be a PKID value or a full URL
    if not str(url).startswith("http"):
        url = 'http://www.pam.ealing.gov.uk/portal/servlets/TPOSearchServlet?PKID=%s' % (url)
    page_html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(page_html)
    form_els = root.cssselect("table.DETAILSFORM")
    list_els = root.cssselect("table.DETAILSLIST")
    if len(form_els) > 0:
        application_data = {
            'pkid': id,
            'ref_num': None,
            'application_date': None,
            'address': None,
            'lat_real': None,
            'lon_real': None,
            'area_type': None,
            'description': None,
            'num_trees': (len(list_els[0].findall("tr")) - 1) if len(list_els) > 0 else 0
        }
        
        for tr_el in form_els[0].findall("tr"):
            td_els = tr_el.findall("td")
            if (len(td_els) == 2):
                name_text = td_els[0].text_content().strip()
                value_text = (td_els[1].text or '').strip() + ''.join([re.sub('\s*<br\s?/?>\s*', ', ', lxml.html.tostring(child).strip()) for child in td_els[1].iterdescendants()])
                
                if name_text == 'Reference number':
                    application_data['ref_num'] = value_text
                elif name_text == 'Application date':
                    application_data['application_date'] = value_text
                elif name_text == 'Address':
                    application_data['address'] = value_text.replace('<br>', ',')
                    print value_text
                elif name_text == 'Area type':
                    application_data['area_type'] = value_text
                elif name_text == 'Description':
                    application_data['description'] = value_text
            
        if application_data['address'] is not None and application_data['address'] != "":
            postcode = get_postcode(application_data['address'])

            # Get lat/lon from postcode, if not available in web page
            if postcode is not None and postcode != ""and application_data['lat_real'] is None and application_data['lon_real'] is None:
                latlng = postcode_to_latlng(postcode)
                application_data['lat_real'] = latlng[0]
                application_data['lon_real'] = latlng[1]
    return application_data


# Save the data
def save_data(data=None):
    #scraperwiki.sqlite.execute("UPDATE swdata SET event_code='%s', not_normally_open=%s, not_normally_free=%s WHERE name='%s' and region='%s'" % (e['event_code'], e['not_normally_open'], e['not_normally_free'], e['name'], e['region']))
    scraperwiki.sqlite.save(unique_keys=['ref_num'], data=data)

def find_postcode(addr):
    m = postcode_regexp.search(addr)
    if m is not None:
        return m.group().upper()
    else:
        return None

def get_postcode(addr):
    pc = find_postcode(addr)
    if pc is not None:
        if pc in postcode_translations:
            return postcode_translations[pc]
        else:
            return pc.replace(" O", " 0")
    else:
        return None

# Lookup postcode
def postcode_to_latlng(postcode):
    return ukp_postcode_to_latlng(postcode)

# Lookup postcode from internal SW service
def sw_postcode_to_latlng(postcode):
    return scraperwiki.geo.gb_postcode_to_latlng(postcode)

# Lookup postcode from uk-postcodes.com
def ukp_postcode_to_latlng(postcode):
    try:
        resp = urllib2.urlopen("http://www.uk-postcodes.com/postcode/%s.json" % (urllib.quote(postcode.replace(" ", ""))))
        respJson = json.loads(resp.read())
        resp.close()
        if 'geo' in respJson:
            return (respJson['geo']['lat'], respJson['geo']['lng'])
        else:
            return None
    except urllib2.HTTPError as e:
        print "Warning: HTTP error resolving postcode %s - %s" % (postcode, e)
        return None
    except urllib2.URLError as e:
        print "Warning: URL opening error resolving postcode %s - %s" % (postcode, e)
        return None
    except httplib.BadStatusLine as e:
        print "Warning: BadStatusLine exception resolving postcode %s - %s" % (postcode, e)
        return None
    

main()

import httplib
import json
import lxml.html
import re
import scraperwiki
import urllib
import urllib2
import datetime

geolink_regexp = re.compile("@(-?[0-9]+\\.[0-9]+),\\+? ?(-?[0-9]+\\.[0-9]+)")
postcode_regexp = re.compile("\\b[a-zA-Z]{1,2}[0-9]{1,2}[a-zA-Z]? ?[0-9a-zA-Z]{3}")
postcode_translations = {}

scraperwiki.sqlite.attach("appsearchserv_system_planning_applications", "appss")
json_dateformat = "%Y-%m-%dT%H:%M:%S"
max_scrapes = 100
min_pkid = 100603 # Smallest PKID identifier value in the system. Authority-specific value.

# Return the largest-known PKID value from the Openly Local planning scraper. We'll assume that there are no records with a larger PKID than this.
def get_max_pkid():
    applications = scraperwiki.sqlite.select("url from appss.Ealing ORDER BY url DESC LIMIT 1");
    if len(applications) == 1:
        return int(applications[0]["url"].split("=")[1]);

def get_next_pkids():
    start_id = scraperwiki.sqlite.get_var('last_id')
    if start_id is None or start_id == 0:
        start_id = min_pkid
    else:
        start_id = int(start_id)
    return range(start_id + 1, min(start_id + max_scrapes + 1, get_max_pkid() + 1))

def get_recent_applications():
    last_scrape_str = scraperwiki.sqlite.get_var('last_scrape_date') or "1970-01-01T00:00:00"
    last_scrape_date = datetime.datetime.strptime(last_scrape_str, json_dateformat)
    pkids = []
    applications = scraperwiki.sqlite.select("* from appss.Ealing WHERE date_scraped IS NOT NULL AND address IS NOT NULL ORDER BY date_scraped DESC LIMIT 500");
    for app in applications:
        if datetime.datetime.strptime(app["date_scraped"], json_dateformat) > last_scrape_date:
            pkids.append(app["url"].replace('ApplicationSearchServlet', 'TPOSearchServlet'))
    return pkids

def main():
    num_successful_scrapes = 0
    now = datetime.datetime.now()
    #pkids = get_recent_applications()
    pkids = get_next_pkids()
    last_id = 0

    for id in pkids:
        application_data = scrape_application(id)

        # Save the data
        if application_data is not None:
            save_data(application_data)
            num_successful_scrapes += 1

        last_id = id

    scraperwiki.sqlite.save_var('last_id', last_id)
    scraperwiki.sqlite.save_var('last_scrape_date', now.strftime(json_dateformat))

def scrape_application(url):
    application_data = None
    # url could be a PKID value or a full URL
    if not str(url).startswith("http"):
        url = 'http://www.pam.ealing.gov.uk/portal/servlets/TPOSearchServlet?PKID=%s' % (url)
    page_html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(page_html)
    form_els = root.cssselect("table.DETAILSFORM")
    list_els = root.cssselect("table.DETAILSLIST")
    if len(form_els) > 0:
        application_data = {
            'pkid': id,
            'ref_num': None,
            'application_date': None,
            'address': None,
            'lat_real': None,
            'lon_real': None,
            'area_type': None,
            'description': None,
            'num_trees': (len(list_els[0].findall("tr")) - 1) if len(list_els) > 0 else 0
        }
        
        for tr_el in form_els[0].findall("tr"):
            td_els = tr_el.findall("td")
            if (len(td_els) == 2):
                name_text = td_els[0].text_content().strip()
                value_text = (td_els[1].text or '').strip() + ''.join([re.sub('\s*<br\s?/?>\s*', ', ', lxml.html.tostring(child).strip()) for child in td_els[1].iterdescendants()])
                
                if name_text == 'Reference number':
                    application_data['ref_num'] = value_text
                elif name_text == 'Application date':
                    application_data['application_date'] = value_text
                elif name_text == 'Address':
                    application_data['address'] = value_text.replace('<br>', ',')
                    print value_text
                elif name_text == 'Area type':
                    application_data['area_type'] = value_text
                elif name_text == 'Description':
                    application_data['description'] = value_text
            
        if application_data['address'] is not None and application_data['address'] != "":
            postcode = get_postcode(application_data['address'])

            # Get lat/lon from postcode, if not available in web page
            if postcode is not None and postcode != ""and application_data['lat_real'] is None and application_data['lon_real'] is None:
                latlng = postcode_to_latlng(postcode)
                application_data['lat_real'] = latlng[0]
                application_data['lon_real'] = latlng[1]
    return application_data


# Save the data
def save_data(data=None):
    #scraperwiki.sqlite.execute("UPDATE swdata SET event_code='%s', not_normally_open=%s, not_normally_free=%s WHERE name='%s' and region='%s'" % (e['event_code'], e['not_normally_open'], e['not_normally_free'], e['name'], e['region']))
    scraperwiki.sqlite.save(unique_keys=['ref_num'], data=data)

def find_postcode(addr):
    m = postcode_regexp.search(addr)
    if m is not None:
        return m.group().upper()
    else:
        return None

def get_postcode(addr):
    pc = find_postcode(addr)
    if pc is not None:
        if pc in postcode_translations:
            return postcode_translations[pc]
        else:
            return pc.replace(" O", " 0")
    else:
        return None

# Lookup postcode
def postcode_to_latlng(postcode):
    return ukp_postcode_to_latlng(postcode)

# Lookup postcode from internal SW service
def sw_postcode_to_latlng(postcode):
    return scraperwiki.geo.gb_postcode_to_latlng(postcode)

# Lookup postcode from uk-postcodes.com
def ukp_postcode_to_latlng(postcode):
    try:
        resp = urllib2.urlopen("http://www.uk-postcodes.com/postcode/%s.json" % (urllib.quote(postcode.replace(" ", ""))))
        respJson = json.loads(resp.read())
        resp.close()
        if 'geo' in respJson:
            return (respJson['geo']['lat'], respJson['geo']['lng'])
        else:
            return None
    except urllib2.HTTPError as e:
        print "Warning: HTTP error resolving postcode %s - %s" % (postcode, e)
        return None
    except urllib2.URLError as e:
        print "Warning: URL opening error resolving postcode %s - %s" % (postcode, e)
        return None
    except httplib.BadStatusLine as e:
        print "Warning: BadStatusLine exception resolving postcode %s - %s" % (postcode, e)
        return None
    

main()

