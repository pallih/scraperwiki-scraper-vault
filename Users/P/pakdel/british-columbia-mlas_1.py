import scraperwiki

import json
import lxml.html
import re
import urllib2
from urlparse import urljoin


MEMBER_LIST_BASE_URL = 'http://www.leg.bc.ca/mla/'
MEMBER_LIST_PAGE = '3-1-6.htm'

def _get_text_from_elem(elem, include_tail=False):
    # Same as elem.text_content(), but replaces <br> with linebreaks
    return ''.join([
        (elem.text or ''),
        ('\n' if elem.tag == 'br' else ''),
        ''.join([_get_text_from_elem(e, True) for e in elem]),
        (elem.tail if elem.tail and include_tail else '')
    ])

def main():
    source_url = MEMBER_LIST_BASE_URL + MEMBER_LIST_PAGE
    root = lxml.html.parse(urllib2.urlopen(source_url)).getroot()
    table = root.cssselect('table.text')[0]
    rows = table.cssselect('tr')[1:]
    assert 82 < len(rows) <= 85

    for row in rows:
        (mlapartycell, constituencycell) = row.cssselect('td')
        name = mlapartycell.cssselect('a')[0].text_content().strip()
        if name.upper() == 'VACANT':
            continue

        full_name = re.match( r"^(van |de |Mac|Mc|O')?([A-Z ]+)(, Q\.C\.)?,\s*(.+)$", 
                    re.sub( r'(Dr|Hon)\.\s', ' ', name )).groups('')
        data = {
            'elected_office': 'MLA',
            'first_name': full_name[3],
            'last_name': full_name[0] + full_name[1].title(),
            'source_url': source_url,
            'url': MEMBER_LIST_BASE_URL + mlapartycell.cssselect('a')[0].get('href'),
            'party_name': re.search(r'[\s\r\n]*\(([^)]+)\)\s*$', mlapartycell.text_content()).group(1),
            'district_name': constituencycell.text_content().strip(),
        }

        offices = []
        scrape_extended_info(data, offices)
        data['offices'] = json.dumps(offices)
        scraperwiki.sqlite.save(unique_keys=['district_name'], data=data)        
          
def scrape_extended_info(data, offices):
    """Scrapes further information on a politician from that politician's detail page.
    Gets the URL from data['url'], and writes results to the data dict."""
    root = lxml.html.parse(urllib2.urlopen(data['url'])).getroot()
    img = root.cssselect('table:not(.noprint) tr td img[alt^="Photo of MLA"]')
    if len(img) < 1:
        img = root.cssselect('table:not(.noprint) tr td img[width="150"][height="200"]')
    base = re.sub(r'[^/]+$', '', data['url'])
    data['photo_url'] = urljoin(base, img[0].get('src'))


    email_cell = root.cssselect('table:not(.noprint) tr td.text a[href^=mailto]')[0]
    data['email'] = email_cell.get('href').replace('mailto:', '')

    website_cell = email_cell.getparent().cssselect('a[href^="javascript:decision"]')
    if len(website_cell) > 0:
        data['personal_url'] = website_cell[0].text_content().strip()
        if not re.match( r'https?://', data['personal_url']):
            data['personal_url'] = 'http://' + data['personal_url']

    parent_table = email_cell.getparent().getparent().getparent()
    address = parent_table.cssselect('td:not(a[href^=mailto])[colspan=2]:contains(":")')
    tels = parent_table.cssselect('td p:contains("Phone:")')
    faxes = parent_table.cssselect('td p:contains("Fax:")')
    for i in range(min(len(address),len(tels))):
        tmp_office = {}

        postal = re.sub( r'[^\S\n]+', ' ',
                 re.sub( r'^[^:]*[:,\s]+', '', _get_text_from_elem(address[i]).strip() ))
        if postal != 'TBD':
            tmp_office['postal'] = re.sub(r'[\n ]*\n[\n ]*', "\n", re.sub(r', BC\s+', ' BC  ', postal))

        office_type = re.sub( r'\s+', ' ',
                      re.match( r'([^:]*):', address[i].text_content()).group(1).strip() ).lower()
        if office_type == 'office':
            office_type = 'legislature'
        # "Constituency" may be followed by "Office" or preceded by a municipality name.
        if office_type.find('constituency') != -1:
            office_type = 'constituency'
        if office_type != 'TBD':
            tmp_office['type'] = office_type

        tel = tels[i].getparent().itersiblings('td').next().text_content().strip()
        if tel != 'TBD':
            tmp_office['tel'] = tel

        if len(faxes) > i:
            fax = faxes[i].getparent().itersiblings('td').next().text_content().strip()
            if fax != 'TBD':
                tmp_office['fax'] = fax

        if len(tmp_office) > 1:
            offices.append(tmp_office)

if scraperwiki.sqlite.select('name FROM sqlite_master WHERE type="table" AND name="swdata"'):
    scraperwiki.sqlite.execute('DROP TABLE `swdata`')
main()