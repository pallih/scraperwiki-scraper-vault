#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import requests
import scraperwiki.sqlite as db

PARENT_ID = 2517  # bury council



def iter_children_areas_kml(parent_id):
    children = getjs('http://mapit.mysociety.org/area/%s/children' % parent_id)
    for id, data in children.items():
        kml = requests.get('http://mapit.mysociety.org/area/%s.kml' % id).content
        entry = {'parent_area': int(data['parent_area']),
                 'id': int(id),
                 'name': data['name'],
                 'kml': kml}
        yield entry


def getjs(url, **opts):
    return json.loads(requests.get(url, **opts).content)


#
# Main
#
data = list(iter_children_areas_kml(PARENT_ID))
db.save(['id'], data, verbose=0)
