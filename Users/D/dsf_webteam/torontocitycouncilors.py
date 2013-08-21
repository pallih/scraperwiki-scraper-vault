import scraperwiki

import json
import lxml.html
import urlparse

import re
import pprint

#phone_re = re.compile(r"Phone:\s*(\d{3}-\d{3}-\d{4})")
phone_re = re.compile(r"Phone:\s*(\d{3}-\d{3}-\S{4})") #nasty workaround for 416-397-FORD
mailto_re = re.compile(r"^mailto:(\S+)$")

def contact_data_from_blob(item, current_data = {}):
    data = {}
    profile_text = item.text_content()
    phone_search = phone_re.search(profile_text)
    if phone_search:
        data['offices'] = json.dumps([{"tel": phone_search.group(1)}])
    mail_link_candidates = item.cssselect('a')
    for link in mail_link_candidates:
        href = link.get('href', default='')
        mail_match = mailto_re.match(href)
        if mail_match:
            data['email'] = mail_match.group(1)
    return data

def parse_councilor(councilor_url):
    councilor_data = {}
    
    councilor_data['source_url'] = councilor_data['url'] = councilor_url
    councilor_data['elected_office'] = "Councillor"
    
    html = scraperwiki.scrape(councilor_url)
    root = lxml.html.fromstring(html)
    
    name_label = root.cssselect('.main h3')[0].text
    name_re = re.compile(r"^Councillor (.+)$")
    name_match = name_re.match(name_label)
    councilor_data['name'] = name_match.group(1)
    
    ward_link_re = re.compile(r"^/wards2000/ward(\d+).htm$")
    ward_label_re = re.compile(r"^Ward (\d+) (.+)$")
    
    for link in root.cssselect('.main a'):
        url = link.attrib.get('href')
        
        ward_link_match = ward_link_re.match(url)
        if (ward_link_match and 'district_id' not in councilor_data):
            councilor_data['district_id'] = int( ward_link_match.group(1) )
            ward_label_match = ward_label_re.match(link.text_content())
            if (ward_label_match):
                councilor_data['district_name'] = '%s (%d)' % (ward_label_match.group(2), councilor_data['district_id'])
    
    councilor_profile = root.cssselect('.main .two_column .last')[0]
    for item in councilor_profile.cssselect('p'):
        councilor_data.update(contact_data_from_blob(item, current_data = councilor_data))
    
    scraperwiki.sqlite.save(['district_id'], councilor_data)

def parse_mayor(mayor_url, original_mayor_url):
    bio_html = scraperwiki.scrape(mayor_url)
    bio_root = lxml.html.fromstring(bio_html)

    # Follow meta refresh.
    if len(bio_root.cssselect('meta[http-equiv="refresh"]')):
        content = bio_root.cssselect('meta[http-equiv="refresh"]')[0].attrib.get('content', '')
        return parse_mayor(content[content.index('http://'):], mayor_url)
    
    mayor_data = {}
    mayor_data['source_url'] = mayor_url
    mayor_data['elected_office'] = "Mayor"
    mayor_data['district_id'] = 0
    mayor_data['boundary_url'] = '/boundaries/census-subdivisions/3520005/'

    mayor_header = bio_root.cssselect('h1.title')[0]
    mayor_name = re.match(r"^Toronto Mayor (.+)$", mayor_header.text_content())
    if mayor_name:
        mayor_data['name'] = mayor_name.group(1)

    contact_url = urlparse.urljoin(original_mayor_url, 'contact.htm')

    contact_html = scraperwiki.scrape(contact_url)
    contact_root = lxml.html.fromstring(contact_html)

    if len(contact_root.cssselect('meta[http-equiv="refresh"]')):
        content = contact_root.cssselect('meta[http-equiv="refresh"]')[0].attrib.get('content', '')
        contact_url = content[content.index('http://'):]
        contact_html = scraperwiki.scrape(contact_url)
        contact_root = lxml.html.fromstring(contact_html)
        #print contact_url

    contact_blob = contact_root.cssselect('.detail')[0]
    mayor_data.update(contact_data_from_blob(contact_blob))
    
    scraperwiki.sqlite.save(['district_id'], mayor_data)

def main():
    ward_urls = set()
    councilor_urls = set()
    mayor_url = ''
    
    html = scraperwiki.scrape('http://app.toronto.ca/im/council/councillors.jsp')
    root = lxml.html.fromstring(html)
    
    all_links = root.cssselect('a')
    ward_re = re.compile(r"^http://www.toronto.ca/wards2000/ward(\d+).htm$")
    councilor_re = re.compile(r"^http://www.toronto.ca/councillors/([^/]+).htm$")
    mayor_re = re.compile(r"^http://www.toronto.ca/mayor_([^/]+)/([^/]+).htm$") # FIXME: this is a fragile way to match the mayor link

    for link in all_links:
        url = link.attrib.get('href', '')
        if councilor_re.match(url):
            councilor_urls.add(url)
        if mayor_re.match(url):
            mayor_url = url
    
    parse_mayor(mayor_url, mayor_url)
    for councilor_url in councilor_urls:
        parse_councilor(councilor_url)

if scraperwiki.sqlite.select('name FROM sqlite_master WHERE type="table" AND name="swdata"'):
    scraperwiki.sqlite.execute('DROP TABLE `swdata`')
main()
