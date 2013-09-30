import scraperwiki
import re

# Blank Python
html = scraperwiki.scrape("http://humanservices.mesacounty.us/aboutus/child-welfare-trend-data.aspx")

import lxml.html
root = lxml.html.fromstring(html)
content = root.find_class('ContentPadding')[0].getchildren()[0]

#for child in content.iterchildren():
#    data = {}
#    if child.tag == 'h3':
#        year = child.text_content()[:4]
#        data[year] = {}
#    else:
#        text = child.text_content()
#        data[year][text[:-4]] = text[-4:]

for child in content.iterchildren():
    if child.tag == 'h3':
        year = re.search(r'^([\d]{4})', child.text_content()).groups()[0]
        data = {'year': year}
    else:
        for text in child.itertext():
            t = re.search('^([\w][\D]+)([\d]+)', text)
            if t:
                label, number = re.search(r'^([\D]+)([\d|,]+)', text).groups()
                label = label.replace('/', ' ')
                number = number.replace(',','')
                data[label] = int(number)
        scraperwiki.sqlite.save(unique_keys=['year'], data = data)

import scraperwiki
import re

# Blank Python
html = scraperwiki.scrape("http://humanservices.mesacounty.us/aboutus/child-welfare-trend-data.aspx")

import lxml.html
root = lxml.html.fromstring(html)
content = root.find_class('ContentPadding')[0].getchildren()[0]

#for child in content.iterchildren():
#    data = {}
#    if child.tag == 'h3':
#        year = child.text_content()[:4]
#        data[year] = {}
#    else:
#        text = child.text_content()
#        data[year][text[:-4]] = text[-4:]

for child in content.iterchildren():
    if child.tag == 'h3':
        year = re.search(r'^([\d]{4})', child.text_content()).groups()[0]
        data = {'year': year}
    else:
        for text in child.itertext():
            t = re.search('^([\w][\D]+)([\d]+)', text)
            if t:
                label, number = re.search(r'^([\D]+)([\d|,]+)', text).groups()
                label = label.replace('/', ' ')
                number = number.replace(',','')
                data[label] = int(number)
        scraperwiki.sqlite.save(unique_keys=['year'], data = data)

