# -*- coding: utf-8 -*-

import scraperwiki
import re
import simplejson

#

url = "http://www.promsbank.ru/files/sgm_nodes.json"
address_re = re.compile("""^.*?>(.+?)<(/|br)""", re.I | re.U | re.S )

i=0

html = scraperwiki.scrape(url)
points = simplejson.loads(html)

for point in points:
    # skip atms and other cash only offices
    if point['cat_tid'] != '20': continue

    branch_name = point['name']
    latlon = point['gmap_coordinates'].split(',')
    body  = address_re.findall(point['body'])[0][0]

    i+=1
    scraperwiki.sqlite.save(unique_keys=['id'], \
        data={'id':i, \
            'lat':latlon[0], \
            'lng':latlon[1], \
            'cat_tid': point['cat_tid'], \
            'branch_name': branch_name , \
            'address':body.strip(' \n\r\t.,'),\
            'body' : point['body']})




# -*- coding: utf-8 -*-

import scraperwiki
import re
import simplejson

#

url = "http://www.promsbank.ru/files/sgm_nodes.json"
address_re = re.compile("""^.*?>(.+?)<(/|br)""", re.I | re.U | re.S )

i=0

html = scraperwiki.scrape(url)
points = simplejson.loads(html)

for point in points:
    # skip atms and other cash only offices
    if point['cat_tid'] != '20': continue

    branch_name = point['name']
    latlon = point['gmap_coordinates'].split(',')
    body  = address_re.findall(point['body'])[0][0]

    i+=1
    scraperwiki.sqlite.save(unique_keys=['id'], \
        data={'id':i, \
            'lat':latlon[0], \
            'lng':latlon[1], \
            'cat_tid': point['cat_tid'], \
            'branch_name': branch_name , \
            'address':body.strip(' \n\r\t.,'),\
            'body' : point['body']})




