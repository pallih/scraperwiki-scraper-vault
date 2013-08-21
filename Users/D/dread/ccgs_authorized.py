#!/usr/bin/env python

import scraperwiki
import requests
import lxml.html
import re

# Clinical Commissioning Groups (CCGs) that have been authorised to commission healthcare services for their communities
html = requests.get('http://www.england.nhs.uk/ccg-details/')

root = lxml.html.fromstring(html.content)
unique_keys = ['title']

colon_separated = re.compile('\s*(.+):[\s\xa0](.+)') # '\nClinical Lead: Dr Navin Kumta'

for entry in root.cssselect("div.entry-content p"):

# e.g.
# <p><strong>NHS&nbsp;Airedale, Wharfedale and Craven CCG</strong><br>
# Clinical Lead:&nbsp;Dr Phil Pue<br>
# Accountable Officer: Dr Phil Pue<br>
# Website:&nbsp;<a href="http://www.airedalewharfedalecravenccg.nhs.uk/">www.airedalewharfedalecravenccg.nhs.uk/</a></p>

    title = entry.cssselect("strong")
    if not title:
        print 'Ignored: ', entry.text_content()
        continue
    
    data = {
        'title' : title[0].text_content().replace(u'\xa0', ' '),
    }
    
    website_anchor = entry.cssselect("a")
    if website_anchor:
        data['website'] = website_anchor[0].get('href')
    
    for line in entry.itertext():
        match = colon_separated.match(line)
        if match:
            position, name = match.groups()
            data[position.lower()] = name
    print 'Saved: ', data
    scraperwiki.sqlite.save(unique_keys, data)

