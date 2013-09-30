import scraperwiki
import lxml.html
import datetime

data = {
    '8gb':  {'url' :'https://play.google.com/store/devices/details?id=nexus_4_8gb'},
    '16gb': {'url' :'https://play.google.com/store/devices/details?id=nexus_4_16gb'}
}

summary = ""

for model in data:
    url = data[model]['url']
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    for title in root.find_class("hardware-price-description"):
        data[model]['status'] = title.text

now = datetime.datetime.now()
newdata = {
    'link': data['8gb']['url'],
    'title' : 'Nexus 4 For Sale checker at ' + str(now),
    'description' : '<a href="{0}">8 GB</a>: {1}<br/><a href="{2}">16 GB</a>: {3}'.format(data['8gb']['url'],data['8gb']['status'],data['16gb']['url'],data['16gb']['status']),
    'pubDate': str(now),
}

scraperwiki.sqlite.save(unique_keys=['link'],data=newdata)

import scraperwiki
import lxml.html
import datetime

data = {
    '8gb':  {'url' :'https://play.google.com/store/devices/details?id=nexus_4_8gb'},
    '16gb': {'url' :'https://play.google.com/store/devices/details?id=nexus_4_16gb'}
}

summary = ""

for model in data:
    url = data[model]['url']
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    for title in root.find_class("hardware-price-description"):
        data[model]['status'] = title.text

now = datetime.datetime.now()
newdata = {
    'link': data['8gb']['url'],
    'title' : 'Nexus 4 For Sale checker at ' + str(now),
    'description' : '<a href="{0}">8 GB</a>: {1}<br/><a href="{2}">16 GB</a>: {3}'.format(data['8gb']['url'],data['8gb']['status'],data['16gb']['url'],data['16gb']['status']),
    'pubDate': str(now),
}

scraperwiki.sqlite.save(unique_keys=['link'],data=newdata)

