#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import time

import requests
import scraperwiki.sqlite as db
import lxml.etree as etree

PARENT_ID = 2352 # Thanet District Council
POLYGON_ONLY = True
SLEEP_TIME = 0.3 # avoid rate limit


def save_kml_for_children_of(id):
    for i, entry in enumerate(iter_children_areas_kml(id)):
        db.save(['id'], entry, verbose=0)
    return i


def iter_children_areas_kml(parent_id):
    children = getjs('http://mapit.mysociety.org/area/%s/children' % parent_id)
    if 'error' in children:
        raise RuntimeError(children['error'])
    db.save(['parent_area'], {'parent_area': parent_id, 'count': len(children)}, table_name="counts", verbose=0)
    for id, data in children.items():
        kml = requests.get('http://mapit.mysociety.org/area/%s.kml' % id).content
        if POLYGON_ONLY:
            kml = extract_polygon(kml)
        entry = {'parent_area': int(data['parent_area']),
                 'id': int(id),
                 'name': data['name'],
                 'kml': kml}
        yield entry
        time.sleep(SLEEP_TIME)
        


def getjs(url, **opts):
    return json.loads(requests.get(url, **opts).content)


def extract_polygon(kmlstring):
    kml = etree.fromstring(kmlstring)
    polygon_el = kml.find('.//kml:Polygon', namespaces={'kml': kml.nsmap[None]})
    return etree.tostring(polygon_el)


def clean_all_kml():
    for entry in db.select('* from swdata'):
        entry['kml'] = extract_polygon(entry['kml'].encode('utf8'))
        db.save(['id'], entry, verbose=0)

#
# Main
if __name__ == 'scraper':
    save_kml_for_children_of(PARENT_ID)
    #clean_all_kml()  # Uncomment this to clean existing data
    print 'Main', __name__