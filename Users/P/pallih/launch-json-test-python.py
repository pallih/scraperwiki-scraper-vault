import scraperwiki

import json

#$json = json_decode(file_get_contents("launch.json"));
#echo $json->scrapername;

#json_object = json.loads('launch.json')

f = open('launch.json', 'r')
print f.read()

with file('launch.json') as f:
    print f.read()
    json_object = json.loads(f.read())
    print json_object
#print json_object

