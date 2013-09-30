# Scrapes the edubase schools database
# http://www.education.gov.uk/edubase/public/quickSearchResult.xhtml

import scraperwiki
import requests
import lxml.html
import re

def details(urn):
    print 'http://www.education.gov.uk/edubase/establishment/summary.xhtml?urn=%s' % urn
    html = requests.get('http://www.education.gov.uk/edubase/establishment/summary.xhtml?urn=%s' % urn).text
    dom = lxml.html.fromstring(html)
    data = {
        'name': dom.cssselect('.tabContent .vcard .org')[0].text,
        'urn': int(urn),
        'local_authority': find(r'LA: \d+ (.+)Establishment', dom.cssselect('.tabContent p')[1].text_content(), 1),
        'local_authority_no': find(r'LA: (\d+)', dom.cssselect('.tabContent p')[1].text_content(), 1),
        'establishment_no': find(r'No: (\d+)', dom.cssselect('.tabContent p')[1].text_content(), 1),
        'status': find(r'Status: ([A-Za-z, ]+)', dom.cssselect('.tabContent p')[0].text_content(), 1),
        'local_authority_gss': find(r'[A-Z0-9]+$', dom.cssselect('.tabContent p')[2].text_content(), 0),
        'street': dom.cssselect('.tabContent .vcard .street-address')[0].text,
        'locality': dom.cssselect('.tabContent .vcard .locality')[0].text,
        'region': dom.cssselect('.tabContent .vcard .region')[0].text,
        'postcode': dom.cssselect('.tabContent .vcard .postal-code')[0].text,
        'lat': None,
        'lng': None,
        'country': dom.cssselect('.tabContent .vcard .country-name')[0].text,
        'phase': details_panel_value(dom, 'Phase of Education'),
        'age_min': None,
        'age_max': None,
        'gender': details_panel_value(dom, 'Gender'),
        'children': details_panel_value(dom, 'Total Number of Children')
    }

    ages = re.findall(r'(\d+)\D+(\d+)', details_panel_value(dom, 'Age Range'))
    if ages:
        data['age_min'] = ages[0][0]
        data['age_max'] = ages[0][1]

    if data['phase'] == 'Not applicable': 
        data['phase'] = None

    return data

def find(regexp, string, group, ):
    results = re.search(regexp, string)
    if results:
        return results.group(group).strip()
    else:
        return False

def details_panel_value(dom, key):
    table = dom.cssselect('table.details')[1]
    for tr in table.cssselect('tr'):
        if tr.cssselect('th')[0].text == key:
            return tr.cssselect('td')[0].text
            break
    return None

def create_table():
    scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS `establishments` (`urn` integer primary key, `establishment_no` integer, `name` text, `local_authority` text, `local_authority_no` integer, `local_authority_gss` text, `status` text, `street` text, `locality` text, `region` text, `country` text, `postcode` text, `lat` integer, `lng` integer, `age_min` integer, `age_max` integer, `children` integer, `gender` text, `phase` text)')
    scraperwiki.sqlite.commit()

def geocode_postcode(postcode, provider='geonames'):
    import urllib2, json
    if provider=='geonames':
        resp = scraperwiki.scrape('http://api.geonames.org/postalCodeSearchJSON?postalcode=%s&maxRows=1&username=scraperwiki' % urllib2.quote(postcode))
        obj = json.loads(resp)
        if 'postalCodes' in obj and len(obj['postalCodes']):
            return (obj['postalCodes'][0]['lat'], obj['postalCodes'][0]['lng'])
        else:
            return (None,None)
    elif provider=='mapit':
        try:
            resp = scraperwiki.scrape('http://mapit.mysociety.org/postcode/%s.json' % urllib2.quote(postcode))
        except urllib2.HTTPError:
            return (None, None)
        else:
            obj = json.loads(resp)
            if 'wgs84_lat' in obj and 'wgs84_lon' in obj:
                return (obj['wgs84_lat'], obj['wgs84_lon'])
            else:
                return (None,None)
    elif provider=='jamiethompson':
        import requests
        try:
            resp = requests.get('http://geo.jamiethompson.co.uk/%s.json' % postcode.replace(' ',''), timeout=5).text
        except:
            return (None,None)
        else:
            obj = json.loads(resp)
            if 'geo' in obj and 'lat' in obj['geo'] and 'lng' in obj['geo']:
                return (obj['geo']['lat'], obj['geo']['lng'])
            else:
                return (None,None)
    else:
        return(None, None)

