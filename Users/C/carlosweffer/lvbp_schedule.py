import datetime
import time
import scraperwiki
import re
from string import Template
import demjson

sdate = datetime.datetime.now()
sdate_split = str(sdate.year) + '/' + str(sdate.month) + '/' + str(sdate.day)
json1 = scraperwiki.scrape("http://mlb.mlb.com/lookup/json/named.schedule_vw_complete_affiliate.bam?game_date='" + sdate_split + "'&game_type='R'&season=2012&league_id=135")
#json1 = scraperwiki.scrape("http://mlb.mlb.com/lookup/json/named.schedule_vw_complete_affiliate.bam?game_date='2012/12/17'&game_type='R'&season=2012&league_id=135")
#RoundRobin
#json1 = scraperwiki.scrape("http://mlb.mlb.com/lookup/json/named.schedule_vw_complete_affiliate.bam?game_date='2013/01/06'&game_type='L'&season=2012&league_id=135")

json_decode1 = demjson.decode(json1)
no_games = int(json_decode1['schedule_vw_complete_affiliate']['queryResults']['totalSize'])
if no_games > 0 : 
    games = json_decode1['schedule_vw_complete_affiliate']['queryResults']['row']

for i in range (no_games) :

    game = games[i]
    game_id_split = game['game_id'].split('/')
    game_date = game_id_split[0] + game_id_split[1] + game_id_split[2]

    record = {}
    record['game_pk'] = game['game_pk']
    record['venue_id'] = game['venue_id']
    record['venue'] = game['venue']
    record['game_time_et'] = game['game_time_et']
    record['game_time_local'] = game['game_time_local']
    eastern_time = time.strptime(game['game_time_et'], "%Y-%m-%dT%H:%M:%S")
    eastern_time_secs = time.mktime(eastern_time)
    #game eastern time in ms
    record['time'] = int(eastern_time_secs * 1000)
    record['location'] = game['venue_city']
    record['game_id'] = game['game_id']
    record['home_team'] = game['home_team_id']
    record['away_team'] = game['away_team_id']
    record['game_id'] = game['game_id']
    record['game_date'] = game_date
    record['home_prob_id'] = game['home_probable_id']
    record['home_probable'] = game['home_probable']
    record['home_prob_era'] = game['home_probable_era']
    record['home_prob_stat'] = game['home_probable_wl']
    record['away_prob_id'] = game['away_probable_id']
    record['away_prob_stat'] = game['away_probable_wl']
    record['away_probable'] = game['away_probable']
    record['away_prob_era'] = game['away_probable_era']
    

    
    #print record
    if record.has_key('game_pk'):
        # save records to the datastore
        scraperwiki.sqlite.save(['game_pk'],record)

import datetime
import time
import scraperwiki
import re
from string import Template
import demjson

sdate = datetime.datetime.now()
sdate_split = str(sdate.year) + '/' + str(sdate.month) + '/' + str(sdate.day)
json1 = scraperwiki.scrape("http://mlb.mlb.com/lookup/json/named.schedule_vw_complete_affiliate.bam?game_date='" + sdate_split + "'&game_type='R'&season=2012&league_id=135")
#json1 = scraperwiki.scrape("http://mlb.mlb.com/lookup/json/named.schedule_vw_complete_affiliate.bam?game_date='2012/12/17'&game_type='R'&season=2012&league_id=135")
#RoundRobin
#json1 = scraperwiki.scrape("http://mlb.mlb.com/lookup/json/named.schedule_vw_complete_affiliate.bam?game_date='2013/01/06'&game_type='L'&season=2012&league_id=135")

json_decode1 = demjson.decode(json1)
no_games = int(json_decode1['schedule_vw_complete_affiliate']['queryResults']['totalSize'])
if no_games > 0 : 
    games = json_decode1['schedule_vw_complete_affiliate']['queryResults']['row']

for i in range (no_games) :

    game = games[i]
    game_id_split = game['game_id'].split('/')
    game_date = game_id_split[0] + game_id_split[1] + game_id_split[2]

    record = {}
    record['game_pk'] = game['game_pk']
    record['venue_id'] = game['venue_id']
    record['venue'] = game['venue']
    record['game_time_et'] = game['game_time_et']
    record['game_time_local'] = game['game_time_local']
    eastern_time = time.strptime(game['game_time_et'], "%Y-%m-%dT%H:%M:%S")
    eastern_time_secs = time.mktime(eastern_time)
    #game eastern time in ms
    record['time'] = int(eastern_time_secs * 1000)
    record['location'] = game['venue_city']
    record['game_id'] = game['game_id']
    record['home_team'] = game['home_team_id']
    record['away_team'] = game['away_team_id']
    record['game_id'] = game['game_id']
    record['game_date'] = game_date
    record['home_prob_id'] = game['home_probable_id']
    record['home_probable'] = game['home_probable']
    record['home_prob_era'] = game['home_probable_era']
    record['home_prob_stat'] = game['home_probable_wl']
    record['away_prob_id'] = game['away_probable_id']
    record['away_prob_stat'] = game['away_probable_wl']
    record['away_probable'] = game['away_probable']
    record['away_prob_era'] = game['away_probable_era']
    

    
    #print record
    if record.has_key('game_pk'):
        # save records to the datastore
        scraperwiki.sqlite.save(['game_pk'],record)

