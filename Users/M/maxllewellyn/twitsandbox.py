###################################################################################
# Twitter API scraper - designed to be forked and used for more interesting things
###################################################################################

import scraperwiki
import simplejson
import urllib2
import time


def parseData(str):
    split = str.split(' ')
    data = {}
    data['id'] = result['id']
    data['text'] = result['text']    
    data['event'] = split[0]
    data['match_type'] = split[2]
    data['match_number'] = split[4]
    data['red_score'] = split[6]
    data['blue_score'] = split[8]
    data['red_team_1'] = split[10]
    data['red_team_2'] = split[11]
    data['red_team_3'] = split[12]
    data['blue_team_1'] = split[14]
    data['blue_team_2'] = split[15]
    data['blue_team_3'] = split[16]
    data['red_climb_score'] = split[18]
    data['blue_climb_score'] = split[20]
    data['red_foul_points'] = split[22]
    data['blue_foul_points'] = split[24]
    data['red_auto_score'] = split[26]
    data['blue_auto_score'] = split[28]
    data['red_teleop_points'] = split[30]
    data['blue_teleop_points'] = split[32]
    return data


RESULTS_PER_PAGE = '200'
PAGE_START = 1
NUM_PAGES = 50

base_url = 'http://api.twitter.com/1/statuses/user_timeline.json?screen_name=frcfms&include_rts=false&exclude_replies=true&trim_user=true'

page = PAGE_START + NUM_PAGES
#for page in range(PAGE_START, NUM_PAGES+1):
while(page >= PAGE_START):
    url = base_url +'&count='+ str(RESULTS_PER_PAGE) +'&page='+ str(page)
    req = urllib2.Request(url)
    
    success = False
    while(not success):
        try:
            response = urllib2.urlopen(req)
            the_page = response.read()
            print the_page
            results_json = simplejson.loads(the_page)
            success = True
            for result in results_json:
                data = parseData(result['text']);
                #print data['text']
                scraperwiki.sqlite.save(["id"], data) 
    
        except urllib2.HTTPError as e:
            print e.code
            print e.read()
            time.sleep(5)
    page = page-1
