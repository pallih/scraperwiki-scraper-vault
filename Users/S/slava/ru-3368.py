import scraperwiki
import demjson
# Blank Python
scraperwiki.sqlite.execute('delete from cities')
scraperwiki.sqlite.execute('delete from branches')
html=scraperwiki.scrape("https://dl.dropbox.com/u/14865435/ru-3368.json")
#html=html.decode('windows-1251')
json=demjson.decode(html)
id=1
for m in json['markers']:
    #print m['id']
    scraperwiki.sqlite.save(unique_keys=['uid'], data={'uid':id, 'type':m['type'], 'lat':m['x'], 'lon':m['y'], 'id':m['id'],'name':m['name']}, table_name="cities")
    id+=1
    if len(m['places'])>0:
        for p in m['places']:
            #print p['id']
            scraperwiki.sqlite.save(unique_keys=['uid'], data={'uid':id, 'type':p['type'], 'lat':p['x'], 'lon':p['y'], 'id':p['id'],'name':p['name'],'en_name':p['en_name'] if 'en_name' in p else '', 'address':p['address'] if 'address' in p else '', 'city_id':p['city_id']} , table_name="branches")
            id+=1

#print json
import scraperwiki
import demjson
# Blank Python
scraperwiki.sqlite.execute('delete from cities')
scraperwiki.sqlite.execute('delete from branches')
html=scraperwiki.scrape("https://dl.dropbox.com/u/14865435/ru-3368.json")
#html=html.decode('windows-1251')
json=demjson.decode(html)
id=1
for m in json['markers']:
    #print m['id']
    scraperwiki.sqlite.save(unique_keys=['uid'], data={'uid':id, 'type':m['type'], 'lat':m['x'], 'lon':m['y'], 'id':m['id'],'name':m['name']}, table_name="cities")
    id+=1
    if len(m['places'])>0:
        for p in m['places']:
            #print p['id']
            scraperwiki.sqlite.save(unique_keys=['uid'], data={'uid':id, 'type':p['type'], 'lat':p['x'], 'lon':p['y'], 'id':p['id'],'name':p['name'],'en_name':p['en_name'] if 'en_name' in p else '', 'address':p['address'] if 'address' in p else '', 'city_id':p['city_id']} , table_name="branches")
            id+=1

#print json
