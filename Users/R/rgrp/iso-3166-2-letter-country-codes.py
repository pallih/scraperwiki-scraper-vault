import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re

url = "http://www.iso.org/iso/english_country_names_and_code_elements"

def Main():
    root = lxml.html.parse(url).getroot()
    for tablerow in root.cssselect('tr'):
        tds = tablerow.cssselect('td')
        if not tds:
            continue
        country_name = tds[0].text.strip().title()
        if country_name and not country_name.startswith('see '):
            code = tds[1].text.strip()
            print code, country_name
            scraperwiki.datastore.save(['code'], {'code': code, 'name': country_name})
        
Main()

                        

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re

url = "http://www.iso.org/iso/english_country_names_and_code_elements"

def Main():
    root = lxml.html.parse(url).getroot()
    for tablerow in root.cssselect('tr'):
        tds = tablerow.cssselect('td')
        if not tds:
            continue
        country_name = tds[0].text.strip().title()
        if country_name and not country_name.startswith('see '):
            code = tds[1].text.strip()
            print code, country_name
            scraperwiki.datastore.save(['code'], {'code': code, 'name': country_name})
        
Main()

                        

