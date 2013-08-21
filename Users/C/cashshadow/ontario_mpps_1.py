import scraperwiki 
import lxml.html
import re
import urllib2
from urlparse import urljoin
import json

MEMBER_ROOT_URL = 'http://www.ontla.on.ca/web/members/'
MEMBER_ROOT_IMG_URL = 'http://www.ontla.on.ca/web/'
MEMBER_CURR_LIST_URL = MEMBER_ROOT_URL + 'members_current.do?locale=en'

def main():
    root = lxml.html.parse(urllib2.urlopen(MEMBER_CURR_LIST_URL)).getroot()
    table = root.cssselect('div.tablebody')[0]
    rows = table.cssselect('tr')[0:]
    # If vacant seats, assertion will fail:
    #assert len(rows) == 107
    
    for row in rows:

        data = {
            'elected_office' : 'MPP',
            'source_url': MEMBER_CURR_LIST_URL
            } 

        riding = row.cssselect('td.ridingcell')[0].text_content().strip()
        data['district_name'] = riding

        nameUrlCell = row.cssselect('td.mppcell')[0]
        name = nameUrlCell.cssselect('a')[0].text_content().strip()
        name = name.replace("&nbsp;", ' ')
        name_parts = name.split(',')
        name = name_parts[1].strip() + ' ' + name_parts[0].strip()
        prefix = 'Hon.' if 'Hon ' in name else None
        name = name.replace('Hon ', '')
        data['name'] = name
        data['extra'] = {}
        if prefix:
            data['extra']['honorific_prefix'] = prefix
        data['url'] = urljoin(MEMBER_ROOT_URL, nameUrlCell.cssselect('a')[0].get('href'))
        
        scrape_extended_info(data)
        data['extra'] = json.dumps(data['extra'])
        scraperwiki.sqlite.save(unique_keys=['district_name'], data=data)

def scrape_extended_info(data):
    """Scrapes further information on a politician from that politician's detail page.
      Gets the URL from data['url'], and writes results to the data dict."""
    root = lxml.html.parse(urllib2.urlopen(data['url'])).getroot()
    content = root.cssselect('div#contentArea')[0]
    
    data['photo_url'] = urljoin(MEMBER_ROOT_IMG_URL, content.cssselect('img.mppimg')[0].get('src'))
    try:
        emailCell = content.cssselect('div.email')[0]
        data['email'] = emailCell.cssselect('a')[0].text_content().strip()
    except IndexError:
        if data['name'] == 'Steven Del Duca':
            data['email'] = 'sdelduca.mpp.co@liberal.ola.org'
        pass
        
    rolesPartyCell = content.cssselect('div.mppinfoblock p')
    roles = []

    for idx, row in enumerate(rolesPartyCell):
        if idx + 1 == len(rolesPartyCell):
            data['party_name'] = content.cssselect('div.mppinfoblock p')[idx].text_content().strip()
        else:
            roles.append(content.cssselect('div.mppinfoblock p')[idx].text_content().strip())

    data['extra']['roles'] = roles

if scraperwiki.sqlite.select('name FROM sqlite_master WHERE type="table" AND name="swdata"'):
    scraperwiki.sqlite.execute('DROP TABLE `swdata`')
main()
