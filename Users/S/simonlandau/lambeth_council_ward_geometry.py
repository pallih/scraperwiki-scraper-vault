#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import requests
import lxml.etree as et
import scraperwiki.sqlite as db
import sys


PARENT_ID = 2537  # Sheffield City Council


def strip_kml(styled_kml):
    tree = et.fromstring(styled_kml)
    # Remove problematic elements 'styleUrl', 'Style'])
    tree[1].remove(tree[1][0])    
    tree.remove(tree[0])
    text = et.tostring(tree, pretty_print=True)
    return text

def iter_children_areas_kml(parent_id):
    children = getjs('http://mapit.mysociety.org/area/%s/children' % parent_id)
    for id, data in children.items():
        kml = requests.get('http://mapit.mysociety.org/area/%s.kml' % id).content
        unstyled_kml = strip_kml(kml)

        entry = {'parent_area': int(data['parent_area']),
                 'id': int(id),
                 'name': data['name'],
                 'kml': unstyled_kml}
        yield entry


def getjs(url, **opts):
    return json.loads(requests.get(url, **opts).content)


#
# Main
#
print sys.version
data = list(iter_children_areas_kml(PARENT_ID))
db.save(['id'], data, verbose=0)
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import requests
import lxml.etree as et
import scraperwiki.sqlite as db
import sys


PARENT_ID = 2537  # Sheffield City Council


def strip_kml(styled_kml):
    tree = et.fromstring(styled_kml)
    # Remove problematic elements 'styleUrl', 'Style'])
    tree[1].remove(tree[1][0])    
    tree.remove(tree[0])
    text = et.tostring(tree, pretty_print=True)
    return text

def iter_children_areas_kml(parent_id):
    children = getjs('http://mapit.mysociety.org/area/%s/children' % parent_id)
    for id, data in children.items():
        kml = requests.get('http://mapit.mysociety.org/area/%s.kml' % id).content
        unstyled_kml = strip_kml(kml)

        entry = {'parent_area': int(data['parent_area']),
                 'id': int(id),
                 'name': data['name'],
                 'kml': unstyled_kml}
        yield entry


def getjs(url, **opts):
    return json.loads(requests.get(url, **opts).content)


#
# Main
#
print sys.version
data = list(iter_children_areas_kml(PARENT_ID))
db.save(['id'], data, verbose=0)
