import scraperwiki

import json
import httplib
import lxml.html
import re
import urllib2
from urlparse import urljoin

MEMBER_LIST_URL = 'http://www.gov.mb.ca/legislature/members/alphabetical.html'
FULL_PARTY_NAMES = {
    'NDP': 'New Democratic Party',
    'PC': 'Progressive Conservative',
    '': 'Independent',
    'Liberal': 'Liberal',
}

_r_whitespace = re.compile(r'[^\S\n]+', flags=re.U)
def clean_string(s):
    return _r_whitespace.sub(' ', unicode(s)).strip()

def main():
    root = lxml.html.parse(urllib2.urlopen(MEMBER_LIST_URL)).getroot()
    table = root.cssselect('table[width=496] table[width=537]:contains("Constituency")')[0]
    rows = table.cssselect('tr')[1:]
    assert len(rows) == 57
    for row in rows:
        (namecell, constitcell, partycell) = row.cssselect('td')
        data = {
            'elected_office': 'MLA',
            'source_url': MEMBER_LIST_URL
        }
        data['district_name'] = constitcell.text_content().strip()
        data['party_name'] = FULL_PARTY_NAMES[partycell.text_content().strip()]
        full_name = namecell.text_content().strip()
        if full_name.lower() == 'vacant':
            continue
        (last, first) = full_name.split(',')
        honorific_prefix = "Hon." if "Hon." in first else None
        if honorific_prefix : data['extra'] = json.dumps({'honorific_prefix': honorific_prefix}) 
        data['first_name'] = first.replace('Hon.', '').strip()
        data['last_name'] = last.title().strip()
        data['url'] = urljoin(MEMBER_LIST_URL, namecell.cssselect('a')[0].get('href'))
        scrape_individual(data)
        scraperwiki.sqlite.save(unique_keys=['district_name'], data=data)

def scrape_individual(data):
    try:
        root = lxml.html.parse(urllib2.urlopen(data['url'])).getroot()
    except httplib.BadStatusLine:
        return
    data['photo_url'] = urljoin(data['url'], root.cssselect('img[hspace=30]')[0].get('src'))
    infocell = root.cssselect('td[valign=top]:contains("Office:")')[0]
    data['email'] = infocell.cssselect('a[href^=mailto]')[0].get('href').replace('mailto:', '')
    infotext = re.sub(r'[\r\t]', '', _get_text_from_elem(infocell).strip())
    infotext = re.sub(r'\n\n+', '\n', infotext) # collapse multiple newlines
    # Hack: there's on MLA whose cell phone number is in an odd place and messes up the scraper. Remove it.
    infotext = re.sub(r'Cell:\s*\d\d\d-\d\d\d\d', '', infotext)
    offices = []
    match = re.search(r'Office:(.+?)Phone:\s+(\d\d\d-\d\d\d\d)', infotext, re.S | re.U)
    assert match
    offices.append({
        'postal': clean_string(match.group(1)),
        'tel': '204-' + match.group(2),
        'type': 'legislature'
    })
    if re.search(r'Constituency\s+Office:\s*\S', infotext, re.U):
        match = re.search(r'Constituency\s+Office:(.+?)Phone:\s+(\d\d\d-\d\d\d\d)?', infotext, re.S | re.U)
        assert match
        o = {
            'postal': clean_string(match.group(1)),
            'type': 'constituency'
        }
        if match.group(2):
            o['tel'] = '204-' + match.group(2)
        offices.append(o)
    data['offices'] = json.dumps(offices)

def _get_text_from_elem(elem, include_tail=False):
    # Same as elem.text_content(), but replaces <br> with linebreaks
    return ''.join([
        (elem.text or ''),
        ('\n' if elem.tag == 'br' else ''),
        ''.join([_get_text_from_elem(e, True) for e in elem]),
        (elem.tail if elem.tail and include_tail else '')
    ])
    
if scraperwiki.sqlite.select('name FROM sqlite_master WHERE type="table" AND name="swdata"'):
    scraperwiki.sqlite.execute('DROP TABLE `swdata`')
