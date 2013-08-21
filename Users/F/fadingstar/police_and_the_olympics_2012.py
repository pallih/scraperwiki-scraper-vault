##
# UK Police Twitter scraper - designed by @jackottaviani
##

import scraperwiki
import simplejson
import urllib2
import time
import traceback

# add stack with non-downloaded accounts

police_accounts = ['from:MPSHackney','from:MetPoliceEvents','from:metpoliceuk','from:MPSHarrow','from:MPSWestminster','from:MPSWandsworth','from:MPSHammFul','from:MPSOnTheStreet','from:MPSIslington','from:MPSBarnet','from:MPSRedbridge','from:MPSCamden','from:MPSCroydon','from:MPSLewisham','from:EalingMPS','from:MPSHaringey','from:MPSHounslow','from:MPSSTC','from:LambethMPS','from:MPSWForest','from:MPSDoI','from:MPSSutton','from:MPSTowerHam','from:MPSBexley','from:MPSBrent','from:MPSHavering','from:MPSKenChel','from:MPSSouthwark','from:MPSEnfield','from:MPSRichmond','from:MPSMerton','from:MPSKingston','from:MPSBarkDag','from:MPSHackney','from:MPSGreenwich','from:MPSHillingdon','from:MPSBromley','from:MPSNewham','from:2012GovPress','from:2012govuk','from:2012GovPress','from:2012govuk']

RESULTS_PER_PAGE = '500'
LANGUAGE = 'en'
NUM_PAGES = 1

for p in police_accounts:
    for page in range(1, NUM_PAGES+1):

        police_accounts.remove(p)

        base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s' \
             % (urllib2.quote(p), RESULTS_PER_PAGE, LANGUAGE, page)

        try:
            results_json = simplejson.loads(scraperwiki.scrape(base_url))
            for result in results_json['results']:
                
                data = {}
    
                data['created_at'] = result['created_at']
                data['geo'] = result['geo']
                data['id'] = result['id']
                data['text'] = result['text']
                data['from_user'] = result['from_user']
                data['from_user_id_str'] = result['from_user_id_str']
                data['to_user'] = result['to_user']
                
                if 'in_reply_to_status_id_str' in result.keys():
                    data['in_reply_to_status_id_str'] = result['in_reply_to_status_id_str']
                else:
                    data['in_reply_to_status_id_str'] = ''

                data['to_user_name'] = result['to_user_name']
    
                scraperwiki.sqlite.save(["id"], data)
            
        except Exception, e:
            police_accounts.append(p)
            traceback.print_exc()
            print 'Oh dear, failed to scrape %s' % base_url
            time.sleep(10)
            continue

        print 'sleeping some seconds... starting %s' % (base_url)
        time.sleep(3)
    
##
# UK Police Twitter scraper - designed by @jackottaviani
##

import scraperwiki
import simplejson
import urllib2
import time
import traceback

# add stack with non-downloaded accounts

police_accounts = ['from:MPSHackney','from:MetPoliceEvents','from:metpoliceuk','from:MPSHarrow','from:MPSWestminster','from:MPSWandsworth','from:MPSHammFul','from:MPSOnTheStreet','from:MPSIslington','from:MPSBarnet','from:MPSRedbridge','from:MPSCamden','from:MPSCroydon','from:MPSLewisham','from:EalingMPS','from:MPSHaringey','from:MPSHounslow','from:MPSSTC','from:LambethMPS','from:MPSWForest','from:MPSDoI','from:MPSSutton','from:MPSTowerHam','from:MPSBexley','from:MPSBrent','from:MPSHavering','from:MPSKenChel','from:MPSSouthwark','from:MPSEnfield','from:MPSRichmond','from:MPSMerton','from:MPSKingston','from:MPSBarkDag','from:MPSHackney','from:MPSGreenwich','from:MPSHillingdon','from:MPSBromley','from:MPSNewham','from:2012GovPress','from:2012govuk','from:2012GovPress','from:2012govuk']

RESULTS_PER_PAGE = '500'
LANGUAGE = 'en'
NUM_PAGES = 1

for p in police_accounts:
    for page in range(1, NUM_PAGES+1):

        police_accounts.remove(p)

        base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s' \
             % (urllib2.quote(p), RESULTS_PER_PAGE, LANGUAGE, page)

        try:
            results_json = simplejson.loads(scraperwiki.scrape(base_url))
            for result in results_json['results']:
                
                data = {}
    
                data['created_at'] = result['created_at']
                data['geo'] = result['geo']
                data['id'] = result['id']
                data['text'] = result['text']
                data['from_user'] = result['from_user']
                data['from_user_id_str'] = result['from_user_id_str']
                data['to_user'] = result['to_user']
                
                if 'in_reply_to_status_id_str' in result.keys():
                    data['in_reply_to_status_id_str'] = result['in_reply_to_status_id_str']
                else:
                    data['in_reply_to_status_id_str'] = ''

                data['to_user_name'] = result['to_user_name']
    
                scraperwiki.sqlite.save(["id"], data)
            
        except Exception, e:
            police_accounts.append(p)
            traceback.print_exc()
            print 'Oh dear, failed to scrape %s' % base_url
            time.sleep(10)
            continue

        print 'sleeping some seconds... starting %s' % (base_url)
        time.sleep(3)
    
