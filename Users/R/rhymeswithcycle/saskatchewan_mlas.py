import scraperwiki

import json
import lxml.html
import re
import urllib2
from urlparse import urljoin

MEMBER_LIST_URL = 'http://www.legassembly.sk.ca/mlas/'
MALE_HONORIFICS = ['Mr.']
FEMALE_HONORIFICS = ['Ms.', 'Mrs.', 'Miss']

def main():
    root = lxml.html.parse(urllib2.urlopen(MEMBER_LIST_URL)).getroot()
    rows = root.cssselect('table#MLAs tr')[1:]
    assert len(rows) == 58
    for row in rows:
        data = {
            'elected_office': 'MLA',
            'source_url': MEMBER_LIST_URL
        }
        (namecell, partycell, districtcell) = row.cssselect('td')
        data['district_name'] = districtcell.text_content().strip()
        data['party_name'] = partycell.text_content().strip()
        name_parts = namecell.cssselect('a')[0].text_content().strip().split(' ')
        assert name_parts[0].endswith('.')
        data['name'] = ' '.join(name_parts[1:])
        if name_parts[0] in MALE_HONORIFICS:
            data['gender'] = 'M'
        elif name_parts[0] in FEMALE_HONORIFICS:
            data['gender'] = 'F'
        data['extra'] = json.dumps({'honorific_prefix': name_parts[0]})
        data['url'] = urljoin(MEMBER_LIST_URL, namecell.cssselect('a')[0].get('href'))
        scrape_individual(data)
        scraperwiki.sqlite.save(unique_keys=['district_name'], data=data)

def scrape_individual(data):
    root = lxml.html.parse(urllib2.urlopen(data['url'])).getroot()
    leg_address = root.cssselect('#mla-contact td.large-column:contains("Legislative Building Address")')[0].text_content()
    leg_phone = re.search(r'Phone:\s*(\d\d\d-\d\d\d\d)', leg_address).group(1)
    offices = [{'type': 'legislature', 'tel': '306-' + leg_phone}]

    constit_address = root.cssselect('#mla-contact td.large-column:contains("Constituency Address")')[0].text_content()
    if len(re.sub(r'(Constituency Address|Phone:|Fax:|\s|,)', '', constit_address)) > 20: # This should get rid of vestigial non-addresses
        constit_address = re.sub(r'(Constituency Address|[\r\t])', '', constit_address).strip()
        o = {
            'type': 'constituency',
            'postal': re.search(r'^(.+?)Phone:', constit_address, re.S).group(1),
        }
        try:
            o['tel'] = '306-' + re.search(r'Phone:\s*(\d\d\d-\d\d\d\d)', constit_address).group(1)
        except AttributeError:
            pass
        offices.append(o)
    data['offices'] = json.dumps(offices)

    online_contact = root.cssselect('#mla-contact td:contains("Online"):not(.large-column)')[0]
    try:
        data['email'] = online_contact.cssselect('a[href^=mailto]')[0].get('href').replace('mailto:', '')
    except IndexError:
        pass
    try:
        data['personal_url'] = online_contact.cssselect('a[href^=http]')[0].get('href')
    except IndexError:
        pass # Some people might not have a URL. That's okay!
    
    data['photo_url'] = urljoin(data['url'], root.cssselect('.mla-image-cell img')[0].get('src'))
    
if scraperwiki.sqlite.select('name FROM sqlite_master WHERE type="table" AND name="swdata"'):
    scraperwiki.sqlite.execute('DROP TABLE `swdata`')
main()
import scraperwiki

import json
import lxml.html
import re
import urllib2
from urlparse import urljoin

MEMBER_LIST_URL = 'http://www.legassembly.sk.ca/mlas/'
MALE_HONORIFICS = ['Mr.']
FEMALE_HONORIFICS = ['Ms.', 'Mrs.', 'Miss']

def main():
    root = lxml.html.parse(urllib2.urlopen(MEMBER_LIST_URL)).getroot()
    rows = root.cssselect('table#MLAs tr')[1:]
    assert len(rows) == 58
    for row in rows:
        data = {
            'elected_office': 'MLA',
            'source_url': MEMBER_LIST_URL
        }
        (namecell, partycell, districtcell) = row.cssselect('td')
        data['district_name'] = districtcell.text_content().strip()
        data['party_name'] = partycell.text_content().strip()
        name_parts = namecell.cssselect('a')[0].text_content().strip().split(' ')
        assert name_parts[0].endswith('.')
        data['name'] = ' '.join(name_parts[1:])
        if name_parts[0] in MALE_HONORIFICS:
            data['gender'] = 'M'
        elif name_parts[0] in FEMALE_HONORIFICS:
            data['gender'] = 'F'
        data['extra'] = json.dumps({'honorific_prefix': name_parts[0]})
        data['url'] = urljoin(MEMBER_LIST_URL, namecell.cssselect('a')[0].get('href'))
        scrape_individual(data)
        scraperwiki.sqlite.save(unique_keys=['district_name'], data=data)

def scrape_individual(data):
    root = lxml.html.parse(urllib2.urlopen(data['url'])).getroot()
    leg_address = root.cssselect('#mla-contact td.large-column:contains("Legislative Building Address")')[0].text_content()
    leg_phone = re.search(r'Phone:\s*(\d\d\d-\d\d\d\d)', leg_address).group(1)
    offices = [{'type': 'legislature', 'tel': '306-' + leg_phone}]

    constit_address = root.cssselect('#mla-contact td.large-column:contains("Constituency Address")')[0].text_content()
    if len(re.sub(r'(Constituency Address|Phone:|Fax:|\s|,)', '', constit_address)) > 20: # This should get rid of vestigial non-addresses
        constit_address = re.sub(r'(Constituency Address|[\r\t])', '', constit_address).strip()
        o = {
            'type': 'constituency',
            'postal': re.search(r'^(.+?)Phone:', constit_address, re.S).group(1),
        }
        try:
            o['tel'] = '306-' + re.search(r'Phone:\s*(\d\d\d-\d\d\d\d)', constit_address).group(1)
        except AttributeError:
            pass
        offices.append(o)
    data['offices'] = json.dumps(offices)

    online_contact = root.cssselect('#mla-contact td:contains("Online"):not(.large-column)')[0]
    try:
        data['email'] = online_contact.cssselect('a[href^=mailto]')[0].get('href').replace('mailto:', '')
    except IndexError:
        pass
    try:
        data['personal_url'] = online_contact.cssselect('a[href^=http]')[0].get('href')
    except IndexError:
        pass # Some people might not have a URL. That's okay!
    
    data['photo_url'] = urljoin(data['url'], root.cssselect('.mla-image-cell img')[0].get('src'))
    
if scraperwiki.sqlite.select('name FROM sqlite_master WHERE type="table" AND name="swdata"'):
    scraperwiki.sqlite.execute('DROP TABLE `swdata`')
main()