main()
import scraperwiki

import json
import httplib
import lxml.html
import re
import urllib2
from urlparse import urljoin

MEMBER_LIST_URL = 'http://www.gov.mb.ca/legislature/members/alphabetical.html'
FULL_PARTY_NAMES = {
    'NDP': 'New Democratic Party',
    'PC': 'Progressive Conservative',
    '': 'Independent',
    'Liberal': 'Liberal',
}

_r_whitespace = re.compile(r'[^\S\n]+', flags=re.U)
def clean_string(s):
    return _r_whitespace.sub(' ', unicode(s)).strip()

def main():
    root = lxml.html.parse(urllib2.urlopen(MEMBER_LIST_URL)).getroot()
    table = root.cssselect('table[width=496] table[width=537]:contains("Constituency")')[0]
    rows = table.cssselect('tr')[1:]
    assert len(rows) == 57
    for row in rows:
        (namecell, constitcell, partycell) = row.cssselect('td')
        data = {
            'elected_office': 'MLA',
            'source_url': MEMBER_LIST_URL
        }
        data['district_name'] = constitcell.text_content().strip()
        data['party_name'] = FULL_PARTY_NAMES[partycell.text_content().strip()]
        full_name = namecell.text_content().strip()
        if full_name.lower() == 'vacant':
            continue
        (last, first) = full_name.split(',')
        honorific_prefix = "Hon." if "Hon." in first else None
        if honorific_prefix : data['extra'] = json.dumps({'honorific_prefix': honorific_prefix}) 
        data['first_name'] = first.replace('Hon.', '').strip()
        data['last_name'] = last.title().strip()
        data['url'] = urljoin(MEMBER_LIST_URL, namecell.cssselect('a')[0].get('href'))
        scrape_individual(data)
        scraperwiki.sqlite.save(unique_keys=['district_name'], data=data)

def scrape_individual(data):
    try:
        root = lxml.html.parse(urllib2.urlopen(data['url'])).getroot()
    except httplib.BadStatusLine:
        return
    data['photo_url'] = urljoin(data['url'], root.cssselect('img[hspace=30]')[0].get('src'))
    infocell = root.cssselect('td[valign=top]:contains("Office:")')[0]
    data['email'] = infocell.cssselect('a[href^=mailto]')[0].get('href').replace('mailto:', '')
    infotext = re.sub(r'[\r\t]', '', _get_text_from_elem(infocell).strip())
    infotext = re.sub(r'\n\n+', '\n', infotext) # collapse multiple newlines
    # Hack: there's on MLA whose cell phone number is in an odd place and messes up the scraper. Remove it.
    infotext = re.sub(r'Cell:\s*\d\d\d-\d\d\d\d', '', infotext)
    offices = []
    match = re.search(r'Office:(.+?)Phone:\s+(\d\d\d-\d\d\d\d)', infotext, re.S | re.U)
    assert match
    offices.append({
        'postal': clean_string(match.group(1)),
        'tel': '204-' + match.group(2),
        'type': 'legislature'
    })
    if re.search(r'Constituency\s+Office:\s*\S', infotext, re.U):
        match = re.search(r'Constituency\s+Office:(.+?)Phone:\s+(\d\d\d-\d\d\d\d)?', infotext, re.S | re.U)
        assert match
        o = {
            'postal': clean_string(match.group(1)),
            'type': 'constituency'
        }
        if match.group(2):
            o['tel'] = '204-' + match.group(2)
        offices.append(o)
    data['offices'] = json.dumps(offices)

def _get_text_from_elem(elem, include_tail=False):
    # Same as elem.text_content(), but replaces <br> with linebreaks
    return ''.join([
        (elem.text or ''),
        ('\n' if elem.tag == 'br' else ''),
        ''.join([_get_text_from_elem(e, True) for e in elem]),
        (elem.tail if elem.tail and include_tail else '')
    ])
    
if scraperwiki.sqlite.select('name FROM sqlite_master WHERE type="table" AND name="swdata"'):
    scraperwiki.sqlite.execute('DROP TABLE `swdata`')
main()
