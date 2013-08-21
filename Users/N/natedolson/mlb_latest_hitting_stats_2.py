import scraperwiki
import re
from string import Template
import demjson

scraperwiki.sqlite.execute('drop table if exists `swdata`')
scraperwiki.sqlite.attach('mlb_rosters_3')
thePlayers = scraperwiki.sqlite.select('player_id from `mlb_rosters_3`.`swdata` where `primary_position` != "1" order by player_id')

for player in thePlayers:
    player_id = player['player_id']
#for n in range (0,1) : 
#    player_id = 462101

#TWO Latest batting stats: results=2
    page_url = Template("http://mlb.mlb.com/lookup/json/named.mlb_bio_hitting_last_10.bam?results=1&season=2013&game_type='R'&player_id=$player_id").substitute(player_id=player_id)
    json1 = scraperwiki.scrape(page_url)
    #json1 = scraperwiki.scrape("http://mlb.mlb.com/lookup/json/named.mlb_bio_hitting_last_10.bam?results=2&season=2013&game_type='R'&player_id=462101")
    json_decode1 = demjson.decode(json1)
    if int(json_decode1['mlb_bio_hitting_last_10']['mlb_individual_hitting_last_x_total']['queryResults']['totalSize']) > 0 :
        latest_len = int(json_decode1['mlb_bio_hitting_last_10']['mlb_individual_hitting_game_log']['queryResults']['totalSize'])
        if latest_len > 0 :
            
            theGames = json_decode1['mlb_bio_hitting_last_10']['mlb_individual_hitting_game_log']['queryResults']['row']
            if latest_len == 1 :
                    record = {}
                    record['playerId'] = player_id
                    record['game_id'] = theGames['game_id']
                    record['key'] = theGames['game_pk'] + str(player_id)

                    ab = int(theGames['ab']) 
                    h = int(theGames['h'])
                    outs = ab - h
                    r = int(theGames['r'])
                    hr = int(theGames['hr'])
                    rbi = int(theGames['rbi'])
                    sb = int(theGames['sb'])
                    bb = int(theGames['bb'])
                    doubles = int(theGames['h2b'])
                    triples = int(theGames['h3b'])

                    game_id_split = theGames['game_id'].split('/')
                    game_date = game_id_split[0] + game_id_split[1] + game_id_split[2]
                    record['game_id_date'] = game_date
                    record['cal_date']  = theGames['date']
                    record['game_pk'] = theGames['game_pk']
                    record['opponent_id'] = theGames['opp_team_id']
                    record['home_away'] = theGames['home_away']
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
                    record['ibb'] = theGames['ibb']
                    record['so'] = theGames['so']
                    record['avg'] = theGames['avg']
                    record['slg'] = theGames['slg']
                    record['outs'] = outs               
                    
                    record['points'] = h + doubles + (triples * 2) + r + (hr * 4) + rbi + (sb * 2) + (bb * 0.5) + (outs * (-0.3))

                    if record.has_key('key'):
                        # save record to the datastore
                        scraperwiki.sqlite.save(['key'],record)

            
            else :

                for i in range (0,latest_len) :

                    record = {}
                    record['playerId'] = player_id
                    record['game_id'] = theGames[i]['game_id']
                    record['key'] = theGames[i]['game_pk'] + str(player_id)
                    
                    ab = int(theGames[i]['ab'])
                    
                    #fix error h="" - occurs when scrapper is executed while baseball games in progress
                    if theGames[i]['h'] == "" :
                        h = int(0)
                    else :
                        h = int(theGames[i]['h'])
                    
                    outs = ab - h
                    r = int(theGames[i]['r'])
                    hr = int(theGames[i]['hr'])
                    rbi = int(theGames[i]['rbi'])
                    
                    #fix error sb="" - occurs when scrapper is executed while baseball games in progress
                    if theGames[i]['sb'] == "" :
                        sb = int(0)
                    else :
                        sb = int(theGames[i]['sb'])

                    bb = int(theGames[i]['bb'])
                    doubles = int(theGames[i]['h2b'])
                    triples = int(theGames[i]['h3b'])

                    game_id_split = theGames[i]['game_id'].split('/')
                    game_date = game_id_split[0] + game_id_split[1] + game_id_split[2]
                    record['game_id_date'] = game_date
                    record['cal_date']  = theGames[i]['date']
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
        