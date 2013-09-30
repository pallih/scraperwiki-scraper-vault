import scraperwiki
import urlparse
import simplejson
import time
import urllib2
import re


QUERY = 'ewert and the two dragons'
RESULTS_PER_PAGE = '100'
LANGUAGE = 'en'
NUM_PAGES = 15 

source_url = "https://graph.facebook.com/search?q=QUERY&type=OBJECT_TYPE"

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
        profile['id'] = int(results_json.get('id'))
        profile['name'] = results_json.get('name', "")
        profile['first_name'] = results_json.get('first_name', "")
        profile['last_name'] = results_json.get('last_name', "")
        profile['link'] = results_json.get('link', "")
        profile['username'] = results_json.get('username', "")
        profile['gender'] = results_json.get('gender', "")
        profile['age'] = results_json.get('age', "")
        profile['locale'] = results_json.get('locale', "")
        profile['interaction'] = results_json.get('interaction', "")
        profile['message'] = results_json.get('message', "")


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


QUERY = 'ewert and the two dragons'
RESULTS_PER_PAGE = '100'
LANGUAGE = 'en'
NUM_PAGES = 15 

source_url = "https://graph.facebook.com/search?q=QUERY&type=OBJECT_TYPE"

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
        profile['id'] = int(results_json.get('id'))
        profile['name'] = results_json.get('name', "")
        profile['first_name'] = results_json.get('first_name', "")
        profile['last_name'] = results_json.get('last_name', "")
        profile['link'] = results_json.get('link', "")
        profile['username'] = results_json.get('username', "")
        profile['gender'] = results_json.get('gender', "")
        profile['age'] = results_json.get('age', "")
        profile['locale'] = results_json.get('locale', "")
        profile['interaction'] = results_json.get('interaction', "")
        profile['message'] = results_json.get('message', "")


        scraperwiki.sqlite.save(unique_keys=['id'], data=profile)
        last_profile_id += 1
    except urllib2.HTTPError, err:
        last_profile_id += 1
        continue
        
            

        
