from scraperwiki.sqlite import save
from lxml.html import fromstring
from urllib2 import urlopen
import re
from time import time
DATE = time()

html = fromstring(urlopen('http://opportunity.net/rwanda/who-we-are/branch-locations').read().replace('<', '\n<'))
lines = html.get_element_by_id('right_column').text_content().split('\n')

d = []
for line in lines[8:]: #Skip the header

    #Clean the line
    line = line.strip()
    if line[:2] == '. ':
        line = line[2:]

    #Skip blanks
    if line == '':
        continue

    if line.upper() == line:
        #New row
        d.append({
            "date_scraped": DATE,
            "branch-name": line,
            "full-address": '',
            "phone": ''
        })
    elif 'Plot no' in line:
        linesplit = re.split(r'[,/] ', line)

        d[-1]['street-address'] = linesplit[0]
        if len(linesplit) == 2:
            d[-1]['town'] = linesplit[1]

        d[-1]['full-address'] += d[-1]['street-address'] + '\n'
    elif 'Tel' in line:
        d[-1]['phone'] += line + '\n'
    else:
        if u'\u2013' in line:
            d[-1]['district'], d[-1]['town'], d[-1]['country'] = line.split(u'\u2013')

        if 'District' in line:
            d[-1]['district'] = line.split('District')[0].strip()

        d[-1]['full-address'] += line

save([], d)