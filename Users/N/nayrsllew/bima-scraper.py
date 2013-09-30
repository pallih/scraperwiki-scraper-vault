"""Scraper wiki script to extract data from www.bima.co.uk

By: Scott B. Bradley, @scott2b, Jan. 25, 2013
For: r2d2c3p0
"""
import lxml.html
import requests
import urlparse
try:
    import scraperwiki
except ImportError:
    pass

SITE_ROOT = 'http://www.bima.co.uk'


def fetch_member_page(url):
    data = { 'address':None, 'image_url':None, 'switchboard':None,
        'company_overview':None, 'future_activity':None }
    page = requests.get(url).text 
    doc = lxml.html.fromstring(page)
    data['name'] = doc.cssselect('div.ttl-hold h1')[0].text_content()
    addr = doc.cssselect('div.memberText h2:contains("Address")')
    if addr:
        addr = addr[0].getparent().text_content()
        addr = addr.replace('Address:', '')
        addr = '\n'.join([l.strip() for l in addr.split('\n') if l.strip()])
        data['address'] = addr
    img = doc.cssselect('div.memberImage img')
    if img:
        data['image_url'] = '%s/%s' % (SITE_ROOT, img[0].get('src').strip('./'))
    switchboard = doc.cssselect('h2:contains("Switchboard:")+p')
    if switchboard:
        data['switchboard'] = switchboard[0].text_content()
    overview = doc.cssselect('h2:contains("Company Overview:")+p')
    if overview:
        data['company_overview'] = overview[0].text_content()
    future_activity = doc.cssselect('h2:contains("Future Activity")+p')
    if future_activity:
        data['future_activity'] = future_activity[0].text_content()
    links = doc.cssselect('h2:contains("Links")+ul>li>a')
    for link in links:
        _type = link.text_content().strip().split(' ')[-1]
        href = link.get('href')
        if _type == 'Email':
            href = href[len('mailto:'):]
        data[_type] = href
    return data
   

def fetch_member_pages(doc):
    members = doc.cssselect('div.people-info a')
    for member in members:
        data = fetch_member_page('http://www.bima.co.uk%s' % member.get('href'))
        try:
            scraperwiki.sqlite.save(unique_keys=['name'], data=data)
        except NameError:
            print data


def fetch_directory_response():
    return requests.get('%s/find-a-supplier/directory.asp' % SITE_ROOT)


def extract_locations(doc):
    locations = [ (option.get('value'), option.text_content()) for option in
        doc.cssselect('select#locationID > option') if option.get('value')]
    return locations  


def get_page_links(doc):
    return doc.cssselect('div#memberlisting > ul.listing > li > a')
    

def fetch_location_results(location_id, pageno, cookie):
    url = 'http://www.bima.co.uk/find-a-supplier/directory.asp?pg=%s&id=' % (
        pageno)
    parsed = urlparse.urlparse(url)
    cookies = { cookie[0]:cookie[1] }
    r = requests.post(url, data={'membersearch':'submit',
        'seachterm':'Keywords...', 'locationID':location_id, 'typeID':'',
        'serviceID':'', 'eventsearchbtn':'Search'}, cookies=cookies)
    page = r.text
    doc = lxml.html.fromstring(page)
    fetch_member_pages(doc)
    links = get_page_links(doc)
    current_link = doc.cssselect(
        'div#memberlisting > ul.listing > li > a[href^="?pg=%s"]' % pageno)
    next_link = current_link[0].getparent().getnext()
    if next_link is not None: # else we are on last page
        next_pageno = next_link.find('a').text_content()
        fetch_location_results(location_id, next_pageno, cookie)  
    

def main():
    directory = fetch_directory_response()
    cookie = directory.cookies.items()[0]
    doc = lxml.html.fromstring(directory.text)
    locations = extract_locations(doc)
    for location_id, location_name in locations:
        print 'Fetching results for location: %s' % location_name
        fetch_location_results(location_id, '1', cookie)