def scrape():
    # 1) get summary figures (total schools, total pages)
    html = requests.get('http://www.education.gov.uk/edubase/public/quickSearchResult.xhtml', verify=False).text
    dom = lxml.html.fromstring(html)
    
    total_establishments = int(re.findall(r'\d+', dom.cssselect('.article .tdSpacer>p')[1].text_content())[0])
    total_pages = int(re.findall(r'\d+', dom.cssselect('p.pagecount')[0].text)[1])
    print total_establishments, 'establishments, over', total_pages, 'pages'
    
    start_page = scraperwiki.sqlite.get_var('last_page_scraped', 0) + 1
    
    # 2) loop through each page, setting aside the URNs, then scraping the details page for each
    for page_number in range(start_page,total_pages+1):
        data = []
        print 'http://www.education.gov.uk/edubase/public/quickSearchResult.xhtml?page=%s' % page_number
        html = requests.get('http://www.education.gov.uk/edubase/public/quickSearchResult.xhtml?page=%s' % page_number, verify=False).text
        dom = lxml.html.fromstring(html)
        for tr in dom.cssselect('table.search_results tbody tr'):
            data.append(details(re.findall(r'\d+$', tr.cssselect('a')[0].get('href'))[0]))
        print 'SAVING'
        scraperwiki.sqlite.save(['urn'], data, 'establishments')
        scraperwiki.sqlite.save_var('last_page_scraped', page_number)

def geocode():
    data = []
    results = scraperwiki.sqlite.execute('select urn, postcode, name from establishments where lat is null and postcode is not null')['data']
    for i in range(0, len(results)):
        lat = lng = None
        (lat, lng) = geocode_postcode(results[i][1])
        if not lat:
            (lat, lng) = geocode_postcode(results[i][1], 'mapit')
        if not lat:
            (lat, lng) = geocode_postcode(results[i][1], 'jamiethompson')
        if lat:
            print 'geocoded', results[i][2], '(', results[i][1], ')'
            data.append({
                'urn': results[i][0],
                'lat': lat,
                'lng': lng
            })
        else:
            print 'could not geocode', results[i][1]
        if len(data) == 20:
            print 'Saving', len(data), 'rows'
            for d in data:
                scraperwiki.sqlite.execute("UPDATE establishments SET lat='%s', lng='%s' WHERE urn='%s'" % (d['lat'], d['lng'], d['urn']))
            scraperwiki.sqlite.commit()
            data = []

    if data:
        print 'Saving', len(data), 'rows'
        for d in data:
            scraperwiki.sqlite.execute("UPDATE establishments SET lat='%s', lng='%s' WHERE urn='%s'" % (d['lat'], d['lng'], d['urn']))
        scraperwiki.sqlite.commit()
        data = []

#scrape()
geocode()




# Scrapes the edubase schools database
# http://www.education.gov.uk/edubase/public/quickSearchResult.xhtml

import scraperwiki
import requests
import lxml.html
import re

def details(urn):
    print 'http://www.education.gov.uk/edubase/establishment/summary.xhtml?urn=%s' % urn
    html = requests.get('http://www.education.gov.uk/edubase/establishment/summary.xhtml?urn=%s' % urn).text
    dom = lxml.html.fromstring(html)
    data = {
        'name': dom.cssselect('.tabContent .vcard .org')[0].text,
        'urn': int(urn),
        'local_authority': find(r'LA: \d+ (.+)Establishment', dom.cssselect('.tabContent p')[1].text_content(), 1),
        'local_authority_no': find(r'LA: (\d+)', dom.cssselect('.tabContent p')[1].text_content(), 1),
        'establishment_no': find(r'No: (\d+)', dom.cssselect('.tabContent p')[1].text_content(), 1),
        'status': find(r'Status: ([A-Za-z, ]+)', dom.cssselect('.tabContent p')[0].text_content(), 1),
        'local_authority_gss': find(r'[A-Z0-9]+$', dom.cssselect('.tabContent p')[2].text_content(), 0),
        'street': dom.cssselect('.tabContent .vcard .street-address')[0].text,
        'locality': dom.cssselect('.tabContent .vcard .locality')[0].text,
        'region': dom.cssselect('.tabContent .vcard .region')[0].text,
        'postcode': dom.cssselect('.tabContent .vcard .postal-code')[0].text,
        'lat': None,
        'lng': None,
        'country': dom.cssselect('.tabContent .vcard .country-name')[0].text,
        'phase': details_panel_value(dom, 'Phase of Education'),
        'age_min': None,
        'age_max': None,
        'gender': details_panel_value(dom, 'Gender'),
        'children': details_panel_value(dom, 'Total Number of Children')
    }

    ages = re.findall(r'(\d+)\D+(\d+)', details_panel_value(dom, 'Age Range'))
    if ages:
        data['age_min'] = ages[0][0]
        data['age_max'] = ages[0][1]

    if data['phase'] == 'Not applicable': 
        data['phase'] = None

    return data

def find(regexp, string, group, ):
    results = re.search(regexp, string)
    if results:
        return results.group(group).strip()
    else:
        return False

