import scraperwiki
import simplejson
jsonstring = scraperwiki.scrape('http://astarkort.tm.is/pins')
process = simplejson.loads(jsonstring)
for m in process['results']:
    record = {}   
    record['story'] = m['story']
    record['date'] = m['date']
    record['lat'] = m['lat']
    record['lng'] = m['lng']
    record['geometry'] = '{"type":"Point","coordinates":['+str(m['lng'])+','+str(m['lat'])+']}'
    record['date_locale'] = m['date_locale']
    record['id'] = m['id']
    record['url'] = 'http://astarkort.tm.is/pin/' + str(m['id'])
    scraperwiki.sqlite.save(['id'], data=record, table_name='astarkort_tm')



    

