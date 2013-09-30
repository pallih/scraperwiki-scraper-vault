import requests
from pyquery import PyQuery as pq

RUNNING_IN_SCRAPERWIKI = False
try:
    import scraperwiki
    RUNNING_IN_SCRAPERWIKI = True
except ImportError:
    pass


CITY_DOMAIN = 'http://www.tulsacouncil.org'

council_home = requests.get(
    '%s/councilors/councilors-home.aspx' % CITY_DOMAIN).content

print dir(council_home)

doc = pq(council_home)

district_list = doc.find('.childPageList')
links = district_list.find('a')

for l in links:
    link = pq(l)
    councilor = dict()
    councilor['url'] = link.attr('href')
    councilor['district'] = link.html().split(' ')[-1]
    councilor_page = requests.get(
        '%s%s' % (CITY_DOMAIN, councilor['url'])).content
    page_data = pq(councilor_page)
    content = page_data.find('#contentBox')
    councilor['bio'] = content.html()
    print councilor
    if RUNNING_IN_SCRAPERWIKI:
        scraperwiki.sqlite.save(unique_keys=['district'], data=councilor)

import requests
from pyquery import PyQuery as pq

RUNNING_IN_SCRAPERWIKI = False
try:
    import scraperwiki
    RUNNING_IN_SCRAPERWIKI = True
except ImportError:
    pass


CITY_DOMAIN = 'http://www.tulsacouncil.org'

council_home = requests.get(
    '%s/councilors/councilors-home.aspx' % CITY_DOMAIN).content

print dir(council_home)

doc = pq(council_home)

district_list = doc.find('.childPageList')
links = district_list.find('a')

for l in links:
    link = pq(l)
    councilor = dict()
    councilor['url'] = link.attr('href')
    councilor['district'] = link.html().split(' ')[-1]
    councilor_page = requests.get(
        '%s%s' % (CITY_DOMAIN, councilor['url'])).content
    page_data = pq(councilor_page)
    content = page_data.find('#contentBox')
    councilor['bio'] = content.html()
    print councilor
    if RUNNING_IN_SCRAPERWIKI:
        scraperwiki.sqlite.save(unique_keys=['district'], data=councilor)

