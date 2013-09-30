import scraperwiki
import re
from string import Template
import demjson

scraperwiki.sqlite.execute('drop table if exists `swdata`')
scraperwiki.sqlite.attach('lvbp_rosters')
#Skip a player
#thePlayers = scraperwiki.sqlite.select('player_id from `lvbp_rosters`.`swdata` where `primary_position` != "1" and player_id = "431157" order by player_id')

thePlayers = scraperwiki.sqlite.select('player_id from `lvbp_rosters`.`swdata` where `primary_position` != "1" order by player_id')

for player in thePlayers:
    player_id = player['player_id']

#Execute only for one player
#for n in range (0,1) : 
#    player_id = 520471

#TWO Latest batting stats: results=2
    page_url = Template("http://mlb.com/lookup/json/named.minors_bio_page_batting.bam?season=2012&num_games=2&game_type='R'&league_id=135&player_id=$player_id").substitute(player_id=player_id)
    json1 = scraperwiki.scrape(page_url)
    json_decode1 = demjson.decode(json1)

    latest_len = int(json_decode1['minors_bio_page_batting']['minors_stats_batting_previous_games']['queryResults']['totalSize'])
    if latest_len > 1 :
            
            theGames = json_decode1['minors_bio_page_batting']['minors_stats_batting_previous_games']['queryResults']['row']
            for i in range (0,latest_len-1) :

                    record = {}
                    record['playerId'] = player_id
                    record['team_id'] = theGames[i]['team_id']
                    record['opponent_id'] = theGames[i]['opponent_id']
                    record['key'] = theGames[i]['game_pk'] + theGames[i]['player_id']
                
                #Skip a game
                #gamepk = theGames[i]['game_pk']
                #if gamepk.find('350115') < 0 :

                    
                    ab = int(theGames[i]['ab']) 
                    h = int(theGames[i]['h'])
                    outs = ab - h
                    r = int(theGames[i]['r'])
                    hr = int(theGames[i]['hr'])
                    rbi = int(theGames[i]['rbi'])
                    sb = int(theGames[i]['sb'])
                    bb = int(theGames[i]['bb'])
                    doubles = int(theGames[i]['d'])
                    triples = int(theGames[i]['t'])

                    game_date_split = theGames[i]['game_date'].split('-')
                    date_display_split = theGames[i]['game_date_display'].split(' ')
                    game_date = game_date_split[0] + game_date_split[1] + date_display_split[1]
                    record['game_id_date'] = game_date
                    record['cal_date']  = theGames[i]['game_date_display']
                    record['game_pk'] = theGames[i]['game_pk']
                    record['g'] = 1
                    record['ab'] = ab
                    record['r'] = r
                    record['h'] = h
                    record['2b'] = doubles
                    record['3b'] = triples
                    record['hr'] = hr
                    record['rbi'] = rbi
                    record['bb'] = bb
                    record['sb'] = sb
                    record['ibb'] = theGames[i]['ibb']
                    record['so'] = theGames[i]['so']
                    record['avg'] = theGames[i]['avg']
                    record['slg'] = theGames[i]['slg']
                    record['outs'] = outs               
                    
                    record['points'] = h + doubles + (triples * 2) + r + (hr * 4) + rbi + (sb * 2) + (bb * 0.5) + (outs * (-0.3))
            
                    if record.has_key('key'):
                    # save records to the datastore
                        scraperwiki.sqlite.save(['key'],record)
        

import scraperwiki
import re
from string import Template
import demjson

scraperwiki.sqlite.execute('drop table if exists `swdata`')
scraperwiki.sqlite.attach('lvbp_rosters')
#Skip a player
#thePlayers = scraperwiki.sqlite.select('player_id from `lvbp_rosters`.`swdata` where `primary_position` != "1" and player_id = "431157" order by player_id')

thePlayers = scraperwiki.sqlite.select('player_id from `lvbp_rosters`.`swdata` where `primary_position` != "1" order by player_id')

for player in thePlayers:
    player_id = player['player_id']

#Execute only for one player
#for n in range (0,1) : 
#    player_id = 520471

#TWO Latest batting stats: results=2
    page_url = Template("http://mlb.com/lookup/json/named.minors_bio_page_batting.bam?season=2012&num_games=2&game_type='R'&league_id=135&player_id=$player_id").substitute(player_id=player_id)
    json1 = scraperwiki.scrape(page_url)
    json_decode1 = demjson.decode(json1)

    latest_len = int(json_decode1['minors_bio_page_batting']['minors_stats_batting_previous_games']['queryResults']['totalSize'])
    if latest_len > 1 :
            
            theGames = json_decode1['minors_bio_page_batting']['minors_stats_batting_previous_games']['queryResults']['row']
            for i in range (0,latest_len-1) :

                    record = {}
                    record['playerId'] = player_id
                    record['team_id'] = theGames[i]['team_id']
                    record['opponent_id'] = theGames[i]['opponent_id']
                    record['key'] = theGames[i]['game_pk'] + theGames[i]['player_id']
                
                #Skip a game
                #gamepk = theGames[i]['game_pk']
                #if gamepk.find('350115') < 0 :

                    
                    ab = int(theGames[i]['ab']) 
                    h = int(theGames[i]['h'])
                    outs = ab - h
                    r = int(theGames[i]['r'])
                    hr = int(theGames[i]['hr'])
                    rbi = int(theGames[i]['rbi'])
                    sb = int(theGames[i]['sb'])
                    bb = int(theGames[i]['bb'])
                    doubles = int(theGames[i]['d'])
                    triples = int(theGames[i]['t'])

                    game_date_split = theGames[i]['game_date'].split('-')
                    date_display_split = theGames[i]['game_date_display'].split(' ')
                    game_date = game_date_split[0] + game_date_split[1] + date_display_split[1]
                    record['game_id_date'] = game_date
                    record['cal_date']  = theGames[i]['game_date_display']
                    record['game_pk'] = theGames[i]['game_pk']
                    record['g'] = 1
                    record['ab'] = ab
                    record['r'] = r
                    record['h'] = h
                    record['2b'] = doubles
                    record['3b'] = triples
                    record['hr'] = hr
                    record['rbi'] = rbi
                    record['bb'] = bb
                    record['sb'] = sb
                    record['ibb'] = theGames[i]['ibb']
                    record['so'] = theGames[i]['so']
                    record['avg'] = theGames[i]['avg']
                    record['slg'] = theGames[i]['slg']
                    record['outs'] = outs               
                    
                    record['points'] = h + doubles + (triples * 2) + r + (hr * 4) + rbi + (sb * 2) + (bb * 0.5) + (outs * (-0.3))
            
                    if record.has_key('key'):
                    # save records to the datastore
                        scraperwiki.sqlite.save(['key'],record)
        

