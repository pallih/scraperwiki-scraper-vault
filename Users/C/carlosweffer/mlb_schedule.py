import datetime
import scraperwiki
import re
from string import Template
import demjson
import time

sdate = datetime.datetime.now()
sdate_split = str(sdate.year) + str(sdate.month) + str(sdate.day)
# json1 = scraperwiki.scrape("http://mlb.mlb.com/components/schedule/schedule_" + sdate_split + ".json") 
json1 = scraperwiki.scrape("http://mlb.mlb.com/components/schedule/schedule_20130818.json")
json_decode1 = demjson.decode(json1)

for i in range (len(json_decode1)) :

    game = json_decode1[i]
    game_id_split = game['game_id'].split('/')
    game_date = game_id_split[0] + game_id_split[1] + game_id_split[2]

    record = {}
    record['game_pk'] = game['game_pk']
    record['game_type'] = game['game_type']
    timeinsecs = (int(game['game_time'])*0.001)- (4 * 60 * 60)
    record['game_time_et'] = time.ctime(timeinsecs)
    record['venue'] = game['game_venue']
    record['venue_id'] = game['venue_id']
    record['time'] = game['game_time']
    record['location'] = game['game_location']
    record['game_id'] = game['game_id']
    record['home_team_fc'] = game['home']['file_code']
    record['away_team_fc'] = game['away']['file_code']
    record['home_team_id'] = game['home']['id']
    record['away_team_id'] = game['away']['id']
    record['game_id'] = game['game_id']
    record['game_date'] = game_date
    record['home_prob_id'] = game['home']['probable_id']
    record['home_probable'] = game['home']['probable']
    record['home_prob_era'] = game['home']['probable_era']
    record['home_prob_stat'] = game['home']['probable_stat']
    record['away_prob_id'] = game['away']['probable_id']
    record['away_prob_stat'] = game['away']['probable_stat']
    record['away_probable'] = game['away']['probable']
    record['away_prob_era'] = game['away']['probable_era']
    record['sport_code'] = game['sport_code']
    

    
    #print record
    if record.has_key('game_pk'):
        # save records to the datastore
        scraperwiki.sqlite.save(['game_pk'],record)

        
    