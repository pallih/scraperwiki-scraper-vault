import json
import time
import requests
import scraperwiki.sqlite as db

# Specify one or the other of the below
PARENT_ID = 0
AREA_TYPE = 'WMC'

if PARENT_ID:
    areas = json.loads(requests.get('http://mapit.mysociety.org/area/%s/children' % PARENT_ID).content)
elif AREA_TYPE:
    areas = json.loads(requests.get('http://mapit.mysociety.org/areas/%s' % AREA_TYPE).content)
else:
    raise Exception, 'Must specify one or other!'

for area in areas.values():
    r = requests.get('http://mapit.mysociety.org/area/%s.kml?simplify_tolerance=0.001' % area['id'])
    if r.status_code == 200:
        area['kml'] = r.content
    db.save(['id'], area)
    time.sleep(1)
import json
import time
import requests
import scraperwiki.sqlite as db

# Specify one or the other of the below
PARENT_ID = 0
AREA_TYPE = 'WMC'

if PARENT_ID:
    areas = json.loads(requests.get('http://mapit.mysociety.org/area/%s/children' % PARENT_ID).content)
elif AREA_TYPE:
    areas = json.loads(requests.get('http://mapit.mysociety.org/areas/%s' % AREA_TYPE).content)
else:
    raise Exception, 'Must specify one or other!'

for area in areas.values():
    r = requests.get('http://mapit.mysociety.org/area/%s.kml?simplify_tolerance=0.001' % area['id'])
    if r.status_code == 200:
        area['kml'] = r.content
    db.save(['id'], area)
    time.sleep(1)