def details_panel_value(dom, key):
    table = dom.cssselect('table.details')[1]
    for tr in table.cssselect('tr'):
        if tr.cssselect('th')[0].text == key:
            return tr.cssselect('td')[0].text
            break
    return None

def create_table():
    scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS `establishments` (`urn` integer primary key, `establishment_no` integer, `name` text, `local_authority` text, `local_authority_no` integer, `local_authority_gss` text, `status` text, `street` text, `locality` text, `region` text, `country` text, `postcode` text, `lat` integer, `lng` integer, `age_min` integer, `age_max` integer, `children` integer, `gender` text, `phase` text)')
    scraperwiki.sqlite.commit()

def geocode_postcode(postcode, provider='geonames'):
    import urllib2, json
    if provider=='geonames':
        resp = scraperwiki.scrape('http://api.geonames.org/postalCodeSearchJSON?postalcode=%s&maxRows=1&username=scraperwiki' % urllib2.quote(postcode))
        obj = json.loads(resp)
        if 'postalCodes' in obj and len(obj['postalCodes']):
            return (obj['postalCodes'][0]['lat'], obj['postalCodes'][0]['lng'])
        else:
            return (None,None)
    elif provider=='mapit':
        try:
            resp = scraperwiki.scrape('http://mapit.mysociety.org/postcode/%s.json' % urllib2.quote(postcode))
        except urllib2.HTTPError:
            return (None, None)
        else:
            obj = json.loads(resp)
            if 'wgs84_lat' in obj and 'wgs84_lon' in obj:
                return (obj['wgs84_lat'], obj['wgs84_lon'])
            else:
                return (None,None)
    elif provider=='jamiethompson':
        import requests
        try:
            resp = requests.get('http://geo.jamiethompson.co.uk/%s.json' % postcode.replace(' ',''), timeout=5).text
        except:
            return (None,None)
        else:
            obj = json.loads(resp)
            if 'geo' in obj and 'lat' in obj['geo'] and 'lng' in obj['geo']:
                return (obj['geo']['lat'], obj['geo']['lng'])
            else:
                return (None,None)
    else:
        return(None, None)

def scrape():
    # 1) get summary figures (total schools, total pages)
    html = requests.get('http://www.education.gov.uk/edubase/public/quickSearchResult.xhtml', verify=False).text
    dom = lxml.html.fromstring(html)
    
    total_establishments = int(re.findall(r'\d+', dom.cssselect('.article .tdSpacer>p')[1].text_content())[0])
    total_pages = int(re.findall(r'\d+', dom.cssselect('p.pagecount')[0].text)[1])
    print total_establishments, 'establishments, over', total_pages, 'pages'
    
    start_page = scraperwiki.sqlite.get_var('last_page_scraped', 0) + 1
    
    # 2) loop through each page, setting aside the URNs, then scraping the details page for each
    for page_number in range(start_page,total_pages+1):
        data = []
        print 'http://www.education.gov.uk/edubase/public/quickSearchResult.xhtml?page=%s' % page_number
        html = requests.get('http://www.education.gov.uk/edubase/public/quickSearchResult.xhtml?page=%s' % page_number, verify=False).text
        dom = lxml.html.fromstring(html)
        for tr in dom.cssselect('table.search_results tbody tr'):
            data.append(details(re.findall(r'\d+$', tr.cssselect('a')[0].get('href'))[0]))
        print 'SAVING'
        scraperwiki.sqlite.save(['urn'], data, 'establishments')
        scraperwiki.sqlite.save_var('last_page_scraped', page_number)

def geocode():
    data = []
    results = scraperwiki.sqlite.execute('select urn, postcode, name from establishments where lat is null and postcode is not null')['data']
    for i in range(0, len(results)):
        lat = lng = None
        (lat, lng) = geocode_postcode(results[i][1])
        if not lat:
            (lat, lng) = geocode_postcode(results[i][1], 'mapit')
        if not lat:
            (lat, lng) = geocode_postcode(results[i][1], 'jamiethompson')
        if lat:
            print 'geocoded', results[i][2], '(', results[i][1], ')'
            data.append({
                'urn': results[i][0],
                'lat': lat,
                'lng': lng
            })
        else:
            print 'could not geocode', results[i][1]
        if len(data) == 20:
            print 'Saving', len(data), 'rows'
            for d in data:
                scraperwiki.sqlite.execute("UPDATE establishments SET lat='%s', lng='%s' WHERE urn='%s'" % (d['lat'], d['lng'], d['urn']))
            scraperwiki.sqlite.commit()
            data = []

    if data:
        print 'Saving', len(data), 'rows'
        for d in data:
            scraperwiki.sqlite.execute("UPDATE establishments SET lat='%s', lng='%s' WHERE urn='%s'" % (d['lat'], d['lng'], d['urn']))
        scraperwiki.sqlite.commit()
        data = []

#scrape()
geocode()




