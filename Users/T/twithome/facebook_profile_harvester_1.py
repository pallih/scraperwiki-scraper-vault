import scraperwiki
import urlparse
import simplejson
import time
import urllib2

source_url = "http://graph.facebook.com/"
profile_id = 17094
while True:
    time.sleep(0)
    profile_url = urlparse.urljoin(source_url, str(profile_id))
    try:
        results_json = simplejson.loads(scraperwiki.scrape(profile_url))
        for result in results_json:
            profile = dict()
            try:
                profile['id'] = int(results_json['id'])
            except:
                profile['id'] = ""
            try:
                profile['name'] = results_json['name']
            except:
                profile['name'] = ""
            try:
                profile['first_name'] = results_json['first_name']
            except:
                profile['first_name'] = ""
            try:
                profile['last_name'] = results_json['last_name']
            except:
                profile['last_name'] = ""
            try:
                profile['link'] = results_json['link']
            except:
                profile['link'] = ""
            try:
                profile['username'] = results_json['username']
            except:
                profile['username'] = ""
            try:
                profile['gender'] = results_json['gender']
            except:
                profile['gender'] = ""
            try:
                profile['locale'] = results_json['locale']
            except:
                profile['locale'] = ""
        scraperwiki.sqlite.save(unique_keys=['id'], data=profile)
        profile_id += 1
    except urllib2.HTTPError, err:
        if err.code == 400:
            profile_id += 1
            continue
        
            

        
import scraperwiki
import urlparse
import simplejson
import time
import urllib2

source_url = "http://graph.facebook.com/"
profile_id = 17094
while True:
    time.sleep(0)
    profile_url = urlparse.urljoin(source_url, str(profile_id))
    try:
        results_json = simplejson.loads(scraperwiki.scrape(profile_url))
        for result in results_json:
            profile = dict()
            try:
                profile['id'] = int(results_json['id'])
            except:
                profile['id'] = ""
            try:
                profile['name'] = results_json['name']
            except:
                profile['name'] = ""
            try:
                profile['first_name'] = results_json['first_name']
            except:
                profile['first_name'] = ""
            try:
                profile['last_name'] = results_json['last_name']
            except:
                profile['last_name'] = ""
            try:
                profile['link'] = results_json['link']
            except:
                profile['link'] = ""
            try:
                profile['username'] = results_json['username']
            except:
                profile['username'] = ""
            try:
                profile['gender'] = results_json['gender']
            except:
                profile['gender'] = ""
            try:
                profile['locale'] = results_json['locale']
            except:
                profile['locale'] = ""
        scraperwiki.sqlite.save(unique_keys=['id'], data=profile)
        profile_id += 1
    except urllib2.HTTPError, err:
        if err.code == 400:
            profile_id += 1
            continue
        
            

        
