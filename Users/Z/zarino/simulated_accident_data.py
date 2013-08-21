import scraperwiki
import requests
import json
point_in_polygon = scraperwiki.utils.swimport('point_in_polygon')

apiurl = 'https://api.scraperwiki.com/api/1.0/datastore/sqlite'

local_authorities = json.loads(requests.get(apiurl, params={
    'format': 'jsondict',
    'name': 'local_authority_geometries',
    'query': 'select la_code, la_name, min_lng, max_lng, min_lat, max_lat from la_geometries'
}, verify=False).text)
print 'Loaded', len(local_authorities), 'local authorities'

local_authority_boundaries = {}

def get_local_authority_boundary(la_code):
    if la_code in local_authority_boundaries:
        return local_authority_boundaries[la_code]
    else:
        r = requests.get(apiurl, params={
            'format': 'jsondict',
            'name': 'local_authority_geometries',
            'query': 'select geojson from la_geometries where la_code="%s"' % la_code
        }, verify=False)
        geojson = json.loads(json.loads(r.content)[0]['geojson'])
        local_authority_boundaries[la_code] = geojson
        return geojson

def detect_local_authority(lat, lng):

    lat = float(lat)
    lng = float(lng)

    possible_local_authorities = []

    for local_authority in local_authorities:
        if local_authority['min_lat'] <= lat <= local_authority['max_lat'] and local_authority['min_lng'] <= lng <=local_authority['max_lng']:
            possible_local_authorities.append(local_authority['la_code'])

    if len(possible_local_authorities) == 1:
        return possible_local_authorities[0]

    elif len(possible_local_authorities) > 1:
        for possible_local_authority in possible_local_authorities:
            geojson = get_local_authority_boundary(possible_local_authority)
            if geojson['type'] == 'MultiPolygon':
                for polygon in geojson['coordinates'][0]:
                    if point_in_polygon.point_in_polygon(lng, lat, polygon):
                        return possible_local_authority
                    else:
                        continue
            else:
                if point_in_polygon.point_in_polygon(lng, lat, geojson['coordinates'][0]):
                    return possible_local_authority
                else:
                    continue

            print lat, lng, "isn't in any local authorities"
            return None
    else:
        print lat, lng, "doesn't seem to be in any local authorities!!"
        return None

carryon = True
offset = 0

scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS `accidents` (`lat` REAL, `lng` REAL, `la_code` TEXT, `var1` INTEGER, `var2` INTEGER, `var3` INTEGER)')
scraperwiki.sqlite.execute('CREATE INDEX la_code_index ON accidents (la_code)')
scraperwiki.sqlite.commit()

while carryon:
    query = 'select Latitude as lat, Longitude as lng, Weather_Conditions as var1, Day_of_Week as var2, Number_of_Casualties as var3 from `RoadAccidents2010 Accidents` order by rowid limit 1000 offset %s' % offset
    j = requests.get(apiurl, params={
        'format':'jsondict', 
        'name':'roadaccidents',
        'query':query}, verify=False).text
    accidents = json.loads(j)
    print 'Loaded accidents', offset, '-', offset+len(accidents)
    if len(accidents) < 1000:
        carryon = False
    else:
        offset = offset + 1000
    print 'Determining local authorities...'
    for accident in accidents:
        accident['la_code'] = detect_local_authority(accident['lat'], accident['lng'])
    print 'Saving...'
    scraperwiki.sqlite.save([], accidents, 'accidents')
    