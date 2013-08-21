import json
import requests
import scraperwiki.sqlite as db
import time

begin = 0

counciltype = json.loads(requests.get('http://mapit.mysociety.org/areas/UTA').content)
for council, data1 in counciltype.items():
    if(db.get_var('id') == council and begin == 0):
        begin = 1
    if(begin == 1):
        print data1['name']
        db.save_var('id', council)
        children = json.loads(requests.get('http://mapit.mysociety.org/area/%s/children' % council).content)
        for id, data in children.items(): 
                time.sleep(0.3)
                json.loads(requests.get('http://mapit.mysociety.org/area/%s' % id).content)
                if (data['type'] == 'UTE' or data['type'] == 'UTW'):            
                  #  time.sleep(0.1)
                    kml = requests.get('http://mapit.mysociety.org/area/%s.kml' % id).content
                    councildata = {'type': data['type'],
                                   'parent_name': data1['name'],
                                   'id': int(id),
                                   'name': data['name'],
                                   'kml': kml[85:-7]}
                    db.save(['id'], councildata, verbose=0)