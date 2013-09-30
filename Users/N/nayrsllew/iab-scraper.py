"""Scraper wiki script to extract data from iabuk.net.

By: Scott B. Bradley, @scott2b, Jan. 23, 2013
For: r2d2c3p0
"""
import lxml.html
import urllib
import urllib2
try:
    import scraperwiki
except ImportError:
    pass

SITE_ROOT = 'http://www.iabuk.net'


def extract_text_content(dom, selector):
    element = dom.cssselect(selector)
    if element:
        return element[0].text_content()
    else:
        return None


def fetch_member_page(link):
    data = { 'iabuk_url':link, 'image_url':None, 'email':None }
    page = urllib2.urlopen(link).read()
    doc = lxml.html.fromstring(page)
    data['name'] = doc.cssselect('#page-title')[0].text_content()
    profile = doc.cssselect('#member-profile')[0]
    image = profile.cssselect('img')
    if image:
        data['image_url'] = image[0].get('src')
        # uncomment below to retrieve file as temp file in home directory
        #opener = urllib.URLopener()
        #opener.retrieve(data['image_url'], data['image_url'].split('/')[-1])
    paragraphs = profile.cssselect('p')
    data['description'] = '\n'.join(p.text_content() for p in paragraphs)
    data['types'] = ';'.join([t.text_content() for t in
        profile.cssselect('a[href*="member_directory_type_filter"]')])
    contact_block = doc.cssselect('.block-contact-details')
    if contact_block:
        info = contact_block[0]
        email = info.cssselect('a[href^="mailto:"]')
        if email:
            data['email'] = email[0].get('href')[len('mailto:'):]
        data['telephone'] = extract_text_content(info,  
            'div.views-field-field-telephone div.field-content')
        data['addr1'] = extract_text_content(info,
            'div.views-field-field-address1 div.field-content')
        data['addr2'] = extract_text_content(info,
            'div.views-field-field-address2 div.field-content')
        data['city'] = extract_text_content(info,
            'div.views-field-field-city div.field-content')
        data['postcode'] = extract_text_content(info,
            'div.views-field-field-postcode div.field-content')
        data['contact name'] = extract_text_content(info,
            'div.views-field-field-contact-name div.field-content')
    return data


def fetch_directory_page(pageno): # 0 indexed, even though 1 indexed in UI
    url = 'http://www.iabuk.net/about/member-directory/all?page=%s'%pageno 
    page = urllib2.urlopen(url).read()
    doc = lxml.html.fromstring(page)
    rows = doc.cssselect('#block-system-main a[href^="%s"]' % '/member-directory/')
    links = set([r.get('href') for r in rows])
    for link in links:
        data = fetch_member_page('%s%s' % (SITE_ROOT, link)) 
        try:
            scraperwiki.sqlite.save(unique_keys=['name'], data=data)
        except NameError:
            print 'Skipping data store: scraperwiki not defined'
            print 'Data:', data


def main():
    for i in range(35, 84):
        fetch_directory_page(i)

main()
"""Scraper wiki script to extract data from iabuk.net.

By: Scott B. Bradley, @scott2b, Jan. 23, 2013
For: r2d2c3p0
"""
import lxml.html
import urllib
import urllib2
try:
    import scraperwiki
except ImportError:
    pass

SITE_ROOT = 'http://www.iabuk.net'


def extract_text_content(dom, selector):
    element = dom.cssselect(selector)
    if element:
        return element[0].text_content()
    else:
        return None


def fetch_member_page(link):
    data = { 'iabuk_url':link, 'image_url':None, 'email':None }
    page = urllib2.urlopen(link).read()
    doc = lxml.html.fromstring(page)
    data['name'] = doc.cssselect('#page-title')[0].text_content()
    profile = doc.cssselect('#member-profile')[0]
    image = profile.cssselect('img')
    if image:
        data['image_url'] = image[0].get('src')
        # uncomment below to retrieve file as temp file in home directory
        #opener = urllib.URLopener()
        #opener.retrieve(data['image_url'], data['image_url'].split('/')[-1])
    paragraphs = profile.cssselect('p')
    data['description'] = '\n'.join(p.text_content() for p in paragraphs)
    data['types'] = ';'.join([t.text_content() for t in
        profile.cssselect('a[href*="member_directory_type_filter"]')])
    contact_block = doc.cssselect('.block-contact-details')
    if contact_block:
        info = contact_block[0]
        email = info.cssselect('a[href^="mailto:"]')
        if email:
            data['email'] = email[0].get('href')[len('mailto:'):]
        data['telephone'] = extract_text_content(info,  
            'div.views-field-field-telephone div.field-content')
        data['addr1'] = extract_text_content(info,
            'div.views-field-field-address1 div.field-content')
        data['addr2'] = extract_text_content(info,
            'div.views-field-field-address2 div.field-content')
        data['city'] = extract_text_content(info,
            'div.views-field-field-city div.field-content')
        data['postcode'] = extract_text_content(info,
            'div.views-field-field-postcode div.field-content')
        data['contact name'] = extract_text_content(info,
            'div.views-field-field-contact-name div.field-content')
    return data


def fetch_directory_page(pageno): # 0 indexed, even though 1 indexed in UI
    url = 'http://www.iabuk.net/about/member-directory/all?page=%s'%pageno 
    page = urllib2.urlopen(url).read()
    doc = lxml.html.fromstring(page)
    rows = doc.cssselect('#block-system-main a[href^="%s"]' % '/member-directory/')
    links = set([r.get('href') for r in rows])
    for link in links:
        data = fetch_member_page('%s%s' % (SITE_ROOT, link)) 
        try:
            scraperwiki.sqlite.save(unique_keys=['name'], data=data)
        except NameError:
            print 'Skipping data store: scraperwiki not defined'
            print 'Data:', data


def main():
    for i in range(35, 84):
        fetch_directory_page(i)

main()
