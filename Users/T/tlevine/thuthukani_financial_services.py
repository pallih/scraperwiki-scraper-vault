from scraperwiki import swimport
from scraperwiki.sqlite import save, execute, commit, show_tables
from lxml.html import fromstring, tostring
from requests import get
options=swimport('options').options
keyify=swimport('keyify').keyify
randomsleep=swimport('randomsleep').randomsleep
from time import time
import re
strip_address = swimport('strip_address').strip_address

DATE=time()

DOMAIN = 'http://www.thuthukani.co.za'

def getprovincepages():
    html = fromstring(get('http://www.thuthukani.co.za/branches-mpumalanga.php').content)
    selects = html.cssselect('select')
    assert 1 == len(selects)
    d = options(selects[0], textname = 'province', valuename = 'url')
    for row in d:
        row['url'] = DOMAIN + '/' + row['url']
        row['date_scraped'] = DATE
    return d

def parseprovincepage(province):
    raw = get(province['url']).content
    withspaces = raw.replace('<br />', '\n').replace('<font', '\n\n<font')
    html = fromstring(withspaces)
    fonts = html.xpath('//td[@valign="top"]/font[img[@src="images/branches.jpg"]]')
    assert 1==len(fonts)
    font = fonts[0]
    lines = font.text_content().split('\n')

    d = []
    previous_line_empty = is_email = False
    lines = [''] + lines[7:]
    print lines
    for line in lines: #Skip select box
        line = line.strip()

        if is_email:
            if line != '':
                d[-1]['email'] = line
                is_email = False

        elif 'mail' in line:
            is_email = True

        elif previous_line_empty and line != '' and len(re.findall(r'[^0-9]', line)) > 0:
            if len(d) > 0:
                # First entry
                while d[-1]['full-address'][-1] not in map(unicode, range(0,10)):
                    d[-1]['full-address'] = d[-1]['full-address'][:-1]
                print d[-1]
            d.append({"full-address": line + '\n'})

        elif line != '':
            d[-1]['full-address'] += line + '\n'

        previous_line_empty = line == ''

    for row in d:
        addresslines = row['full-address'].split('\n')
        while '' in addresslines:
            addresslines.remove('')

        postcodes = re.findall(r'\d{4}', row['full-address'])
        if len(postcodes) > 0:
            row['postcode'] = postcodes[-1]
        row['town'] = addresslines[-2]

        if addresslines[0] == addresslines[-2]:
            addresslines.pop(0)
        row['street_address'] = '\n'.join(addresslines[0:-2])

        row.update(province)
        
    return d

def main():
    d = []
    for province in getprovincepages():
        d.extend(parseprovincepage(province))
    for row in d:
        if row.has_key('full-address'):
            row['full-address'] = strip_address(row['full-address'])
        if row.has_key('street_address'):
            row['street_address'] = strip_address(row['street_address'])
    save([], d)

main()