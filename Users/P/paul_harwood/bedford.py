import json
import requests
import scraperwiki.sqlite as db
import time

counciltype = json.loads(requests.get('http://mapit.mysociety.org/area/2248/children?;type=UTE').content)
for ward, id in counciltype.items():
        print id['name']
        json.loads(requests.get('http://mapit.mysociety.org/area/%s' % ward).content)
        kml = requests.get('http://mapit.mysociety.org/area/%s.kml' % ward).content
        councildata = {'type': id['type'],
                       'parent_name': 'Northumberland County Council',
                       'id': int(ward),
                       'name': id['name'],
                       'kml': kml[85:-7]}
        db.save(['id'], councildata, verbose=0)import json
import requests
import scraperwiki.sqlite as db
import time

counciltype = json.loads(requests.get('http://mapit.mysociety.org/area/2248/children?;type=UTE').content)
for ward, id in counciltype.items():
        print id['name']
        json.loads(requests.get('http://mapit.mysociety.org/area/%s' % ward).content)
        kml = requests.get('http://mapit.mysociety.org/area/%s.kml' % ward).content
        councildata = {'type': id['type'],
                       'parent_name': 'Northumberland County Council',
                       'id': int(ward),
                       'name': id['name'],
                       'kml': kml[85:-7]}
        db.save(['id'], councildata, verbose=0)