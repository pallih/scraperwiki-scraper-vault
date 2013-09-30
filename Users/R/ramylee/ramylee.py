import scraperwiki
import urlparse
import simplejson
import time
import urllib2
import re

source_url = "http://graph.facebook.com/ramylee"

try:
    last_db_value = scraperwiki.sqlite.execute("select MAX(id) from swdata")
    value = str(last_db_value.values()[1])
    last_profile_id = int(re.sub(r'\W+', '', value))
except:
    last_profile_id = 1

while True:
    time.sleep(0)
    profile_url = urlparse.urljoin(source_url, "1681027838")
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
        profile['locale'] = results_json.get('locale', "")

        scraperwiki.sqlite.save(unique_keys=['id'], data=profile)        import scraperwiki
import urlparse
import simplejson
import time
import urllib2
import re

source_url = "http://graph.facebook.com/ramylee"

try:
    last_db_value = scraperwiki.sqlite.execute("select MAX(id) from swdata")
    value = str(last_db_value.values()[1])
    last_profile_id = int(re.sub(r'\W+', '', value))
except:
    last_profile_id = 1

while True:
    time.sleep(0)
    profile_url = urlparse.urljoin(source_url, "1681027838")
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
        profile['locale'] = results_json.get('locale', "")

        scraperwiki.sqlite.save(unique_keys=['id'], data=profile)        