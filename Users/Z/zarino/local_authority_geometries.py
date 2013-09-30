import scraperwiki
import requests
import json
import time
import re

def bounding_box(coordinates):
    """ takes a list of lists: [ [-0.5,3.5], [-0.5,2.8] …]
        returns a list of 4 values: [ max_lat, min_lat, max_lng, min_lng ]
    """
    lats_lngs = zip(*coordinates)
    max_lng_lat = map(max, lats_lngs)
    min_lng_lat = map(min, lats_lngs)
    return [ max_lng_lat[1], min_lng_lat[1], max_lng_lat[0], min_lng_lat[0] ]


url = 'https://api.scraperwiki.com/api/1.0/datastore/sqlite'
params = {
    'format': 'jsondict',
    'name': 'lsoa_data',
    'query': 'select post_2009_la_code as la_code, post_2009_la_name as la_name, count(lsoa_code) as total_lsoas from imd_2010 group by post_2009_la_code'
}
r = requests.get(url, params=params, verify=False)
la_list = json.loads(r.content)


la_list = scraperwiki.sqlite.select("* from la_geometries")
#la_list = scraperwiki.sqlite.select("""* from la_geometries where geojson like '{"type": "MultiPolygon%'""")

i = 1
for la_dict in la_list:
    r = requests.get('http://mapit.mysociety.org/area/%s.geojson' % la_dict['la_code'])
    mapit_area_id = re.findall(r'\d+', r.url)[0]
    geojson = json.loads(r.content)
    #mapit_area_id = la_dict['mapit_area_id']
    #geojson = json.loads(la_dict['geojson'])
    
    if geojson['type'] == 'MultiPolygon':
        l = []
        for poly in geojson['coordinates']:
            this_polys_bounds = bounding_box(poly[0])
            l.append(this_polys_bounds)
        zipped = map(list, zip(*l))
        bounds = [ max(zipped[0]), min(zipped[1]), max(zipped[2]), min(zipped[3]) ]
    else:
        bounds = bounding_box(geojson['coordinates'][0])
    la_dict.update({
        'mapit_area_id': mapit_area_id,
        'geojson': json.dumps(geojson),
        'max_lat': bounds[0],
        'min_lat': bounds[1],
        'max_lng': bounds[2],
        'min_lng': bounds[3]
    })
    scraperwiki.sqlite.save(['la_code'], la_dict, 'la_geometries')
    print 'saved %s of %s local authorities: %s %s' % (i, len(la_list), la_dict['la_name'], la_dict['la_code'])
    i += 1
    time.sleep(2)import scraperwiki
import requests
import json
import time
import re

def bounding_box(coordinates):
    """ takes a list of lists: [ [-0.5,3.5], [-0.5,2.8] …]
        returns a list of 4 values: [ max_lat, min_lat, max_lng, min_lng ]
    """
    lats_lngs = zip(*coordinates)
    max_lng_lat = map(max, lats_lngs)
    min_lng_lat = map(min, lats_lngs)
    return [ max_lng_lat[1], min_lng_lat[1], max_lng_lat[0], min_lng_lat[0] ]


url = 'https://api.scraperwiki.com/api/1.0/datastore/sqlite'
params = {
    'format': 'jsondict',
    'name': 'lsoa_data',
    'query': 'select post_2009_la_code as la_code, post_2009_la_name as la_name, count(lsoa_code) as total_lsoas from imd_2010 group by post_2009_la_code'
}
r = requests.get(url, params=params, verify=False)
la_list = json.loads(r.content)


la_list = scraperwiki.sqlite.select("* from la_geometries")
#la_list = scraperwiki.sqlite.select("""* from la_geometries where geojson like '{"type": "MultiPolygon%'""")

i = 1
for la_dict in la_list:
    r = requests.get('http://mapit.mysociety.org/area/%s.geojson' % la_dict['la_code'])
    mapit_area_id = re.findall(r'\d+', r.url)[0]
    geojson = json.loads(r.content)
    #mapit_area_id = la_dict['mapit_area_id']
    #geojson = json.loads(la_dict['geojson'])
    
    if geojson['type'] == 'MultiPolygon':
        l = []
        for poly in geojson['coordinates']:
            this_polys_bounds = bounding_box(poly[0])
            l.append(this_polys_bounds)
        zipped = map(list, zip(*l))
        bounds = [ max(zipped[0]), min(zipped[1]), max(zipped[2]), min(zipped[3]) ]
    else:
        bounds = bounding_box(geojson['coordinates'][0])
    la_dict.update({
        'mapit_area_id': mapit_area_id,
        'geojson': json.dumps(geojson),
        'max_lat': bounds[0],
        'min_lat': bounds[1],
        'max_lng': bounds[2],
        'min_lng': bounds[3]
    })
    scraperwiki.sqlite.save(['la_code'], la_dict, 'la_geometries')
    print 'saved %s of %s local authorities: %s %s' % (i, len(la_list), la_dict['la_name'], la_dict['la_code'])
    i += 1
    time.sleep(2)