import scraperwiki

import json
import lxml.html
import re
import urllib2
from urlparse import urljoin

MEMBER_LIST_URL = 'http://www.assembly.pe.ca/index.php3?number=1024584&lang=E'
FULL_PARTY_NAMES = {
    'PC': 'Progressive Conservative',
    'LIB': 'Liberal'
}

def main():
    root = lxml.html.parse(urllib2.urlopen(MEMBER_LIST_URL)).getroot()
    table = root.cssselect('table')[0]
    rows = table.cssselect('tr')[1:]
    assert len(rows) == 27 # There should be 27 districts

    for row in rows:
        (districtnumcell, districtcell, membercell, dummy2) = row.cssselect('td')
    
        data = {
            'elected_office': 'MLA',
            'source_url': MEMBER_LIST_URL
        }
        data['district_id'] = districtnumcell.text_content().strip()
        data['district_name'] = districtcell.cssselect('a')[0].text_content().strip()
        data['name'] = membercell.cssselect('a')[0].text_content().replace('Hon. ', '')\
            .replace(' (LIB)', '').replace(' (PC)', '').strip()
        data['url'] = urljoin(MEMBER_LIST_URL, membercell.cssselect('a')[0].get('href'))
        data['party_name'] = FULL_PARTY_NAMES[re.search(r'\(([A-Z]+)\)', membercell.text_content()).group(1)]
        prefix = 'Hon.' if 'Hon.' in membercell.cssselect('a')[0].text_content() else None
        if prefix: data['extra'] = json.dumps({'honorific_prefix': prefix })
        scrape_extended_info(data)
        scraperwiki.sqlite.save(unique_keys=['district_id'], data=data)

_r_whitespace = re.compile(r'[^\S\n]+', flags=re.U)
def clean_string(s):
    return _r_whitespace.sub(' ', unicode(s)).strip()

def scrape_extended_info(data):
    """Scrapes further information on a politician from that politician's detail page.
    Gets the URL from data['url'], and writes results to the data dict."""
    root = lxml.html.parse(urllib2.urlopen(data['url'])).getroot()
    main = root.cssselect('#content table')[0]
    data['photo_url'] = urljoin(data['url'], main.cssselect('img')[0].get('src'))
    contact_cell = main.cssselect('td:contains("Contact information")')[0]
    offices = [{
        'postal': clean_string(re.search(r'Mailing\s+address:\s+(.+?)Office\s+address', contact_cell.text_content(), re.U | re.S).group(1)),
        'tel': clean_string(re.search(r'(?:Telephone|Tel|Phone):(.+?)\n', contact_cell.text_content()).group(1))
    }]
    data['offices'] = json.dumps(offices)
    data['email'] = contact_cell.cssselect('a[href^=mailto]')[0].get('href').replace('mailto:', '')

if scraperwiki.sqlite.select('name FROM sqlite_master WHERE type="table" AND name="swdata"'):
    scraperwiki.sqlite.execute('DROP TABLE `swdata`')
main()
import scraperwiki

import json
import lxml.html
import re
import urllib2
from urlparse import urljoin

MEMBER_LIST_URL = 'http://www.assembly.pe.ca/index.php3?number=1024584&lang=E'
FULL_PARTY_NAMES = {
    'PC': 'Progressive Conservative',
    'LIB': 'Liberal'
}

def main():
    root = lxml.html.parse(urllib2.urlopen(MEMBER_LIST_URL)).getroot()
    table = root.cssselect('table')[0]
    rows = table.cssselect('tr')[1:]
    assert len(rows) == 27 # There should be 27 districts

    for row in rows:
        (districtnumcell, districtcell, membercell, dummy2) = row.cssselect('td')
    
        data = {
            'elected_office': 'MLA',
            'source_url': MEMBER_LIST_URL
        }
        data['district_id'] = districtnumcell.text_content().strip()
        data['district_name'] = districtcell.cssselect('a')[0].text_content().strip()
        data['name'] = membercell.cssselect('a')[0].text_content().replace('Hon. ', '')\
            .replace(' (LIB)', '').replace(' (PC)', '').strip()
        data['url'] = urljoin(MEMBER_LIST_URL, membercell.cssselect('a')[0].get('href'))
        data['party_name'] = FULL_PARTY_NAMES[re.search(r'\(([A-Z]+)\)', membercell.text_content()).group(1)]
        prefix = 'Hon.' if 'Hon.' in membercell.cssselect('a')[0].text_content() else None
        if prefix: data['extra'] = json.dumps({'honorific_prefix': prefix })
        scrape_extended_info(data)
        scraperwiki.sqlite.save(unique_keys=['district_id'], data=data)

_r_whitespace = re.compile(r'[^\S\n]+', flags=re.U)
def clean_string(s):
    return _r_whitespace.sub(' ', unicode(s)).strip()

def scrape_extended_info(data):
    """Scrapes further information on a politician from that politician's detail page.
    Gets the URL from data['url'], and writes results to the data dict."""
    root = lxml.html.parse(urllib2.urlopen(data['url'])).getroot()
    main = root.cssselect('#content table')[0]
    data['photo_url'] = urljoin(data['url'], main.cssselect('img')[0].get('src'))
    contact_cell = main.cssselect('td:contains("Contact information")')[0]
    offices = [{
        'postal': clean_string(re.search(r'Mailing\s+address:\s+(.+?)Office\s+address', contact_cell.text_content(), re.U | re.S).group(1)),
        'tel': clean_string(re.search(r'(?:Telephone|Tel|Phone):(.+?)\n', contact_cell.text_content()).group(1))
    }]
    data['offices'] = json.dumps(offices)
    data['email'] = contact_cell.cssselect('a[href^=mailto]')[0].get('href').replace('mailto:', '')

if scraperwiki.sqlite.select('name FROM sqlite_master WHERE type="table" AND name="swdata"'):
    scraperwiki.sqlite.execute('DROP TABLE `swdata`')
main()