main()

"""Scraper wiki script to extract data from www.bima.co.uk

By: Scott B. Bradley, @scott2b, Jan. 25, 2013
For: r2d2c3p0
"""
import lxml.html
import requests
import urlparse
try:
    import scraperwiki
except ImportError:
    pass

SITE_ROOT = 'http://www.bima.co.uk'


def fetch_member_page(url):
    data = { 'address':None, 'image_url':None, 'switchboard':None,
        'company_overview':None, 'future_activity':None }
    page = requests.get(url).text 
    doc = lxml.html.fromstring(page)
    data['name'] = doc.cssselect('div.ttl-hold h1')[0].text_content()
    addr = doc.cssselect('div.memberText h2:contains("Address")')
    if addr:
        addr = addr[0].getparent().text_content()
        addr = addr.replace('Address:', '')
        addr = '\n'.join([l.strip() for l in addr.split('\n') if l.strip()])
        data['address'] = addr
    img = doc.cssselect('div.memberImage img')
    if img:
        data['image_url'] = '%s/%s' % (SITE_ROOT, img[0].get('src').strip('./'))
    switchboard = doc.cssselect('h2:contains("Switchboard:")+p')
    if switchboard:
        data['switchboard'] = switchboard[0].text_content()
    overview = doc.cssselect('h2:contains("Company Overview:")+p')
    if overview:
        data['company_overview'] = overview[0].text_content()
    future_activity = doc.cssselect('h2:contains("Future Activity")+p')
    if future_activity:
        data['future_activity'] = future_activity[0].text_content()
    links = doc.cssselect('h2:contains("Links")+ul>li>a')
    for link in links:
        _type = link.text_content().strip().split(' ')[-1]
        href = link.get('href')
        if _type == 'Email':
            href = href[len('mailto:'):]
        data[_type] = href
    return data
   

def fetch_member_pages(doc):
    members = doc.cssselect('div.people-info a')
    for member in members:
        data = fetch_member_page('http://www.bima.co.uk%s' % member.get('href'))
        try:
            scraperwiki.sqlite.save(unique_keys=['name'], data=data)
        except NameError:
            print data


def fetch_directory_response():
    return requests.get('%s/find-a-supplier/directory.asp' % SITE_ROOT)


def extract_locations(doc):
    locations = [ (option.get('value'), option.text_content()) for option in
        doc.cssselect('select#locationID > option') if option.get('value')]
    return locations  


def get_page_links(doc):
    return doc.cssselect('div#memberlisting > ul.listing > li > a')
    

def fetch_location_results(location_id, pageno, cookie):
    url = 'http://www.bima.co.uk/find-a-supplier/directory.asp?pg=%s&id=' % (
        pageno)
    parsed = urlparse.urlparse(url)
    cookies = { cookie[0]:cookie[1] }
    r = requests.post(url, data={'membersearch':'submit',
        'seachterm':'Keywords...', 'locationID':location_id, 'typeID':'',
        'serviceID':'', 'eventsearchbtn':'Search'}, cookies=cookies)
    page = r.text
    doc = lxml.html.fromstring(page)
    fetch_member_pages(doc)
    links = get_page_links(doc)
    current_link = doc.cssselect(
        'div#memberlisting > ul.listing > li > a[href^="?pg=%s"]' % pageno)
    next_link = current_link[0].getparent().getnext()
    if next_link is not None: # else we are on last page
        next_pageno = next_link.find('a').text_content()
        fetch_location_results(location_id, next_pageno, cookie)  
    

def main():
    directory = fetch_directory_response()
    cookie = directory.cookies.items()[0]
    doc = lxml.html.fromstring(directory.text)
    locations = extract_locations(doc)
    for location_id, location_name in locations:
        print 'Fetching results for location: %s' % location_name
        fetch_location_results(location_id, '1', cookie)

main()

