import scraperwiki

# Weather Scraper


import lxml.html
import urllib2
import json

#f = urllib2.urlopen('http://api.wunderground.com/api/2b91c329c7f2c78c/geolookup/conditions/q/Australia/Melbourne.json')
f = urllib2.urlopen('http://api.wunderground.com/api/2b91c329c7f2c78c/conditions/q/Australia/Melbourne.json?pws=0&bestfct=true')
json_string = f.read()
print json_string
parsed_json = json.loads(json_string)
location = parsed_json['location']['city']
temp_c = parsed_json['current_observation']['temp_c']
weather = parsed_json['current_observation']['weather']
print "Current temperature in %s is: %s and the current condition is %s" % (location, temp_c, weather)

print parsed_json['current_observation']

f.close()

import scraperwiki

# Weather Scraper


import lxml.html
import urllib2
import json

#f = urllib2.urlopen('http://api.wunderground.com/api/2b91c329c7f2c78c/geolookup/conditions/q/Australia/Melbourne.json')
f = urllib2.urlopen('http://api.wunderground.com/api/2b91c329c7f2c78c/conditions/q/Australia/Melbourne.json?pws=0&bestfct=true')
json_string = f.read()
print json_string
parsed_json = json.loads(json_string)
location = parsed_json['location']['city']
temp_c = parsed_json['current_observation']['temp_c']
weather = parsed_json['current_observation']['weather']
print "Current temperature in %s is: %s and the current condition is %s" % (location, temp_c, weather)

print parsed_json['current_observation']

f.close()

