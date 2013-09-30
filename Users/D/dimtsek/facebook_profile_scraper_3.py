import scraperwiki
import urlparse
import simplejson
import time
import urllib2
import re

source_url = http://graph.facebook.com/ramylee

try:
    last_db_value = scraperwiki.sqlite.execute("select MAX(id) from swdata")
    value = str(last_db_value.values()[1])
    last_profile_id = int(re.sub(r'\W+', '', value))
except:
    last_profile_id = 1

while True:
    time.sleep(0)
    profile_url = urlparse.urljoin(source_url, str(last_profile_id))
    try:
        results_json = simplejson.loads(scraperwiki.scrape(profile_url))
        profile = dict()

        profile['name'] = results_json.get('name', "")
        profile['link'] = results_json.get('link', "")
        profile['birth'] = results_json.get('birth', "")
        profile['username'] = results_json.get('username', "")
        profile['gender'] = results_json.get('gender', "")
        profile['locale'] = results_json.get('locale', "")

        scraperwiki.sqlite.save(unique_keys=['id'], data=profile)
        last_profile_id += 1
    except urllib2.HTTPError, err:
        last_profile_id += 1
        continue
        
        
            

        
import scraperwiki
import urlparse
import simplejson
import time
import urllib2
import re

source_url = http://graph.facebook.com/ramylee

try:
    last_db_value = scraperwiki.sqlite.execute("select MAX(id) from swdata")
    value = str(last_db_value.values()[1])
    last_profile_id = int(re.sub(r'\W+', '', value))
except:
    last_profile_id = 1

while True:
    time.sleep(0)
    profile_url = urlparse.urljoin(source_url, str(last_profile_id))
    try:
        results_json = simplejson.loads(scraperwiki.scrape(profile_url))
        profile = dict()

        profile['name'] = results_json.get('name', "")
        profile['link'] = results_json.get('link', "")
        profile['birth'] = results_json.get('birth', "")
        profile['username'] = results_json.get('username', "")
        profile['gender'] = results_json.get('gender', "")
        profile['locale'] = results_json.get('locale', "")

        scraperwiki.sqlite.save(unique_keys=['id'], data=profile)
        last_profile_id += 1
    except urllib2.HTTPError, err:
        last_profile_id += 1
        continue
        
        
            

        
